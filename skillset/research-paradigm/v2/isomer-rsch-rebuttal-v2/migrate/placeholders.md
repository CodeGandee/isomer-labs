# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <REVIEW_PACKAGE_NORMALIZATION> | reviewer feedback package | Normalized source-faithful reviewer material. | isomer-rsch-rebuttal-v2 | rebuttal | evidence |
| <REVIEWER_ITEM_MATRIX> | review matrix | Atomic reviewer item matrix with stable ids, classes, severity, affected claims, evidence anchors, and routes. | isomer-rsch-rebuttal-v2 | rebuttal, analysis, write | handoff |
| <REBUTTAL_ACTION_PLAN> | paper/rebuttal/action_plan.md | Planned explanation, evidence, text, limitation, baseline, literature, or analysis actions for reviewer items. | isomer-rsch-rebuttal-v2 | analysis, write, scout, baseline | handoff |
| <REVIEWER_LINKED_EVIDENCE_TODO> | reviewer-linked experiment/action TODOs | Concrete reviewer-id-linked evidence work. | isomer-rsch-rebuttal-v2 | analysis, experiment, decision | research task |
| <REBUTTAL_EVIDENCE_UPDATE> | paper/rebuttal/evidence_update.md | Status and evidence update after routed reviewer work. | isomer-rsch-rebuttal-v2 and routed skills | rebuttal, write, finalize | evidence |
| <MANUSCRIPT_TEXT_DELTA> | text deltas | Concrete manuscript changes tied to reviewer items. | isomer-rsch-write-v2 or rebuttal | rebuttal, finalize | draft |
| <RESPONSE_LETTER_DRAFT> | response letter | Point-by-point author response with evidence basis and manuscript deltas. | isomer-rsch-rebuttal-v2 | user, finalize | draft |
| <REVISION_HANDOFF_BUNDLE> | revised paper bundle | Final handoff package containing response, text deltas, evidence updates, and unresolved risks. | isomer-rsch-rebuttal-v2 | finalize, user | handoff |
