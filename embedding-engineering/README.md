# Embedding Engineering

An **embedding** turns text (or an image, or code) into a list of numbers, a vector, such
that things with similar *meaning* land near each other. Embedding engineering is the set of
design decisions around representing and retrieving information with them: which model,
how to split documents, dense vs. sparse search, fusion, reranking, and how to measure
whether retrieval works.

It is the engine of retrieval-augmented generation (RAG): the quality of the context the
model receives ([Select](../context-engineering/types/dynamic-context.md)) is capped by the
quality of retrieval. **Most "the model hallucinated" bugs in RAG systems are really "the
right passage was never retrieved."**

## The pipeline

```text
documents -> clean -> chunk -> embed -> index
                                          |
query -> embed -> search (dense / sparse / hybrid) -> rerank -> top-k chunks -> context
```

## Types

| Topic | Decision it covers | Page | Run it |
|---|---|---|---|
| Dense vs. sparse | Meaning-based vs. keyword-based retrieval | [dense-vs-sparse.md](./types/dense-vs-sparse.md) | [`hybrid_search.py`](./examples/hybrid_search.py) |
| Chunking | How to split documents into retrievable units | [chunking.md](./types/chunking.md) | [`chunking_recall.py`](./examples/chunking_recall.py) |
| Hybrid search | Combining both rankers | [hybrid-search.md](./types/hybrid-search.md) | [`hybrid_search.py`](./examples/hybrid_search.py) |
| Reranking | A second, more precise pass over the top candidates | [reranking.md](./types/reranking.md) | - |
| Retrieval evaluation | Measuring retrieval separately from generation | [retrieval-evaluation.md](./types/retrieval-evaluation.md) | [`chunking_recall.py`](./examples/chunking_recall.py) |

## Run the examples

```bash
cd examples
python chunking_recall.py
python hybrid_search.py
```

Stdlib only, deterministic, offline. Shared toy corpus and TF-IDF retriever in
[`examples/corpus.py`](./examples/corpus.py). Logged output next to each script.

### What the logged runs show

Chunking, same retriever, six questions ([`chunking_recall_output.txt`](./examples/chunking_recall_output.txt)):

| Strategy | recall@1 | recall@3 |
|---|---|---|
| Fixed 100 chars, no overlap | 0.17 | 0.33 |
| Fixed 100 chars, 30 overlap | 0.50 | 0.67 |
| Paragraph | 0.83 | 0.83 |

Chunk boundaries alone moved recall@1 from 0.17 to 0.83, with no change to the embedding or
the search. Chunking is not a preprocessing detail.

Retrieval ([`hybrid_search_output.txt`](./examples/hybrid_search_output.txt)): sparse, dense,
and hybrid all scored 5/6 at recall@1, and they all missed the same question ("How big can an
uploaded payload be?" vs. text saying "payloads larger than 10 MB are rejected"). Hybrid did
**not** help here because both rankers failed the same way, and the "dense" ranker is a toy
(character-trigram hashing), not a semantic model. That is a vocabulary mismatch a real
embedding model is designed to close. Do not read this table as evidence about real dense
retrievers; read it as a harness you can drop a real embedding model into.

## Practical heuristics

1. **Evaluate retrieval before touching the prompt.** Build 20-50 question -> expected-passage
   pairs and track recall@k ([retrieval evaluation](./types/retrieval-evaluation.md)).
2. **Chunk by structure first** (sections, paragraphs, code blocks), by size second.
3. **Use the same embedding model for documents and queries**, and re-embed everything if you
   change it. Vectors from different models are not comparable.
4. **Try hybrid search** when queries contain exact terms: ids, error codes, names, jargon.
5. **Store metadata** (source, section, date, permissions) with each chunk. You will want to
   filter and cite.
6. **Enforce access control at retrieval time**, not in the prompt.

## See it at production scale

- [DocuVet](https://github.com/beawesome8/DocuVet) - multimodal document intake with structured extraction (OCR + embeddings)
- [Recurring Research Agent](https://github.com/beawesome8/Recurring-research-agent) - Chroma-based vector memory
