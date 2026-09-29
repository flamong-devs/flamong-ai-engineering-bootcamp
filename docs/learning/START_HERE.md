# Your first bootcamp session

Start here after cloning the repository. You will check your setup, choose preparation work, and record a learning plan before Module 1. Allow 45-60 minutes for setup and the diagnostic; preparation time depends on your starting point.

## 1. Get a working baseline

You need Git, Python 3.10 or later, a text editor, and a terminal. After downloading the repository, the core exercises run offline with Python's standard library. A GPU, model download, and paid API are optional.

Open a terminal in `flamong-ai-engineering-bootcamp`, the directory containing `README.md`, `bootcamp/`, and `tests/`:

```sh
python --version
git status --short
python -m bootcamp audit
python -m unittest discover -s tests -v
```

If your Python command is `python3` or `py -3`, substitute that throughout the guides. The starter audit reports 36 training, 12 development, and 12 test tickets. The starter test suite reports `Ran 19 tests` and `OK`. Learners who add tests will see a higher count.

| Symptom | Next action |
| --- | --- |
| Python command is missing or older than 3.10 | Install a supported Python version for your operating system; reopen the terminal and check again. |
| `No module named bootcamp` | Change into the repository root and rerun the command. |
| `Ran 0 tests` | Confirm that `tests/test_core.py` exists and run the exact discovery command above from the root. |
| Audit or tests fail | Save the error, check `git diff`, and ask a facilitator to help reproduce it before continuing. |
| An Ollama command fails | Start with the offline commands above; follow the optional model setup in the [README](../../README.md) when needed. |

Record the Python version, operating system, `git rev-parse HEAD`, and the audit/test outcome. Do not paste environment variables or credentials into your report.

## 2. Find your preparation work

Complete the [beginner diagnostic](DIAGNOSTIC.md) before opening its answers. It is a placement aid, not a certificate or an entrance exam. Score each of its five areas separately.

For any area scoring below 2/2, complete the matching preparation task below. A high total does not replace a missing prerequisite. If every area scores 2/2 and your setup works, start Module 1 directly.

| Area | Preparation task | Evidence you are ready |
| --- | --- | --- |
| Python | Practice lists, dictionaries, loops, and functions. Write a function that counts labels in a list of three fictional ticket dictionaries. Try an empty list too. | You can explain each line and predict both outputs before running it. |
| Maths | Calculate a proportion, mean, and dot product on paper; verify with Python. Use 3/8, the mean of 2, 4, 6, and the dot product of `[1, 2]` and `[3, 4]`. | You obtain 0.375, 4, and 11 and can explain how. Review workbook Module 2 for the next step. |
| Git | On a practice branch, make a small Markdown edit, inspect it with `git diff`, stage that file, commit, and inspect `git status`. | You can distinguish an edit, a staged change, a local commit, and a pushed commit. No push is needed for this preparation task. |
| Evaluation | Read workbook Module 3. Write down which data fits the system, which selects a change, and which evaluates the frozen candidate. | You can explain why reusing final-test feedback for tuning requires a new independent evaluation set. |
| AI systems | Run `python -m bootcamp search "pending transfer" --k 3` and the default `ask` command in the README. Read the source passages. | You can distinguish retrieved policy text, a generated answer, and a transaction observation. |

After preparation, explain a different example to a peer or facilitator. Use that explanation to check understanding; repeating a memorised diagnostic answer is not new evidence.

## 3. Keep a learning plan

Create a local `reports/learning-plan.md`. Include only information you intend to share if you later commit it:

```markdown
# My learning plan
- Goal: what I want to build or understand
- Time available each week:
- Setup: Python version, operating system, starting commit, audit/test result
- Diagnostic: Python __/2; maths __/2; Git __/2; evaluation __/2; AI systems __/2
- Preparation tasks and readiness evidence:
- Next module: 1
- Capstone route: offline / local model / decide after Module 8

| Module | Date | Evidence file or commit | What I can explain | What needs review |
| --- | --- | --- | --- | --- |
```

Follow the [12-module build route](../../LABS.md), using the workbook for explanations. Read the [capstone rubric](CAPSTONE_RUBRIC.md) early so you know what evidence to retain. The offline route can earn the full score; local-model work adds requirements for any generation claims you make.
