# Context Engineering

Context engineering is the design of everything a model sees before it generates a response:
system instructions, retrieved knowledge, tool definitions and results, conversation memory,
structured state, and guardrails. It displaced "prompt engineering" as the umbrella term once
agentic systems made the instruction string a small fraction of what is fed to the model.

## Why it displaced prompt engineering

In a single-turn chatbot the prompt was almost the whole story. In an agent that runs dozens
of tool calls, retrieves documents mid-task, and keeps memory across sessions, the
instruction text is one layer among several, and often not the layer that decides success.
A model can only use what is in its context window, so *what goes in the window* is the
engineering problem.

## The four operations

A widely used framing (popularized by LangChain) splits the work into four verbs. Use them
as a checklist when a system gives bad answers: which verb failed?

| Operation | Question it answers | Typical failure | Where in this repo |
|---|---|---|---|
| **Write** | What persistent instructions, rules, and format does the model always get? | Vague or contradictory system prompt | [static context](./types/static-context.md), [prompt engineering](./prompt-engineering/) |
| **Select** | Which knowledge, history, and tools are relevant *this turn*? | Right document never retrieved; wrong tool offered | [dynamic context](./types/dynamic-context.md), [embedding engineering](../embedding-engineering/) |
| **Compress** | How do we stay inside the window as context grows? | Summary drops the user's original goal | [context compaction](./types/context-compaction.md) |
| **Isolate** | How do we keep unrelated concerns from interfering? | One agent's tool noise pollutes another's reasoning | [structured context](./types/structured-context.md), [orchestrator-workers](../agent-engineering/types/orchestrator-workers.md) |

## Types of context

| Type | What it governs | Page |
|---|---|---|
| Static | Fixed system prompt, persona, standing rules | [static-context.md](./types/static-context.md) |
| Dynamic / retrieval-augmented | Context assembled per turn from retrieval, memory, live data | [dynamic-context.md](./types/dynamic-context.md) |
| Compaction / pruning | Summarizing or trimming so the window does not degrade | [context-compaction.md](./types/context-compaction.md) |
| Structured | Typed, delimited input and output (tags, JSON, schemas) | [structured-context.md](./types/structured-context.md) |

## Sub-disciplines

- **[Prompt Engineering](./prompt-engineering/)** - the instruction layer: wording, examples,
  reasoning elicitation. 10 techniques with example prompts.
- **[Guardrail Engineering](./guardrail-engineering/)** - the constraint layer: input and output
  validation, grounding, adversarial testing.

## Run the example

```bash
python examples/context_budget.py
```

Builds one context from system prompt + selected documents + compressed history + the user
question under a token budget, and prints each section's token cost. Logged output:
[`examples/context_budget_output.txt`](./examples/context_budget_output.txt). Run it at two
budgets and read what gets sacrificed first, and whether that was the right sacrifice.

## Practical heuristics

1. **Smallest sufficient context.** Add something only if you can say what failure it fixes.
2. **Order matters.** Stable content first (cacheable), the task and question last.
3. **Every token is a budget line.** Cost, latency, and attention all scale with context.
4. **Debug by reading the actual context.** When output is wrong, print exactly what the model
   received before blaming the model. Most bugs are visible there.
