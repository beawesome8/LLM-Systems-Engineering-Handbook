"""
few_shot_vs_zero_shot.py

Runs the same classification task two ways against the Claude API — zero-shot and
few-shot — and logs both outputs so the difference is inspectable, not asserted.

Task: classify a short customer support message into one of a fixed set of categories
that aren't self-explanatory from the label alone (deliberately picked so zero-shot has
to guess at the taxonomy).

Requires: ANTHROPIC_API_KEY set in your environment.
    pip install anthropic --break-system-packages   (if not already installed)

Usage:
    python few_shot_vs_zero_shot.py

Paste the printed output into few_shot_vs_zero_shot_output.md — don't hand-edit the
output, the point of this example is that it's a real logged run.
"""

import os
import json
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-sonnet-4-6"

# Deliberately ambiguous category names — a model has to infer the taxonomy's intent,
# not just pattern-match on obvious keywords. This is where few-shot should help most.
CATEGORIES = ["escalation-risk", "self-serve-resolvable", "needs-context", "noise"]

TEST_MESSAGES = [
    "This is the third time I've written in. If this isn't fixed today I'm cancelling.",
    "Where do I find my invoice history?",
    "It stopped working after the update but I'm not sure what changed on my end.",
    "just checking in :)",
]

FEW_SHOT_EXAMPLES = """
Message: "I've asked twice already and no one has responded. I want a refund now."
Category: escalation-risk

Message: "How do I reset my password?"
Category: self-serve-resolvable

Message: "The dashboard looks different today and some of my data seems missing."
Category: needs-context

Message: "thanks for the help earlier!"
Category: noise
"""


def zero_shot_classify(message: str) -> str:
    prompt = (
        f"Classify this customer support message into one of these categories: "
        f"{', '.join(CATEGORIES)}.\n\nMessage: \"{message}\"\n\n"
        f"Respond with only the category name."
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=20,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


def few_shot_classify(message: str) -> str:
    prompt = (
        f"Classify a customer support message into one of these categories: "
        f"{', '.join(CATEGORIES)}.\n\nHere are examples:\n{FEW_SHOT_EXAMPLES}\n"
        f"Now classify this message:\n\"{message}\"\n\n"
        f"Respond with only the category name."
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=20,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


def main():
    results = []
    for msg in TEST_MESSAGES:
        zero = zero_shot_classify(msg)
        few = few_shot_classify(msg)
        results.append({
            "message": msg,
            "zero_shot": zero,
            "few_shot": few,
            "agree": zero == few,
        })

    print(json.dumps(results, indent=2))

    disagreements = [r for r in results if not r["agree"]]
    print(f"\n{len(disagreements)}/{len(results)} messages classified differently "
          f"between zero-shot and few-shot.")


if __name__ == "__main__":
    main()
