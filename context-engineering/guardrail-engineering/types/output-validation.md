# Output Validation

**Definition:** Checks on what the model returned *before* your code uses it or a user sees
it: parseable, matches the schema, values in allowed ranges, no forbidden content.

**When to use it:** Whenever output feeds code (JSON parsing, tool arguments, SQL, API calls)
or reaches a user in a regulated or high-stakes setting.

**When not to:** Free-form chat where any text is acceptable, and even there a basic content
filter often applies.

## Validation ladder (cheapest first)

1. **Parses?** Valid JSON / XML / SQL syntax.
2. **Matches schema?** Required keys, types, enum values. (Pydantic, JSON Schema.)
3. **Semantically sane?** Dates in range, totals add up, ids exist in your database.
4. **Safe?** No secrets, no disallowed content, no unapproved links.
5. **Grounded?** Supported by the source ([hallucination grounding](./hallucination-grounding.md)).

## Example

```python
data = json.loads(raw)                                  # 1. parses
assert set(data) == {"intent", "days", "evidence"}      # 2. schema
assert data["intent"] in ALLOWED_INTENT                 #    enum
assert data["evidence"] in source                       # 5. grounded: verbatim quote
```

Runnable, with a scored test set: [`../examples/output_validation_gate.py`](../examples/output_validation_gate.py).

## What to do when validation fails

- **Retry with the error fed back** ("Your JSON was missing key `days`. Return it again.").
  Usually fixes format errors in one extra call. Cap at 1-2 retries
  ([retry harness](../../../harness-engineering/types/retry-and-backoff.md)).
- **Fall back** to a safe default or a simpler path.
- **Escalate** to a human.
- **Refuse** and say why.

Never silently pass invalid output through.

## Prefer enforcement to hope

If your provider supports structured outputs / tool schemas, use them to constrain the
response, then validate anyway: schemas guarantee shape, not truth.
