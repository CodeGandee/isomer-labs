# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <NATURE_FIGURE_BACKEND_CHOICE> | Python or R selection | The selected plotting backend and selection basis. | isomer-rsch-nature-figure-v2 or user | nature-figure | decision |
| <NATURE_FIGURE_CONTRACT> | figure contract | Conclusion, evidence chain, panel roles, dimensions, statistics, integrity notes, and export formats. | isomer-rsch-nature-figure-v2 | nature-figure, write, finalize | handoff |
| <NATURE_FIGURE_RUNTIME_CHECK> | selected runtime and packages | Availability and blockers for the selected backend. | isomer-rsch-nature-figure-v2 | nature-figure, user | report |
| <NATURE_PANEL_EVIDENCE_MAP> | panel to evidence links | Panel-level evidence map and source-data/statistics note. | isomer-rsch-nature-figure-v2 | nature-figure, review | evidence |
| <NATURE_FIGURE_ARCHETYPE> | figure structure | Selected composition archetype and design rationale. | isomer-rsch-nature-figure-v2 | nature-figure | decision |
| <NATURE_EXPORT_CONTRACT> | journal export contract | Required formats, dimensions, editable text, statistics, and integrity checks. | isomer-rsch-nature-figure-v2 | nature-figure, finalize | handoff |
| <NATURE_FIGURE_EXPORT_BUNDLE> | backend-specific plotting script and exports | Script, source data, exports, and preview files produced with the selected backend. | isomer-rsch-nature-figure-v2 | write, finalize, user | figure |
| <NATURE_FIGURE_QA_REPORT> | preview and QA evidence | Rendered-preview QA and revision record. | isomer-rsch-nature-figure-v2 | nature-figure, review, finalize | report |
| <NATURE_FIGURE_BLOCKER> | runtime unavailable or evidence defect | Blocked state when selected backend, source data, statistics, or evidence chain is insufficient. | isomer-rsch-nature-figure-v2 | user, decision | decision |
