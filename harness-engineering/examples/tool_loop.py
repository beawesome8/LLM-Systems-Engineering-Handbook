"""
tool_loop.py

The core agentic harness: call model -> if it asks for a tool, run it and feed the result
back -> repeat until it answers, with hard limits and a human-approval gate on risky tools.

The model is a scripted stub that emits the same *shape* of turn a real tool-using model
does (a tool request, then a final answer), so the loop runs offline and deterministically.
To go real: replace `scripted_model` with a Messages API call and map `tool_use` blocks to
the `("tool", name, args)` tuples below.

Usage: python tool_loop.py
"""

TOOLS = {
    "get_order":    lambda order_id: {"id": order_id, "status": "shipped", "total": 42.0},
    "refund_order": lambda order_id: {"id": order_id, "refunded": True},
}
NEEDS_APPROVAL = {"refund_order"}   # side-effecting tools get a human checkpoint


def scripted_model(script):
    it = iter(script)
    return lambda history: next(it)   # ponytail: ignores history; a real model reads it


def run(model, user_msg, approve, max_steps=6):
    history = [("user", user_msg)]
    for step in range(1, max_steps + 1):
        kind, *payload = model(history)
        if kind == "final":
            return payload[0], history
        name, args = payload
        if name not in TOOLS:                                   # model hallucinated a tool
            result = {"error": f"unknown tool {name}"}
        elif name in NEEDS_APPROVAL and not approve(name, args):  # human-in-the-loop gate
            result = {"error": "denied by human reviewer"}
        else:
            try:
                result = TOOLS[name](**args)
            except Exception as e:                              # errors go back to the model, not up the stack
                result = {"error": str(e)}
        history.append(("tool", name, args, result))
        print(f"  step {step}: {name}({args}) -> {result}")
    return "STOPPED: max_steps reached", history                # bounded: a loop must never run forever


if __name__ == "__main__":
    script = [("tool", "get_order", {"order_id": "A1"}),
              ("tool", "refund_order", {"order_id": "A1"}),
              ("final", "Order A1 has been refunded.")]
    print("approved:")
    print("  ->", run(scripted_model(script), "Refund order A1", approve=lambda n, a: True)[0])
    print("denied:")
    script2 = [("tool", "refund_order", {"order_id": "A1"}), ("final", "I could not refund it; a human declined.")]
    print("  ->", run(scripted_model(script2), "Refund order A1", approve=lambda n, a: False)[0])
    print("runaway model hits the step limit:")
    print("  ->", run(scripted_model([("tool", "get_order", {"order_id": "A1"})] * 10), "loop", approve=lambda n, a: True, max_steps=3)[0])
