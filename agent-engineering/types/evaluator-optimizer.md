# Evaluator-Optimizer (Reflection Loop)

**Definition:** One call generates; a second call critiques against criteria; the generator
revises using the critique; repeat until the critic approves or a cap is hit.

**When to use it:** Tasks with clear, checkable quality criteria where a first draft is
usually imperfect: translation with a style guide, code that must pass tests, writing that
must meet a rubric.

**When not to:** When the critic cannot judge better than the generator (it will rubber-stamp
or invent problems), when criteria are vague, or when one pass is already good enough.

## Sketch

```python
draft = generate(task)
for round in range(MAX_ROUNDS):                  # always bounded
    verdict = critique(task, draft)              # {"ok": bool, "issues": [...]}
    if verdict["ok"]:
        break
    draft = revise(task, draft, verdict["issues"])
return draft
```

## Make the critic strong

- **Prefer objective critics**: run the tests, validate the schema, check the quote exists
  ([output validation](../../context-engineering/guardrail-engineering/types/output-validation.md)).
  A compiler or test suite is a better critic than a model.
- **If using a model critic**, give it a rubric and ask for specific, actionable issues, and
  validate it against human labels in an [eval](../../harness-engineering/types/eval-harness.md).
- **Different instructions, possibly a different model**, for the critic, to avoid shared
  blind spots.

## Pitfalls

- **Endless polish**: each round costs a call. Stop on approval, on no-improvement, or at the
  cap.
- **Sycophantic critic** that approves everything, or **nitpicking critic** that never does.
- **Drift**: revisions that fix one issue and break an earlier requirement. Re-check *all*
  criteria each round.
