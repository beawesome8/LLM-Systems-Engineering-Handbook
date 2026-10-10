# Retry and Backoff Harness

**Definition:** Wrapping model (and tool) calls so transient failures are retried safely,
with growing delays, and permanent failures are surfaced immediately.

**When to use it:** Always, on any networked call. Rate limits (HTTP 429), overload (5xx),
and timeouts are routine at scale, not exceptional.

**When not to retry:** Permanent errors: bad request (400), auth failure (401/403), a
schema your own code got wrong. Retrying only wastes time and money.

## Recipe

1. **Classify the error**: transient (429, 5xx, timeout, connection reset) vs. permanent.
2. **Exponential backoff with jitter**: wait `random(0, min(cap, base * 2^attempt))`.
   Jitter stops many clients retrying in lockstep and re-crashing the service.
3. **Honor `Retry-After`** headers when the server sends them.
4. **Bound attempts** (3-5) and total time.
5. **Make retries safe**: retrying a *read* is free; retrying a *write* (send email, charge
   card) needs an idempotency key or it happens twice.
6. **Fail loudly** after the last attempt, with the original error attached.

## Run it

[`../examples/retry_backoff.py`](../examples/retry_backoff.py), logged in
[`retry_backoff_output.txt`](../examples/retry_backoff_output.txt): recovery after two
transient errors, an immediately raised permanent error, and a bounded give-up. The sleep is
printed rather than performed so the demo is instant and deterministic.

## Beyond retries

- **Fallback model or provider** when the primary is down.
- **Circuit breaker**: after N consecutive failures, stop calling for a while.
- **Timeouts on every call.** An unbounded call is worse than a failed one.
- **Validation retries** are a different thing: re-asking because the *output* was malformed
  (see [output validation](../../context-engineering/guardrail-engineering/types/output-validation.md)).
  Cap them separately and low (1-2).
