# Chunking Strategy

**Definition:** Splitting documents into the units you embed and retrieve. A chunk is both
what gets matched against the query and what gets pasted into the model's context.

**Why it matters:** Too small and a chunk lacks the context to be understood or to hold the
whole answer. Too large and the embedding blurs several topics together, wasting context
tokens on noise. A fact cut in half by a boundary may be unretrievable.

## Strategies

| Strategy | How | Good for | Watch out for |
|---|---|---|---|
| Fixed size | Every N characters/tokens | Quick baseline | Cuts mid-sentence and mid-fact |
| Fixed size + overlap | Windows share some text | Reduces boundary loss | Duplicates, larger index |
| Sentence / paragraph | Split on natural boundaries | Prose | Uneven chunk sizes |
| Structure-aware | Split on headings, sections, code blocks, table rows | Docs, manuals, code | Needs a parser per format |
| Semantic | Split where topic shifts (embedding similarity drops) | Long unstructured text | Extra cost, tuning |
| Parent-child | Retrieve small chunks, return their larger parent | Precision *and* context | More plumbing |

## Practical advice

- **Start with structure-aware or paragraph chunks**; measure before getting fancier.
- **Typical sizes**: a few hundred tokens; tune against your eval.
- **Prepend context to each chunk** (document title, section heading). A chunk reading "it
  expires after 30 days" is useless without knowing what *it* is.
- **Keep metadata**: source, section, page, date, permissions.
- **Treat tables and code as special cases**; naive splitting wrecks them.

## Run it

[`../examples/chunking_recall.py`](../examples/chunking_recall.py) holds the retriever and
questions constant and varies only chunking
([logged output](../examples/chunking_recall_output.txt)):

| Strategy | chunks | recall@1 | recall@3 |
|---|---|---|---|
| Fixed 100 chars, no overlap | 15 | 0.17 | 0.33 |
| Fixed 100 chars, 30 overlap | 21 | 0.50 | 0.67 |
| Paragraph | 12 | 0.83 | 0.83 |

Overlap helped by letting facts that straddled a boundary appear whole in some chunk.
Paragraph chunking won because this toy corpus is written in paragraphs, so a paragraph *is*
the natural unit. **Caveat:** six questions on a four-document corpus is a demonstration of
the method, not a benchmark; the ranking of strategies on your data may differ. That is the
reason to run the experiment on your own documents.
