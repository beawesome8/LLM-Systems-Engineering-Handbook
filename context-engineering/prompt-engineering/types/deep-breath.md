# Deep Breath (Softened Chain of Thought)

**Definition:** A casual phrasing of the step-by-step instruction, e.g. "Take a deep breath
and work on this problem step by step", in place of a formal "think step by step" directive.

**Where it came from:** Yang et al., 2023 ("Large Language Models as Optimizers") had one model
propose instruction phrasings and scored each on GSM8K math problems. With PaLM 2-L as the
scored model, "Take a deep breath and work on this problem step-by-step." reached 80.2%,
versus 71.8% for "Let's think step by step." But a different optimizer's top phrase,
"Break this down.", scored 79.9%, and the paper also shows that near-synonymous phrasings
can differ by 10+ points (e.g. "Let's work together to solve this problem step by step."
scored 49.4%). The finding is "phrasing matters a lot and is hard to predict", about one
model on one benchmark, not "this phrase is magic".

**When to use it:** As a tone choice in conversational or customer-facing prompts where a
clinical "Step 1, Step 2" instruction would feel off.

**When not to:** When you are choosing it *for accuracy*. There is no reliable evidence it
beats a direct step-by-step instruction across models; phrasing effects vary by model and
shift between versions. Treat it as a hypothesis to test, not a technique to trust.

## Example prompt

```text
Take a deep breath and work through this carefully, step by step.

A train leaves at 9:40 and the trip takes 2 hours 35 minutes. When does it arrive?
Give the time on a final line starting with "ANSWER:".
```

## How to evaluate a phrasing claim like this

Run both phrasings over the same labelled question set and compare pass rate and token cost
using an eval harness: [`../../../harness-engineering/examples/eval_harness.py`](../../../harness-engineering/examples/eval_harness.py).
The lesson of this technique is less "say this magic phrase" than "phrasing claims need
measurement on *your* model and *your* task."
