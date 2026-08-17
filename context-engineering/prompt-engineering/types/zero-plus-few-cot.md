# Zero-Plus-Few-Shot Chain of Thought

**Definition:** A hybrid: give no examples, or just one, but explicitly instruct the model to
reason step-by-step. Different from plain zero-shot (no reasoning elicited) and from full
few-shot CoT (multiple worked examples with reasoning shown).

**When to use it:** You want the reasoning-quality benefit of CoT but can't afford the token
cost of multiple full worked examples — one example plus an explicit instruction is often
enough to anchor the pattern.

**When not to:** The task genuinely needs multiple examples to disambiguate an unusual output
format — one example won't be enough signal.

**Worked example:** Not yet built.
