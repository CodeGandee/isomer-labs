# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file>`. Workspace Runtime snapshots the accepted payload into managed JSON file storage. Render Markdown on demand for human review; update the JSON payload rather than editing rendered Markdown as the source of truth.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name consumed, produced, routed, supported, superseded, summarized, or cited records; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and payload file and optional export metadata on created records.
- Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.
- For paper-line Nature figure outputs, use figure-specific profiles such as `figure.contract.nature`, `figure.runtime-check`, `figure.panel-evidence-map`, `figure.export-contract.nature`, `figure.export.nature`, and `figure.render-review.nature` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store structured figure payloads and generated figure views as Artifacts; create Evidence Items for render inspection when needed. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <NATURE_FIGURE_BACKEND_CHOICE> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/nature-figure-backend-choice/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<NATURE_FIGURE_BACKEND_CHOICE>' --format-profile isomer:deepsci/record-format/profile/decision/nature-figure-backend-choice/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure or user' --consumer 'nature-figure' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_figure_backend_choice"}'` |
| <NATURE_FIGURE_CONTRACT> | handoff | Nature figure contract Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/contract/nature/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<NATURE_FIGURE_CONTRACT>' --format-profile isomer:deepsci/record-format/profile/figure/contract/nature/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'nature-figure, write, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_figure_contract"}'` |
| <NATURE_FIGURE_RUNTIME_CHECK> | report | Nature figure runtime-check Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/runtime-check/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<NATURE_FIGURE_RUNTIME_CHECK>' --format-profile isomer:deepsci/record-format/profile/figure/runtime-check/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'nature-figure, user' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_figure_runtime_check"}'` |
| <NATURE_PANEL_EVIDENCE_MAP> | evidence | Nature panel evidence map Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/panel-evidence-map/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<NATURE_PANEL_EVIDENCE_MAP>' --format-profile isomer:deepsci/record-format/profile/figure/panel-evidence-map/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'nature-figure, review' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_panel_evidence_map"}'` |
| <NATURE_FIGURE_ARCHETYPE> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/nature-figure-archetype/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<NATURE_FIGURE_ARCHETYPE>' --format-profile isomer:deepsci/record-format/profile/decision/nature-figure-archetype/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'nature-figure' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_figure_archetype"}'` |
| <NATURE_EXPORT_CONTRACT> | handoff | Nature export contract Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/export-contract/nature/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<NATURE_EXPORT_CONTRACT>' --format-profile isomer:deepsci/record-format/profile/figure/export-contract/nature/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'nature-figure, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_export_contract"}'` |
| <NATURE_FIGURE_EXPORT_BUNDLE> | figure | Nature figure export bundle Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/export/nature/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<NATURE_FIGURE_EXPORT_BUNDLE>' --format-profile isomer:deepsci/record-format/profile/figure/export/nature/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'write, finalize, user' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_figure_export_bundle"}'` |
| <NATURE_FIGURE_QA_REPORT> | report | Nature figure render-review Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/figure/render-review/nature/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<NATURE_FIGURE_QA_REPORT>' --format-profile isomer:deepsci/record-format/profile/figure/render-review/nature/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'nature-figure, review, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_figure_qa_report"}'` |
| <NATURE_FIGURE_BLOCKER> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/nature-figure-blocker/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<NATURE_FIGURE_BLOCKER>' --format-profile isomer:deepsci/record-format/profile/decision/nature-figure-blocker/v1 --skill isomer-deepsci-nature-figure --producer 'isomer-deepsci-nature-figure' --consumer 'user, decision' --payload-file <payload-file> --metadata-json '{"paper_surface":"nature_figure_blocker"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file>` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
