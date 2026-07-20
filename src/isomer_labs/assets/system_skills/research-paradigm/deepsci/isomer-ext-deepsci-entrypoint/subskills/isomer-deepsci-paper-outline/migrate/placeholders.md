# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:PAPER-STATE-SNAPSHOT | current outline, paper contract, evidence surfaces | The source state for outline creation or repair. | isomer-rsch-paper-outline | paper-outline, write | runtime state |
| DEEPSCI:ONE-SENTENCE-PAPER-IDEA | one-sentence paper idea | The concise reader-facing claim the paper should make memorable. | isomer-rsch-paper-outline | paper-outline, write, review | draft |
| DEEPSCI:CLAIM-EVIDENCE-BOUNDARY | facts versus interpretation | Allowed claims, supporting evidence, limitations, and falsification boundaries. | isomer-rsch-paper-outline | write, review, rebuttal | evidence |
| DEEPSCI:PAPER-VIEW | paper_view | Reader-facing thesis, claim spine, method abstraction, evaluation plan, and analysis plan. | isomer-rsch-paper-outline | write, review | handoff |
| DEEPSCI:EVIDENCE-VIEW | evidence_view | Runs, paths, metrics, settings, source data, and reproducibility material kept outside the story spine. | isomer-rsch-paper-outline | write, review, finalize | evidence |
| DEEPSCI:OUTLINE-VALIDATION-REPORT | artifact.validate_academic_outline(detail="full") | Validation record for outline maturity and evidence support. | isomer-rsch-paper-outline | paper-outline, write, decision | report |
| DEEPSCI:SECTION-WRITING-PLAN | artifact.compile_outline_to_writing_plan(detail="full") | Section jobs derived from a valid outline. | isomer-rsch-paper-outline | write | research task |
| DEEPSCI:PAPER-OUTLINE-ROUTE-DECISION | repair, compile writing plan, or route back | Decision when outline repair exposes missing evidence or route ambiguity. | isomer-rsch-paper-outline | analysis, decision, write | decision |
