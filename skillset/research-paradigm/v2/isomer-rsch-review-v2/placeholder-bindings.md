# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line outputs, use paper-specific profiles such as `review.report`, `review.revision-log`, `review.experiment-todo`, `paper.experiment-matrix`, and `paper.validation.*` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then summarize the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| research task | Research Task for resumable paper-writing work | `research_task` | `topic.records.tasks` | `review` | Use this when a review-generated TODO must be resumed, assigned, or queried as work. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <REVIEW_AUDIT_PLAN> | report | Review audit-plan Artifact | `artifact` | `topic.records.artifacts` | `review.audit-plan` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<REVIEW_AUDIT_PLAN>' --profile review.audit-plan --skill isomer-rsch-review-v2 --producer 'isomer-rsch-review-v2' --consumer 'review' --body-file <body-file> --content-name review-audit-plan.md --metadata-json '{"paper_surface":"review_audit_plan"}'` |
| <LITERATURE_BENCHMARK_NOTE> | evidence | Literature benchmark Evidence Item | `evidence_item` | `topic.records.artifacts` | `review.literature-benchmark-note` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<LITERATURE_BENCHMARK_NOTE>' --profile review.literature-benchmark-note --skill isomer-rsch-review-v2 --producer 'isomer-rsch-review-v2' --consumer 'review, scout, write' --body-file <body-file> --content-name literature-benchmark-note.md --metadata-json '{"paper_surface":"literature_benchmark_note"}'` |
| <REVIEW_REPORT> | report | Review report Artifact | `artifact` | `topic.records.artifacts` | `review.report` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<REVIEW_REPORT>' --profile review.report --skill isomer-rsch-review-v2 --producer 'isomer-rsch-review-v2' --consumer 'write, rebuttal, finalize' --body-file <body-file> --content-name review-report.md --metadata-json '{"paper_surface":"review_report"}'` |
| <REVISION_LOG> | handoff | Revision log Artifact | `artifact` | `topic.records.artifacts` | `review.revision-log` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<REVISION_LOG>' --profile review.revision-log --skill isomer-rsch-review-v2 --producer 'isomer-rsch-review-v2' --consumer 'write, analysis, decision' --body-file <body-file> --content-name revision-log.md --metadata-json '{"paper_surface":"revision_log"}'` |
| <REVIEW_EXPERIMENT_TODO> | research task | Research Task for review-requested experiment work | `research_task` | `topic.records.tasks` | `review.experiment-todo` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind research_task --semantic-label topic.records.tasks --placeholder '<REVIEW_EXPERIMENT_TODO>' --profile review.experiment-todo --skill isomer-rsch-review-v2 --producer 'isomer-rsch-review-v2' --consumer 'analysis, experiment, decision' --body-file <body-file> --content-name review-experiment-todo.json --metadata-json '{"paper_surface":"review_experiment_todo"}'` |
| <PAPER_EXPERIMENT_MATRIX_UPDATE> | runtime state | Paper experiment-matrix View Manifest | `view_manifest` | `topic.records.views` | `paper.experiment-matrix` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-label topic.records.views --placeholder '<PAPER_EXPERIMENT_MATRIX_UPDATE>' --profile paper.experiment-matrix --skill isomer-rsch-review-v2 --producer 'isomer-rsch-review-v2' --consumer 'write, analysis, rebuttal' --body-file <body-file> --content-name paper-experiment-matrix-update.json --metadata-json '{"paper_surface":"experiment_matrix_update"}'` |
| <REVIEW_ROUTE_DECISION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.review-route-decision` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<REVIEW_ROUTE_DECISION>' --profile decision.review-route-decision --skill isomer-rsch-review-v2 --producer 'isomer-rsch-review-v2' --consumer 'any selected v2 skill' --body-file <body-file> --metadata-json '{"paper_surface":"review_route_decision"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
