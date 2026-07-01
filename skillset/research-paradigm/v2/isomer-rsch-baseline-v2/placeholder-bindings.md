# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

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
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <BASELINE_CONTEXT_BRIEF> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.baseline-context-brief` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<BASELINE_CONTEXT_BRIEF>' --profile evidence.baseline-context-brief --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'route selection' --body-file <body-file>` |
| <COMPARATOR_ROUTE_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.comparator-route-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<COMPARATOR_ROUTE_RECORD>' --profile decision.comparator-route-record --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'verification' --body-file <body-file>` |
| <BASELINE_ROUTE_PLAN> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.baseline-route-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<BASELINE_ROUTE_PLAN>' --profile control.baseline-route-plan --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'verification and closeout' --body-file <body-file>` |
| <BASELINE_GATE_CHECKLIST> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.baseline-gate-checklist` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<BASELINE_GATE_CHECKLIST>' --profile control.baseline-gate-checklist --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'verification and closeout' --body-file <body-file>` |
| <COMPARABILITY_CONTRACT> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.comparability-contract` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<COMPARABILITY_CONTRACT>' --profile handoff.comparability-contract --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'idea, experiment, analysis, decision' --body-file <body-file>` |
| <CODEBASE_AUDIT_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.codebase-audit-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<CODEBASE_AUDIT_RECORD>' --profile evidence.codebase-audit-record --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'reproduce, repair, verification' --body-file <body-file>` |
| <BASELINE_PROVENANCE_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.baseline-provenance-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<BASELINE_PROVENANCE_RECORD>' --profile evidence.baseline-provenance-record --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'verification and acceptance' --body-file <body-file>` |
| <BASELINE_VERIFICATION_EVIDENCE> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.baseline-verification-evidence` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<BASELINE_VERIFICATION_EVIDENCE>' --profile evidence.baseline-verification-evidence --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'accepted baseline or blocker' --body-file <body-file>` |
| <BASELINE_PAYLOAD_RECORD> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.baseline-payload-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<BASELINE_PAYLOAD_RECORD>' --profile handoff.baseline-payload-record --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'downstream v2 research skills' --body-file <body-file>` |
| <ACCEPTED_BASELINE_RECORD> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.accepted-baseline-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<ACCEPTED_BASELINE_RECORD>' --profile handoff.accepted-baseline-record --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'idea, experiment, analysis, decision' --body-file <body-file>` |
| <BASELINE_WAIVER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.baseline-waiver-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<BASELINE_WAIVER_RECORD>' --profile decision.baseline-waiver-record --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2 or decision' --consumer 'idea, experiment, decision' --body-file <body-file>` |
| <BASELINE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.baseline-blocker-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<BASELINE_BLOCKER_RECORD>' --profile decision.baseline-blocker-record --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'user or decision' --body-file <body-file>` |
| <BASELINE_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.baseline-route-decision` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<BASELINE_ROUTE_DECISION>' --profile decision.baseline-route-decision --skill isomer-rsch-baseline-v2 --producer 'isomer-rsch-baseline-v2' --consumer 'any v2 research skill' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
