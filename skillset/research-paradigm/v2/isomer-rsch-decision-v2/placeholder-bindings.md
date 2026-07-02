# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

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
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <DECISION_CONTEXT_BRIEF> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.decision-context-brief` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<DECISION_CONTEXT_BRIEF>' --profile evidence.decision-context-brief --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'route judgment' --body-file <body-file>` |
| <ROUTE_QUESTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.route-question` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<ROUTE_QUESTION>' --profile decision.route-question --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'decision evidence packet' --body-file <body-file>` |
| <DECISION_EVIDENCE_PACKET> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.decision-evidence-packet` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<DECISION_EVIDENCE_PACKET>' --profile evidence.decision-evidence-packet --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'route decision record' --body-file <body-file>` |
| <ROUTE_DECISION_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.route-decision-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<ROUTE_DECISION_RECORD>' --profile decision.route-decision-record --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'any v2 research skill' --body-file <body-file>` |
| <DECISION_CHECKPOINT_MEMORY> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.decision-checkpoint-memory` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<DECISION_CHECKPOINT_MEMORY>' --profile control.decision-checkpoint-memory --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'future work' --body-file <body-file>` |
| <USER_DECISION_REQUEST> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.user-decision-request` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<USER_DECISION_REQUEST>' --profile decision.user-decision-request --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'user' --body-file <body-file>` |
| <DECISION_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.decision-blocker-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<DECISION_BLOCKER_RECORD>' --profile decision.decision-blocker-record --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'user or continued decision work' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
