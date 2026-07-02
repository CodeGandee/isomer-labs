# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, structured payload, generated view, or queryable ref.

Use `isomer-cli ext research records` as the current transitional accepted research artifact CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates an accepted research artifact record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Payload-first structured record flow

For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create or update the record with `--payload-file <payload-file> --render markdown`. The generated Markdown view is review material; update the JSON payload and rerender rather than editing generated Markdown as the source of truth.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, format profile ref, payload file role, and generated view naming metadata on created records.
- Resolve generated view locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the generated Markdown view or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <RSCH_WORKSPACE_CONTEXT> | evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/rsch-workspace-context/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<RSCH_WORKSPACE_CONTEXT>' --format-profile isomer:deepsci/record-format/profile/evidence/rsch-workspace-context/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'all v2 research skills and Topic Service Master fallback flows' --payload-file <payload-file> --render markdown --content-name rsch-workspace-context.md` |
| <RSCH_STORAGE_LABEL_PLAN> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/rsch-storage-label-plan/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<RSCH_STORAGE_LABEL_PLAN>' --format-profile isomer:deepsci/record-format/profile/control/rsch-storage-label-plan/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'all v2 research skills' --payload-file <payload-file> --render markdown --content-name rsch-storage-label-plan.md` |
| <RSCH_PLACEHOLDER_BINDING_REGISTRY> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/rsch-placeholder-binding-registry/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_PLACEHOLDER_BINDING_REGISTRY>' --format-profile isomer:deepsci/record-format/profile/report/rsch-placeholder-binding-registry/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'all v2 research skills, validators, and later storage-binding work' --payload-file <payload-file> --render markdown --content-name rsch-placeholder-binding-registry.md` |
| <RSCH_PLACEHOLDER_BINDING_INDEX> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/rsch-placeholder-binding-index/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<RSCH_PLACEHOLDER_BINDING_INDEX>' --format-profile isomer:deepsci/record-format/profile/control/rsch-placeholder-binding-index/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'Topic Actors, formal agents, and all v2 research skills' --payload-file <payload-file> --render markdown --content-name rsch-placeholder-binding-index.md` |
| <RSCH_STORAGE_BOOTSTRAP_RECORD> | evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/rsch-storage-bootstrap-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<RSCH_STORAGE_BOOTSTRAP_RECORD>' --format-profile isomer:deepsci/record-format/profile/evidence/rsch-storage-bootstrap-record/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2, Topic Service Master, Project Operator Session, or Operator Agent' --consumer 'all v2 research skills and future maintenance passes' --payload-file <payload-file> --render markdown --content-name rsch-storage-bootstrap-record.md` |
| <RSCH_AGENT_ACCESS_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/handoff/rsch-agent-access-plan/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_AGENT_ACCESS_PLAN>' --format-profile isomer:deepsci/record-format/profile/handoff/rsch-agent-access-plan/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'Agent Team Instance members and v2 research skills' --payload-file <payload-file> --render markdown --content-name rsch-agent-access-plan.md` |
| <RSCH_BOOTSTRAP_VALIDATION_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/rsch-bootstrap-validation-report/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_BOOTSTRAP_VALIDATION_REPORT>' --format-profile isomer:deepsci/record-format/profile/report/rsch-bootstrap-validation-report/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'Topic Service Master, Project Operator Session, Operator Agent, and all v2 research skills' --payload-file <payload-file> --render markdown --content-name rsch-bootstrap-validation-report.md` |
| <RSCH_WORKSPACE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/rsch-workspace-blocker-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<RSCH_WORKSPACE_BLOCKER_RECORD>' --format-profile isomer:deepsci/record-format/profile/decision/rsch-workspace-blocker-record/v1 --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'setup services, Topic Service Master fallback, Operator Agent, or user' --payload-file <payload-file> --render markdown --content-name rsch-workspace-blocker-record.md` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` to inspect one stored record, payload, and generated view when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file> --render markdown` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves generated view files by default.
