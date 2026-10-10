"""
chunking_recall.py

Compares three chunking strategies on the same corpus and questions by measuring recall@k:
for what fraction of questions does a top-k retrieved chunk contain the answer text?

Retrieval is held constant (TF-IDF, see corpus.py) so only chunking varies.

Usage: python chunking_recall.py
"""
from corpus import DOCS, QUESTIONS, tfidf_rank


def fixed(text, size=100, overlap=0):
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step)]


def by_paragraph(text):
    return [p.strip() for p in text.split("\n\n") if p.strip()]


STRATEGIES = {
    "fixed 100 chars, no overlap": lambda t: fixed(t, 100, 0),
    "fixed 100 chars, 30 overlap": lambda t: fixed(t, 100, 30),
    "paragraph":                   by_paragraph,
}


def recall_at_k(chunker, k):
    chunks = [c for t in DOCS.values() for c in chunker(t)]
    hits = 0
    for question, answer in QUESTIONS:
        top = [chunks[i] for i in tfidf_rank(question, chunks)[:k]]
        hits += any(answer in c for c in top)
    return hits / len(QUESTIONS), len(chunks)


if __name__ == "__main__":
    print(f"{'strategy':32} {'chunks':>6} {'recall@1':>9} {'recall@3':>9}")
    for name, chunker in STRATEGIES.items():
        r1, n = recall_at_k(chunker, 1)
        r3, _ = recall_at_k(chunker, 3)
        print(f"{name:32} {n:>6} {r1:>9.2f} {r3:>9.2f}")
