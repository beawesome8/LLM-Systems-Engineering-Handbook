# Tree of Thought

**Definition:** Instead of one linear reasoning path, generate multiple candidate next-steps
("branches") at each stage, evaluate or score them, and choose the best path forward — a
decision tree for reasoning rather than a single chain.

**When to use it:** Problems with multiple plausible solution paths where early mistakes are
expensive and hard to recover from — planning tasks, puzzles, multi-step decisions where
backtracking matters.

**When not to:** Straightforward tasks with one clear reasoning path — the branching and
evaluation overhead (more calls, more tokens) buys nothing over plain CoT.

**Worked example:** Not yet built — highest token cost of any technique here, so the
comparison example will specifically measure cost vs. accuracy gain, not just accuracy.
