# Lesson template for facilitators

Use this structure when expanding a row of [LABS.md](../../LABS.md) into a guided lesson. Replace every bracketed field before publishing. Keep commands runnable from the repository root, name expected outputs, and link to the relevant workbook module. A completed example is [Module 8: retrieval](MODULE_08_RETRIEVAL.md).

## Module [number]: [concrete learner outcome]

- **Prerequisites:** [Earlier modules and specific skills the learner needs.]
- **Time:** [Guided practice estimate; state that independent extension takes additional time.]
- **Equipment:** [Python-only baseline; list optional services or hardware separately.]
- **Workbook:** [Module and lesson references in the workbook.]
- **Deliverable:** [One report, implementation, or other reviewable artifact.]

### The problem

[Describe a concrete user task and one failure that matters. State what successful behaviour would look like.]

### What you will be able to explain

[List two or three observable outcomes: calculate, implement, compare, diagnose, or justify. Include one misconception the lesson should resolve.]

### Understand the smallest version

[Explain the mechanism with a short example, formula, or diagram. State assumptions and ask learners to predict an output before running code.]

### Run and record the baseline

[Give exact commands and working directory. Include expected counts, fields, or error behaviour. Record code commit, dataset version, settings, and relevant environment details. Use development data for experiments.]

### Build one change

[Give bounded steps with a stopping point. Name the interface and invariants to preserve. Separate required work from optional extensions. Introduce a framework comparison only after learners can explain the underlying operation.]

### Evaluate the change

[Run baseline and candidate with the same cases and settings except the intended change. Name metrics, denominators, expected failures, and a regression check. An unchanged or worse result is valid evidence; do not require a manufactured gain.]

### Submit evidence

- [ ] Problem, hypothesis, and predicted result.
- [ ] Baseline and candidate commits, commands, versions, and settings.
- [ ] Measured comparison with denominators and inspected failures.
- [ ] Small code or configuration diff and a reason for the change.
- [ ] Limitations, assistance or external sources used, and the next experiment.

### Check understanding

[Ask one mechanism question, one boundary question, and one transfer question that uses a new example. Put facilitator answers in a separate file when appropriate.]

### Extend the work

[Offer a reinforcement task, an application task, and an optional stretch task. State any added dependencies or compute needs.]

## Design reference

The lesson-structure discussion was informed by [AI Engineering from Scratch](https://aiengineeringfromscratch.com/) and its [lesson template](https://github.com/rohitg00/ai-engineering-from-scratch/blob/main/LESSON_TEMPLATE.md). This guide is written for Flamong's existing workbook and runnable baseline; it does not imply affiliation with that project.
