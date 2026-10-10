# Zero-Shot Chain of Thought

**Definition:** No examples, but the prompt asks the model to reason step by step before it
gives the final answer.

**When to use it:** Multi-step arithmetic, logic, or judgment tasks where you want the
simplicity of zero-shot but a bare question gets too many wrong answers.

**When not to:** Simple lookups or classification (reasoning tokens add cost and latency
without improving anything), or when you are using a model with built-in reasoning / extended
thinking, which already does this internally. Measure; do not assume.

## Example prompt

```text
A store sells pens in packs of 6 for $4 and singles for $0.90. I need 20 pens.
What is the cheapest way to buy them, and what does it cost?

Think through this step by step, then give the final answer on a new line
starting with "ANSWER:".
```

The `ANSWER:` marker matters in production: reasoning text is unparseable, so give your
code one line it can extract reliably.

## Pitfalls

- Visible reasoning can be fluent and wrong. It is a *means* to a better answer, not a
  trustworthy explanation of one.
- Reasoning inflates output tokens. Log token cost next to accuracy when you adopt it.

**Origin:** Kojima et al., 2022 ("Large Language Models are Zero-Shot Reasoners") - the
phrase "Let's think step by step" alone raised accuracy on reasoning benchmarks.
