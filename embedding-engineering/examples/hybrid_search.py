"""
hybrid_search.py

Hybrid retrieval: fuse a sparse ranking (TF-IDF, exact words) with a dense-style ranking
(vector similarity) using Reciprocal Rank Fusion (RRF), then compare recall@1 for each.

HONEST CAVEAT: there is no embedding model here. `toy_embed` hashes character trigrams
into a fixed-size vector, so it matches *spelling-similar* text ("refunded" ~ "refund"),
not *meaning-similar* text ("money back" ~ "refund"). It stands in for the dense side so the
fusion mechanics run offline. Swap it for a real embedding model (sentence-transformers, a
hosted embeddings API) to see genuine semantic matching; `rrf()` does not change.

Usage: python hybrid_search.py
"""
import math
import zlib
from corpus import DOCS, QUESTIONS, tfidf_rank
from chunking_recall import by_paragraph

DIM = 256


def toy_embed(text):
    v = [0.0] * DIM
    t = f"  {text.lower()}  "
    for i in range(len(t) - 2):
        v[zlib.crc32(t[i:i + 3].encode()) % DIM] += 1.0   # crc32, not hash(): Python's str hash is salted per run
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def dense_rank(query, chunks):
    q = toy_embed(query)
    scores = [sum(a * b for a, b in zip(q, toy_embed(c))) for c in chunks]
    return sorted(range(len(chunks)), key=lambda i: -scores[i])


def rrf(rankings, k=60):
    """Reciprocal Rank Fusion: score = sum over rankers of 1/(k + rank). Needs ranks, not scores."""
    score = {}
    for ranking in rankings:
        for rank, idx in enumerate(ranking, start=1):
            score[idx] = score.get(idx, 0) + 1 / (k + rank)
    return sorted(score, key=lambda i: -score[i])


if __name__ == "__main__":
    chunks = [c for t in DOCS.values() for c in by_paragraph(t)]
    rankers = {
        "sparse (tf-idf)":     lambda q: tfidf_rank(q, chunks),
        "dense (toy trigram)": lambda q: dense_rank(q, chunks),
        "hybrid (RRF)":        lambda q: rrf([tfidf_rank(q, chunks), dense_rank(q, chunks)]),
    }
    print(f"{'retriever':22} recall@1")
    for name, rank in rankers.items():
        hits = sum(answer in chunks[rank(q)[0]] for q, answer in QUESTIONS)
        print(f"{name:22} {hits}/{len(QUESTIONS)}")
