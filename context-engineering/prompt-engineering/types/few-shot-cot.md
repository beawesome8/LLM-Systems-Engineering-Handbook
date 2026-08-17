# Few-Shot Chain of Thought

**Definition:** Like few-shot prompting, but each example includes the reasoning steps that
lead to the answer, not just the final answer itself.

**When to use it:** Tasks involving multi-step reasoning, arithmetic, or judgment calls where
the *path* to the answer matters as much as the answer — the examples teach the model how to
reason, not just what to output.

**When not to:** Simple lookup or classification tasks with no real reasoning chain — the
extra tokens spent on reasoning steps in the examples buy nothing.

**Worked example:** Not yet built — planned: compare accuracy on a multi-step word-problem
set with vs. without reasoning shown in the examples.
