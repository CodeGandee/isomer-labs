# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <PAPER_TYPE_DIAGNOSIS> | paper type | Paper-type logic selected before editing. | isomer-rsch-nature-polishing | nature-polishing | decision |
| <PROSE_FAILURE_DIAGNOSIS> | failure mode | Argument, evidence, section-logic, or sentence-level defect diagnosis. | isomer-rsch-nature-polishing | nature-polishing, write | report |
| <CLAIM_BOUNDARY_CHECK> | evidence boundary | What the evidence can and cannot support. | isomer-rsch-nature-polishing | nature-polishing, write, review | evidence |
| <SECTION_LOGIC_REBUILD> | rebuilt section logic | Reordered or restructured section-level argument plan. | isomer-rsch-nature-polishing | nature-polishing, write | draft |
| <POLISHED_MANUSCRIPT_TEXT> | revised text | Polished or translated manuscript prose. | isomer-rsch-nature-polishing | write, user | draft |
| <POLISHING_STYLE_QA> | style guardrails | Register, mechanics, paragraph, citation, AI-boundary, and claim-calibration QA. | isomer-rsch-nature-polishing | nature-polishing, write | report |
| <POLISHING_EVIDENCE_BLOCKER> | unsupported claim warning | Warning or blocker when requested prose would overstate evidence. | isomer-rsch-nature-polishing | user, write, decision | decision |
