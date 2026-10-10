"""
orchestrator_workers.py

Multi-agent orchestration, smallest honest version: an orchestrator splits a task into
independent subtasks, each worker gets ONLY its own slice of context (isolation), workers
run in parallel, and the orchestrator merges their results.

Workers are stubs. In a real system each is a model call (or its own agent loop) with its
own system prompt and tool set. What carries over unchanged: fan-out, isolated contexts,
a typed result contract, and a merge step that tolerates a failed worker.

Usage: python orchestrator_workers.py
"""
from concurrent.futures import ThreadPoolExecutor

DOCS = {
    "pricing.md":  "Pro plan is $20/user/month. Enterprise is custom. Annual billing saves 15%.",
    "security.md": "Data is encrypted at rest with AES-256. SSO via SAML is Enterprise only.",
    "support.md":  "",   # empty on purpose: a worker will fail on it
}


def worker(name, text):
    """Stub for `model(system=f'summarise {name}', input=text)`. Returns the typed contract."""
    if not text:
        raise ValueError(f"{name} is empty")
    return {"source": name, "summary": text.split(". ")[0].rstrip(".")}


def orchestrate(docs):
    with ThreadPoolExecutor() as pool:                      # fan out: each worker sees only (name, text)
        futures = {n: pool.submit(worker, n, t) for n, t in docs.items()}
    ok, failed = [], {}
    for name, f in futures.items():
        try:
            ok.append(f.result())
        except Exception as e:                              # one bad worker must not sink the run
            failed[name] = str(e)
    merged = "\n".join(f"- {r['source']}: {r['summary']}" for r in ok)
    return merged, failed


if __name__ == "__main__":
    merged, failed = orchestrate(DOCS)
    print("merged report:\n" + merged)
    print("failed workers:", failed)
