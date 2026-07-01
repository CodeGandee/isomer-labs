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
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <PAPER_STATE_SNAPSHOT> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.paper-state-snapshot` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<PAPER_STATE_SNAPSHOT>' --profile control.paper-state-snapshot --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'paper-outline, write' --body-file <body-file>` |
| <ONE_SENTENCE_PAPER_IDEA> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.one-sentence-paper-idea` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<ONE_SENTENCE_PAPER_IDEA>' --profile draft.one-sentence-paper-idea --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'paper-outline, write, review' --body-file <body-file>` |
| <CLAIM_EVIDENCE_BOUNDARY> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.claim-evidence-boundary` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<CLAIM_EVIDENCE_BOUNDARY>' --profile evidence.claim-evidence-boundary --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write, review, rebuttal' --body-file <body-file>` |
| <PAPER_VIEW> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.paper-view` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PAPER_VIEW>' --profile handoff.paper-view --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write, review' --body-file <body-file>` |
| <EVIDENCE_VIEW> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.evidence-view` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<EVIDENCE_VIEW>' --profile evidence.evidence-view --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write, review, finalize' --body-file <body-file>` |
| <OUTLINE_VALIDATION_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.outline-validation-report` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<OUTLINE_VALIDATION_REPORT>' --profile report.outline-validation-report --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'paper-outline, write, decision' --body-file <body-file>` |
| <SECTION_WRITING_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.section-writing-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<SECTION_WRITING_PLAN>' --profile handoff.section-writing-plan --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write' --body-file <body-file>` |
| <PAPER_OUTLINE_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.paper-outline-route-decision` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<PAPER_OUTLINE_ROUTE_DECISION>' --profile decision.paper-outline-route-decision --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'analysis, decision, write' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
