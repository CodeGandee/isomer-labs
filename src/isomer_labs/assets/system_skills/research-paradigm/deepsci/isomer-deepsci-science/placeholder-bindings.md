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
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `run` | Use Run records for commands, configs, logs, outputs, metrics, environment facts, and validation refs. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <SCIENCE_TASK_BRIEF> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/handoff/science-task-brief/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<SCIENCE_TASK_BRIEF>' --format-profile isomer:deepsci/record-format/profile/handoff/science-task-brief/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science or caller' --consumer 'science execution and validation' --payload-file <payload-file> --render markdown --content-name science-task-brief.md` |
| <SCIENCE_PACKAGE_CHECK> | evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/science-package-check/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCIENCE_PACKAGE_CHECK>' --format-profile isomer:deepsci/record-format/profile/evidence/science-package-check/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'science run decision' --payload-file <payload-file> --render markdown --content-name science-package-check.md` |
| <SCIENCE_RUN_RECORD> | run record | Run record with optional Artifact or Evidence links | `run` | `topic.records.runs` | `isomer:deepsci/record-format/profile/run/science-run-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind run --placeholder '<SCIENCE_RUN_RECORD>' --format-profile isomer:deepsci/record-format/profile/run/science-run-record/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'validation and claims' --payload-file <payload-file> --render markdown --content-name science-run-record.md` |
| <SCIENCE_VALIDATION_RESULT> | evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/science-validation-result/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCIENCE_VALIDATION_RESULT>' --format-profile isomer:deepsci/record-format/profile/evidence/science-validation-result/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'claim record and downstream analysis' --payload-file <payload-file> --render markdown --content-name science-validation-result.md` |
| <SCIENCE_CLAIM_RECORD> | evidence | Evidence Item with an Artifact generated view when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/science-claim-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCIENCE_CLAIM_RECORD>' --format-profile isomer:deepsci/record-format/profile/evidence/science-claim-record/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'experiment, analysis, decision, finalize' --payload-file <payload-file> --render markdown --content-name science-claim-record.md` |
| <SCIENCE_EVIDENCE_GRAPH_UPDATE> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/science-evidence-graph-update/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<SCIENCE_EVIDENCE_GRAPH_UPDATE>' --format-profile isomer:deepsci/record-format/profile/control/science-evidence-graph-update/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'downstream research skills' --payload-file <payload-file> --render markdown --content-name science-evidence-graph-update.md` |
| <SCIENCE_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/science-blocker-record/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<SCIENCE_BLOCKER_RECORD>' --format-profile isomer:deepsci/record-format/profile/decision/science-blocker-record/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'caller or user' --payload-file <payload-file> --render markdown --content-name science-blocker-record.md` |
| <SCIENCE_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/decision/science-route-decision/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<SCIENCE_ROUTE_DECISION>' --format-profile isomer:deepsci/record-format/profile/decision/science-route-decision/v1 --skill isomer-deepsci-science --producer 'isomer-deepsci-science' --consumer 'any production DeepSci research skill' --payload-file <payload-file> --render markdown --content-name science-route-decision.md` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body` to inspect one stored record, payload, and generated view when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --payload-file <payload-file> --render markdown` when the same semantic record receives a revised payload or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves generated view files by default.
