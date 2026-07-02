# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional accepted research artifact CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates an accepted research artifact record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <RSCH_WORKSPACE_CONTEXT> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.rsch-workspace-context` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<RSCH_WORKSPACE_CONTEXT>' --profile evidence.rsch-workspace-context --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'all v2 research skills and Topic Service Master fallback flows' --body-file <body-file>` |
| <RSCH_STORAGE_LABEL_PLAN> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.rsch-storage-label-plan` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<RSCH_STORAGE_LABEL_PLAN>' --profile control.rsch-storage-label-plan --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'all v2 research skills' --body-file <body-file>` |
| <RSCH_PLACEHOLDER_BINDING_REGISTRY> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.rsch-placeholder-binding-registry` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_PLACEHOLDER_BINDING_REGISTRY>' --profile report.rsch-placeholder-binding-registry --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'all v2 research skills, validators, and later storage-binding work' --body-file <body-file>` |
| <RSCH_PLACEHOLDER_BINDING_INDEX> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.rsch-placeholder-binding-index` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<RSCH_PLACEHOLDER_BINDING_INDEX>' --profile control.rsch-placeholder-binding-index --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'Topic Actors, formal agents, and all v2 research skills' --body-file <body-file>` |
| <RSCH_STORAGE_BOOTSTRAP_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.rsch-storage-bootstrap-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<RSCH_STORAGE_BOOTSTRAP_RECORD>' --profile evidence.rsch-storage-bootstrap-record --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2, Topic Service Master, Project Operator Session, or Operator Agent' --consumer 'all v2 research skills and future maintenance passes' --body-file <body-file>` |
| <RSCH_AGENT_ACCESS_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.rsch-agent-access-plan` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_AGENT_ACCESS_PLAN>' --profile handoff.rsch-agent-access-plan --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'Agent Team Instance members and v2 research skills' --body-file <body-file>` |
| <RSCH_BOOTSTRAP_VALIDATION_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.rsch-bootstrap-validation-report` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RSCH_BOOTSTRAP_VALIDATION_REPORT>' --profile report.rsch-bootstrap-validation-report --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'Topic Service Master, Project Operator Session, Operator Agent, and all v2 research skills' --body-file <body-file>` |
| <RSCH_WORKSPACE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.rsch-workspace-blocker-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<RSCH_WORKSPACE_BLOCKER_RECORD>' --profile decision.rsch-workspace-blocker-record --skill isomer-rsch-workspace-mgr-v2 --producer 'isomer-rsch-workspace-mgr-v2' --consumer 'setup services, Topic Service Master fallback, Operator Agent, or user' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
