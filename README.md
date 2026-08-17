# LLM Systems Engineering

Applied notes and worked examples across the disciplines that sit above raw model calls and
below full production deployment. This is a companion repo to my deployed engineering
projects (see [portfolio](https://beawesome8.github.io)) — those repos prove I can ship;
this one documents that I understand the field's own taxonomy, including where that taxonomy
has recently changed.

## Why this is structured the way it is

"Prompt engineering" used to be the umbrella term for getting good output from a model. That
changed in 2025: Andrej Karpathy proposed **context engineering** as the more accurate
umbrella — the discipline of designing everything a model sees before it generates a
response (instructions, retrieved knowledge, tool results, memory, guardrails) — and
Anthropic, LangChain, and Chroma converged on that framing within months. Prompt engineering
and guardrail design didn't disappear; they became **sub-disciplines inside context
engineering**, not peers to it.

This repo's structure reflects that lineage instead of ignoring it:

```
LLM-Systems-Engineering/
  context-engineering/          # the umbrella: designing the full information environment
    prompt-engineering/         # sub-discipline: crafting the instruction layer
    guardrail-engineering/      # sub-discipline: constraints, validation, safety nets
  harness-engineering/          # the scaffolding around a model call: loops, retries, evals
  agent-engineering/            # multi-step, tool-using, multi-agent system design
  embedding-engineering/        # representation, retrieval, and chunking strategy
```

Harness, Agent, and Embedding Engineering are not sub-disciplines of context engineering —
they're adjacent systems-engineering concerns that overlap with it but aren't subsumed by it.

## Format

Every domain follows the same shape:

- `README.md` — what the domain is, why it matters, when it applies
- `types/` — one short file per technique or sub-type: definition, when to use it / when not
  to, and a worked example
- `examples/` — runnable code with logged, actual output, not just prose

## Status

| Domain | Status |
|---|---|
| Context Engineering (parent) | Overview complete |
| ├─ Prompt Engineering | **Built** — 9 techniques, worked example included |
| └─ Guardrail Engineering | Stub — next up |
| Harness Engineering | Stub |
| Agent Engineering | Stub |
| Embedding Engineering | Stub |

## Related production repos

Guardrail and Agent Engineering concepts are demonstrated at production scale elsewhere in my
work rather than re-explained here:

- [PromptGuard](https://github.com/beawesome8/Prompt-Guard) — CI/CD safety gate for LLM prompt changes
- [CodeMark Red-Team](https://github.com/beawesome8/codemark-redteam) — adversarial robustness testing
- [Recurring Research Agent](https://github.com/beawesome8/Recurring-research-agent) — multi-node LangGraph agent with memory
- [BQ-Vertex-Analyst](https://github.com/beawesome8/BQ-Vertex-Analyst) — schema-aware SQL generation agent with validation gating
