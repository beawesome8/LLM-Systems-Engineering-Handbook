"""
retry_backoff.py

Retry harness: wrap a flaky model call with exponential backoff + jitter, retry only
errors that are worth retrying, and give up loudly after a bounded number of attempts.

The "model" is a stub that fails on a script, so the run is deterministic and needs no key.
To use a real client, replace `flaky_model` with a function that calls the API and raises
`Transient` for 429/5xx/timeouts and `Permanent` for 400/401/403.

Usage: python retry_backoff.py
"""
import random


class Transient(Exception):
    """Worth retrying: rate limit, 5xx, timeout."""


class Permanent(Exception):
    """Retrying cannot help: bad request, auth failure."""


def call_with_retry(fn, max_attempts=4, base=0.5, cap=8.0, sleep=print, rng=random.Random(0)):
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except Permanent:
            raise                                   # never retry these
        except Transient as e:
            if attempt == max_attempts:
                raise RuntimeError(f"gave up after {attempt} attempts: {e}") from e
            delay = rng.uniform(0, min(cap, base * 2 ** (attempt - 1)))   # "full jitter"
            sleep(f"  attempt {attempt} failed ({e}); waiting {delay:.2f}s")


def scripted(*outcomes):
    """A stub model: each call pops the next outcome (an exception to raise, or a string to return)."""
    it = iter(outcomes)

    def call():
        out = next(it)
        if isinstance(out, Exception):
            raise out
        return out
    return call


if __name__ == "__main__":
    print("1) recovers after two transient errors")
    print("  ->", call_with_retry(scripted(Transient("429 rate limited"), Transient("503"), "ok: answer")))

    print("2) permanent error is not retried")
    try:
        call_with_retry(scripted(Permanent("401 bad key"), "never reached"))
    except Permanent as e:
        print("  -> raised immediately:", e)

    print("3) gives up after max_attempts")
    try:
        call_with_retry(scripted(*[Transient("timeout")] * 4), max_attempts=3)
    except RuntimeError as e:
        print("  ->", e)
