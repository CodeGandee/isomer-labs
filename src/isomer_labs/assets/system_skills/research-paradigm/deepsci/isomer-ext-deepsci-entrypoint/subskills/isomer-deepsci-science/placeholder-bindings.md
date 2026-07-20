# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

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
| run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run` | Use Run records for commands, configs, logs, outputs, metrics, environment facts, and validation refs. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| DEEPSCI:SCIENCE-TASK-BRIEF | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/handoff/science-task-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id 'DEEPSCI:SCIENCE-TASK-BRIEF' --format-profile isomer:deepsci/record-format/profile/handoff/science-task-brief/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science or caller' --consumer 'science execution and validation' --payload-file <payload-file>` |
| DEEPSCI:SCIENCE-PACKAGE-CHECK | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/science-package-check/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:SCIENCE-PACKAGE-CHECK' --format-profile isomer:deepsci/record-format/profile/evidence/science-package-check/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'science run decision' --payload-file <payload-file>` |
| DEEPSCI:SCIENCE-RUN-RECORD | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `isomer:deepsci/record-format/profile/run/science-run-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind run --semantic-id 'DEEPSCI:SCIENCE-RUN-RECORD' --format-profile isomer:deepsci/record-format/profile/run/science-run-record/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'validation and claims' --payload-file <payload-file>` |
| DEEPSCI:SCIENCE-VALIDATION-RESULT | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/science-validation-result/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:SCIENCE-VALIDATION-RESULT' --format-profile isomer:deepsci/record-format/profile/evidence/science-validation-result/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'claim record and downstream analysis' --payload-file <payload-file>` |
| DEEPSCI:SCIENCE-CLAIM-RECORD | evidence | Evidence Item with an Artifact on-demand view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/science-claim-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-id 'DEEPSCI:SCIENCE-CLAIM-RECORD' --format-profile isomer:deepsci/record-format/profile/evidence/science-claim-record/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'experiment, analysis, decision, finalize' --payload-file <payload-file>` |
| DEEPSCI:SCIENCE-EVIDENCE-GRAPH-UPDATE | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/science-evidence-graph-update/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id 'DEEPSCI:SCIENCE-EVIDENCE-GRAPH-UPDATE' --format-profile isomer:deepsci/record-format/profile/control/science-evidence-graph-update/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'downstream research skills' --payload-file <payload-file>` |
| DEEPSCI:SCIENCE-BLOCKER-RECORD | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/science-blocker-record/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-id 'DEEPSCI:SCIENCE-BLOCKER-RECORD' --format-profile isomer:deepsci/record-format/profile/decision/science-blocker-record/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'caller or user' --payload-file <payload-file>` |
| DEEPSCI:SCIENCE-ROUTE-DECISION | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/science-route-decision/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-id 'DEEPSCI:SCIENCE-ROUTE-DECISION' --format-profile isomer:deepsci/record-format/profile/decision/science-route-decision/v2 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'any production DeepSci research skill' --payload-file <payload-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --semantic-id 'DEEPSCI:WHAT'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect one stored record, payload, and metadata.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --semantic-id 'DEEPSCI:WHAT' --payload-file <payload-file>` for status, metadata, or repair updates. Use `isomer-cli --print-json ext research records revise <record-id> --topic <topic> --payload-file <payload-file>` when accepted content changes and must remain visible as a new descendant revision.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves managed payload files by default.
