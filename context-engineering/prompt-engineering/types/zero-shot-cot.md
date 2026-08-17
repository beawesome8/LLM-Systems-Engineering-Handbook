# Zero-Shot Chain of Thought

**Definition:** No examples provided, but the prompt explicitly instructs the model to
"think step-by-step" before answering.

**When to use it:** Reasoning, judgment, or multi-step analysis tasks where you want the
simplicity of zero-shot but need better accuracy than a bare instruction gives — the
step-by-step nudge alone often closes much of that gap.

**When not to:** Latency-sensitive, simple-lookup tasks — the extra reasoning tokens add cost
and time without improving a task that didn't need reasoning in the first place.

**Worked example:** Not yet built — planned: same reasoning task with vs. without the
step-by-step instruction, same model, output and token cost logged.
