# Chain of Density

**Definition:** Write a sparse first summary, then rewrite it several times. Each pass adds
1-3 missing important entities or facts from the source while keeping the length fixed.
The summary gets denser, not longer.

**When to use it:** Summaries where the first draft is vague ("The report discusses
financial performance") and you want concrete names, numbers, and causal links in the same
word budget.

**When not to:** When brevity or readability is the goal. Very dense summaries become hard
to read. In the original paper (5 rounds, news articles), the first-place votes clustered around
the middle rounds (modal round 2, median round 3), not the densest. Caveat: only four raters,
all of them the authors, with low agreement between them.

## Example prompt

```text
Article: {article}

You will write 3 summaries of the article, each about 70 words.
Summary 1: sparse, mostly general statements.
Summary 2: identify 2 important entities or facts missing from Summary 1, then rewrite it
           to include them WITHOUT making it longer (compress wording to make room).
Summary 3: repeat once more.

Output JSON: a list of objects with keys "missing_entities" and "summary".
```

## Measure it

Density is measurable: count distinct named entities or numbers per word in each summary. If
pass 3 does not beat pass 2 on that count, stop at pass 2 and save the tokens.

**Origin:** Adams et al., 2023 ("From Sparse to Dense: GPT-4 Summarization with Chain of
Density Prompting").
