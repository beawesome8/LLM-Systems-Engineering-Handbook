# Human-in-the-Loop (HITL) Harness

**Definition:** Checkpoints in the loop where a person approves, edits, or rejects what the
system is about to do or return.

**When to use it:** Actions that are hard to undo or outward-facing (sending messages,
spending money, deleting or overwriting data, publishing), high-stakes outputs (medical,
legal, financial), and the early life of any new system while you learn its failure modes.

**When not to:** Read-only or easily reversible steps. Approval prompts on everything cause
**approval fatigue**: people click "yes" without reading, which is worse than no gate because
it creates false assurance.

## Placement patterns

| Pattern | How it works | Good for |
|---|---|---|
| Approve-before-act | Pause before a risky tool call; human says yes/no | Destructive or costly tools |
| Review-before-send | Model drafts, human edits and sends | Customer communication |
| Escalate-on-uncertainty | Low confidence or failed validation routes to a person | Mixed-difficulty queues |
| Sample audit | Humans review a random slice after the fact | High volume, lower risk |

## Design rules

- **Gate by risk, not by default.** Classify tools as read / reversible-write / irreversible
  and gate only the last (or the last two).
- **Show the human what will happen**, not what the model said. "Refund order A1 for $42.00"
  beats a paragraph of reasoning.
- **Make "no" a first-class result.** The model should receive the denial and adapt.
- **Log decisions** (who, what, when). They become eval data.
- **Enforce in code.** The gate must be in the harness, not in a prompt asking the model to
  "check with the user first."

## Run it

[`../examples/tool_loop.py`](../examples/tool_loop.py) marks `refund_order` as needing
approval. Its `approve` callback is a lambda here; in a real system it is a UI prompt, a
Slack message, or a ticket. See the denied run in
[`tool_loop_output.txt`](../examples/tool_loop_output.txt): the model receives
`denied by human reviewer` as a tool result and answers accordingly.
