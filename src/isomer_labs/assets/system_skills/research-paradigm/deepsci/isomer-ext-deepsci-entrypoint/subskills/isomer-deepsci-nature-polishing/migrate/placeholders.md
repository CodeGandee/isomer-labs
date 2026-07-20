# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:PAPER-TYPE-DIAGNOSIS | paper type | Paper-type logic selected before editing. | isomer-rsch-nature-polishing | nature-polishing | decision |
| DEEPSCI:PROSE-FAILURE-DIAGNOSIS | failure mode | Argument, evidence, section-logic, or sentence-level defect diagnosis. | isomer-rsch-nature-polishing | nature-polishing, write | report |
| DEEPSCI:CLAIM-BOUNDARY-CHECK | evidence boundary | What the evidence can and cannot support. | isomer-rsch-nature-polishing | nature-polishing, write, review | evidence |
| DEEPSCI:SECTION-LOGIC-REBUILD | rebuilt section logic | Reordered or restructured section-level argument plan. | isomer-rsch-nature-polishing | nature-polishing, write | draft |
| DEEPSCI:POLISHED-MANUSCRIPT-TEXT | revised text | Polished or translated manuscript prose. | isomer-rsch-nature-polishing | write, user | draft |
| DEEPSCI:POLISHING-STYLE-QA | style guardrails | Register, mechanics, paragraph, citation, AI-boundary, and claim-calibration QA. | isomer-rsch-nature-polishing | nature-polishing, write | report |
| DEEPSCI:POLISHING-EVIDENCE-BLOCKER | unsupported claim warning | Warning or blocker when requested prose would overstate evidence. | isomer-rsch-nature-polishing | user, write, decision | decision |
