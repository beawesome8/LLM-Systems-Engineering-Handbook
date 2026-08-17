# Context Engineering

Context engineering is the systematic design of everything a model sees before it generates
a response: system instructions, retrieved knowledge, tool definitions and results,
conversation/session memory, structured state, and guardrails. It replaced "prompt
engineering" as the field's umbrella term once agentic systems made the instruction string a
small fraction of what actually gets fed to the model.

## Why it displaced prompt engineering

In a single-turn chatbot, the prompt was almost the whole story. In a multi-step agent
running dozens of tool calls, retrieving documents mid-task, and maintaining memory across
sessions, the instruction text is one layer among several — and often not the layer that
determines success or failure. LangChain's widely-cited framework breaks the discipline into
four operations: **Write** (bake persistent instructions/constraints into the system, before
any user turn), **Select** (retrieve the right slice of knowledge/history for this turn),
**Compress** (keep the context window from collapsing under its own weight as it grows), and
**Isolate** (partition context so unrelated concerns don't interfere with each other, e.g.
multi-agent context routing).

## Sub-disciplines documented in this repo

- **[Prompt Engineering](./prompt-engineering/)** — the "Write" layer at its most granular:
  crafting the instruction itself. Still necessary, no longer sufficient.
- **[Guardrail Engineering](./guardrail-engineering/)** — the constraint/policy layer that
  gets embedded into context to bound model behavior (validation, refusal patterns, safety
  nets).

## Types of context engineering (beyond what's broken into sub-folders)

| Type | What it governs | When it matters most |
|---|---|---|
| Static context | Fixed system prompt, persona, rules that don't change per request | Simple, single-turn applications |
| Dynamic/retrieval-augmented context | Context assembled per-turn from retrieval, memory, or live data | Agents, RAG systems, anything with state |
| Context compaction/pruning | Summarizing or trimming history so the window doesn't degrade | Long-running agent sessions, multi-hour conversations |
| Structured context | Context passed as structured data (JSON, XML tags) rather than free text | Tool-use, multi-source context, anything requiring reliable parsing |

A worked comparison (static vs. dynamic context injection, measuring token cost and answer
accuracy on the same task) is the next planned addition to this folder — not yet built.
