# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line figure outputs, use figure-specific profiles such as `figure.message`, `figure.style-contract`, `figure.render-review`, `figure.export`, and `figure.provenance-record` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then summarize the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store exported figures and figure bundles as Artifacts; create Evidence Items for render inspection when needed. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| provenance | Provenance Record with source identity and downstream links | `provenance_record` | `topic.records.artifacts` | `provenance` | Use this for durable source-to-output chains until a dedicated provenance semantic label exists. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <FIGURE_SURFACE_CLASS> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.figure-surface-class` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<FIGURE_SURFACE_CLASS>' --profile decision.figure-surface-class --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish' --body-file <body-file> --metadata-json '{"paper_surface":"figure_surface_class"}'` |
| <FIGURE_MESSAGE> | handoff | Figure message Artifact | `artifact` | `topic.records.artifacts` | `figure.message` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIGURE_MESSAGE>' --profile figure.message --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish, write, review' --body-file <body-file> --content-name figure-message.md --metadata-json '{"paper_surface":"figure_message"}'` |
| <FIGURE_STYLE_CONTRACT> | report | Figure style-contract Artifact | `artifact` | `topic.records.artifacts` | `figure.style-contract` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIGURE_STYLE_CONTRACT>' --profile figure.style-contract --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish' --body-file <body-file> --content-name figure-style-contract.json --metadata-json '{"paper_surface":"figure_style_contract"}'` |
| <FIGURE_RENDER_REVIEW> | report | Figure render-review Evidence Item | `evidence_item` | `topic.records.artifacts` | `figure.render-review` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<FIGURE_RENDER_REVIEW>' --profile figure.render-review --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'figure-polish' --body-file <body-file> --content-name figure-render-review.md --metadata-json '{"paper_surface":"figure_render_review"}'` |
| <FINAL_FIGURE_EXPORT> | figure | Final figure export Artifact | `artifact` | `topic.records.artifacts` | `figure.export` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FINAL_FIGURE_EXPORT>' --profile figure.export --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'write, review, finalize' --body-file <body-file> --content-name final-figure-export.json --metadata-json '{"paper_surface":"final_figure_export"}'` |
| <FIGURE_PROVENANCE_RECORD> | provenance | Figure provenance Record | `provenance_record` | `topic.records.artifacts` | `figure.provenance-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind provenance_record --semantic-label topic.records.artifacts --placeholder '<FIGURE_PROVENANCE_RECORD>' --profile figure.provenance-record --skill isomer-rsch-figure-polish-v2 --producer 'isomer-rsch-figure-polish-v2' --consumer 'write, review, finalize' --body-file <body-file> --content-name figure-provenance-record.json --metadata-json '{"paper_surface":"figure_provenance"}'` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
