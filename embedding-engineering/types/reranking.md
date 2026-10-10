# Reranking

**Definition:** A two-stage retrieval design. Stage 1 (fast, approximate) pulls a broad
candidate set, say the top 50, with embeddings and/or keywords. Stage 2 (slow, precise)
re-scores just those candidates with a stronger model and keeps the top 3-5.

**Why it works:** Embedding search compares a query vector to precomputed document vectors,
so the query and document never "see" each other. A **cross-encoder** reranker reads the query
and a candidate *together*, which is far better at judging relevance but too slow to run
over the whole corpus.

**When to use it:** Retrieval finds the right chunk *somewhere* in the top 20 but not at the
top (high recall@20, low recall@3), and context space is tight.

**When not to:** When recall@k is already high at the k you actually send, or latency and
cost budgets are very tight. Rerankers add a model call per candidate set.

## Options

- **Cross-encoder reranker models** (hosted rerank APIs or open models).
- **LLM-as-reranker**: ask a model to score or order candidates. Flexible, slower, costlier.
- **Heuristic rerank**: boost by recency, source authority, or exact-term match.

## Sketch

```python
candidates = hybrid_search(query, top_n=50)          # cheap, broad
scored = [(reranker.score(query, c.text), c) for c in candidates]   # precise, narrow
context = [c for _, c in sorted(scored, reverse=True)[:5]]
```

## How to know it helped

Measure recall@k and answer quality **before and after** on your eval set
([retrieval evaluation](./retrieval-evaluation.md)). If recall@50 is already low, reranking
cannot help: it only reorders what stage 1 found.
