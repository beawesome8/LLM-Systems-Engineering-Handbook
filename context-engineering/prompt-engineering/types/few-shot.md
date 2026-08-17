# Few-Shot Prompting

**Definition:** Provide the model with a small number of example input/output pairs inside
the prompt before asking it to handle a new case. The examples set the pattern the model
follows.

**When to use it:** The task has a specific output format, tone, or edge-case handling that's
hard to describe in words but easy to demonstrate. Classification with unusual categories,
structured extraction, style matching.

**When not to:** The task is simple enough that a clear instruction alone works (adds token
cost for no accuracy gain), or examples would leak sensitive/proprietary data into every call.

**Worked example:** See [`../examples/few_shot_vs_zero_shot.py`](../examples/few_shot_vs_zero_shot.py) —
same classification task run few-shot vs zero-shot, output logged in
[`../examples/few_shot_vs_zero_shot_output.md`](../examples/few_shot_vs_zero_shot_output.md).
