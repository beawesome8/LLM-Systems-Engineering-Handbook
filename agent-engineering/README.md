# Agent Engineering

An **agent** is a system where a model decides, step by step, what to do next (which tool to
call, whether to keep going, when to stop) toward a goal, instead of answering a single turn.
Agent engineering is the design of those decision structures.

**Agent vs. harness:** agent engineering decides *what* the system does (the control
structure); [harness engineering](../harness-engineering/) supplies the limits, retries,
evals, and approvals it runs inside. You need both.

## Start simple

The most important rule in this folder: **use the least autonomy that solves the problem.**

```text
single model call  ->  fixed workflow (prompt chain)  ->  single agent + tools  ->  multi-agent
  cheapest, most predictable                                          most flexible, costly, hardest to debug
```

Each step right buys flexibility and costs predictability, latency, money, and debuggability.
Move right only when an eval shows the simpler design cannot do the job.

## Workflows vs. agents

- **Workflow**: *your code* fixes the path (step 1 -> step 2 -> step 3), the model fills in
  each step. Predictable, testable. Right for most production tasks.
- **Agent**: *the model* picks the path at runtime. Flexible, but variable in cost, time, and
  outcome. Right when the steps cannot be known in advance.

## Types

| Pattern | Idea | Page | Run it |
|---|---|---|---|
| Single-agent tool use | One model, a set of tools, a loop | [single-agent-tool-use.md](./types/single-agent-tool-use.md) | [`tool_loop.py`](../harness-engineering/examples/tool_loop.py) |
| Planner / executor | Plan first as inspectable data, then execute; re-plan on failure | [planner-executor.md](./types/planner-executor.md) | [`planner_executor.py`](./examples/planner_executor.py) |
| Orchestrator-workers | A lead splits work; isolated workers run in parallel; results merge | [orchestrator-workers.md](./types/orchestrator-workers.md) | [`orchestrator_workers.py`](./examples/orchestrator_workers.py) |
| Evaluator-optimizer | One call produces, another critiques, loop until good enough | [evaluator-optimizer.md](./types/evaluator-optimizer.md) | sketch in page |

## Design principles

1. **Tools are the interface.** Name them clearly, describe when to use each, keep arguments
   few and typed, return concise results. Poor tool design causes more agent failures than
   poor prompts.
2. **Make state explicit.** Keep goal, plan, and progress in structured form, not scattered
   in chat history ([compaction](../context-engineering/types/context-compaction.md)).
3. **Define "done."** An agent without a stopping criterion either quits early or never quits.
4. **Isolate context** between sub-agents so one task's noise does not pollute another's
   ([Isolate](../context-engineering/README.md)).
5. **Design for failure.** Tools will break and plans will be wrong; decide in advance what
   the agent does next ([planner/executor re-plan](./types/planner-executor.md)).
6. **Trace everything.** Agent bugs are sequence bugs; you need the full trajectory.

## Run the examples

```bash
cd examples
python planner_executor.py
python orchestrator_workers.py
```

Offline, stub-driven, logged next to each script as `*_output.txt`. The stubs stand in for
model calls; the control structure (plan data, re-plan, fan-out, merge, partial failure) is
the real content.

## See it at production scale

- [Recurring Research Agent](https://github.com/beawesome8/Recurring-research-agent) - multi-node LangGraph agent (planner, search, synthesis) with dual memory
- [BQ-Vertex-Analyst](https://github.com/beawesome8/BQ-Vertex-Analyst) - LangGraph agent with AST-based validation gating on generated SQL
