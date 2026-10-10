# Hybrid Search

**Definition:** Run sparse (keyword) and dense (embedding) retrieval on the same query and
fuse the two ranked lists into one.

**When to use it:** Queries that mix natural language with exact terms: "error E1042 when
refunding annual plan", product names, ids, legal citations. Each retriever covers the
other's blind spot.

**When not to:** Purely conversational queries over prose where dense alone scores well on
your eval; the extra index and complexity are not free.

## Fusing the rankings: Reciprocal Rank Fusion (RRF)

Dense scores and sparse scores live on different scales, so adding them is meaningless. RRF
ignores scores and uses only *ranks*:

```text
score(doc) = sum over rankers of  1 / (k + rank_in_that_ranker)        (k is typically 60)
```

A document ranked high by both rises to the top; a document one ranker loves and the other
ignores still gets a place. No tuning needed to start.

```python
def rrf(rankings, k=60):
    score = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking, start=1):
            score[idx] = score.get(idx, 0) + 1 / (k + rank)
    return sorted(score, key=lambda i: -score[i])
```

Alternative: a weighted sum of *normalized* scores, which allows tuning how much each side
counts but needs calibration.

## Run it

[`../examples/hybrid_search.py`](../examples/hybrid_search.py), logged in
[`hybrid_search_output.txt`](../examples/hybrid_search_output.txt).

**Honest result:** sparse, toy-dense, and hybrid all scored 5/6 at recall@1 and all missed
the same question (vocabulary mismatch between "uploaded payload... big" and "payloads larger
than 10 MB are rejected"). Fusion cannot fix a miss that *both* rankers share. It helps when
the rankers fail on *different* queries. Also, the dense side here is a character-trigram
toy, so this run demonstrates the fusion mechanics, not real semantic retrieval. Plug a real
embedding model into `dense_rank()` and re-run; the rest of the file does not change.

## Then consider

A [reranker](./reranking.md) over the fused top-N to fix the order, and
[retrieval evaluation](./retrieval-evaluation.md) to know whether any of this helped.
