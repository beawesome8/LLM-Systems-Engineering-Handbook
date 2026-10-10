# Few-Shot Prompting

**Definition:** Put a small number of example input/output pairs in the prompt before the new
case. The examples set the pattern the model follows.

**When to use it:** The task has an output format, tone, or edge-case rule that is hard to
describe but easy to demonstrate: classification with unusual labels, structured extraction,
style matching.

**When not to:** A clear instruction alone already works (examples add token cost for no
accuracy gain), or the examples would leak sensitive data into every call.

## Example prompt

```text
Classify a customer support message into: escalation-risk, self-serve-resolvable,
needs-context, noise.

Message: "I've asked twice already and no one has responded. I want a refund now."
Category: escalation-risk

Message: "How do I reset my password?"
Category: self-serve-resolvable

Message: "The dashboard looks different today and some of my data seems missing."
Category: needs-context

Message: "thanks for the help earlier!"
Category: noise

Message: "{new_message}"
Category:
```

## Rules of thumb

- **Cover every label at least once**, and include one borderline case per label pair you
  expect to be confused.
- **Keep formatting identical across examples.** The model copies surface form exactly,
  including mistakes.
- **Order matters a little.** Models can over-weight the last example; shuffle when testing.
- **Most gain comes from the first 2-5 examples.** Past that, measure before adding more.
- **Examples are data you maintain.** Version them, and test them against a labelled set
  (see [Harness Engineering](../../../harness-engineering/)).

## Runnable comparison

[`../examples/few_shot_vs_zero_shot.py`](../examples/few_shot_vs_zero_shot.py), with a logging
template in [`../examples/few_shot_vs_zero_shot_output.md`](../examples/few_shot_vs_zero_shot_output.md).

**Origin:** Brown et al., 2020 ("Language Models are Few-Shot Learners").
