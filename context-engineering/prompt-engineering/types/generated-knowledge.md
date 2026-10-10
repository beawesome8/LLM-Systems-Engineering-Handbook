# Generated Knowledge Prompting

**Definition:** Two steps instead of one. First ask the model to write out relevant facts
about the question. Then give it those facts along with the question and ask for the answer.

**When to use it:** Commonsense or domain questions where the model knows the relevant facts
but does not surface them unprompted. Also useful for *debugging*: the generated facts show
what the model thinks is relevant, so you can see whether a wrong answer comes from a wrong
fact or wrong reasoning.

**When not to:** The model already answers reliably in one call (you pay double latency and
cost for nothing), or the facts must be accurate. Model-generated "knowledge" can be
hallucinated. For facts that must be right, retrieve them from a trusted source instead
([Embedding Engineering](../../../embedding-engineering/)).

## Example prompts

Call 1:

```text
List 4 short, factual statements relevant to this question. Do not answer it.
Question: Can a customer on a monthly plan get a refund after 10 days?
```

Call 2:

```text
Facts:
{facts_from_call_1}

Using only the facts above plus the policy text below, answer the question.
Policy: {policy_text}
Question: Can a customer on a monthly plan get a refund after 10 days?
```

## Pitfalls

- Generated facts can be confidently false and then get laundered into the final answer as
  if they were sources. Anchor step 2 to a real document when stakes are non-trivial.

**Origin:** Liu et al., 2022 ("Generated Knowledge Prompting for Commonsense Reasoning").
