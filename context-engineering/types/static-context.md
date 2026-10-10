# Static Context

**Definition:** Context that is fixed across requests: the system prompt, persona, output
format, standing rules, and any reference text that never changes.

**When to use it:** Single-turn or narrow applications (classifiers, extractors, formatters),
and as the stable *prefix* of every other kind of system.

**When not to:** When the knowledge changes per request or per user. Pasting a whole
knowledge base into a static prompt makes it expensive, stale, and noisy.

## Example

```text
SYSTEM
You are a support assistant for Acme Cloud.
Rules: answer only from the provided documents; cite the doc id; if unsure, say so.
Output: 1-3 sentences, then "Source: <doc id>".
```

## Engineering notes

- **Put stable text first, variable text last.** Providers that support prompt caching can
  reuse an unchanged prefix, which cuts cost and latency. Changing one early token
  invalidates everything after it.
- **Version it.** A system prompt is code: keep it in the repo, review changes, and run evals
  before shipping (see [Harness Engineering](../../harness-engineering/)).
- **Write the "why" with each rule.** Models generalize better from "cite the doc id so
  support staff can verify" than from a bare "cite the doc id".

Used in: [`../examples/context_budget.py`](../examples/context_budget.py) (the `SYSTEM` constant).
