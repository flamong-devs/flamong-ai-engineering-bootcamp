# Shared public repository
Repository: [`flamong-devs/flamong-ai-engineering-bootcamp`](https://github.com/flamong-devs/flamong-ai-engineering-bootcamp).
Visibility: **public**. Every other repository's visibility remains unchanged.

The starter kit is extracted directly into the repository root. The workbook is included at [`docs/AI_Engineering_Bootcamp_Flamong.pdf`](docs/AI_Engineering_Bootcamp_Flamong.pdf). The repository owner approved MIT for code and software configuration, and CC BY 4.0 for the workbook, teaching materials, prose documentation, and synthetic datasets. See [Licensing and attribution](LICENSING.md).

Recommended collaboration setup: protect the main branch and use pull requests with one reviewer. Branch protection is a recommendation, not a claim that it has been configured.

## Learning materials

- Begin with the [setup and preparation guide](docs/learning/START_HERE.md) and [diagnostic](docs/learning/DIAGNOSTIC.md); consult the separate answer guide after the first attempt.
- Expand module sessions using the [lesson template](docs/learning/LESSON_TEMPLATE.md). The [guided retrieval lesson](docs/learning/MODULE_08_RETRIEVAL.md) demonstrates the expected format.
- Review final projects with the [capstone rubric](docs/learning/CAPSTONE_RUBRIC.md), including independently held cases, reproducibility, and explicit claim boundaries.
- Workbook edition 1.1 integrates these guides while preserving the original lesson page numbers and fillable fields. Its builder reads diagnostic and rubric text from a pinned Markdown revision; full regeneration of every lesson from shared source remains future work. See [edition and publishing notes](docs/WORKBOOK_EDITIONS.md).

## Collaboration
- Each learner creates a branch such as `learner-name/module-03` and submits a small change plus evidence.
- Pair review rotates roles: implementer, reviewer and evaluator. Each person explains their own work.
- Maintain a facilitator-held assessment set outside learner branches.
- Proposed milestone tags: `m01-data`, `m03-classifier`, `m08-retrieval`, `m09-rag`, `m10-tools`, `m12-capstone`. These are planned, not already-created tags.
- Never commit API keys, actual customer records or private company documents.
- Issue template: problem, hypothesis, baseline, change, evaluation command, result, failure cases, next step.
- PR checklist: tests run, data provenance explained, split boundaries preserved, result reproducible, limitations stated.

## First issues
1. Improve ambiguous card/access routing with an explicitly justified feature change.
2. Add paragraph chunking with stable citation IDs.
3. Evaluate three paraphrases per intent, with approved labels.
4. Add a claim-support evaluation sheet for generated answers.
5. Add a hostile-document fixture and demonstrate that tool permissions hold.
6. Add a timing/cost report and a release decision note.
