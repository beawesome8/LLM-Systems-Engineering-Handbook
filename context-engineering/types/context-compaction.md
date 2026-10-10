# Context Compaction and Pruning

**Definition:** Keeping a growing context inside the window and inside the model's useful
attention range by summarizing, trimming, or offloading old material. This is the
**Compress** operation.

**When to use it:** Long conversations, long-running agents, tool-heavy loops where results
pile up. Models degrade on very long contexts even before the hard limit ("context rot"):
more tokens is not free quality.

**When not to:** Short sessions. Compaction is lossy; do not pay that cost until the window
actually becomes a problem.

## Techniques, cheapest first

| Technique | How | Loses |
|---|---|---|
| Truncate | Drop the oldest turns | Everything early, including the original goal |
| Trim tool output | Keep only the fields you need from big results | Detail you later wanted |
| Summarize | An LLM call condenses old turns | Nuance, exact wording, small facts |
| Offload | Write details to a file/DB, keep a pointer in context | Nothing, but needs a retrieval step |
| Structured notes | The agent maintains a running "state" object | Depends on what the schema captures |

## Engineering notes

- **Pin what must survive**: the user's goal, hard constraints, decisions already made.
  Summaries tend to lose exactly these.
- **Compact on a trigger** (e.g. 70% of budget), not every turn.
- **Test it.** Ask a question whose answer lives only in the compacted part and check it
  survives. That is an eval case ([Harness Engineering](../../harness-engineering/)).

Run it: [`../examples/context_budget.py`](../examples/context_budget.py) collapses old turns
into a one-line summary and keeps the last turns verbatim. Its summarizer is a naive
word-truncation stand-in; in production this step is an LLM call.
