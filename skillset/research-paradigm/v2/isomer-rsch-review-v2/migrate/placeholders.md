# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <REVIEW_AUDIT_PLAN> | claim set, strongest/weakest evidence, likely rejection reasons | The plan for a skeptical manuscript audit. | isomer-rsch-review-v2 | review | report |
| <LITERATURE_BENCHMARK_NOTE> | nearby strong papers or venue expectations | Comparison against relevant literature and reviewer expectations. | isomer-rsch-review-v2 | review, scout, write | evidence |
| <REVIEW_REPORT> | paper/review/review.md | Independent review report with strengths, weaknesses, risks, and actionable suggestions. | isomer-rsch-review-v2 | write, rebuttal, finalize | report |
| <REVISION_LOG> | paper/review/revision_log.md | Concrete issue-to-fix log for manuscript, evidence, figure, and routing work. | isomer-rsch-review-v2 | write, analysis, decision | handoff |
| <REVIEW_EXPERIMENT_TODO> | paper/review/experiment_todo.md | Concrete evidence TODOs when review finds real missing evidence. | isomer-rsch-review-v2 | analysis, experiment, decision | handoff |
| <PAPER_EXPERIMENT_MATRIX_UPDATE> | paper/paper_experiment_matrix.md and .json | Paper-facing experiment plan update caused by review. | isomer-rsch-review-v2 | write, analysis, rebuttal | runtime state |
| <REVIEW_ROUTE_DECISION> | write, scout, baseline, analysis-campaign, decision route | The next route selected from review findings. | isomer-rsch-review-v2 | any selected v2 skill | decision |
