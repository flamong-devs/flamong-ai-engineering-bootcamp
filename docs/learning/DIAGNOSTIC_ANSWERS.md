# Diagnostic answers and facilitator notes

Complete the [diagnostic](DIAGNOSTIC.md) first. Award one point when both the answer and its explanation show the understanding described below; otherwise award zero and identify the missing concept. Equivalent wording and valid command variants are acceptable. Scores select preparation work, not admission or certification.

| Question | Answer and evidence for one point |
| --- | --- |
| 1 | `2`. The expression contributes one for each row whose label is `card`; the transfer row is excluded. |
| 2 | Accessing `items[0]` on an empty list raises `IndexError`. Return `len(items)` to count items, including zero for an empty list. |
| 3 | `9/12 = 0.75 = 75%`. The denominator is all 12 evaluated tickets. |
| 4 | `2*3 + 1*4 = 10`. Multiply corresponding entries, then sum. |
| 5 | No. `git add` stages a snapshot locally. A commit records staged changes in local history; a push sends commits to a remote such as GitHub. |
| 6 | `git status --short`, `git diff`, and `git diff --cached` (or `--staged`). The staged diff shows what the next commit includes, which may differ from the latest working files. |
| 7 | Fit on train, select changes on dev, and evaluate the frozen candidate on test. Once final-test feedback guides tuning, use a fresh independent set for a new final claim. |
| 8 | Accuracy is `90/100 = 90%`; card recall is `0/10 = 0%`. The system misses every card ticket despite high overall accuracy. |
| 9 | No. A policy describes a procedure, not this transaction's outcome. An authorised transaction-status observation is needed, with its source and time; the bootcamp fixtures are dated fictional records, not live financial evidence. |
| 10 | No. The application supplies the trusted caller context and enforces ownership at the tool boundary. The supplied dispatcher rejects extra actor arguments. CLI actor flags simulate sessions; they do not authenticate a real user. |

Group questions 1-2 as Python, 3-4 as maths, 5-6 as Git, 7-8 as evaluation, and 9-10 as AI systems. Each group scores 0-2. Any group below two maps to its preparation row in [Start here](START_HERE.md).

For a follow-up check, change the example rather than repeat the answer: use a new list, different class counts, or a different tool request. Ask learners to explain predictions before execution. Keep notes about concepts needing practice rather than comparing learners by total score.
