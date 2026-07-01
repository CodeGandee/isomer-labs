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
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store exported figures and figure bundles as Artifacts; create Evidence Items for render inspection when needed. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <FIGURE_SURFACE_CLASS> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.figure-surface-class` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<FIGURE_SURFACE_CLASS>' --profile decision.figure-surface-class --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish' --body-file <body-file>` |
| <FIGURE_MESSAGE> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.figure-message` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FIGURE_MESSAGE>' --profile handoff.figure-message --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish, write, review' --body-file <body-file>` |
| <FIGURE_STYLE_CONTRACT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.figure-style-contract` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FIGURE_STYLE_CONTRACT>' --profile report.figure-style-contract --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish' --body-file <body-file>` |
| <FIGURE_RENDER_REVIEW> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.figure-render-review` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FIGURE_RENDER_REVIEW>' --profile report.figure-render-review --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish' --body-file <body-file>` |
| <FINAL_FIGURE_EXPORT> | figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure.final-figure-export` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FINAL_FIGURE_EXPORT>' --profile figure.final-figure-export --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'write, review, finalize' --body-file <body-file>` |
| <FIGURE_PROVENANCE_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.figure-provenance-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<FIGURE_PROVENANCE_RECORD>' --profile evidence.figure-provenance-record --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'write, review, finalize' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
