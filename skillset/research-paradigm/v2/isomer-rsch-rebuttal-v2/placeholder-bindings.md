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
| draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft` | Store drafts outside agent scratch once another skill may depend on them. |
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <REVIEW_PACKAGE_NORMALIZATION> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.review-package-normalization` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<REVIEW_PACKAGE_NORMALIZATION>' --profile evidence.review-package-normalization --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'rebuttal' --body-file <body-file>` |
| <REVIEWER_ITEM_MATRIX> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.reviewer-item-matrix` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<REVIEWER_ITEM_MATRIX>' --profile handoff.reviewer-item-matrix --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'rebuttal, analysis, write' --body-file <body-file>` |
| <REBUTTAL_ACTION_PLAN> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.rebuttal-action-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<REBUTTAL_ACTION_PLAN>' --profile handoff.rebuttal-action-plan --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'analysis, write, scout, baseline' --body-file <body-file>` |
| <REVIEWER_LINKED_EVIDENCE_TODO> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.reviewer-linked-evidence-todo` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<REVIEWER_LINKED_EVIDENCE_TODO>' --profile handoff.reviewer-linked-evidence-todo --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'analysis, experiment, decision' --body-file <body-file>` |
| <REBUTTAL_EVIDENCE_UPDATE> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.rebuttal-evidence-update` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<REBUTTAL_EVIDENCE_UPDATE>' --profile evidence.rebuttal-evidence-update --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2 and routed skills' --consumer 'rebuttal, write, finalize' --body-file <body-file>` |
| <MANUSCRIPT_TEXT_DELTA> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.manuscript-text-delta` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<MANUSCRIPT_TEXT_DELTA>' --profile draft.manuscript-text-delta --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-write-v2 or rebuttal' --consumer 'rebuttal, finalize' --body-file <body-file>` |
| <RESPONSE_LETTER_DRAFT> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.response-letter-draft` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<RESPONSE_LETTER_DRAFT>' --profile draft.response-letter-draft --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'user, finalize' --body-file <body-file>` |
| <REVISION_HANDOFF_BUNDLE> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.revision-handoff-bundle` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<REVISION_HANDOFF_BUNDLE>' --profile handoff.revision-handoff-bundle --skill isomer-rsch-rebuttal-v2 --producer 'isomer-rsch-rebuttal-v2' --consumer 'finalize, user' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
