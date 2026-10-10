# Glossary

Terms used across the handbook, alphabetical.

**Agent** - A system where the model decides at runtime which step or tool comes next. See
[Agent Engineering](./agent-engineering/).

**Backoff (exponential)** - Waiting longer after each failed retry (1s, 2s, 4s...), usually
with random *jitter*. See [retry and backoff](./harness-engineering/types/retry-and-backoff.md).

**BM25 / TF-IDF** - Classic sparse ranking methods that score documents by matching query
words, weighted by how rare each word is.

**Chain of thought (CoT)** - Having the model write out intermediate reasoning before its
answer. See [Zero-Shot CoT](./context-engineering/prompt-engineering/types/zero-shot-cot.md).

**Chunk** - A piece of a document that is embedded and retrieved as one unit.
See [chunking](./embedding-engineering/types/chunking.md).

**Context engineering** - Designing everything the model sees before it responds.
See [Context Engineering](./context-engineering/).

**Context window** - The maximum amount of text (measured in tokens) a model can consider
in one call: input plus output.

**Cosine similarity** - A measure of how closely two vectors point in the same direction;
the usual way to compare embeddings.

**Cross-encoder** - A model that reads query and candidate *together* to score relevance;
used for [reranking](./embedding-engineering/types/reranking.md).

**Dense retrieval** - Retrieval using embedding vectors that capture meaning.

**Embedding** - A vector of numbers representing a piece of text so that similar meanings are
close together. See [Embedding Engineering](./embedding-engineering/).

**Eval (evaluation) harness** - Code that runs a test set through a system and scores the
output. See [eval harness](./harness-engineering/types/eval-harness.md).

**False positive / false negative** - For a guardrail: blocking good output / letting bad
output through. See [Guardrail Engineering](./context-engineering/guardrail-engineering/).

**Few-shot / zero-shot** - Prompting with a few examples / with none.

**Grounding** - Tying model claims to supplied source material.
See [hallucination grounding](./context-engineering/guardrail-engineering/types/hallucination-grounding.md).

**Guardrail** - A check or constraint that bounds what a system accepts, does, or emits.

**Hallucination** - Fluent output that is unsupported or false.

**Harness** - The code around a model call providing loops, retries, limits, evals, and
oversight. See [Harness Engineering](./harness-engineering/).

**Human-in-the-loop (HITL)** - A checkpoint where a person approves or edits before the system
acts. See [HITL](./harness-engineering/types/human-in-the-loop.md).

**Hybrid search** - Combining sparse and dense retrieval.
See [hybrid search](./embedding-engineering/types/hybrid-search.md).

**Idempotency key** - A token that makes a repeated request take effect only once, so
retrying a write is safe.

**LLM-as-judge** - Using a model to grade another model's output against a rubric.

**Prompt caching** - Provider feature that reuses a processed, unchanged prompt prefix to
cut cost and latency. Favors putting stable text first.

**Prompt injection** - Text in the input (or in retrieved content) that tries to override your
instructions. *Indirect* injection hides in documents, pages, or emails the model reads.

**RAG (retrieval-augmented generation)** - Retrieving relevant documents and putting them in
context so the model answers from them.

**recall@k** - Fraction of queries whose correct passage appears in the top k results.
See [retrieval evaluation](./embedding-engineering/types/retrieval-evaluation.md).

**Reranking** - A second, more precise scoring pass over top retrieval candidates.

**RRF (reciprocal rank fusion)** - Merging ranked lists by summing `1/(k+rank)`.

**Sparse retrieval** - Keyword-based retrieval over word-occurrence vectors.

**System prompt** - Persistent instructions given to the model ahead of the conversation.

**Token** - The unit a model reads and writes, roughly a short word or word fragment (about 4
characters of English). Cost, latency, and window size are all counted in tokens.

**Tool use (function calling)** - The model requesting that your code run a named function
with given arguments, then receiving the result. See [tool loop](./harness-engineering/types/tool-loop.md).

**Vector index** - A data structure for finding the nearest embeddings quickly.

**Workflow** - A predefined sequence of steps where your code, not the model, chooses the
path. Contrast with *agent*.
