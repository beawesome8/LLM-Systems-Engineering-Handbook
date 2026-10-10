# Zero-Plus-Few-Shot Chain of Thought

**Definition:** A hybrid. Zero or one worked example, plus an explicit instruction to reason
step by step. Sits between [zero-shot CoT](./zero-shot-cot.md) (no anchor) and
[few-shot CoT](./few-shot-cot.md) (several full examples).

**When to use it:** You want the accuracy of reasoning and a consistent answer *shape*, but
cannot afford the tokens of many worked examples. One example anchors the format; the
instruction supplies the behavior.

**When not to:** The output format is unusual enough that one example cannot disambiguate it,
or the task is simple enough that neither the example nor the reasoning is needed.

## Example prompt

```text
Work out the total cost, reasoning step by step before giving the final number.

Example:
Q: 3 notebooks at $2.50 and 1 pen at $1.20.
Steps: 3 x 2.50 = 7.50. Add 1.20 = 8.70.
ANSWER: 8.70

Q: {new_question}
Steps:
```

## When this is the right default

If you are unsure which CoT variant to use, start here: it is cheap, gives you a parseable
`ANSWER:` line, and you can add examples only where the eval shows failures
(see [Harness Engineering](../../../harness-engineering/)).
