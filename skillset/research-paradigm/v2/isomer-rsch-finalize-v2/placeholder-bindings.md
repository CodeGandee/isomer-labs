# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then summarize the durable meaning through the binding row here.

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
| <FINALIZE_CONTEXT_BRIEF> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.finalize-context-brief` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<FINALIZE_CONTEXT_BRIEF>' --profile evidence.finalize-context-brief --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2' --consumer 'closure gate' --body-file <body-file>` |
| <CLAIM_LEDGER> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.claim-ledger` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<CLAIM_LEDGER>' --profile report.claim-ledger --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2' --consumer 'final summary, writing, archive' --body-file <body-file>` |
| <FINAL_LIMITATIONS_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.final-limitations-report` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FINAL_LIMITATIONS_REPORT>' --profile report.final-limitations-report --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2' --consumer 'final summary and user' --body-file <body-file>` |
| <FINAL_SUMMARY> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.final-summary` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FINAL_SUMMARY>' --profile report.final-summary --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2' --consumer 'user and future work' --body-file <body-file>` |
| <RESUME_PACKET> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.resume-packet` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RESUME_PACKET>' --profile handoff.resume-packet --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2' --consumer 'future work' --body-file <body-file>` |
| <CLOSURE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.closure-decision` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<CLOSURE_DECISION>' --profile decision.closure-decision --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2 or decision' --consumer 'user and future work' --body-file <body-file>` |
| <FINALIZE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.finalize-blocker-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<FINALIZE_BLOCKER_RECORD>' --profile decision.finalize-blocker-record --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2' --consumer 'decision or upstream skill' --body-file <body-file>` |
| <FINALIZE_CONTINUITY_UPDATE> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.finalize-continuity-update` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<FINALIZE_CONTINUITY_UPDATE>' --profile control.finalize-continuity-update --skill isomer-rsch-finalize-v2 --producer 'isomer-rsch-finalize-v2' --consumer 'future work' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
