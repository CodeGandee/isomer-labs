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
| <PAPER_CONTROL_STATE> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.paper-control-state` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<PAPER_CONTROL_STATE>' --profile control.paper-control-state --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'write, paper-outline, review, finalize' --body-file <body-file>` |
| <PAPER_CONTRACT> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.paper-contract` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PAPER_CONTRACT>' --profile handoff.paper-contract --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'write, review, finalize, nature companion skills' --body-file <body-file>` |
| <PAPER_OUTLINE> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.paper-outline` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PAPER_OUTLINE>' --profile handoff.paper-outline --skill isomer-rsch-write-v2 --producer 'isomer-rsch-paper-outline-v2 or write' --consumer 'write, review' --body-file <body-file>` |
| <WRITING_PLAN> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.writing-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<WRITING_PLAN>' --profile report.writing-plan --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'write' --body-file <body-file>` |
| <SOURCE_MATERIAL_LEDGER> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.source-material-ledger` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SOURCE_MATERIAL_LEDGER>' --profile evidence.source-material-ledger --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'write, review, rebuttal' --body-file <body-file>` |
| <CITATION_LEDGER> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.citation-ledger` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<CITATION_LEDGER>' --profile evidence.citation-ledger --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'write, review, finalize' --body-file <body-file>` |
| <DISPLAY_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.display-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<DISPLAY_PLAN>' --profile handoff.display-plan --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'paper-plot, figure-polish, review' --body-file <body-file>` |
| <DRAFT_SECTION_SET> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.draft-section-set` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<DRAFT_SECTION_SET>' --profile draft.draft-section-set --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'review, finalize, rebuttal' --body-file <body-file>` |
| <MANUSCRIPT_VALIDATION_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.manuscript-validation-report` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<MANUSCRIPT_VALIDATION_REPORT>' --profile report.manuscript-validation-report --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'review, finalize, decision' --body-file <body-file>` |
| <PAPER_BUNDLE_CHECKPOINT> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.paper-bundle-checkpoint` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PAPER_BUNDLE_CHECKPOINT>' --profile handoff.paper-bundle-checkpoint --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'review, finalize, user' --body-file <body-file>` |
| <WRITING_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.writing-route-decision` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<WRITING_ROUTE_DECISION>' --profile decision.writing-route-decision --skill isomer-rsch-write-v2 --producer 'isomer-rsch-write-v2' --consumer 'any selected v2 skill' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
