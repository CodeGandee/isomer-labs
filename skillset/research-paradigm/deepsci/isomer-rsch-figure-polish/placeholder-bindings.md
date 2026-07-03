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
- For paper-line figure outputs, use figure-specific profiles such as `figure.message`, `figure.style-contract`, `figure.render-review`, `figure.export`, and `figure.provenance-record` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the generated Markdown view or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store structured figure payloads and generated figure views as Artifacts; create Evidence Items for render inspection when needed. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| provenance | Provenance Record with source identity and downstream links | `provenance_record` | `topic.records.artifacts` | `provenance` | Use this for durable source-to-output chains until a dedicated provenance semantic label exists. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <FIGURE_SURFACE_CLASS> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/figure-surface-class/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<FIGURE_SURFACE_CLASS>' --format-profile isomer:deepsci/record-format/profile/decision/figure-surface-class/v1 --skill isomer-rsch-figure-polish --producer 'isomer-rsch-figure-polish' --consumer 'figure-polish' --payload-file <payload-file> --render markdown --content-name figure-surface-class.md --metadata-json '{"paper_surface":"figure_surface_class"}'` |
| <FIGURE_MESSAGE> | handoff | Figure message Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/message/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIGURE_MESSAGE>' --format-profile isomer:deepsci/record-format/profile/figure/message/v1 --skill isomer-rsch-figure-polish --producer 'isomer-rsch-figure-polish' --consumer 'figure-polish, write, review' --payload-file <payload-file> --render markdown --content-name figure-message.md --metadata-json '{"paper_surface":"figure_message"}'` |
| <FIGURE_STYLE_CONTRACT> | report | Figure style-contract Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/style-contract/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FIGURE_STYLE_CONTRACT>' --format-profile isomer:deepsci/record-format/profile/figure/style-contract/v1 --skill isomer-rsch-figure-polish --producer 'isomer-rsch-figure-polish' --consumer 'figure-polish' --payload-file <payload-file> --render markdown --content-name figure-style-contract.md --metadata-json '{"paper_surface":"figure_style_contract"}'` |
| <FIGURE_RENDER_REVIEW> | report | Figure render-review Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/render-review/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<FIGURE_RENDER_REVIEW>' --format-profile isomer:deepsci/record-format/profile/figure/render-review/v1 --skill isomer-rsch-figure-polish --producer 'isomer-rsch-figure-polish' --consumer 'figure-polish' --payload-file <payload-file> --render markdown --content-name figure-render-review.md --metadata-json '{"paper_surface":"figure_render_review"}'` |
| <FINAL_FIGURE_EXPORT> | figure | Final figure export Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/export/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FINAL_FIGURE_EXPORT>' --format-profile isomer:deepsci/record-format/profile/figure/export/v1 --skill isomer-rsch-figure-polish --producer 'isomer-rsch-figure-polish' --consumer 'write, review, finalize' --payload-file <payload-file> --render markdown --content-name final-figure-export.md --metadata-json '{"paper_surface":"final_figure_export"}'` |
| <FIGURE_PROVENANCE_RECORD> | provenance | Figure provenance Record | `provenance_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/provenance-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind provenance_record --semantic-label topic.records.artifacts --placeholder '<FIGURE_PROVENANCE_RECORD>' --format-profile isomer:deepsci/record-format/profile/figure/provenance-record/v1 --skill isomer-rsch-figure-polish --producer 'isomer-rsch-figure-polish' --consumer 'write, review, finalize' --payload-file <payload-file> --render markdown --content-name figure-provenance-record.md --metadata-json '{"paper_surface":"figure_provenance"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` to inspect one stored record, payload, and generated view when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file> --render markdown` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves generated view files by default.
