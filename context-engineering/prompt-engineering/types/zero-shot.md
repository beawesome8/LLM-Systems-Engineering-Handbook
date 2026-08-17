# Zero-Shot Prompting

**Definition:** Ask the model to perform a task with a clear instruction or question and no
examples, relying entirely on what it learned during training.

**When to use it:** The task is common and well-represented in training data (summarization,
translation, general Q&A), or you need to minimize token cost/latency and the task doesn't
need a specific idiosyncratic format.

**When not to:** The output format is unusual, the task is narrow/domain-specific, or early
testing shows the model guessing at conventions it hasn't been told.

**Worked example:** See [`../examples/few_shot_vs_zero_shot.py`](../examples/few_shot_vs_zero_shot.py) —
direct comparison against few-shot on the same task.
