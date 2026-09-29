# Build route
Read the corresponding workbook module, run the baseline, then make and explain your own change. A passing test is evidence about that test, not proof of complete safety or correctness.

Before Module 1, complete [Your first bootcamp session](docs/learning/START_HERE.md) and the diagnostic preparation it recommends. Save evidence after every module in your learning plan. Use the [lesson template](docs/learning/LESSON_TEMPLATE.md) for a consistent hypothesis, baseline, experiment, and submission record.

| Module | Starting point | Learner contribution |
|---|---|---|
| 1 | `audit()` and JSONL | Dataset contract and annotation guide |
| 2 | `math_demo()` | Dot product, mean and probability calculations |
| 3 | `NaiveBayes` | Error analysis and one dev-tested improvement |
| 4 | Scalar update | Ten-step optimization loop and bias gradient |
| 5 | `Retriever.vector()` | Cosine similarity and representation comparison |
| 6 | `bigram_demo()` | Count model inspection and reviewed SFT examples |
| 7 | `validate_answer()` | Prompt comparison and validation cases |
| 8 | `Retriever.search()` | [Guided retrieval comparison and paragraph chunking](docs/learning/MODULE_08_RETRIEVAL.md); optional dense retrieval |
| 9 | `llm.ask()` | Real-model RAG run if available, claim-level review |
| 10 | `execute_tool()` and `llm.agent()` | Trace analysis, malformed-argument and injection cases |
| 11 | Tests and reports | Release gates, timing, cost and rollback plan using the [capstone evidence requirements](docs/learning/CAPSTONE_RUBRIC.md) |
| 12 | Frozen system | Independent final evaluation and defence assessed with the [capstone rubric](docs/learning/CAPSTONE_RUBRIC.md) |

## Evidence to retain

For each module, save the command and starting commit, your prediction, the observed result, your explanation, and one limitation. Include denominators when reporting rates. Mark optional or untested capabilities explicitly. Keep development experiments separate from the frozen final evaluation.

Module 8 is currently the completed guided lesson example. The other modules use the workbook and the build tasks above; facilitators can expand them with the template.

## Stretch sequence
1. Add paragraph chunking while preserving document/version/permission metadata.
2. Add a sentence-embedding retriever behind the same interface; compare on frozen questions.
3. Add a reranker and measure the latency/quality tradeoff.
4. Define JSON Schema/Pydantic output validation in a dependency-pinned branch.
5. Add an authenticated web API with real server-side user isolation; keep all external actions read-only.
6. Train a small neural classifier or a parameter-efficient adapter with approved data; compare fairly.
7. Introduce a framework only after explaining the plain-Python control flow it replaces.

Each stretch experiment needs a hypothesis, unchanged baseline, dev comparison, failure inspection, and a final held-out check. Framework setup and GPU training are not required to run the shipped core.
