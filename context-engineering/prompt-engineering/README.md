# Prompt Engineering

*A sub-discipline of [Context Engineering](../).*

Designing the instruction layer of a model call: how a task is worded, how many examples are
given, and whether reasoning is elicited explicitly. It is necessary but not sufficient for
production systems. It optimizes one layer of what a model sees; the other layers (retrieved
knowledge, tool definitions, memory, guardrails) are covered elsewhere in this handbook.

## Techniques

Each page has a definition, when to use it, when not to, and a copy-pasteable example prompt.

| Technique | One-line summary | Cost | Reach for it when |
|---|---|---|---|
| [Zero-Shot](./types/zero-shot.md) | Ask directly, no examples | Lowest | Always, as your baseline |
| [Few-Shot](./types/few-shot.md) | Show example input/output pairs | Low-medium | Unusual labels or format |
| [Zero-Shot CoT](./types/zero-shot-cot.md) | Ask for step-by-step reasoning | Medium (output tokens) | Multi-step reasoning |
| [Few-Shot CoT](./types/few-shot-cot.md) | Examples that include the reasoning | Medium-high | Domain-specific reasoning rules |
| [Zero-Plus-Few CoT](./types/zero-plus-few-cot.md) | One example + step-by-step instruction | Medium | Good default for reasoning tasks |
| [Deep Breath](./types/deep-breath.md) | Informal step-by-step nudge | Medium | Tone choice; unproven for accuracy |
| [Generated Knowledge](./types/generated-knowledge.md) | Generate facts first, then answer | 2x calls | Surfacing / debugging model assumptions |
| [Tree of Thought](./types/tree-of-thought.md) | Branch, evaluate, choose | Highest | Planning where early mistakes are costly |
| [Directional Stimulus](./types/directional-stimulus.md) | Hint what to focus on | Low | You know what a good output contains |
| [Chain of Density](./types/chain-of-density.md) | Iteratively densify a summary | Medium | Vague summaries need concrete detail |

## How to choose

1. Start **zero-shot**. It is your baseline.
2. Wrong format or labels? Add **few-shot**.
3. Wrong *reasoning*? Add **CoT** (or use a model with built-in reasoning).
4. Wrong *facts*? Prompting will not fix it. Retrieve them
   ([dynamic context](../types/dynamic-context.md)).
5. Change one thing at a time and measure on a labelled set. A technique that helps on one
   model or task can do nothing on another.

## A note on reasoning models

Models with built-in step-by-step reasoning (extended thinking or equivalent) already do much
of what the CoT techniques ask for. For them, explicit "think step by step" instructions often
add little, and over-prescribing the reasoning can hurt. Describe the goal and constraints
clearly and let the model decide how to think, then verify with an eval.

## Universal prompt-writing rules

- **State the task, the audience, and the output format.** Do not make the model guess.
- **Give the reason behind a rule**, not only the rule.
- **Say what to do**, not only what to avoid.
- **Separate instructions from data** with delimiters.
- **Specify what to do when the answer is unknown** ("say so"), or it will invent one.
- **Treat prompts as code**: version control, review, tests.

## Runnable example

[`examples/few_shot_vs_zero_shot.py`](./examples/few_shot_vs_zero_shot.py) runs the same
classification task zero-shot and few-shot against the Claude API and prints both results
side by side. It needs an `ANTHROPIC_API_KEY`, so this repo does not ship a canned result;
[`examples/few_shot_vs_zero_shot_output.md`](./examples/few_shot_vs_zero_shot_output.md) is a
template for logging your own run. That is deliberate: run it yourself and write down what
you actually see, because the exercise is learning to read the differences.
