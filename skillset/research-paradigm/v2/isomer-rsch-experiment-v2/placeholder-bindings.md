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
| code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `code` | Work in `topic.repos.main` or an Agent Workspace first, then promote durable code outputs into topic records. |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run` | Use Run records for commands, configs, logs, outputs, metrics, environment facts, and validation refs. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <EXPERIMENT_CONTEXT_BRIEF> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.experiment-context-brief` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<EXPERIMENT_CONTEXT_BRIEF>' --profile evidence.experiment-context-brief --skill isomer-rsch-experiment-v2 --producer 'idea, optimize, baseline, decision, or user context' --consumer 'isomer-rsch-experiment-v2' --body-file <body-file>` |
| <EXPERIMENT_CONTRACT> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.experiment-contract` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<EXPERIMENT_CONTRACT>' --profile handoff.experiment-contract --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'execution and validation' --body-file <body-file>` |
| <EXPERIMENT_PLAN> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.experiment-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<EXPERIMENT_PLAN>' --profile control.experiment-plan --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'execution and validation' --body-file <body-file>` |
| <EXPERIMENT_CHECKLIST> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.experiment-checklist` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<EXPERIMENT_CHECKLIST>' --profile control.experiment-checklist --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'execution and validation' --body-file <body-file>` |
| <IMPLEMENTATION_CHANGE_MAP> | code | Code Artifact or promoted Agent Workspace material | `artifact` | `topic.records.artifacts` | `code.implementation-change-map` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<IMPLEMENTATION_CHANGE_MAP>' --profile code.implementation-change-map --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'execution' --body-file <body-file>` |
| <SMOKE_CHECK_RECORD> | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run.smoke-check-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind run --placeholder '<SMOKE_CHECK_RECORD>' --profile run.smoke-check-record --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'real run decision' --body-file <body-file>` |
| <MAIN_RUN_RECORD> | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run.main-run-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind run --placeholder '<MAIN_RUN_RECORD>' --profile run.main-run-record --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'analysis, decision, optimize, finalize' --body-file <body-file>` |
| <EXPERIMENT_ARTIFACT_MANIFEST> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.experiment-artifact-manifest` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<EXPERIMENT_ARTIFACT_MANIFEST>' --profile evidence.experiment-artifact-manifest --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'analysis, decision, optimize, finalize' --body-file <body-file>` |
| <CLAIM_VALIDATION_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.claim-validation-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<CLAIM_VALIDATION_RECORD>' --profile evidence.claim-validation-record --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'analysis, write, decision, finalize' --body-file <body-file>` |
| <EXPERIMENT_RESULT_SUMMARY> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.experiment-result-summary` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<EXPERIMENT_RESULT_SUMMARY>' --profile evidence.experiment-result-summary --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'analysis, decision, optimize, finalize' --body-file <body-file>` |
| <EXPERIMENT_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.experiment-route-decision` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<EXPERIMENT_ROUTE_DECISION>' --profile decision.experiment-route-decision --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'analysis, optimize, decision, finalize, idea' --body-file <body-file>` |
| <EXPERIMENT_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.experiment-blocker-record` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<EXPERIMENT_BLOCKER_RECORD>' --profile decision.experiment-blocker-record --skill isomer-rsch-experiment-v2 --producer 'isomer-rsch-experiment-v2' --consumer 'user or decision' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
