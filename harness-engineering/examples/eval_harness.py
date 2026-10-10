"""
eval_harness.py

A minimal eval harness: run a fixed test set through two versions of a "system", score each
output with deterministic rubric checks, print pass rates and which cases regressed.

The two systems are stubs that stand in for "prompt v1" and "prompt v2". Swap `system_v1` /
`system_v2` for real model calls and the harness does not change - that is the point:
the harness is the stable part, the system under test is the part you iterate on.

Usage: python eval_harness.py
"""
import json

CASES = [
    {"id": "refund-annual", "input": "Refund for annual plan?",   "must_contain": "30 days", "must_be_json": True},
    {"id": "refund-month",  "input": "Refund for monthly plan?",  "must_contain": "not refundable", "must_be_json": True},
    {"id": "invoice",       "input": "Where are my invoices?",    "must_contain": "Billing", "must_be_json": True},
    {"id": "sso",           "input": "Do you support SSO?",       "must_contain": "Enterprise", "must_be_json": True},
]

ANSWERS_V1 = {  # v1: sometimes chatty, misses one fact
    "Refund for annual plan?":  '{"answer": "Annual plans: refund within 30 days."}',
    "Refund for monthly plan?": 'Monthly plans are not refundable.',                      # not JSON
    "Where are my invoices?":   '{"answer": "Open Billing > History."}',
    "Do you support SSO?":      '{"answer": "Yes, SSO is supported."}',                   # misses "Enterprise"
}
ANSWERS_V2 = {  # v2: fixes format + SSO, but regresses the invoice answer
    "Refund for annual plan?":  '{"answer": "Annual plans: refund within 30 days."}',
    "Refund for monthly plan?": '{"answer": "Monthly plans are not refundable."}',
    "Where are my invoices?":   '{"answer": "Check your email."}',                        # regression
    "Do you support SSO?":      '{"answer": "SSO is Enterprise plan only."}',
}


def system_v1(q): return ANSWERS_V1[q]
def system_v2(q): return ANSWERS_V2[q]


def score(case, output):
    """Return {check_name: bool}. Deterministic checks first: cheap, stable, debuggable."""
    checks = {}
    if case["must_be_json"]:
        try:
            json.loads(output)
            checks["json"] = True
        except json.JSONDecodeError:
            checks["json"] = False
    checks["contains"] = case["must_contain"].lower() in output.lower()
    return checks


def run(system):
    return {c["id"]: all(score(c, system(c["input"])).values()) for c in CASES}


if __name__ == "__main__":
    v1, v2 = run(system_v1), run(system_v2)
    for name, res in (("v1", v1), ("v2", v2)):
        print(f"{name}: {sum(res.values())}/{len(res)} pass  {res}")
    regressed = [k for k in v1 if v1[k] and not v2[k]]
    fixed = [k for k in v1 if not v1[k] and v2[k]]
    print(f"fixed by v2:     {fixed}")
    print(f"regressed in v2: {regressed}   <- a higher average can still hide this")
