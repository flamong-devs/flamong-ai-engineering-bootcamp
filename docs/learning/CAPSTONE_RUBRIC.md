# Capstone assessment rubric

Use this rubric for Modules 11-12. Agree the project scope, metrics, and pass conditions with a reviewer before the final evaluation. This assesses a bootcamp project; a pass does not establish production readiness or award an external certification.

## Choose a route

| Route | Demonstration and claim boundaries |
| --- | --- |
| Offline | Improve one part of the fictional support workflow, such as routing or retrieval. Demonstrate evidence preview, boundary tests, and a scripted tool trace. Label the trace as scripted and generation as untested. |
| Local model | Meet the offline requirements and demonstrate actual generation or model-directed tool use. Record the installed model, settings, prompt version, raw outputs, tool traces where applicable, and a manual review of claim support. |

Either route can earn 100 points. Judge each submission against its declared capability; a model download or a more elaborate architecture earns no points by itself. A model route with no live-model evidence must be reassessed as an offline submission or completed before making generation claims.

## Required evidence bundle

Submit a branch or commit plus a Markdown report linking to:

1. **Project brief:** intended user, one workflow, expected outcome, non-goals, baseline, and one justified change.
2. **Run manifest:** baseline and frozen candidate commits; Python and dependency versions; data/source versions; commands; machine details; model/prompt settings if used.
3. **Evaluation:** development comparison, independent final cases and labels, outputs, denominators, per-case judgements, and at least three inspected failure or boundary cases.
4. **Boundary evidence:** passing starter tests, relevant new regression tests, and observations for permissions, unsupported requests, stale evidence, and malformed tool input.
5. **Release note:** measured latency, cost assumptions, acceptance thresholds, fallback behaviour, rollback trigger, and a named role responsible for reviewing feedback.
6. **Defence:** a successful case, a failed or limited case, an explanation of the change, sources or AI assistance used, and the next experiment.

Store the report in `reports/capstone.md`. The starter ignores `reports/*.json`; include reviewable tables or redacted text evidence in Markdown, or document how a reviewer can reproduce the ignored machine-readable outputs.

## Final evaluation procedure

Choose metrics that match the change. For routing, report accuracy and per-class recall with counts. For retrieval, report hit/recall at the chosen `k` and unsupported-query behaviour. For generation, additionally assess factual claims against evidence and abstention. Tool-use claims need action, observation, permission, and stopping evidence. A retrieval metric alone does not score answer quality.

Use development cases to select the candidate. Then record its commit and freeze the data, prompt, model, and evaluation settings. A facilitator or peer should hold a fresh final set outside the learner branch until this freeze. For self-study, arrange an independent peer set where possible; otherwise label the result a self-evaluation and leave the independent-assessment requirement pending.

Include at least 12 fresh final cases appropriate to the declared task, with expected outcomes written before execution. Cover ordinary successful use, ambiguous or unsupported requests, and relevant permission or stale-source boundaries. For a classifier, cover every label and report the count for each. Twelve cases are a teaching minimum, not evidence of population-level performance.

Run baseline and candidate on the same final cases under the same procedure. Retain every result. If the candidate is changed after reading final results, record the iteration and obtain a new independent set before another final claim. Public starter test labels are suitable only if they have not already guided development; they do not replace the fresh-case requirement here.

## Scoring: 100 points

Score each row as zero, half, or full credit using the anchors. Record evidence links and a reason for each score. Half credit is exactly half the listed weight, including 2.5 for a five-point row.

| Criterion | Weight | Zero | Half credit | Full credit |
| --- | ---: | --- | --- | --- |
| Problem and scope | 10 | No clear user task or outcome. | Task named, but success criteria or boundaries are vague. | User, workflow, measurable outcome, baseline, and exclusions are explicit. |
| Implementation and understanding | 15 | No runnable contribution or cannot explain it. | Change runs, but rationale or mechanism is weak. | Bounded change works as described; learner explains the mechanism and a meaningful tradeoff. |
| Evaluation quality | 20 | No comparable evidence or split leakage. | Development comparison exists, but coverage, counts, or analysis are incomplete. | Fair baseline/candidate comparison, versioned independent final cases, relevant metrics with counts, and inspected failures. |
| Permissions and failure behaviour | 15 | Declared access boundary is bypassed or failure behaviour is unexamined. | Starter checks pass; project-specific failure evidence is incomplete. | Relevant boundary and negative cases run; observed behaviour and remaining gaps are explained, including limits of simulated authentication. |
| Reproducibility | 15 | Reviewer cannot run the submission. | Runs with undocumented intervention or missing settings. | Reviewer reproduces the declared result from the frozen commit using the manifest. |
| Release and operation | 10 | No operational evidence or recovery plan. | Some timing, cost, or fallback work, with gaps. | Measured timing, labelled cost assumptions, observable gates, fallback, rollback trigger, and feedback owner. |
| Defence and limitations | 10 | Claims exceed evidence or learner cannot explain the work. | Explains the demo but gives weak failure analysis or next steps. | Explains success and limitation cases, attributes changes carefully, discloses assistance, and proposes a testable next step. |
| Documentation and attribution | 5 | Missing usable instructions or attribution. | Instructions or credits exist but are incomplete. | Clear run instructions, linked evidence, readable diff, and appropriate source/licence attribution. |

A well-designed experiment that fails to improve the baseline can earn full credit. Assess the quality of the implementation, comparison, and resulting decision.

## Completion gates and decision

Before awarding a pass, all of these must hold:

- The project runs from the submitted commit. All 19 starter tests still pass without weakening or removing checks; relevant additional tests also pass.
- No credentials, actual customer records, or private company documents are included in the submission.
- Evaluated cases do not bypass the declared caller/role restrictions or allowed-tool boundary. Any detected bypass is repaired and retested before completion.
- Final results come from the frozen candidate and an independently held fresh set; no undisclosed tuning on final cases occurred.
- Claims match the evidence: fixtures remain fictional, scripted loops are labelled, and generated-answer claims have live-model and source-support evidence.

**Pass:** at least 70/100, every gate met, and at least half credit in both evaluation quality and permissions/failure behaviour. **Distinction:** at least 85/100 with the same gates and minimums. **Revise:** below the pass criteria. An unmet gate remains pending even when the numeric score is high.

Use this reviewer record:

```markdown
- Route and scope:
- Baseline commit / frozen candidate commit:
- Final set owner, version, freeze date, and evaluation date:
- Scores by criterion and evidence links:
- Total /100:
- Completion gates: met / pending, with evidence
- Decision: pass / distinction / revise
- Required revisions:
- Reviewer role and review date:
```

## Defence prompts

Explain what changed from the baseline and why. Reproduce one result. Show one case where the system fails or cannot make a supported claim. Identify which component enforces permissions. Explain what you would measure next and who would review it before expanding the system's use.
