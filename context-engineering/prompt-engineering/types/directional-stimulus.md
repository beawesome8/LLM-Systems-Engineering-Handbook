# Directional Stimulus Prompting

**Definition:** Add a hint, keyword list, or focus instruction that steers the model toward
the aspects that matter before it does the main task, so the output stays on target instead
of drifting to generic coverage.

**When to use it:** You know in advance what a good output must include: "summarize this
report, focusing on cost and timeline", or a list of keywords the summary should contain.

**When not to:** Exploratory tasks where you *want* broad coverage. The stimulus narrows the
output, which is the opposite of what you need there. Also avoid hints that are wrong: the
model will follow a bad steer faithfully.

## Example prompt

```text
Summarize the incident report below in 3 sentences.
Focus on: root cause, customer impact, and the fix. Hint keywords: "database failover",
"14 minutes", "retry storm".

Report:
{report_text}
```

## Variations

- **Static hint**: fixed focus list, as above.
- **Learned hint**: a small model generates the hint per input and feeds it to the large
  model. This is the original research setup; the prompt-only version above captures the
  idea cheaply.

**Origin:** Li et al., 2023 ("Guiding Large Language Models via Directional Stimulus
Prompting").
