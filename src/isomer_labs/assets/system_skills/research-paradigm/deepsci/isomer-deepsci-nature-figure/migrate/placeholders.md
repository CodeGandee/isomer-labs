# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:NATURE-FIGURE-BACKEND-CHOICE | Python or R selection | The selected plotting backend and selection basis. | isomer-rsch-nature-figure or user | nature-figure | decision |
| DEEPSCI:NATURE-FIGURE-CONTRACT | figure contract | Conclusion, evidence chain, panel roles, dimensions, statistics, integrity notes, and export formats. | isomer-rsch-nature-figure | nature-figure, write, finalize | handoff |
| DEEPSCI:NATURE-FIGURE-RUNTIME-CHECK | selected runtime and packages | Availability and blockers for the selected backend. | isomer-rsch-nature-figure | nature-figure, user | report |
| DEEPSCI:NATURE-PANEL-EVIDENCE-MAP | panel to evidence links | Panel-level evidence map and source-data/statistics note. | isomer-rsch-nature-figure | nature-figure, review | evidence |
| DEEPSCI:NATURE-FIGURE-ARCHETYPE | figure structure | Selected composition archetype and design rationale. | isomer-rsch-nature-figure | nature-figure | decision |
| DEEPSCI:NATURE-EXPORT-CONTRACT | journal export contract | Required formats, dimensions, editable text, statistics, and integrity checks. | isomer-rsch-nature-figure | nature-figure, finalize | handoff |
| DEEPSCI:NATURE-FIGURE-EXPORT-BUNDLE | backend-specific plotting script and exports | Script, source data, exports, and preview files produced with the selected backend. | isomer-rsch-nature-figure | write, finalize, user | figure |
| DEEPSCI:NATURE-FIGURE-QA-REPORT | preview and QA evidence | Rendered-preview QA and revision record. | isomer-rsch-nature-figure | nature-figure, review, finalize | report |
| DEEPSCI:NATURE-FIGURE-BLOCKER | runtime unavailable or evidence defect | Blocked state when selected backend, source data, statistics, or evidence chain is insufficient. | isomer-rsch-nature-figure | user, decision | decision |
