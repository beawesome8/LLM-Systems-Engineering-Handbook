# Generated Knowledge Prompting

**Definition:** Ask the model to first generate relevant background facts or context, then
use that generated knowledge to answer the actual question — a two-step call rather than one.

**When to use it:** The task needs world knowledge or context the model has but wouldn't
surface unprompted, multi-step reasoning tasks, or when you want to inspect what the model
"believes" is relevant before it commits to an answer (useful for debugging bad answers).

**When not to:** The extra call doubles latency and cost — not worth it for tasks where the
model already answers reliably in one shot.

**Worked example:** Not yet built.
