# LLM Systems Engineering: A Handbook

A practical handbook for engineers learning to build systems around large language models.
Every topic has a plain-language definition, guidance on **when to use it and when not to**,
copy-pasteable examples, and (where it can run offline) a script whose real output is logged
in the repo.

It covers the layers that sit above a raw model call and below full production deployment.

## Who this is for

Software engineers who can read Python and have called an LLM API at least once, and now need
to make LLM-powered features *reliable*. No ML background required.

## How to use it

- **Read in order** (below) if you are new. Each section builds on the previous one.
- **Use it as a reference** when debugging: the table under [Debugging by symptom](#debugging-by-symptom)
  sends you to the right page.
- **Run the examples.** They take seconds. Change a number, break something, re-run.

## Learning path

| Step | Read | You will learn | Time |
|---|---|---|---|
| 1 | [Context Engineering](./context-engineering/) | The mental model: a model only knows what is in its context window | 20 min |
| 2 | [Prompt Engineering](./context-engineering/prompt-engineering/) | 10 techniques for the instruction layer | 40 min |
| 3 | [Embedding Engineering](./embedding-engineering/) | How retrieval (RAG) finds the right context | 40 min |
| 4 | [Guardrail Engineering](./context-engineering/guardrail-engineering/) | Validating inputs and outputs; why no check is perfect | 30 min |
| 5 | [Harness Engineering](./harness-engineering/) | Tool loops, retries, evals, human approval | 45 min |
| 6 | [Agent Engineering](./agent-engineering/) | Planners, multi-agent systems, and when *not* to use them | 40 min |
| Ref | [Glossary](./GLOSSARY.md) | Every term in one place | - |

## The map

"Prompt engineering" used to be the umbrella term for getting good output from a model. In
2025 **context engineering** (a term popularized by Andrej Karpathy and quickly adopted across
the industry) took over as the umbrella: the discipline of designing *everything* a model sees
before it responds: instructions, retrieved knowledge, tool results, memory, and guardrails.
Prompt engineering and guardrail design became **sub-disciplines inside it**.

```text
LLM-Systems-Engineering/
  context-engineering/          # umbrella: designing the full information environment
    types/                      #   static, dynamic, compaction, structured context
    examples/                   #   context_budget.py
    prompt-engineering/         # sub-discipline: the instruction layer (10 techniques)
    guardrail-engineering/      # sub-discipline: validation, grounding, red-teaming
  embedding-engineering/        # representation and retrieval: chunking, dense/sparse, hybrid
  harness-engineering/          # reliability scaffolding: loops, retries, evals, approvals
  agent-engineering/            # control structures: tool use, planning, multi-agent
```

Harness, Agent, and Embedding Engineering are not sub-disciplines of context engineering.
They are adjacent systems concerns that overlap with it but are not subsumed by it.

How the pieces fit in one request:

```text
user request
   -> guardrail: validate input
   -> embedding: retrieve relevant chunks            (Select)
   -> context: assemble system prompt + chunks + history under a budget   (Write, Compress, Isolate)
   -> agent: model chooses tools / plan
   -> harness: loop, retry, limit, ask a human if risky
   -> guardrail: validate output, check grounding
   -> response
(eval harness runs all of the above against a test set on every change)
```

## Every domain has the same shape

- `README.md`: what it is, why it matters, design principles, how to run the examples
- `types/`: one page per technique, with definition, when to use / not to use, and an example
- `examples/`: runnable code with logged output (`*_output.txt`)

## Running the examples

Python 3.9+. All examples are standard library only and run offline, with stub models,
except one:

```bash
python context-engineering/examples/context_budget.py
python context-engineering/guardrail-engineering/examples/output_validation_gate.py
python harness-engineering/examples/tool_loop.py            # also retry_backoff.py, eval_harness.py
python agent-engineering/examples/planner_executor.py       # also orchestrator_workers.py
python embedding-engineering/examples/chunking_recall.py    # also hybrid_search.py
```

The exception is [`few_shot_vs_zero_shot.py`](./context-engineering/prompt-engineering/examples/few_shot_vs_zero_shot.py),
which calls the Claude API (`pip install anthropic`, set `ANTHROPIC_API_KEY`). Its output is
left for you to log, because the value is in reading real differences yourself.

**About the stubs.** Stub models and toy retrievers are labelled as such in each file. They let
you see the *structure* (loops, limits, fusion, gates) deterministically and for free. They are
not evidence about how real models behave. Each page says what the stub stands in for and how
to swap in the real thing.

## Debugging by symptom

| Symptom | Likely layer | Start at |
|---|---|---|
| Answer is wrong but the right document exists | Retrieval | [Retrieval evaluation](./embedding-engineering/types/retrieval-evaluation.md), [Chunking](./embedding-engineering/types/chunking.md) |
| Answer invents facts | Grounding | [Hallucination grounding](./context-engineering/guardrail-engineering/types/hallucination-grounding.md) |
| Output format breaks downstream code | Output validation | [Output validation](./context-engineering/guardrail-engineering/types/output-validation.md) |
| Wrong labels or style on a narrow task | Prompt | [Few-shot](./context-engineering/prompt-engineering/types/few-shot.md) |
| Fails multi-step reasoning | Prompt | [Zero-shot CoT](./context-engineering/prompt-engineering/types/zero-shot-cot.md) |
| Gets worse in long conversations | Context | [Context compaction](./context-engineering/types/context-compaction.md) |
| Agent loops or picks wrong tools | Agent / harness | [Single-agent tool use](./agent-engineering/types/single-agent-tool-use.md), [Tool loop](./harness-engineering/types/tool-loop.md) |
| Random 429 / 5xx errors | Harness | [Retry and backoff](./harness-engineering/types/retry-and-backoff.md) |
| "Did my prompt change help?" | Harness | [Eval harness](./harness-engineering/types/eval-harness.md) |
| Dangerous or irreversible actions | Harness / guardrail | [Human-in-the-loop](./harness-engineering/types/human-in-the-loop.md) |
| Prompt injection worries | Guardrail | [Input validation](./context-engineering/guardrail-engineering/types/input-validation.md), [Adversarial testing](./context-engineering/guardrail-engineering/types/adversarial-testing.md) |

## Five principles that run through everything

1. **The model only knows what is in its context.** Debug by reading exactly what it received.
2. **Measure, do not assume.** Every technique here is a hypothesis until an eval says otherwise.
3. **Use the least complexity that works.** Single call before workflow, workflow before agent.
4. **Enforce limits in code, not in prompts.** Prompts are requests; code is a guarantee.
5. **Count your failures.** Every guardrail and retriever has false positives and false
   negatives; know your numbers.

## Status

| Domain | Pages | Runnable example |
|---|---|---|
| [Context Engineering](./context-engineering/) | 4 types | `context_budget.py` |
| [Prompt Engineering](./context-engineering/prompt-engineering/) | 10 techniques | `few_shot_vs_zero_shot.py` (needs API key) |
| [Guardrail Engineering](./context-engineering/guardrail-engineering/) | 4 types | `output_validation_gate.py` |
| [Embedding Engineering](./embedding-engineering/) | 5 topics | `chunking_recall.py`, `hybrid_search.py` |
| [Harness Engineering](./harness-engineering/) | 4 types | `tool_loop.py`, `retry_backoff.py`, `eval_harness.py` |
| [Agent Engineering](./agent-engineering/) | 4 patterns | `planner_executor.py`, `orchestrator_workers.py` |

## Production-scale companions

Concepts here are demonstrated end to end in these projects:

- [PromptGuard](https://github.com/beawesome8/Prompt-Guard) - CI/CD safety gate for LLM prompt changes
- [CodeMark Red-Team](https://github.com/beawesome8/codemark-redteam) - adversarial robustness testing
- [Recurring Research Agent](https://github.com/beawesome8/Recurring-research-agent) - multi-node LangGraph agent with memory
- [BQ-Vertex-Analyst](https://github.com/beawesome8/BQ-Vertex-Analyst) - schema-aware SQL generation agent with validation gating
- [DocuVet](https://github.com/beawesome8/DocuVet) - multimodal document intake with structured extraction

## Further reading

- Anthropic, *Building effective agents* (workflows vs. agents, the patterns in
  [Agent Engineering](./agent-engineering/)) and the Claude documentation on prompt
  engineering and tool use.
- Papers behind the prompting techniques are cited at the bottom of each technique page.

## License

See [LICENSE](./LICENSE).
