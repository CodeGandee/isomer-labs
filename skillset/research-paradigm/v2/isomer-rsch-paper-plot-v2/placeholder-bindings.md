# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
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
| <CHART_QUESTION> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.chart-question` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<CHART_QUESTION>' --profile handoff.chart-question --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2 or write' --consumer 'paper-plot' --body-file <body-file>` |
| <PLOT_STYLE_SELECTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.plot-style-selection` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<PLOT_STYLE_SELECTION>' --profile decision.plot-style-selection --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot' --body-file <body-file>` |
| <PLOT_TEMPLATE_COPY> | code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `code.plot-template-copy` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PLOT_TEMPLATE_COPY>' --profile code.plot-template-copy --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot, figure-polish' --body-file <body-file>` |
| <PLOT_DATA_SUBSTITUTION_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.plot-data-substitution-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<PLOT_DATA_SUBSTITUTION_RECORD>' --profile evidence.plot-data-substitution-record --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot, review' --body-file <body-file>` |
| <FIRST_PASS_FIGURE> | figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure.first-pass-figure` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FIRST_PASS_FIGURE>' --profile figure.first-pass-figure --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'write, figure-polish, review' --body-file <body-file>` |
| <PLOT_RENDER_INSPECTION> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.plot-render-inspection` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PLOT_RENDER_INSPECTION>' --profile report.plot-render-inspection --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'paper-plot, figure-polish' --body-file <body-file>` |
| <FIGURE_POLISH_HANDOFF> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.figure-polish-handoff` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FIGURE_POLISH_HANDOFF>' --profile handoff.figure-polish-handoff --skill isomer-rsch-paper-plot-v2 --producer 'isomer-rsch-paper-plot-v2' --consumer 'isomer-rsch-figure-polish-v2' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
