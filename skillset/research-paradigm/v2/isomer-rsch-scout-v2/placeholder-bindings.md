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
| <SCOUT_CONTEXT_BRIEF> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.scout-context-brief` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_CONTEXT_BRIEF>' --profile evidence.scout-context-brief --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2` from user context, Workspace Runtime records, Artifacts, Findings, Evidence Items, and Decision Records.' --consumer 'isomer-rsch-scout-v2`, `isomer-rsch-baseline-v2`, `isomer-rsch-idea-v2`, `isomer-rsch-decision-v2`.' --body-file <body-file>` |
| <SCOUT_MEMORY_REUSE_NOTE> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.scout-memory-reuse-note` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_MEMORY_REUSE_NOTE>' --profile evidence.scout-memory-reuse-note --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2` through compatibility memory or Workspace Runtime-backed retrieval.' --consumer 'isomer-rsch-scout-v2` unknown selection and discovery narrowing.' --body-file <body-file>` |
| <SCOUT_MINIMUM_UNKNOWNS> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.scout-minimum-unknowns` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<SCOUT_MINIMUM_UNKNOWNS>' --profile report.scout-minimum-unknowns --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2`.' --consumer 'isomer-rsch-scout-v2`, literature discovery, evaluation contract drafting, baseline shortlist drafting.' --body-file <body-file>` |
| <SCOUT_DISCOVERY_LEDGER> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.scout-discovery-ledger` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_DISCOVERY_LEDGER>' --profile evidence.scout-discovery-ledger --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2` through Literature Provider Binding, repository inspection, and compatibility artifact calls.' --consumer '<LITERATURE_SCOUTING_REPORT>`, `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, `<NEXT_ROUTE_DECISION>`.' --body-file <body-file>` |
| <LITERATURE_SCOUTING_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.literature-scouting-report` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<LITERATURE_SCOUTING_REPORT>' --profile report.literature-scouting-report --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2`.' --consumer 'isomer-rsch-baseline-v2`, `isomer-rsch-idea-v2`, `isomer-rsch-decision-v2`, future scout passes.' --body-file <body-file>` |
| <EVALUATION_CONTRACT> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.evaluation-contract` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<EVALUATION_CONTRACT>' --profile handoff.evaluation-contract --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2`, later refined by `isomer-rsch-baseline-v2` or `isomer-rsch-experiment-v2`.' --consumer 'isomer-rsch-baseline-v2`, `isomer-rsch-idea-v2`, `isomer-rsch-experiment-v2`, `isomer-rsch-analysis-v2`.' --body-file <body-file>` |
| <BASELINE_SHORTLIST> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.baseline-shortlist` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<BASELINE_SHORTLIST>' --profile handoff.baseline-shortlist --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2`.' --consumer 'isomer-rsch-baseline-v2`, `isomer-rsch-idea-v2`, `isomer-rsch-decision-v2`.' --body-file <body-file>` |
| <NEXT_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.next-route-decision` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<NEXT_ROUTE_DECISION>' --profile decision.next-route-decision --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2` or `isomer-rsch-decision-v2`.' --consumer 'Any v2 research skill selected as the next route.' --body-file <body-file>` |
| <SCOUT_BLOCKER_RECORD> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.scout-blocker-record` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<SCOUT_BLOCKER_RECORD>' --profile decision.scout-blocker-record --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2`.' --consumer 'User, Operator Agent, `isomer-rsch-decision-v2`, or continued `isomer-rsch-scout-v2`.' --body-file <body-file>` |
| <SCOUT_CONTINUITY_UPDATE> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.scout-continuity-update` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<SCOUT_CONTINUITY_UPDATE>' --profile control.scout-continuity-update --skill isomer-rsch-scout-v2 --producer 'isomer-rsch-scout-v2`.' --consumer 'Future scout, baseline, idea, experiment, analysis, decision, and finalize work.' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
