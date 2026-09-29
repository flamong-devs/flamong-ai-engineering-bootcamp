# Beginner diagnostic

Allow 20-30 minutes. Answer from your current understanding before running the snippets or opening the [answer guide](DIAGNOSTIC_ANSWERS.md). Write a short reason for each answer. Record uncertainty honestly; the result chooses useful preparation work.

There are ten questions worth one point each, grouped into five areas. Setup readiness is checked separately in [Start here](START_HERE.md).

## Python: questions 1-2

**1. Predict the output and explain the filter.**

```python
rows = [{"label": "card"}, {"label": "transfer"}, {"label": "card"}]
print(sum(1 for row in rows if row["label"] == "card"))
```

**2. Repair the function.** It should return zero for an empty list and the number of items otherwise. What causes its current error, and what would you return instead?

```python
def count_items(items):
    return len(items[0])

print(count_items([]))
```

## Maths: questions 3-4

**3. Calculate a rate.** A classifier gets 9 of 12 tickets correct. What is its accuracy as a fraction and percentage? What does the denominator count?

**4. Calculate a dot product.** What is the dot product of `[2, 1]` and `[3, 4]`? Show the multiplication and addition.

## Git: questions 5-6

**5. Explain the next step.** You edit `LABS.md`, then run `git add LABS.md`. Has this published your change to GitHub? What do a commit and a push do next?

**6. Inspect before committing.** Name the Git commands you would use to see changed filenames, unstaged differences, and staged differences. Why check the staged differences?

## Evaluation: questions 7-8

**7. Assign each data split a job.** Which split should fit the classifier, which should guide feature or prompt choices, and when should the final test split be used?

**8. Diagnose a weak metric.** Out of 100 tickets, 90 are transfer tickets and 10 are card tickets. A system always predicts transfer. State its accuracy and card recall, then explain what accuracy hides.

## AI systems: questions 9-10

**9. Distinguish evidence from a conclusion.** A retrieved passage explains how pending transfers should be checked. Does it prove that a particular customer's transfer succeeded? What evidence would be needed, and does the bootcamp fixture provide live financial information?

**10. Locate the permission boundary.** A model requests a transaction tool with `actor="learner_b"`, while the application's caller is `learner_a`. Should the model's actor value change access? Where should caller identity and access enforcement come from?

## Choose your next step

Open the [answer guide](DIAGNOSTIC_ANSWERS.md) after your first attempt. Record each area out of two, complete the preparation tasks for areas below 2/2, then return to [Start here](START_HERE.md). Do not skip the bootcamp modules based only on this short quiz.
