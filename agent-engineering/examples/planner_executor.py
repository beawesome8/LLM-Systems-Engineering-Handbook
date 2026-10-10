"""
planner_executor.py

Planner/executor pattern: one call produces an explicit plan (a list of steps), an executor
runs the steps with tools, and a failed step triggers a re-plan of only the remaining work.

`plan()` is a rule-based stub standing in for a model call that returns JSON steps. The
structure is the lesson: plan is data you can inspect, log, validate, and edit before any
tool runs - something a single opaque loop does not give you.

Usage: python planner_executor.py
"""

TOOLS = {
    "search": lambda q: {"snippet": f"Acme revenue 2024 was $12M (source: report for '{q}')"},
    "calc":   lambda expr: {"value": eval(expr, {"__builtins__": {}})},   # ponytail: eval is demo-only, use a real expression parser
    "fetch_prior_year": lambda: (_ for _ in ()).throw(RuntimeError("data source offline")),
}


def plan(goal, failed=None):
    """Stub planner. A real one prompts a model: 'return a JSON list of {tool, args}' for the goal."""
    if failed == "fetch_prior_year":                                   # re-plan around the broken tool
        return [{"tool": "search", "args": {"q": "Acme revenue 2023"}},
                {"tool": "calc", "args": {"expr": "12 / 10 - 1"}}]
    return [{"tool": "search", "args": {"q": "Acme revenue 2024"}},
            {"tool": "fetch_prior_year", "args": {}},
            {"tool": "calc", "args": {"expr": "12 / 10 - 1"}}]


def execute(goal, max_replans=1):
    steps, done, replans = plan(goal), [], 0
    while steps:
        step = steps.pop(0)
        try:
            out = TOOLS[step["tool"]](**step["args"])
            done.append((step, out))
            print(f"  ok     {step['tool']}{step['args']} -> {out}")
        except Exception as e:
            print(f"  FAILED {step['tool']}: {e}")
            if replans >= max_replans:
                return "FAILED: out of replans", done
            replans += 1
            steps = plan(goal, failed=step["tool"])               # replace only the remaining work
            print(f"  re-planned -> {[s['tool'] for s in steps]}")
    return f"growth = {done[-1][1]['value']:.0%}", done


if __name__ == "__main__":
    print("goal: year-over-year revenue growth for Acme")
    result, _ = execute("yoy growth")
    print("result:", result)
