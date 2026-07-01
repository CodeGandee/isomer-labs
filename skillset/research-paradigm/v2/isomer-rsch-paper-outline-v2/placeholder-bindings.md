# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line outputs, use paper-specific profiles such as `paper.line-state`, `paper.outline.idea`, `paper.claim-evidence-map`, `paper.contract.evidence-view`, `paper.validation.academic-outline`, and `paper.writing-plan` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then summarize the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| research task | Research Task for resumable paper-writing work | `research_task` | `topic.records.tasks` | `paper` | Use this when a writing plan or reviewer-facing TODO must be resumed, assigned, or queried as work. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <PAPER_STATE_SNAPSHOT> | runtime state | View Manifest for active paper-line state | `view_manifest` | `topic.records.views` | `paper.line-state` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<PAPER_STATE_SNAPSHOT>' --profile paper.line-state --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'paper-outline, write' --body-file <body-file> --content-name paper-state-snapshot.json --metadata-json '{"paper_surface":"state_snapshot"}'` |
| <ONE_SENTENCE_PAPER_IDEA> | draft | Paper outline Artifact body | `artifact` | `topic.records.artifacts` | `paper.outline.idea` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<ONE_SENTENCE_PAPER_IDEA>' --profile paper.outline.idea --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'paper-outline, write, review' --body-file <body-file> --content-name one-sentence-paper-idea.md --metadata-json '{"paper_surface":"outline_idea"}'` |
| <CLAIM_EVIDENCE_BOUNDARY> | evidence | Claim-evidence map View Manifest | `view_manifest` | `topic.records.views` | `paper.claim-evidence-map` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<CLAIM_EVIDENCE_BOUNDARY>' --profile paper.claim-evidence-map --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write, review, rebuttal' --body-file <body-file> --content-name claim-evidence-boundary.json --metadata-json '{"paper_surface":"claim_evidence_boundary"}'` |
| <PAPER_VIEW> | handoff | Paper-view Artifact body for the selected outline contract | `artifact` | `topic.records.artifacts` | `paper.outline.paper-view` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PAPER_VIEW>' --profile paper.outline.paper-view --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write, review' --body-file <body-file> --content-name paper-view.json --metadata-json '{"paper_surface":"paper_view"}'` |
| <EVIDENCE_VIEW> | evidence | Evidence-view View Manifest for the selected outline contract | `view_manifest` | `topic.records.views` | `paper.contract.evidence-view` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<EVIDENCE_VIEW>' --profile paper.contract.evidence-view --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write, review, finalize' --body-file <body-file> --content-name evidence-view.json --metadata-json '{"paper_surface":"evidence_view"}'` |
| <OUTLINE_VALIDATION_REPORT> | report | Academic outline validation View Manifest | `view_manifest` | `topic.records.views` | `paper.validation.academic-outline` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<OUTLINE_VALIDATION_REPORT>' --profile paper.validation.academic-outline --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'paper-outline, write, decision' --body-file <body-file> --content-name academic-outline-validation.json --metadata-json '{"paper_surface":"outline_validation"}'` |
| <SECTION_WRITING_PLAN> | research task | Research Task for section-level writing jobs | `research_task` | `topic.records.tasks` | `paper.writing-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind research_task --semantic-label topic.records.tasks --placeholder '<SECTION_WRITING_PLAN>' --profile paper.writing-plan --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'write' --body-file <body-file> --content-name section-writing-plan.json --metadata-json '{"paper_surface":"writing_plan"}'` |
| <PAPER_OUTLINE_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.paper-outline-route-decision` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PAPER_OUTLINE_ROUTE_DECISION>' --profile decision.paper-outline-route-decision --skill isomer-rsch-paper-outline-v2 --producer 'isomer-rsch-paper-outline-v2' --consumer 'analysis, decision, write' --body-file <body-file> --metadata-json '{"paper_surface":"outline_route_decision"}'` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
