# Retrieval Evaluation

**Definition:** Measuring retrieval quality on its own, *separately* from generation. Without
this, a bad answer could come from retrieval, ranking, context assembly, or the model, and
you cannot tell which to fix.

## The test set

A list of `(question, where the answer lives)` pairs. 20-50 real questions is enough to
start. In the examples here, "where the answer lives" is a text span that must appear in a
retrieved chunk:

```python
("What encryption protects stored customer data?", "encrypted at rest using AES-256")
```

Build it from real user questions, support tickets, and the failures you have seen. Write
the expected passage by hand; generating both question and answer with a model produces
flattering, easy tests.

## Metrics

| Metric | Meaning | Use it for |
|---|---|---|
| **recall@k** | Fraction of questions where a correct chunk is in the top k | The main one: "did the answer reach the model?" |
| **precision@k** | Fraction of the top k that are relevant | Noise in the context |
| **MRR** (mean reciprocal rank) | Average of 1/rank of the first correct chunk | How high the right chunk sits |
| **nDCG** | Rank-weighted relevance with graded labels | Multiple relevant chunks of varying quality |

Pick the **k you actually send to the model**. recall@3 means little if you send 8 chunks.

## Workflow

1. Build the question set.
2. Compute recall@k for the current pipeline. This is your baseline.
3. Change **one** thing (chunking, embedding model, hybrid, reranker, top-k).
4. Re-measure. Keep the change only if the numbers say so.
5. Then evaluate end-to-end answer quality
   ([eval harness](../../harness-engineering/types/eval-harness.md)).

## Reading failures

Look at every miss by hand. Typical causes: answer split across chunks
([chunking](./chunking.md)); question and passage share no words
([hybrid](./hybrid-search.md), better embeddings); passage never ingested; correct chunk
retrieved but ranked low ([reranking](./reranking.md)).

## Run it

[`../examples/chunking_recall.py`](../examples/chunking_recall.py) computes recall@1 and
recall@3 for each chunking strategy. Copy its `recall_at_k` and point it at your own corpus
and questions.
