# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line outputs, use paper-specific profiles such as `rebuttal.reviewer-item-matrix`, `rebuttal.action-plan`, `rebuttal.reviewer-linked-evidence-todo`, `rebuttal.response-letter`, and `package.paper.revision-handoff-bundle` on existing generic semantic labels; do not add paper-specific top-level labels.
- Use `isomer-cli ext deepsci call ...` only for source-shaped compatibility behavior, then summarize the durable meaning through the binding row here.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision` | Record route choices, blockers, waivers, and closure decisions as Decision Records with linked evidence when available. |
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| research task | Research Task for resumable paper-writing work | `research_task` | `topic.records.tasks` | `rebuttal` | Use this when a reviewer-linked TODO must be resumed, assigned, or queried as work. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <REVIEW_PACKAGE_NORMALIZATION> | evidence | Review package normalization Evidence Item | `evidence_item` | `topic.records.artifacts` | `rebuttal.review-package-normalization` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<REVIEW_PACKAGE_NORMALIZATION>' --profile rebuttal.review-package-normalization --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'rebuttal' --body-file <body-file> --content-name review-package-normalization.md --metadata-json '{"paper_surface":"review_package_normalization"}'` |
| <REVIEWER_ITEM_MATRIX> | handoff | Reviewer item matrix Artifact | `artifact` | `topic.records.artifacts` | `rebuttal.reviewer-item-matrix` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<REVIEWER_ITEM_MATRIX>' --profile rebuttal.reviewer-item-matrix --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'rebuttal, analysis, write' --body-file <body-file> --content-name reviewer-item-matrix.json --metadata-json '{"paper_surface":"reviewer_item_matrix"}'` |
| <REBUTTAL_ACTION_PLAN> | handoff | Rebuttal action-plan Artifact | `artifact` | `topic.records.artifacts` | `rebuttal.action-plan` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<REBUTTAL_ACTION_PLAN>' --profile rebuttal.action-plan --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'analysis, write, scout, baseline' --body-file <body-file> --content-name rebuttal-action-plan.json --metadata-json '{"paper_surface":"rebuttal_action_plan"}'` |
| <REVIEWER_LINKED_EVIDENCE_TODO> | research task | Research Task for reviewer-linked evidence work | `research_task` | `topic.records.tasks` | `rebuttal.reviewer-linked-evidence-todo` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind research_task --semantic-label topic.records.tasks --placeholder '<REVIEWER_LINKED_EVIDENCE_TODO>' --profile rebuttal.reviewer-linked-evidence-todo --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'analysis, experiment, decision' --body-file <body-file> --content-name reviewer-linked-evidence-todo.json --metadata-json '{"paper_surface":"reviewer_linked_evidence_todo"}'` |
| <REBUTTAL_EVIDENCE_UPDATE> | evidence | Rebuttal Evidence Item update | `evidence_item` | `topic.records.artifacts` | `rebuttal.evidence-update` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<REBUTTAL_EVIDENCE_UPDATE>' --profile rebuttal.evidence-update --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2 and routed skills' --consumer 'rebuttal, write, finalize' --body-file <body-file> --content-name rebuttal-evidence-update.md --metadata-json '{"paper_surface":"rebuttal_evidence_update"}'` |
| <MANUSCRIPT_TEXT_DELTA> | draft | Manuscript text-delta Artifact | `artifact` | `topic.records.artifacts` | `rebuttal.text-deltas` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<MANUSCRIPT_TEXT_DELTA>' --profile rebuttal.text-deltas --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-write-v2 or rebuttal' --consumer 'rebuttal, finalize' --body-file <body-file> --content-name manuscript-text-delta.md --metadata-json '{"paper_surface":"manuscript_text_delta"}'` |
| <RESPONSE_LETTER_DRAFT> | draft | Response letter Artifact | `artifact` | `topic.records.artifacts` | `rebuttal.response-letter` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<RESPONSE_LETTER_DRAFT>' --profile rebuttal.response-letter --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'user, finalize' --body-file <body-file> --content-name response-letter-draft.md --metadata-json '{"paper_surface":"response_letter_draft"}'` |
| <REVISION_HANDOFF_BUNDLE> | handoff | Revision handoff bundle Artifact | `artifact` | `topic.records.artifacts` | `package.paper.revision-handoff-bundle` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<REVISION_HANDOFF_BUNDLE>' --profile package.paper.revision-handoff-bundle --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'finalize, user' --body-file <body-file> --content-name revision-handoff-bundle.json --metadata-json '{"paper_surface":"revision_handoff_bundle"}'` |

## Read, Update, and Archive Patterns

Use `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
