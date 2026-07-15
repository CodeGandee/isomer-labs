# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:CHART-QUESTION | comparison, units, grouping, output target | The chart question and display target. | isomer-rsch-paper-plot or write | paper-plot | handoff |
| DEEPSCI:PLOT-STYLE-SELECTION | Available Styles table | The selected bundled plot family and source script. | isomer-rsch-paper-plot | paper-plot | decision |
| DEEPSCI:PLOT-TEMPLATE-COPY | task-local copied plotting script | The mutable copied script in the active workspace. | isomer-rsch-paper-plot | paper-plot, figure-polish | code |
| DEEPSCI:PLOT-DATA-SUBSTITUTION-RECORD | changed data, labels, category fields | Record of data and label substitutions made to the copied script. | isomer-rsch-paper-plot | paper-plot, review | evidence |
| DEEPSCI:FIRST-PASS-FIGURE | first-pass rendered figure | The rendered image produced from the copied template. | isomer-rsch-paper-plot | write, figure-polish, review | figure |
| DEEPSCI:PLOT-RENDER-INSPECTION | inspect rendered output | Visual QA note from inspecting the actual first-pass render. | isomer-rsch-paper-plot | paper-plot, figure-polish | evidence |
| DEEPSCI:FIGURE-POLISH-HANDOFF | handoff to figure-polish | A durable figure handoff containing script, data, render, message, and remaining QA needs. | isomer-rsch-paper-plot | isomer-rsch-figure-polish | handoff |
