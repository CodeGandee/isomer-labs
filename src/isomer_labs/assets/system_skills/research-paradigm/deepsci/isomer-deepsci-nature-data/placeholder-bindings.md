# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file>`. Workspace Runtime snapshots the accepted payload into managed JSON file storage. Render Markdown on demand for human review; update the JSON payload rather than editing rendered Markdown as the source of truth.

## Canonical lineage metadata

When a durable record is produced from prior durable records, pass immediate parents through `--parents-json`, choose `--lineage-kind`, and add `--generation-id` plus `--generation-purpose` for sibling candidate passes. Use `revision_of` only through `ext research records revise <record-id>` when accepted content changes; use `--relationships-json`, `--files-json`, and `--index-hints-json` only for non-lineage query metadata.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name evidence, citations, file materialization, support links, summaries, routes, or other non-canonical refs; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and payload file and optional export metadata on created records.
- Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.
- For paper-line data-availability outputs, use profiles such as `paper.data-availability-context`, `paper.dataset-inventory`, `paper.data-repository-strategy`, `paper.data-availability-statement`, `paper.dataset-citation-actions`, and `paper.fair-metadata-audit` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <DATA_AVAILABILITY_CONTEXT> | runtime state | Data availability context View Manifest | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/paper/data-availability-context/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<DATA_AVAILABILITY_CONTEXT>' --format-profile isomer:deepsci/record-format/profile/paper/data-availability-context/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'nature-data' --payload-file <payload-file> --metadata-json '{"paper_surface":"data_availability_context"}'` |
| <DATASET_INVENTORY> | evidence | Dataset inventory Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/dataset-inventory/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<DATASET_INVENTORY>' --format-profile isomer:deepsci/record-format/profile/paper/dataset-inventory/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'nature-data, write, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"dataset_inventory"}'` |
| <DATA_ACCESS_CLASSIFICATION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/data-access-classification/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<DATA_ACCESS_CLASSIFICATION>' --format-profile isomer:deepsci/record-format/profile/decision/data-access-classification/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'nature-data' --payload-file <payload-file> --metadata-json '{"paper_surface":"data_access_classification"}'` |
| <REPOSITORY_STRATEGY> | handoff | Data repository strategy Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/data-repository-strategy/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<REPOSITORY_STRATEGY>' --format-profile isomer:deepsci/record-format/profile/paper/data-repository-strategy/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'nature-data, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"repository_strategy"}'` |
| <DATA_AVAILABILITY_STATEMENT> | draft | Data availability statement Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/data-availability-statement/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<DATA_AVAILABILITY_STATEMENT>' --format-profile isomer:deepsci/record-format/profile/paper/data-availability-statement/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'write, finalize, user' --payload-file <payload-file> --metadata-json '{"paper_surface":"data_availability_statement"}'` |
| <DATASET_CITATION_ACTIONS> | report | Dataset citation actions Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/dataset-citation-actions/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<DATASET_CITATION_ACTIONS>' --format-profile isomer:deepsci/record-format/profile/paper/dataset-citation-actions/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'write, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"dataset_citation_actions"}'` |
| <FAIR_METADATA_AUDIT> | report | FAIR metadata audit Artifact | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/paper/fair-metadata-audit/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<FAIR_METADATA_AUDIT>' --format-profile isomer:deepsci/record-format/profile/paper/fair-metadata-audit/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'nature-data, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"fair_metadata_audit"}'` |
| <DATA_AVAILABILITY_BLOCKER> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/data-availability-blocker/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<DATA_AVAILABILITY_BLOCKER>' --format-profile isomer:deepsci/record-format/profile/decision/data-availability-blocker/v1 --skill isomer-deepsci-nature-data --producer 'isomer-deepsci-nature-data' --consumer 'user, decision, finalize' --payload-file <payload-file> --metadata-json '{"paper_surface":"data_availability_blocker"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file>` for status, metadata, or repair updates. Use `isomer-cli --print-json ext research records revise <record-id> --topic <topic> --payload-file <payload-file>` when accepted content changes and must remain visible as a new descendant revision.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
