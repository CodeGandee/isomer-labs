# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <CHART_QUESTION> | comparison, units, grouping, output target | The chart question and display target. | isomer-rsch-paper-plot-v2 or write | paper-plot | handoff |
| <PLOT_STYLE_SELECTION> | Available Styles table | The selected bundled plot family and source script. | isomer-rsch-paper-plot-v2 | paper-plot | decision |
| <PLOT_TEMPLATE_COPY> | task-local copied plotting script | The mutable copied script in the active workspace. | isomer-rsch-paper-plot-v2 | paper-plot, figure-polish | code |
| <PLOT_DATA_SUBSTITUTION_RECORD> | changed data, labels, category fields | Record of data and label substitutions made to the copied script. | isomer-rsch-paper-plot-v2 | paper-plot, review | evidence |
| <FIRST_PASS_FIGURE> | first-pass rendered figure | The rendered image produced from the copied template. | isomer-rsch-paper-plot-v2 | write, figure-polish, review | figure |
| <PLOT_RENDER_INSPECTION> | inspect rendered output | Visual QA note from inspecting the actual first-pass render. | isomer-rsch-paper-plot-v2 | paper-plot, figure-polish | report |
| <FIGURE_POLISH_HANDOFF> | handoff to figure-polish | A durable figure handoff containing script, data, render, message, and remaining QA needs. | isomer-rsch-paper-plot-v2 | isomer-rsch-figure-polish-v2 | handoff |
