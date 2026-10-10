# Guardrail Engineering

*A sub-discipline of [Context Engineering](../).*

Guardrails are the constraints and checks that bound what a model system will accept, do, and
emit. They are layered: some live *in* the context (instructions and delimiters), others live
*around* the model call as code (validators, filters, tests). No single layer is reliable on
its own, so you stack them.

## The layers

```text
user input -> [input guardrails] -> context + model -> [output guardrails] -> action / user
                      ^                                        ^
                      +----------- adversarial testing --------+  (measures both)
```

| Type | Question it answers | Page |
|---|---|---|
| Input validation | Should this request reach the model at all? | [input-validation.md](./types/input-validation.md) |
| Output validation | Is the output well-formed and allowed? | [output-validation.md](./types/output-validation.md) |
| Hallucination grounding | Is every claim supported by the source? | [hallucination-grounding.md](./types/hallucination-grounding.md) |
| Adversarial testing | How do we find the holes before attackers do? | [adversarial-testing.md](./types/adversarial-testing.md) |

## Design principles

1. **Defense in depth.** Assume each layer will sometimes fail; make sure the next one is
   independent of it.
2. **Prefer deterministic checks first** (schema, regex, allow-lists, quote matching). They
   are cheap, explainable, and testable. Use a model-as-judge for what rules cannot express.
3. **Put the hard limit in code, not in the prompt.** A prompt saying "never delete data" is
   a request. A tool that has no delete permission is a guarantee.
4. **Least privilege for tools.** Give the model the narrowest capability that does the job.
5. **Measure the guardrail itself.** Every guardrail has false positives (blocks good output)
   and false negatives (lets bad output through). Count both, or you do not know what it does.
6. **Decide the failure mode.** When a check fails: retry, fall back, ask a human, or refuse?
   Pick deliberately.

## Run the example

```bash
python examples/output_validation_gate.py
```

A schema + groundedness gate scored against 11 labelled outputs. Logged result:
[`examples/output_validation_gate_output.txt`](./examples/output_validation_gate_output.txt).
It reports **1 false positive and 1 false negative** on purpose: the false negative is a
fabricated conclusion backed by a real quote (the gate checks the quote, not the reasoning),
and the false positive is a correct paraphrase rejected for not being a verbatim quote. Both
are the characteristic failures of this kind of check; the fix for each is a different layer,
not a tweak to this one.

## See it at larger scale

- [PromptGuard](https://github.com/beawesome8/Prompt-Guard) - CI/CD safety gate for LLM prompt changes
- [CodeMark Red-Team](https://github.com/beawesome8/codemark-redteam) - adversarial robustness testing, including negative findings
