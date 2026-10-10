# Harness Engineering

A **harness** is the code around a model call that makes it reliable: the tool-calling loop,
retries and error handling, evaluation, and human checkpoints. The model proposes; the
harness decides what actually happens, what gets retried, what gets stopped, and what gets
measured.

**Harness vs. agent engineering:** [agent engineering](../agent-engineering/) is about *what*
the system decides to do (plans, tool choices, delegation). Harness engineering is the
*reliability infrastructure* that decision-making runs inside: limits, recovery, measurement,
and oversight. A great agent design in a weak harness still fails in production.

## Types

| Type | What it provides | Page | Run it |
|---|---|---|---|
| Tool-loop harness | The call -> tool -> result -> call cycle, with step limits and error handling | [tool-loop.md](./types/tool-loop.md) | [`tool_loop.py`](./examples/tool_loop.py) |
| Retry / backoff harness | Survival of rate limits, timeouts, and 5xx errors | [retry-and-backoff.md](./types/retry-and-backoff.md) | [`retry_backoff.py`](./examples/retry_backoff.py) |
| Eval harness | Repeatable measurement; regression detection | [eval-harness.md](./types/eval-harness.md) | [`eval_harness.py`](./examples/eval_harness.py) |
| Human-in-the-loop harness | Approval gates for risky actions | [human-in-the-loop.md](./types/human-in-the-loop.md) | [`tool_loop.py`](./examples/tool_loop.py) |

## Design principles

1. **Bound everything.** Max steps, max tokens, max retries, max wall-clock time, max spend.
   A loop without a limit is an outage waiting for a trigger.
2. **Errors are information.** Feed tool errors back to the model as results; it can often
   recover. Reserve exceptions for things the model cannot fix.
3. **Distinguish transient from permanent failures.** Retry the first, surface the second.
4. **Log the whole trace.** Every model input, output, tool call, and result, with ids.
   You cannot debug what you cannot replay.
5. **Evals before opinions.** Every prompt, model, or tool change is a hypothesis; the eval
   harness is how you test it.
6. **Side effects need gates.** Read-only tools can run freely; writes, sends, and spends
   need approval or tight limits.

## Run the examples

All examples are stdlib-only, deterministic, and use a stub model, so they run offline:

```bash
cd examples
python tool_loop.py
python retry_backoff.py
python eval_harness.py
```

Logged output sits next to each script as `*_output.txt`. The stub model is the point: the
harness is the stable part, and swapping the stub for a real API call does not change it.

## Going further

Anthropic's Claude Agent SDK and Claude Code are production harnesses of this kind: a tool
loop, permissions, hooks, and context management around a model. Reading their docs is the
fastest way to see these ideas at industrial scale.
