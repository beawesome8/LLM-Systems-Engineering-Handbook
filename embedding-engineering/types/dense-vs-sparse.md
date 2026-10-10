# Dense vs. Sparse Retrieval

**Sparse** retrieval represents text by *which words it contains* (vectors with one slot per
vocabulary word, mostly zero). TF-IDF and BM25 are the classics. It matches exact terms.

**Dense** retrieval represents text with a learned embedding model: a few hundred to a few
thousand numbers per text, with *meaning* encoded across all of them. It matches paraphrases.

| | Sparse (BM25 / TF-IDF) | Dense (embeddings) |
|---|---|---|
| Matches | Same words | Same meaning, different words |
| Strong at | Ids, error codes, names, rare jargon | Paraphrase, natural-language questions, cross-language |
| Weak at | Synonyms ("money back" vs "refund") | Exact strings, rare tokens, numbers |
| Cost | Cheap, no model | Embedding calls + vector index |
| Explainable | Yes (which words matched) | Hard |
| Needs training data | No | Uses a pretrained model |

## How similarity works

Dense retrieval compares vectors, usually with **cosine similarity** (the angle between
them). Closer angle = more similar meaning. A vector index (FAISS, HNSW-based stores, Chroma,
pgvector, and others) finds nearest neighbors fast, usually approximately.

## Choosing

- **Start with what you can measure.** Build the eval first
  ([retrieval evaluation](./retrieval-evaluation.md)).
- **Natural-language Q&A over prose** -> dense is usually stronger.
- **Lookup of exact identifiers** -> sparse is usually stronger.
- **Unsure, or mixed queries** -> [hybrid](./hybrid-search.md).

## Embedding model choice

Consider: quality on your domain (check your own eval, not only public benchmarks), vector
dimension (storage and speed), maximum input length (limits chunk size), language coverage,
cost and latency, and whether you can self-host. Changing models means re-embedding the
whole corpus.

## Run it

[`../examples/hybrid_search.py`](../examples/hybrid_search.py) has a real TF-IDF ranker and a
**toy** dense ranker (hashed character trigrams, which matches spelling similarity, not
meaning). It is labelled as a stand-in in the file; swap in a real embedding model to see
genuine semantic matching.
