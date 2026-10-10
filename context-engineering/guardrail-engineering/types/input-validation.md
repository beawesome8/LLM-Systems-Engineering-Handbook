# Input Validation

**Definition:** Checks applied to a request (and to any untrusted text that will enter the
context) *before* the model sees it: size limits, format checks, allow-lists, PII handling,
and prompt-injection screening.

**When to use it:** Always, at every trust boundary. User text, uploaded files, web pages,
emails, and tool results are all untrusted input.

**When not to skip it:** Never. Scale the effort to the risk instead.

## What to check

| Check | Example | Method |
|---|---|---|
| Size / rate | Reject a 2 MB "question" | Plain code |
| Format | Order id must match `^[A-Z]\d{4}$` | Regex / schema |
| Topic scope | Is this a support question at all? | Small classifier or allow-list |
| PII | Redact card numbers before logging or sending | Pattern + library |
| Injection phrasing | "Ignore previous instructions..." | Patterns, classifier |
| Indirect injection | Instructions hidden in a retrieved web page or email | Delimit as data; restrict tool permissions |

## Example

```python
INJECTION = re.compile(r"ignore (all |any )?(previous|prior) instructions|reveal.*system prompt", re.I)
def input_guard(text): return not INJECTION.search(text)
```

Full runnable version: [`../examples/output_validation_gate.py`](../examples/output_validation_gate.py)
(`input_guard`).

## The honest limit

Pattern screens catch lazy attacks only. A paraphrase, another language, or encoded text will
walk past a regex. Treat injection screening as a *speed bump*, and put the real protection
elsewhere: wrap untrusted text in delimiters
([structured context](../../types/structured-context.md)), keep tool permissions minimal, and
require human approval for risky actions
([HITL harness](../../../harness-engineering/types/human-in-the-loop.md)). The strongest
design assumption is: **the model will eventually follow a malicious instruction, so limit
what following it can do.**
