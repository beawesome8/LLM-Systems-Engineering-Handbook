# Eval Harness

**Definition:** Code that runs a fixed set of test cases through your system, scores each
output against a rubric, and reports pass rate and regressions. It is the unit-test suite of
LLM systems.

**When to use it:** Before you change anything (prompt, model, retrieval, tools) and after.
Without it, "this prompt seems better" is an opinion.

**When not to skip it:** Never for anything shipped. Start with 10-20 cases; a small real
test set beats a large imagined one.

## Anatomy

```text
cases (input + expected properties)  ->  run system  ->  score each output  ->  report
```

## Scoring methods, cheapest first

| Method | Example | Pros | Cons |
|---|---|---|---|
| Exact / contains | Output contains "30 days" | Fast, stable | Brittle to wording |
| Code-based checks | Valid JSON, schema, regex, number within tolerance | Deterministic | Cannot judge quality |
| Reference comparison | Compare to a gold answer | Clear target | Needs gold answers |
| LLM-as-judge | A model grades against a rubric | Flexible | Costs calls; has bias; must itself be validated against human labels |
| Human review | Sample and grade by hand | Ground truth | Slow, expensive |

Use deterministic checks wherever possible and LLM judges only for what they cannot express.

## What to report

- **Pass rate** overall and per category.
- **Regressions**: cases that passed before and fail now. An average can rise while one
  important case breaks.
- **Cost and latency** next to accuracy. A +2% gain at 5x cost is a decision, not a win.
- **Variance**: model output varies run to run; for borderline cases, run several times.

## Run it

[`../examples/eval_harness.py`](../examples/eval_harness.py) compares two system versions on
four cases, logged in [`eval_harness_output.txt`](../examples/eval_harness_output.txt). v2
scores higher (3/4 vs 2/4) **and** regresses one case ("invoice") that v1 got right, which is
exactly why the regression list is printed alongside the average.

## Building the test set

- Start from **real inputs**, including the ones that failed in production.
- Include **easy, hard, and adversarial** cases, and some where the right answer is "I
  don't know".
- When you find a bug, **add it as a case** before fixing it.
- Keep a **held-out** subset you do not tune against.
