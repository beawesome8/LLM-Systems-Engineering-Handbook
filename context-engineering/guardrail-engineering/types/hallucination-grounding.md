# Hallucination Grounding

**Definition:** Making sure claims in the output are supported by provided source material,
and detecting or blocking those that are not.

**When to use it:** Question answering over documents, summaries, anything where an invented
fact causes real harm (legal, medical, finance, policy, customer commitments).

**When not to:** Creative writing, brainstorming, and other tasks where invention is the
point.

## Techniques

| Technique | How it works | Strength | Weakness |
|---|---|---|---|
| Provide the source | Put the facts in context; instruct "answer only from the documents; say so if absent" | Biggest single improvement | Model can still drift |
| Quote-then-answer | Ask for a verbatim supporting quote, then verify the quote exists in the source with string matching | Cheap, deterministic | Rejects correct paraphrases; real quote can support a wrong conclusion |
| Citations | Require a source id per claim; check ids exist | Auditable | Ids can be valid but irrelevant |
| Entailment check | A second model call asks "does the source support this claim? yes/no" | Handles paraphrase | Costs a call; the judge can be wrong too |
| Abstention | Allow `"unknown"` as a first-class answer | Reduces forced guesses | Needs eval to avoid over-abstaining |

## Example

The gate in [`../examples/output_validation_gate.py`](../examples/output_validation_gate.py)
requires `evidence` to be a verbatim substring of the source, and the number in the answer to
appear inside that evidence. Its logged result
([`output_validation_gate_output.txt`](../examples/output_validation_gate_output.txt)) shows
both failure directions:

- **False negative**: `intent=refund_allowed` backed by the quote "Monthly plans are not
  refundable." The quote is real; the conclusion contradicts it. String matching cannot see that.
- **False positive**: a correct answer whose evidence was lightly paraphrased is blocked.

The next layer up is an entailment check, which trades a model call for fewer of both errors.

## Rule

Grounding reduces hallucination; it does not eliminate it. For high-stakes outputs, add a
human review step ([HITL](../../../harness-engineering/types/human-in-the-loop.md)).
