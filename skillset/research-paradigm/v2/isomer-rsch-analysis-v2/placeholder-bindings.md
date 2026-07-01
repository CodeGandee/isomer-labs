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
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <ANALYSIS_CONTEXT_BRIEF> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.analysis-context-brief` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<ANALYSIS_CONTEXT_BRIEF>' --profile evidence.analysis-context-brief --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'analysis slices and route decision' --body-file <body-file>` |
| <PARENT_RESULT_EVIDENCE> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.parent-result-evidence` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<PARENT_RESULT_EVIDENCE>' --profile evidence.parent-result-evidence --skill isomer-rsch-analysis-v2 --producer 'experiment, write, review, decision, or user context' --consumer 'isomer-rsch-analysis-v2' --body-file <body-file>` |
| <ANALYSIS_RESOURCE_ENVELOPE> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.analysis-resource-envelope` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<ANALYSIS_RESOURCE_ENVELOPE>' --profile control.analysis-resource-envelope --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'campaign design and execution' --body-file <body-file>` |
| <ANALYSIS_CAMPAIGN_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.analysis-campaign-plan` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<ANALYSIS_CAMPAIGN_PLAN>' --profile handoff.analysis-campaign-plan --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'slice execution and downstream decision' --body-file <body-file>` |
| <ANALYSIS_CAMPAIGN_CHECKLIST> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.analysis-campaign-checklist` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<ANALYSIS_CAMPAIGN_CHECKLIST>' --profile control.analysis-campaign-checklist --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'campaign validation' --body-file <body-file>` |
| <ANALYSIS_SLICE_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.analysis-slice-plan` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<ANALYSIS_SLICE_PLAN>' --profile handoff.analysis-slice-plan --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'slice execution' --body-file <body-file>` |
| <ANALYSIS_SLICE_RECORD> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.analysis-slice-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<ANALYSIS_SLICE_RECORD>' --profile evidence.analysis-slice-record --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'campaign summary and downstream decision' --body-file <body-file>` |
| <ANALYSIS_WRITEBACK_MAP> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.analysis-writeback-map` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<ANALYSIS_WRITEBACK_MAP>' --profile handoff.analysis-writeback-map --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'write, review, rebuttal, decision, finalize' --body-file <body-file>` |
| <ANALYSIS_CAMPAIGN_SUMMARY> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.analysis-campaign-summary` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<ANALYSIS_CAMPAIGN_SUMMARY>' --profile report.analysis-campaign-summary --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'decision, finalize, write, experiment, idea' --body-file <body-file>` |
| <ANALYSIS_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.analysis-route-decision` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<ANALYSIS_ROUTE_DECISION>' --profile decision.analysis-route-decision --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'any v2 research skill' --body-file <body-file>` |
| <ANALYSIS_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.analysis-blocker-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<ANALYSIS_BLOCKER_RECORD>' --profile decision.analysis-blocker-record --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'user, decision, or continued analysis' --body-file <body-file>` |
| <ANALYSIS_CONTINUITY_UPDATE> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.analysis-continuity-update` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<ANALYSIS_CONTINUITY_UPDATE>' --profile control.analysis-continuity-update --skill isomer-rsch-analysis-v2 --producer 'isomer-rsch-analysis-v2' --consumer 'future research work' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
