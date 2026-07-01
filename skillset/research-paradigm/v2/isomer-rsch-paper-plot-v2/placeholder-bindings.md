# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line figure outputs, use paper and figure profiles such as `paper.experiment-matrix`, `figure.chart-question`, `figure.plot-data-substitution`, `figure.export.first-pass`, `figure.render-inspection`, and `figure.polish-handoff` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then summarize the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `code` | Work in `topic.repos.main` or an Agent Workspace first, then promote durable code outputs into topic records. |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store exported figures and figure bundles as Artifacts; create Evidence Items for render inspection when needed. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <CHART_QUESTION> | handoff | Chart question Artifact linked to the paper display plan | `artifact` | `topic.records.artifacts` | `figure.chart-question` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<CHART_QUESTION>' --profile figure.chart-question --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2 or write' --consumer 'paper-plot' --body-file <body-file> --content-name chart-question.md --metadata-json '{"paper_surface":"chart_question"}'` |
| <PLOT_STYLE_SELECTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.plot-style-selection` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PLOT_STYLE_SELECTION>' --profile decision.plot-style-selection --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot' --body-file <body-file> --metadata-json '{"paper_surface":"plot_style_selection"}'` |
| <PLOT_TEMPLATE_COPY> | code | Plot template copy Code Artifact | `artifact` | `topic.records.artifacts` | `code.plot-template-copy` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PLOT_TEMPLATE_COPY>' --profile code.plot-template-copy --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot, figure-polish' --body-file <body-file> --content-name plot-template-copy.json --metadata-json '{"paper_surface":"plot_template_copy"}'` |
| <PLOT_DATA_SUBSTITUTION_RECORD> | evidence | Plot data substitution Evidence Item | `evidence_item` | `topic.records.artifacts` | `figure.plot-data-substitution` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<PLOT_DATA_SUBSTITUTION_RECORD>' --profile figure.plot-data-substitution --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot, review' --body-file <body-file> --content-name plot-data-substitution.json --metadata-json '{"paper_surface":"plot_data_substitution"}'` |
| <FIRST_PASS_FIGURE> | figure | First-pass figure Artifact | `artifact` | `topic.records.artifacts` | `figure.export.first-pass` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIRST_PASS_FIGURE>' --profile figure.export.first-pass --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'write, figure-polish, review' --body-file <body-file> --content-name first-pass-figure.json --metadata-json '{"paper_surface":"first_pass_figure"}'` |
| <PLOT_RENDER_INSPECTION> | evidence | Plot render-inspection Evidence Item | `evidence_item` | `topic.records.artifacts` | `figure.render-inspection` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<PLOT_RENDER_INSPECTION>' --profile figure.render-inspection --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot, figure-polish' --body-file <body-file> --content-name plot-render-inspection.md --metadata-json '{"paper_surface":"plot_render_inspection"}'` |
| <FIGURE_POLISH_HANDOFF> | handoff | Figure polish handoff Artifact | `artifact` | `topic.records.artifacts` | `figure.polish-handoff` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIGURE_POLISH_HANDOFF>' --profile figure.polish-handoff --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'isomer-rsch-figure-polish-v2' --body-file <body-file> --content-name figure-polish-handoff.json --metadata-json '{"paper_surface":"figure_polish_handoff"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
