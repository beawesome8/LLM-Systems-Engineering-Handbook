# Tool-Loop Harness

**Definition:** The cycle at the heart of every agent: send context to the model; if it
requests a tool, run the tool, append the result, and call the model again; stop when it
returns a final answer.

```text
          +--------------------------------------------+
          v                                            |
user -> [model call] -> tool requested? --yes--> run tool, append result
                              |
                              no
                              v
                        final answer
```

**When to use it:** Any task where the model needs information or actions it does not have:
lookups, calculations, database queries, file edits.

**When not to:** Tasks a single call can answer. Each loop iteration adds latency and cost.

## What the harness must do

| Responsibility | Why |
|---|---|
| Cap the number of steps | A confused model can loop forever |
| Validate tool names and arguments | Models invent tools and mangle arguments |
| Catch tool exceptions and return them as results | The model can often recover from "file not found" |
| Truncate or summarize large tool results | They flood the context ([compaction](../../context-engineering/types/context-compaction.md)) |
| Gate side-effecting tools | See [human-in-the-loop](./human-in-the-loop.md) |
| Log every step | Debugging and evals |

## Run it

[`../examples/tool_loop.py`](../examples/tool_loop.py), logged in
[`tool_loop_output.txt`](../examples/tool_loop_output.txt): a successful two-tool run, a run
where a human denies a refund, and a runaway model stopped by the step cap.

The stub emits the same *shape* a real tool-using model does: either a tool request
(name + arguments) or a final answer. With a real API, a tool request arrives as a
structured block in the response; your loop executes it and sends the result back in the next
request tied to that block's id. The loop logic is identical.

## Common bugs

- Dropping the tool result's id, so the model cannot match results to requests.
- Returning a Python traceback as the "result" (huge, unhelpful). Return a short message.
- No distinction between "tool failed" and "tool returned nothing".
