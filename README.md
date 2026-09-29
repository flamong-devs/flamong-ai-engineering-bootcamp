# AI Engineering Bootcamp
Prepared by **Flamong.com**.

This is a readable teaching baseline for the accompanying workbook. It grows from a synthetic support-ticket classifier to retrieval, optional local-model RAG, and a bounded tool loop. All people, policies, transactions and company scenarios are fictional. This is not production financial software.

## Start here
Python 3.10 or later. Core commands require no third-party Python packages and no network.
Clone the public repository and open a terminal in its root:

```sh
git clone https://github.com/flamong-devs/flamong-ai-engineering-bootcamp.git
cd flamong-ai-engineering-bootcamp
```

Read the [AI Engineering Bootcamp workbook](docs/AI_Engineering_Bootcamp_Flamong.pdf), then run:

```sh
python -m bootcamp audit
python -m unittest discover -s tests -v
python -m bootcamp classify --split dev
python -m bootcamp math
python -m bootcamp bigram
python -m bootcamp search "pending transfer" --k 3
python -m bootcamp ask "How should a failed transfer be handled?"
python -m bootcamp evaluate --split dev --k 3
python -m bootcamp transaction TX100 --actor learner_a
```

Use `python3` or `py -3` if that is how your machine names Python. Run commands from the project root; otherwise the `bootcamp` package will not be found. The core requires a computer with Python; a phone/PDF viewer alone cannot execute it.

The default `ask` mode is **extractive evidence preview, not LLM generation**. It returns permitted current source passages so you can inspect retrieval without downloading a model.

## Optional real generation with Ollama
Install Ollama separately using its official instructions: https://docs.ollama.com/quickstart . Select and install a model that fits your machine and usage rights. This kit does not download a model or start the service. Model downloads and inference can require substantial storage/RAM. The core baseline remains available without them.

Check installed models with `ollama list`, ensure the service is running, and set the exact model name:

```sh
# macOS/Linux: replace the value with an installed model name
export OLLAMA_MODEL="your-installed-model"
python -m bootcamp ask "How should a failed transfer be handled?" --mode ollama
python -m bootcamp agent "What should I do about TX100?" --mode ollama
```

PowerShell equivalent: `$env:OLLAMA_MODEL = "your-installed-model"`.
The adapter talks only to `http://127.0.0.1:11434/api/chat`, sends `stream=false`, requests JSON and uses a 120-second timeout. It does not transmit to a hosted provider. Connection errors mean the service/model needs setup; invalid JSON or citations are surfaced as failures. API source: https://docs.ollama.com/api/chat .

**Verification limit:** the core was executed with Python 3.12 and 19 tests passed. The Ollama HTTP contract was checked with a mocked response; no live model was installed or evaluated during kit preparation. Generated answer quality, live-model compatibility and model-driven agent performance must be tested by your group. Never count the scripted planner test as an intelligent agent result.

## What is included
- `bootcamp/core.py`: data audit, multinomial Naive Bayes, TF-IDF retrieval, metrics, scalar-gradient demonstration, bigram sampling, fixture tools and output validation.
- `bootcamp/llm.py`: optional local-model generation and bounded loop with two allowed read-only tools.
- `bootcamp/__main__.py`: command-line interface.
- `data/tickets.jsonl`: 60 original synthetic tickets (36 train, 12 dev, 12 test).
- `data/knowledge.json`: eight short documents: six public/support current policies, one restricted current risk policy, one archived policy.
- `data/questions.json`: 16 hand-authored retrieval questions, eight dev and eight test. Gold IDs are local because this is a study kit; a facilitator should hold a fresh set separately for assessment.
- `data/transactions.json`: two dated synthetic transaction fixtures.
- `tests/test_core.py`: regression and boundary tests.
- `LABS.md`: the incremental build route.
- `REPOSITORY_PLAN.md`: suggested GitHub setup and collaboration workflow.

## Expected initial results
The supplied classifier gets 9/12 correct on dev: 75%, compared with the balanced majority baseline of 33.3%. Its card recall is 0.50. It misses an ATM PIN example, a supermarket-terminal example and a remittance paraphrase. The six answerable dev retrieval questions all have a relevant passage in the top three in the supplied baseline. These are tiny synthetic demonstrations, not evidence of real-world performance. No claims are made about the final test score before learners freeze their candidate.

## Boundaries worth studying
- Retrieval filters archived and role-restricted documents before returning passages.
- Actor and role are passed from the application context to tools, not from model arguments. CLI actor/role switches are **simulation fixtures, not authentication**.
- Tool dispatch rejects unknown names and extra arguments; ownership is checked for transaction reads.
- The loop stops on repeated identical actions or budget exhaustion. There are no write tools.
- Citation validation proves only that IDs came from retrieved documents; it does not prove semantic support.
- The agent's final answer is deliberately flagged for human review. Learners add a semantic evaluation before any serious use.
- The starter is lexical retrieval, not a dense-vector database. Each small document is one chunk. Chunking, embeddings, reranking and a production API are build exercises.

## Reproducible experiments
Create `reports/` if your unzip tool omits an empty directory. Save command output, model/settings, prompt version, corpus version and a code commit ID. Keep dev and test roles distinct. Do not add evaluation questions to training to improve a score. Use `--split test` only after freezing the candidate, and obtain a fresh set if you already tuned against it.

## Sharing and credits
These exercises and fictional data were prepared for Flamong's bootcamp. They are independent teaching material, not Stanford assignment solutions or an official Stanford course. Course and documentation references are in the PDF. This repository is public. No software licence has been selected; the repository owner will decide the licence separately.
