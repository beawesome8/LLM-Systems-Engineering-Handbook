# Embedding Engineering

**Status: stub — not yet built.**

The design decisions around representing and retrieving information: embedding model choice,
chunking strategy, dense vs. sparse retrieval, and hybrid search.

## Where this is already demonstrated at production scale

- [DocuVet](https://github.com/beawesome8/DocuVet) — multimodal document intake with
  structured extraction (OCR + embeddings)
- [Recurring Research Agent](https://github.com/beawesome8/Recurring-research-agent) —
  Chroma-based vector memory

## Planned content for this folder

- Types: dense vs. sparse embeddings, chunking strategy, hybrid search
- Worked example: retrieval-quality comparison (recall@k) across 2-3 chunking strategies on
  the same document set — not yet built.
