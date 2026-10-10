# Tree of Thought

**Definition:** Instead of one linear reasoning path, generate several candidate next steps
("branches"), score or critique them, keep the promising ones, and continue. Reasoning
becomes a search over a tree, with the option to backtrack.

**When to use it:** Problems with several plausible solution paths where an early mistake is
expensive: planning, puzzles, constrained scheduling, multi-step decisions.

**When not to:** Anything with one obvious path. It is the most expensive technique in this
folder (many calls, many tokens) and plain [CoT](./zero-shot-cot.md) is usually enough.
Log cost per correct answer, not only accuracy.

## Example (single-prompt version)

```text
Goal: schedule 3 meetings (A: 60 min, B: 30 min, C: 45 min) between 9:00 and 12:00.
A must come before C. B cannot be first.

Propose 3 different complete schedules. For each, check every constraint and mark it
PASS or FAIL. Then choose the best schedule and state why.
```

## Example (full search version, sketch)

```text
for depth in range(max_depth):
    candidates = [model.propose_next_step(state) for _ in range(branching)]
    scored     = [(model.score(c), c) for c in candidates]     # a separate "judge" call
    state      = best(scored)                                   # or keep top-k and backtrack
```

The single-prompt version is cheap and captures part of the benefit. The full version is a
[harness](../../../harness-engineering/) problem: it needs call budgets, scoring rubrics,
and a stop condition.

**Origin:** Yao et al., 2023 ("Tree of Thoughts: Deliberate Problem Solving with Large
Language Models").
