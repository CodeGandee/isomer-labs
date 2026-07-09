# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional accepted research artifact CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates an accepted research artifact record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file>`. Workspace Runtime snapshots the accepted payload into managed JSON file storage. Render Markdown on demand for human review; update the JSON payload rather than editing rendered Markdown as the source of truth.

Every structured payload file must include non-empty top-level `title` and `summary` strings. If the payload contains idea-bearing entries that can become canonical Research Ideas, each accepted idea object must include its own non-empty `title` and `summary`; labels, candidate ids, and aliases may be present but do not replace those display fields.

## Canonical lineage metadata

When a durable record is produced from prior durable records, pass immediate parents through `--parents-json`, choose `--lineage-kind`, and add `--generation-id` plus `--generation-purpose` for sibling candidate passes. Use `revision_of` only through `ext research records revise <record-id>` when accepted content changes; use `--relationships-json`, `--files-json`, and `--index-hints-json` only for non-lineage query metadata.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name evidence, citations, file materialization, support links, summaries, routes, or other non-canonical refs; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and payload file and optional export metadata on created records.
- Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the on-demand Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <RSCH_WORKSPACE_CONTEXT> | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/rsch-workspace-context/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<RSCH_WORKSPACE_CONTEXT>' --format-profile isomer:deepsci/record-format/profile/evidence/rsch-workspace-context/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr' --consumer 'all production DeepSci research skills and Topic Service Master fallback flows' --payload-file <payload-file>` |
| <RSCH_STORAGE_LABEL_PLAN> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/rsch-storage-label-plan/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<RSCH_STORAGE_LABEL_PLAN>' --format-profile isomer:deepsci/record-format/profile/control/rsch-storage-label-plan/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr' --consumer 'all production DeepSci research skills' --payload-file <payload-file>` |
| <RSCH_PLACEHOLDER_BINDING_REGISTRY> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/rsch-placeholder-binding-registry/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_PLACEHOLDER_BINDING_REGISTRY>' --format-profile isomer:deepsci/record-format/profile/report/rsch-placeholder-binding-registry/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr' --consumer 'all production DeepSci research skills, validators, and later storage-binding work' --payload-file <payload-file>` |
| <RSCH_PLACEHOLDER_BINDING_INDEX> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/rsch-placeholder-binding-index/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<RSCH_PLACEHOLDER_BINDING_INDEX>' --format-profile isomer:deepsci/record-format/profile/control/rsch-placeholder-binding-index/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr' --consumer 'Topic Actors, formal agents, and all production DeepSci research skills' --payload-file <payload-file>` |
| <RSCH_STORAGE_BOOTSTRAP_RECORD> | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/rsch-storage-bootstrap-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<RSCH_STORAGE_BOOTSTRAP_RECORD>' --format-profile isomer:deepsci/record-format/profile/evidence/rsch-storage-bootstrap-record/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr, Topic Service Master, Project Operator Session, or Operator Agent' --consumer 'all production DeepSci research skills and future maintenance passes' --payload-file <payload-file>` |
| <RSCH_AGENT_ACCESS_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/handoff/rsch-agent-access-plan/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_AGENT_ACCESS_PLAN>' --format-profile isomer:deepsci/record-format/profile/handoff/rsch-agent-access-plan/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr' --consumer 'Agent Team Instance members and production DeepSci research skills' --payload-file <payload-file>` |
| <RSCH_BOOTSTRAP_VALIDATION_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/rsch-bootstrap-validation-report/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_BOOTSTRAP_VALIDATION_REPORT>' --format-profile isomer:deepsci/record-format/profile/report/rsch-bootstrap-validation-report/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr' --consumer 'Topic Service Master, Project Operator Session, Operator Agent, and all production DeepSci research skills' --payload-file <payload-file>` |
| <RSCH_WORKSPACE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/rsch-workspace-blocker-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<RSCH_WORKSPACE_BLOCKER_RECORD>' --format-profile isomer:deepsci/record-format/profile/decision/rsch-workspace-blocker-record/v2 --skill isomer-deepsci-workspace-mgr --producer 'isomer-deepsci-workspace-mgr' --consumer 'setup services, Topic Service Master fallback, Operator Agent, or user' --payload-file <payload-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file>` for status, metadata, or repair updates. Use `isomer-cli --print-json ext research records revise <record-id> --topic <topic> --payload-file <payload-file>` when accepted content changes and must remain visible as a new descendant revision.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
