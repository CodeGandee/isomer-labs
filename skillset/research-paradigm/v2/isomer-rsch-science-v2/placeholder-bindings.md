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
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run` | Use Run records for commands, configs, logs, outputs, metrics, environment facts, and validation refs. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <SCIENCE_TASK_BRIEF> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.science-task-brief` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<SCIENCE_TASK_BRIEF>' --profile handoff.science-task-brief --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2 or caller' --consumer 'science execution and validation' --body-file <body-file>` |
| <SCIENCE_PACKAGE_CHECK> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.science-package-check` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCIENCE_PACKAGE_CHECK>' --profile evidence.science-package-check --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2' --consumer 'science run decision' --body-file <body-file>` |
| <SCIENCE_RUN_RECORD> | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run.science-run-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind run --placeholder '<SCIENCE_RUN_RECORD>' --profile run.science-run-record --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2' --consumer 'validation and claims' --body-file <body-file>` |
| <SCIENCE_VALIDATION_RESULT> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.science-validation-result` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCIENCE_VALIDATION_RESULT>' --profile evidence.science-validation-result --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2' --consumer 'claim record and downstream analysis' --body-file <body-file>` |
| <SCIENCE_CLAIM_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.science-claim-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCIENCE_CLAIM_RECORD>' --profile evidence.science-claim-record --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2' --consumer 'experiment, analysis, decision, finalize' --body-file <body-file>` |
| <SCIENCE_EVIDENCE_GRAPH_UPDATE> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.science-evidence-graph-update` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<SCIENCE_EVIDENCE_GRAPH_UPDATE>' --profile control.science-evidence-graph-update --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2' --consumer 'downstream research skills' --body-file <body-file>` |
| <SCIENCE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.science-blocker-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<SCIENCE_BLOCKER_RECORD>' --profile decision.science-blocker-record --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2' --consumer 'caller or user' --body-file <body-file>` |
| <SCIENCE_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.science-route-decision` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<SCIENCE_ROUTE_DECISION>' --profile decision.science-route-decision --skill isomer-rsch-science-v2 --producer 'isomer-rsch-science-v2' --consumer 'any v2 research skill' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
