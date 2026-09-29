# Module 8: retrieve evidence and explain the result

- **Prerequisites:** Modules 1-7, especially split discipline, vector similarity, and output validation.
- **Time:** 60-90 minutes for the guided comparison; allow a separate session for chunking.
- **Equipment:** Python 3.10+ and the repository. No model or network required.
- **Workbook:** Module 8, lessons 8.1-8.2 and its build lab in the [workbook](../AI_Engineering_Bootcamp_Flamong.pdf).
- **Deliverable:** `reports/module-08.md`, with a baseline comparison, plus a paragraph-chunking implementation and its evaluation.

## The problem

A support learner asks about a pending transfer. Search must return relevant current policies that their role may read. A returned passage still needs interpretation: a procedure for checking transactions does not establish the state of any particular transaction.

By the end, explain how token overlap and cosine similarity rank passages, what changing `k` can change, and why a retrieval score does not measure generated-answer quality.

## Understand the smallest version

Read `tokens()`, `Retriever.vector()`, and `Retriever.search()` in [core.py](../../bootcamp/core.py). Document vectors and query vectors are normalised; the dot product of those vectors gives cosine similarity. Search excludes archived documents and documents unavailable to the requested role before adding results.

Predict whether asking for three results guarantees three passages. Inspect the score threshold and the slice applied after ranking, then test your prediction.

## Run the baseline

Run these commands from the repository root and copy their output into your report:

```sh
git rev-parse HEAD
python -m bootcamp search "pending transfer" --k 3
python -m bootcamp evaluate --split dev --k 1
python -m bootcamp evaluate --split dev --k 3
python -m unittest discover -s tests -v
```

For the shipped starter, the search returns `P01` followed by `P02`, even with `k=3`. The dev evaluation has six answerable and two unanswerable cases:

| Setting | Answerable hit rate | Mean recall | Unanswerable cases with hits |
| --- | --- | --- | --- |
| `k=1` | 6/6 (1.0) | 1.0 | 0/2 |
| `k=3` | 6/6 (1.0) | 1.0 | 0/2 |

These are starter results, not targets to hard-code. Both settings already saturate these small answerable cases, so this comparison cannot show an improvement in their hit rate. Additional passages can still alter relevance, latency, and the context supplied to a model.

## Build and compare one experiment

1. State a hypothesis about `k=1` versus `k=3` before inspecting outputs.
2. Run both settings and compare the same cases. Read the retrieved passages as well as the summary metrics.
3. Add three clearly labelled development probes to your report: a paraphrase, an unsupported request, and a request made under a role that cannot read the relevant restricted source. Define expected behaviour before running them.
4. For each probe, record the role, expected source or abstention, returned IDs, and your relevance judgement. Record failures honestly; if a case behaves correctly, explain what it demonstrates and what remains untested.
5. Make a retain-or-change decision about `k` for this exercise. Do not tune on the `test` split.

The CLI supports `--role customer`, `--role support`, and `--role risk` for these simulations. The role flags are not a real authentication system.

## Next build: paragraph chunking

The starter currently treats each short document as one chunk. For a follow-on implementation:

1. Add a longer, fictional development document with distinct paragraphs; name its version and role permissions.
2. Assign deterministic chunk IDs, retain the parent document ID, and preserve `status`, `roles`, `version`, and `source` on every chunk. Document how an edit or reordering affects IDs.
3. Preserve the `Retriever.search()` call signature and downstream result fields. Document any added parent-ID field.
4. Define citation and evaluation mapping explicitly. Existing gold IDs refer to parent documents; do not compare those directly with new chunk IDs. Deduplicate parent IDs when calculating document-level recall, and record chunk relevance separately.
5. Check role filtering, archive exclusion, empty queries, citation validation, and a query whose answer spans paragraphs. Measure behaviour with the same development cases before and after the change.

Keep this extension separate from the initial `k` comparison so you can attribute a difference to the change that caused it.

## Submit and explain

Your report should include the hypothesis, baseline and candidate commits, settings, comparison table, three probes, inspected limitations, and the chunking evaluation mapping. Link the chunking implementation and its regression evidence. Use the checklist in the [lesson template](LESSON_TEMPLATE.md) to review the submission. If you have only completed the guided comparison, mark the chunking build as pending.

Before moving on, explain:

- Why can `k=3` return two passages?
- Why would valid citation IDs alone fail to prove an answer is supported?
- How could splitting one document into five chunks distort an evaluation that counts documents?

Take this evidence into Module 9. Learners using the offline route can review source support manually and label generation as untested.
