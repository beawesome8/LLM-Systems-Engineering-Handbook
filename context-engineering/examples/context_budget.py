"""
context_budget.py

Assembles one model context from competing sources under a token budget, using the four
context-engineering operations:

  Write    - fixed system instructions (always included)
  Select   - pick only the knowledge-base docs relevant to this query
  Compress - collapse old conversation turns, keep recent ones verbatim
  Isolate  - only docs in the caller's `scope` are even candidates

No API key needed: this shows what you *send*, not what comes back.
Usage: python context_budget.py
"""

SYSTEM = ("You are a support assistant for Acme Cloud. Answer only from the provided "
          "documents and cite the doc id. If the answer is not in them, say so.")

# (id, scope, text)
DOCS = [
    ("kb-1", "billing",  "Refunds are available within 30 days of purchase for annual plans. Monthly plans are not refundable."),
    ("kb-2", "security", "To reset your password open Settings > Security and choose Reset password. A link is emailed to you."),
    ("kb-3", "billing",  "Invoices are under Billing > History. Each invoice can be downloaded as a PDF."),
    ("kb-4", "security", "SSO via SAML 2.0 is supported on the Enterprise plan only."),
    ("kb-5", "billing",  "Annual plans renew automatically. Cancel at least 7 days before renewal to avoid being charged."),
]

HISTORY = [
    ("user", "Hi, I'm on the annual plan and I have a few questions about my account."),
    ("assistant", "Thanks for reaching out! I'd be glad to help with your account today."),
    ("user", "I bought it 10 days ago and it turns out it doesn't fit what our team needs."),
    ("assistant", "I'm sorry to hear that. Let me see which options are available to you."),
    ("user", "Can I get my money back for the annual plan I bought 10 days ago?"),
]


def tokens(text: str) -> int:
    return max(1, len(text) // 4)  # ponytail: ~4 chars/token heuristic, use the provider's token counter in production


def overlap(query: str, text: str) -> int:
    stem = lambda w: w.strip(".,?!").lower()[:5]   # ponytail: 5-char prefix "stem" so refund ~ refunds; use embeddings/BM25 for real
    q = {stem(w) for w in query.split() if len(w) > 3}
    return len(q & {stem(w) for w in text.split()})


def compress_history(turns, keep_last):
    old, recent = turns[:-keep_last], turns[-keep_last:]
    if not old:
        return [f"{r}: {t}" for r, t in recent]
    # ponytail: first-6-words truncation; real systems summarize old turns with an LLM call
    gist = "; ".join(" ".join(t.split()[:6]) for _, t in old)
    return [f"[summary of {len(old)} earlier turns: {gist}]"] + [f"{r}: {t}" for r, t in recent]


def build_context(query, scope, budget):
    candidates = sorted(((overlap(query, t), i, t) for i, s, t in DOCS if s == scope), reverse=True)  # Isolate
    docs = [(score, i, t) for score, i, t in candidates if score > 0]                                 # Select
    keep_last = 2
    while True:
        history = compress_history(HISTORY, keep_last)                                                # Compress
        sections = {"system": SYSTEM,                                                                 # Write
                    "docs": "\n".join(f"[{i}] {t}" for _, i, t in docs),
                    "history": "\n".join(history),
                    "query": query}
        total = sum(tokens(v) for v in sections.values())
        if total <= budget:
            return sections, total
        if docs:
            docs.pop()          # drop least relevant doc first
        elif keep_last > 1:
            keep_last -= 1      # then shrink verbatim history
        else:
            return sections, total  # cannot fit: caller must raise the budget or fail loudly


if __name__ == "__main__":
    q = "Can I get a refund for my annual plan?"
    for budget in (400, 120):
        sections, total = build_context(q, "billing", budget)
        print(f"=== budget {budget} tokens -> used {total} ===")
        for name, text in sections.items():
            print(f"-- {name} ({tokens(text)} tok)\n{text}")
        print()
