"""Shared toy corpus + retrieval helpers for the embedding-engineering examples (stdlib only)."""
import math
import re
from collections import Counter

DOCS = {
    "refunds": (
        "Refund policy\n\n"
        "Customers on an annual plan may request a full refund within 30 days of the purchase date. "
        "After 30 days, refunds are not available but the plan can be cancelled to stop renewal.\n\n"
        "Monthly plans are never refundable. Cancelling a monthly plan takes effect at the end of the billing period. "
        "Refunds, when granted, are issued to the original payment method within 5 to 10 business days."
    ),
    "security": (
        "Security overview\n\n"
        "All customer data is encrypted at rest using AES-256 and in transit using TLS 1.3. "
        "Encryption keys are rotated every 90 days by an automated job.\n\n"
        "Single sign-on through SAML 2.0 is available on the Enterprise plan only. "
        "Administrators can enforce two-factor authentication for every user in the workspace settings."
    ),
    "limits": (
        "API limits\n\n"
        "The default rate limit is 600 requests per minute per API key. "
        "Requests above the limit receive HTTP 429 and should be retried with exponential backoff.\n\n"
        "Payloads larger than 10 MB are rejected with HTTP 413. "
        "Batch endpoints accept up to 500 items per call and are billed per item."
    ),
    "billing": (
        "Billing guide\n\n"
        "Invoices are available under Billing then History, and each one can be downloaded as a PDF. "
        "Invoices are generated on the first day of each billing period.\n\n"
        "Failed card payments are retried three times over seven days before the workspace is suspended. "
        "Updating the card on file triggers an immediate retry."
    ),
}

# (question, text that must be inside a retrieved chunk for the retrieval to count as a hit)
QUESTIONS = [
    ("How long do annual customers have to ask for their money back?", "within 30 days of the purchase date"),
    ("What encryption protects stored customer data?", "encrypted at rest using AES-256"),
    ("Which plan supports SAML single sign-on?", "available on the Enterprise plan only"),
    ("What status code means I sent too many requests?", "receive HTTP 429"),
    ("How many times is a failed card charge retried?", "retried three times over seven days"),
    ("How big can an uploaded payload be?", "larger than 10 MB are rejected"),
]

WORD = re.compile(r"[a-z0-9]+")


def words(text):
    return WORD.findall(text.lower())


def tfidf_rank(query, chunks):
    """Return chunk indices best-first, scored by TF-IDF cosine similarity (sparse retrieval)."""
    df = Counter(w for c in chunks for w in set(words(c)))
    n = len(chunks)
    idf = lambda w: math.log((n + 1) / (df.get(w, 0) + 1)) + 1

    def vec(text):
        tf = Counter(words(text))
        return {w: c * idf(w) for w, c in tf.items()}

    def cos(a, b):
        dot = sum(a[w] * b.get(w, 0) for w in a)
        na, nb = math.sqrt(sum(v * v for v in a.values())), math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    q = vec(query)
    scores = [cos(q, vec(c)) for c in chunks]
    return sorted(range(n), key=lambda i: -scores[i])
