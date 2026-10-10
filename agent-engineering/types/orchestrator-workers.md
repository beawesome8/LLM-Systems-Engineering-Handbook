# Orchestrator-Workers (Multi-Agent)

**Definition:** A lead (orchestrator) breaks a task into subtasks and delegates each to a
worker with its own focused context and tools. Workers run (often in parallel) and return
results; the orchestrator merges them.

**When to use it:** Work that splits into independent pieces (research several topics,
review many files, summarize many documents), or work where one context window cannot hold
everything, or where different subtasks want different tools or instructions.

**When not to:** Tightly coupled tasks where every step needs the full picture; workers
cannot share context cheaply. Multi-agent systems also cost more tokens (often several
times a single agent), add coordination bugs, and are harder to debug. Do not reach for
this before a single agent has demonstrably failed.

## Why it works: context isolation

Each worker sees only its slice. That gives focus (less noise), parallelism (lower latency),
and independence (one worker's mess stays out of the others'). This is the **Isolate**
operation from [context engineering](../../context-engineering/).

## Design rules

- **Typed contract between agents.** Workers return a defined shape
  (`{"source": ..., "summary": ...}`), not free prose the orchestrator must re-interpret.
- **Write clear delegation instructions.** The worker has none of your context; give it the
  objective, scope, expected output, and tool guidance. Vague delegation causes duplicated
  or missing work.
- **Plan for partial failure.** Merge what succeeded and report what did not.
- **Bound the fan-out.** Cap the number of workers and the depth of delegation.
- **Avoid worker-to-worker chatter** unless you have a reason; route through the
  orchestrator.

## Run it

[`../examples/orchestrator_workers.py`](../examples/orchestrator_workers.py), logged in
[`orchestrator_workers_output.txt`](../examples/orchestrator_workers_output.txt): three
documents fan out in parallel, one worker fails on an empty input, and the orchestrator
still returns a merged report of the other two plus the failure. Workers are stubs; in a real
system each is a model call or its own agent loop.

## Variants

- **Routing**: classify the input, then hand it to one specialist (no parallelism, just
  dispatch).
- **Handoff**: one agent passes the whole conversation to another (e.g. support -> billing).
- **Parallel voting**: run the same task several times and compare, for higher confidence.
