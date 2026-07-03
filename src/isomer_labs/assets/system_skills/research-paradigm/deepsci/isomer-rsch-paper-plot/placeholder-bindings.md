# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload, generated view, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file> --render markdown`. The generated Markdown view is review material; update the JSON payload and rerender rather than editing generated Markdown as the source of truth.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and generated view naming metadata on created records.
- Resolve generated view locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line figure outputs, use paper and figure profiles such as `paper.experiment-matrix`, `figure.chart-question`, `figure.plot-data-substitution`, `figure.export.first-pass`, `figure.render-inspection`, and `figure.polish-handoff` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `code` | Work in `topic.repos.main` or an Agent Workspace first, then promote durable code outputs into topic records. |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the generated Markdown view or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store structured figure payloads and generated figure views as Artifacts; create Evidence Items for render inspection when needed. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <CHART_QUESTION> | handoff | Chart question Artifact linked to the paper display plan | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/chart-question/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<CHART_QUESTION>' --format-profile isomer:deepsci/record-format/profile/figure/chart-question/v1 --skill isomer-rsch-paper-plot --producer 'isomer-rsch-paper-plot or write' --consumer 'paper-plot' --payload-file <payload-file> --render markdown --content-name chart-question.md --metadata-json '{"paper_surface":"chart_question"}'` |
| <PLOT_STYLE_SELECTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/plot-style-selection/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PLOT_STYLE_SELECTION>' --format-profile isomer:deepsci/record-format/profile/decision/plot-style-selection/v1 --skill isomer-rsch-paper-plot --producer 'isomer-rsch-paper-plot' --consumer 'paper-plot' --payload-file <payload-file> --render markdown --content-name plot-style-selection.md --metadata-json '{"paper_surface":"plot_style_selection"}'` |
| <PLOT_TEMPLATE_COPY> | code | Plot template copy Code Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/code/plot-template-copy/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PLOT_TEMPLATE_COPY>' --format-profile isomer:deepsci/record-format/profile/code/plot-template-copy/v1 --skill isomer-rsch-paper-plot --producer 'isomer-rsch-paper-plot' --consumer 'paper-plot, figure-polish' --payload-file <payload-file> --render markdown --content-name plot-template-copy.md --metadata-json '{"paper_surface":"plot_template_copy"}'` |
| <PLOT_DATA_SUBSTITUTION_RECORD> | evidence | Plot data substitution Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/plot-data-substitution/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<PLOT_DATA_SUBSTITUTION_RECORD>' --format-profile isomer:deepsci/record-format/profile/figure/plot-data-substitution/v1 --skill isomer-rsch-paper-plot --producer 'isomer-rsch-paper-plot' --consumer 'paper-plot, review' --payload-file <payload-file> --render markdown --content-name plot-data-substitution.md --metadata-json '{"paper_surface":"plot_data_substitution"}'` |
| <FIRST_PASS_FIGURE> | figure | First-pass figure Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/export/first-pass/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIRST_PASS_FIGURE>' --format-profile isomer:deepsci/record-format/profile/figure/export/first-pass/v1 --skill isomer-rsch-paper-plot --producer 'isomer-rsch-paper-plot' --consumer 'write, figure-polish, review' --payload-file <payload-file> --render markdown --content-name first-pass-figure.md --metadata-json '{"paper_surface":"first_pass_figure"}'` |
| <PLOT_RENDER_INSPECTION> | evidence | Plot render-inspection Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/render-inspection/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<PLOT_RENDER_INSPECTION>' --format-profile isomer:deepsci/record-format/profile/figure/render-inspection/v1 --skill isomer-rsch-paper-plot --producer 'isomer-rsch-paper-plot' --consumer 'paper-plot, figure-polish' --payload-file <payload-file> --render markdown --content-name plot-render-inspection.md --metadata-json '{"paper_surface":"plot_render_inspection"}'` |
| <FIGURE_POLISH_HANDOFF> | handoff | Figure polish handoff Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/polish-handoff/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIGURE_POLISH_HANDOFF>' --format-profile isomer:deepsci/record-format/profile/figure/polish-handoff/v1 --skill isomer-rsch-paper-plot --producer 'isomer-rsch-paper-plot' --consumer 'isomer-rsch-figure-polish' --payload-file <payload-file> --render markdown --content-name figure-polish-handoff.md --metadata-json '{"paper_surface":"figure_polish_handoff"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` to inspect one stored record, payload, and generated view when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file> --render markdown` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves generated view files by default.
