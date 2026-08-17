# Prompt Engineering

*A sub-discipline of [Context Engineering](../).*

Designing the instruction layer of a model call: how a task is worded, how many examples are
given, and whether reasoning is elicited explicitly. Prompt engineering is necessary but not
sufficient for production systems — it optimizes one layer of what a model sees; the other
layers (retrieved knowledge, tool definitions, memory, guardrails) are covered under Context
Engineering's other sub-disciplines.

## Types covered here

| Technique | One-line summary |
|---|---|
| [Few-Shot Prompting](./types/few-shot.md) | Show example input/output pairs to set the pattern |
| [Zero-Shot Prompting](./types/zero-shot.md) | Ask directly, no examples, rely on prior training |
| [Few-Shot Chain of Thought](./types/few-shot-cot.md) | Examples that include the reasoning steps, not just answers |
| [Zero-Shot Chain of Thought](./types/zero-shot-cot.md) | No examples, but explicitly ask the model to reason step by step |
| [Zero-Plus-Few-Shot CoT](./types/zero-plus-few-cot.md) | Hybrid: one or zero examples, explicit step-by-step instruction |
| [Deep Breath / Softened CoT](./types/deep-breath.md) | Informal phrasing that nudges step-by-step reasoning without formal instruction |
| [Generated Knowledge](./types/generated-knowledge.md) | Ask the model to generate relevant facts before answering the real question |
| [Tree of Thought](./types/tree-of-thought.md) | Explore multiple reasoning branches, evaluate, choose the best |
| [Directional Stimulus](./types/directional-stimulus.md) | Prime the model's attention toward specific aspects before the task |
| [Chain of Density](./types/chain-of-density.md) | Iteratively densify a response with more detail without losing clarity |

## Worked example

[`examples/few_shot_vs_zero_shot.py`](./examples/few_shot_vs_zero_shot.py) runs the same
classification task both ways against the Claude API and logs the actual outputs side by
side. See [`examples/few_shot_vs_zero_shot_output.md`](./examples/few_shot_vs_zero_shot_output.md)
for the template to paste your logged run into — I run this myself with my own API key rather
than publish a canned result, so the output in the repo is real, not illustrative.
