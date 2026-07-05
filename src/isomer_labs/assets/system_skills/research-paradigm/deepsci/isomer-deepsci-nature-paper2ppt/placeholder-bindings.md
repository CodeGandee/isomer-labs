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
- For paper-line presentation outputs, use profiles such as `presentation.source-packet`, `presentation.plan`, `presentation.asset-manifest`, `presentation.slide-content`, `package.presentation.pptx-deck`, `presentation.qa-report`, and `presentation.revision-log` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store structured figure payloads and generated figure views as Artifacts; create Evidence Items for render inspection when needed. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <PAPER_PRESENTATION_SOURCE_PACKET> | evidence | Presentation source-packet Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/presentation/source-packet/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<PAPER_PRESENTATION_SOURCE_PACKET>' --format-profile isomer:deepsci/record-format/profile/presentation/source-packet/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'nature-paper2ppt' --payload-file <payload-file> --metadata-json '{"paper_surface":"presentation_source_packet"}'` |
| <PAPER_TYPE_CLASSIFICATION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/paper-type-classification/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PAPER_TYPE_CLASSIFICATION>' --format-profile isomer:deepsci/record-format/profile/decision/paper-type-classification/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'nature-paper2ppt' --payload-file <payload-file> --metadata-json '{"paper_surface":"paper_type_classification"}'` |
| <CHINESE_PRESENTATION_PLAN> | draft | Chinese presentation plan Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/presentation/plan/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<CHINESE_PRESENTATION_PLAN>' --format-profile isomer:deepsci/record-format/profile/presentation/plan/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'nature-paper2ppt, user' --payload-file <payload-file> --metadata-json '{"paper_surface":"chinese_presentation_plan"}'` |
| <PRESENTATION_FIGURE_SELECTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/presentation-figure-selection/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PRESENTATION_FIGURE_SELECTION>' --format-profile isomer:deepsci/record-format/profile/decision/presentation-figure-selection/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'nature-paper2ppt' --payload-file <payload-file> --metadata-json '{"paper_surface":"presentation_figure_selection"}'` |
| <PRESENTATION_ASSET_MANIFEST> | figure | Presentation asset manifest Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/presentation/asset-manifest/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PRESENTATION_ASSET_MANIFEST>' --format-profile isomer:deepsci/record-format/profile/presentation/asset-manifest/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'nature-paper2ppt, user' --payload-file <payload-file> --metadata-json '{"paper_surface":"presentation_asset_manifest"}'` |
| <CHINESE_SLIDE_CONTENT> | draft | Chinese slide content Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/presentation/slide-content/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<CHINESE_SLIDE_CONTENT>' --format-profile isomer:deepsci/record-format/profile/presentation/slide-content/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'nature-paper2ppt, user' --payload-file <payload-file> --metadata-json '{"paper_surface":"chinese_slide_content"}'` |
| <PPTX_DECK> | report | PPTX deck package Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/package/presentation/pptx-deck/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PPTX_DECK>' --format-profile isomer:deepsci/record-format/profile/package/presentation/pptx-deck/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'user' --payload-file <payload-file> --metadata-json '{"paper_surface":"pptx_deck"}'` |
| <PPTX_QA_REPORT> | report | PPTX QA report Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/presentation/qa-report/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PPTX_QA_REPORT>' --format-profile isomer:deepsci/record-format/profile/presentation/qa-report/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'user' --payload-file <payload-file> --metadata-json '{"paper_surface":"pptx_qa_report"}'` |
| <PPTX_REVISION_LOG> | report | PPTX revision log Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/presentation/revision-log/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PPTX_REVISION_LOG>' --format-profile isomer:deepsci/record-format/profile/presentation/revision-log/v1 --skill isomer-deepsci-nature-paper2ppt --producer 'isomer-deepsci-nature-paper2ppt' --consumer 'user' --payload-file <payload-file> --metadata-json '{"paper_surface":"pptx_revision_log"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file>` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
