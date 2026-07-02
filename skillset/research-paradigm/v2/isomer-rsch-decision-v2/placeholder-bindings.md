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
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then status the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the generated Markdown view or source summary through the resolved topic records label. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <DECISION_CONTEXT_BRIEF> | evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/decision-context-brief/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<DECISION_CONTEXT_BRIEF>' --format-profile isomer:deepsci/record-format/profile/evidence/decision-context-brief/v1 --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'route judgment' --payload-file <payload-file> --render markdown --content-name decision-context-brief.md` |
| <ROUTE_QUESTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/route-question/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<ROUTE_QUESTION>' --format-profile isomer:deepsci/record-format/profile/decision/route-question/v1 --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'decision evidence packet' --payload-file <payload-file> --render markdown --content-name route-question.md` |
| <DECISION_EVIDENCE_PACKET> | evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/decision-evidence-packet/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<DECISION_EVIDENCE_PACKET>' --format-profile isomer:deepsci/record-format/profile/evidence/decision-evidence-packet/v1 --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'route decision record' --payload-file <payload-file> --render markdown --content-name decision-evidence-packet.md` |
| <ROUTE_DECISION_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/route-decision-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<ROUTE_DECISION_RECORD>' --format-profile isomer:deepsci/record-format/profile/decision/route-decision-record/v1 --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'any v2 research skill' --payload-file <payload-file> --render markdown --content-name route-decision-record.md` |
| <DECISION_CHECKPOINT_MEMORY> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/decision-checkpoint-memory/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<DECISION_CHECKPOINT_MEMORY>' --format-profile isomer:deepsci/record-format/profile/control/decision-checkpoint-memory/v1 --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'future work' --payload-file <payload-file> --render markdown --content-name decision-checkpoint-memory.md` |
| <USER_DECISION_REQUEST> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/user-decision-request/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<USER_DECISION_REQUEST>' --format-profile isomer:deepsci/record-format/profile/decision/user-decision-request/v1 --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'user' --payload-file <payload-file> --render markdown --content-name user-decision-request.md` |
| <DECISION_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/decision-blocker-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<DECISION_BLOCKER_RECORD>' --format-profile isomer:deepsci/record-format/profile/decision/decision-blocker-record/v1 --skill isomer-rsch-decision-v2 --producer 'isomer-rsch-decision-v2' --consumer 'user or continued decision work' --payload-file <payload-file> --render markdown --content-name decision-blocker-record.md` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` to inspect one stored record, payload, and generated view when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file> --render markdown` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves generated view files by default.
