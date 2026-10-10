# Planner / Executor

**Definition:** Split deciding from doing. A planner call produces an explicit plan (an
ordered list of steps, as data). An executor runs the steps with tools. If a step fails, the
system re-plans the *remaining* work.

**When to use it:** Multi-step tasks where you want the plan to be visible, reviewable, and
loggable *before* any action happens, or where steps are expensive and wasted work hurts.

**When not to:** Tasks where the next step truly depends on the previous result at every
turn (a plain [tool loop](./single-agent-tool-use.md) adapts more naturally), or short tasks
where planning overhead exceeds the work.

## Why a separate plan helps

- **Inspectable**: log it, show it to a user, diff it against expected plans in evals.
- **Checkable**: validate the plan (allowed tools only? within budget?) before executing.
- **Editable**: a human can approve or change the plan ([HITL](../../harness-engineering/types/human-in-the-loop.md)).
- **Cheaper executors**: the planner can be a stronger model; steps can run on a cheaper one.

## Plan as data

```json
[
  {"tool": "search", "args": {"q": "Acme revenue 2024"}},
  {"tool": "fetch_prior_year", "args": {}},
  {"tool": "calc", "args": {"expr": "12 / 10 - 1"}}
]
```

## Run it

[`../examples/planner_executor.py`](../examples/planner_executor.py), logged in
[`planner_executor_output.txt`](../examples/planner_executor_output.txt). Step 2
(`fetch_prior_year`) fails, the executor re-plans the remaining work around it, and the task
completes. `plan()` is a rule-based stub for a model call, so the re-plan is scripted, and
the stub's search tool returns the 2024 figure for a 2023 query: a reminder that executors
need tool results *validated*, not just received.

## Pitfalls

- **Stale plans**: a plan made at step 0 can be wrong by step 3. Cap re-plans (the demo
  allows 1) and re-plan only the remainder.
- **Over-planning**: fine-grained plans for tasks the model could just do.
- **Unvalidated plans**: a model can plan a tool that does not exist. Check before running.
