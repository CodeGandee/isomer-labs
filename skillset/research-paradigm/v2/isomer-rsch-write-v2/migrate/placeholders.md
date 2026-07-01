# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <PAPER_CONTROL_STATE> | memory cards, source quest state, active paper surfaces, paper contract health | The refreshed writing context before prose begins. | isomer-rsch-write-v2 | write, paper-outline, review, finalize | runtime state |
| <PAPER_CONTRACT> | outline, evidence ledger, experiment matrix, references, venue/report target | The agreed manuscript claim, audience, evidence boundary, displays, citation status, and bundle status. | isomer-rsch-write-v2 | write, review, finalize, nature companion skills | handoff |
| <PAPER_OUTLINE> | selected paper outline and paper_view/evidence_view | The reader-facing outline and evidence mapping used to control section jobs. | isomer-rsch-paper-outline-v2 or write | write, review | handoff |
| <WRITING_PLAN> | compiled section jobs | Section-level writing jobs with inputs, claim limits, display needs, and stop criteria. | isomer-rsch-write-v2 | write | research task |
| <SOURCE_MATERIAL_LEDGER> | claims, settings, reproducibility details, implementation details, artifact history | The separated source material that prevents run logs and route controls from entering manuscript prose. | isomer-rsch-write-v2 | write, review, rebuttal | evidence |
| <CITATION_LEDGER> | references, bibliography, real-source citation checks | Verified citation and bibliography state used by the draft. | isomer-rsch-write-v2 | write, review, finalize | evidence |
| <DISPLAY_PLAN> | planned figures and tables | The table and figure plan that routes first-pass plots and durable figures. | isomer-rsch-write-v2 | paper-plot, figure-polish, review | handoff |
| <DRAFT_SECTION_SET> | updated manuscript sections or report text | The authored or revised manuscript sections constrained by the paper contract. | isomer-rsch-write-v2 | review, finalize, rebuttal | draft |
| <MANUSCRIPT_VALIDATION_REPORT> | validation over coverage, claims, figures, citations, language, bundle readiness | The draft-state check that determines whether to checkpoint or route back. | isomer-rsch-write-v2 | review, finalize, decision | report |
| <PAPER_BUNDLE_CHECKPOINT> | artifact.submit_paper_bundle(...) | A coherent draft, review, or submission package checkpoint before downstream routing. | isomer-rsch-write-v2 | review, finalize, user | handoff |
| <WRITING_ROUTE_DECISION> | analysis-campaign, review, finalize, paper-outline, nature companion route | The next route when writing exposes evidence, outline, review, figure, or submission-readiness issues. | isomer-rsch-write-v2 | any selected v2 skill | decision |
