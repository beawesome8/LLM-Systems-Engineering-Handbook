# Few-Shot Chain of Thought

**Definition:** [Few-shot](./few-shot.md), but each example shows the reasoning steps that
lead to the answer, not only the answer.

**When to use it:** The path to the answer matters: multi-step arithmetic, policy decisions,
eligibility checks. The examples teach *how* to reason in your domain, including which rules
to apply and in what order.

**When not to:** Lookup or plain classification, where the reasoning in each example costs
tokens and teaches nothing.

## Example prompt

```text
Decide whether the customer is eligible for a refund. Policy: annual plans are refundable
within 30 days; monthly plans are never refundable.

Q: Annual plan, bought 12 days ago.
Reasoning: Annual plan, so the 30-day rule applies. 12 days is within 30. Eligible.
Answer: eligible

Q: Monthly plan, bought 3 days ago.
Reasoning: Monthly plan. Monthly plans are never refundable, regardless of age. Not eligible.
Answer: not eligible

Q: Annual plan, bought 45 days ago.
Reasoning: Annual plan, so the 30-day rule applies. 45 days is outside 30. Not eligible.
Answer: not eligible

Q: {new_case}
Reasoning:
```

## Pitfalls

- If your examples reason badly, the model reasons badly the same way. Review them like code.
- Reasoning is part of the output: parse the `Answer:` line, never the whole completion.

**Origin:** Wei et al., 2022 ("Chain-of-Thought Prompting Elicits Reasoning in Large
Language Models").
