# Dynamic / Retrieval-Augmented Context

**Definition:** Context assembled fresh for each request from external sources: retrieved
documents (RAG), user memory, live API data, tool results. This is the **Select** operation.

**When to use it:** Any application with state, private knowledge, or facts that change:
support bots, agents, assistants over company data.

**When not to:** When the whole relevant corpus fits comfortably in a static prompt and
changes rarely. Retrieval adds a failure mode (the right document is not retrieved), so do
not add it before you need it.

## Example

```text
SYSTEM (static) ...
DOCUMENTS (selected for this query)
[kb-1] Refunds are available within 30 days of purchase for annual plans...
[kb-5] Annual plans renew automatically. Cancel at least 7 days before renewal...
USER: Can I get a refund for my annual plan?
```

## Engineering notes

- **Most RAG failures are retrieval failures, not generation failures.** If the answer is not
  in the context, no prompt can recover it. Measure retrieval separately
  ([Embedding Engineering](../../embedding-engineering/)).
- **Less is more.** Irrelevant documents are not neutral: they distract the model and cost
  tokens. Rank, threshold, and cap.
- **Label sources.** Give each chunk an id so the model can cite and you can audit.
- **Treat retrieved text as untrusted data.** A document can contain instructions
  ("ignore previous instructions..."). See [Guardrail Engineering](../guardrail-engineering/).

## Run it

[`../examples/context_budget.py`](../examples/context_budget.py) - doc selection under a
token budget. Note what happens at the 120-token budget in
[`../examples/context_budget_output.txt`](../examples/context_budget_output.txt): *every*
document gets dropped, so the model would be asked to answer with no knowledge. A budget
policy must decide what is allowed to be sacrificed; here it should protect at least the top
document and shrink history first, or fail loudly.
