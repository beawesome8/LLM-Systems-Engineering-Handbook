# Zero-Shot Prompting

**Definition:** Ask the model to perform a task with a clear instruction and no examples,
relying entirely on what it learned in training.

**When to use it:** The task is common and well represented in training data (summarization,
translation, general Q&A, simple extraction), or you need to minimize tokens and latency and
the task has no idiosyncratic output format. It is also the right *baseline*: always try this
first so you know what examples or reasoning tricks actually buy you.

**When not to:** The output format is unusual, the labels or categories are domain-specific
and not self-explanatory, or early testing shows the model guessing at conventions you never
stated.

## Example prompt

```text
Classify this customer message as one of: escalation-risk, self-serve-resolvable,
needs-context, noise.

Message: "This is the third time I've written in. If this isn't fixed today I'm cancelling."

Respond with only the category name.
```

## Pitfalls

- Category names that are not self-explanatory (`needs-context`) get interpreted, not
  followed. Either define each label in the prompt or move to [few-shot](./few-shot.md).
- "Respond with only the category name" is a request, not a guarantee. Validate the output
  (see [Guardrail Engineering](../../guardrail-engineering/)).

## Runnable comparison

[`../examples/few_shot_vs_zero_shot.py`](../examples/few_shot_vs_zero_shot.py) runs this exact
task zero-shot and few-shot side by side (needs `ANTHROPIC_API_KEY`).

**Origin:** The "zero-shot" vs "few-shot" vocabulary comes from Brown et al., 2020 (GPT-3).
