# Single-Agent Tool Use

**Definition:** One model, given a set of tools and a goal, repeatedly chooses a tool, sees
the result, and decides the next step until it can answer. (Often called a ReAct-style loop:
reason, act, observe.)

**When to use it:** Open-ended tasks where the sequence of steps depends on what earlier
steps return: debugging, research, data analysis, customer-service lookups.

**When not to:** When the steps are known in advance. Hard-code that workflow instead: it
is cheaper, faster, and testable.

## Anatomy

```text
goal + tool definitions -> model -> (tool call -> result) x N -> final answer
```

The loop machinery is a [tool-loop harness](../../harness-engineering/types/tool-loop.md);
what makes it an *agent* is that the model chooses the path.

## Tool design checklist

- **Name and describe for the model**, not for yourself: "Look up one order by id. Use
  before any refund." beats `get_o`.
- **Few, orthogonal tools.** Ten overlapping tools cause misrouting. Merge or remove.
- **Typed, minimal arguments** with enums where possible.
- **Concise, informative results.** Return what the next decision needs. Include helpful
  errors ("order not found; ids look like A1234").
- **Mark side effects** and gate them ([HITL](../../harness-engineering/types/human-in-the-loop.md)).

## Failure modes

| Symptom | Likely cause |
|---|---|
| Calls the wrong tool | Ambiguous names/descriptions; too many tools |
| Repeats the same call | No memory of progress; tool result not informative |
| Never stops | No clear done-criterion; no step cap |
| Gives up early | Tool errors not recoverable or not explained |
| Context balloons | Large tool results not trimmed |

## Run it

[`../../harness-engineering/examples/tool_loop.py`](../../harness-engineering/examples/tool_loop.py)
runs this loop with two tools, an approval gate, and a step limit.
