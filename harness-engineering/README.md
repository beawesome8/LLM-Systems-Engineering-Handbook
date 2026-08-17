# Harness Engineering

**Status: stub — not yet built.**

A harness is the scaffolding around a raw model call: the tool-calling loop, retry and
error-handling logic, evaluation harnesses that score model output against a rubric, and
human-in-the-loop checkpoints. Distinct from agent engineering (which is about *what* the
system decides to do) — a harness is about the *reliability infrastructure* the decision-
making runs inside.

## Planned content

- Types: agentic tool-loop harness, eval harness, human-in-the-loop harness, retry/backoff
  harness
- Ties to: Anthropic Claude Agent SDK certification (Claude Code in Action — Skilljar)
- Worked example: a minimal eval harness scoring N model outputs against a rubric, with
  pass-rate logged — not yet built.
