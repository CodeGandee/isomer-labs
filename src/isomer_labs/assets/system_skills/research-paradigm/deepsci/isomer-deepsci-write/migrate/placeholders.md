# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:PAPER-CONTROL-STATE | memory cards, source quest state, active paper surfaces, paper contract health | The refreshed writing context before prose begins. | isomer-rsch-write | write, paper-outline, review, finalize | runtime state |
| DEEPSCI:PAPER-CONTRACT | outline, evidence ledger, experiment matrix, references, venue/report target | The agreed manuscript claim, audience, evidence boundary, displays, citation status, and bundle status. | isomer-rsch-write | write, review, finalize, nature companion skills | handoff |
| DEEPSCI:PAPER-OUTLINE | selected paper outline and paper_view/evidence_view | The reader-facing outline and evidence mapping used to control section jobs. | isomer-rsch-paper-outline or write | write, review | handoff |
| DEEPSCI:WRITING-PLAN | compiled section jobs | Section-level writing jobs with inputs, claim limits, display needs, and stop criteria. | isomer-rsch-write | write | research task |
| DEEPSCI:SOURCE-MATERIAL-LEDGER | claims, settings, reproducibility details, implementation details, artifact history | The separated source material that prevents run logs and route controls from entering manuscript prose. | isomer-rsch-write | write, review, rebuttal | evidence |
| DEEPSCI:CITATION-LEDGER | references, bibliography, real-source citation checks | Verified citation and bibliography state used by the draft. | isomer-rsch-write | write, review, finalize | evidence |
| DEEPSCI:DISPLAY-PLAN | planned figures and tables | The table and figure plan that routes first-pass plots and durable figures. | isomer-rsch-write | paper-plot, figure-polish, review | handoff |
| DEEPSCI:DRAFT-SECTION-SET | updated manuscript sections or report text | The authored or revised manuscript sections constrained by the paper contract. | isomer-rsch-write | review, finalize, rebuttal | draft |
| DEEPSCI:MANUSCRIPT-VALIDATION-REPORT | validation over coverage, claims, figures, citations, language, bundle readiness | The draft-state check that determines whether to checkpoint or route back. | isomer-rsch-write | review, finalize, decision | report |
| DEEPSCI:PAPER-BUNDLE-CHECKPOINT | artifact.submit_paper_bundle(...) | A coherent draft, review, or submission package checkpoint before downstream routing. | isomer-rsch-write | review, finalize, user | handoff |
| DEEPSCI:WRITING-ROUTE-DECISION | analysis-campaign, review, finalize, paper-outline, nature companion route | The next route when writing exposes evidence, outline, review, figure, or submission-readiness issues. | isomer-rsch-write | any selected production DeepSci skill | decision |
