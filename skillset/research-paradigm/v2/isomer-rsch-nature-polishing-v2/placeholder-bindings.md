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
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <PAPER_TYPE_DIAGNOSIS> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.paper-type-diagnosis` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<PAPER_TYPE_DIAGNOSIS>' --profile decision.paper-type-diagnosis --skill isomer-rsch-nature-polishing-v2 --producer 'isomer-rsch-nature-polishing-v2' --consumer 'nature-polishing' --body-file <body-file>` |
| <PROSE_FAILURE_DIAGNOSIS> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.prose-failure-diagnosis` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PROSE_FAILURE_DIAGNOSIS>' --profile report.prose-failure-diagnosis --skill isomer-rsch-nature-polishing-v2 --producer 'isomer-rsch-nature-polishing-v2' --consumer 'nature-polishing, write' --body-file <body-file>` |
| <CLAIM_BOUNDARY_CHECK> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.claim-boundary-check` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<CLAIM_BOUNDARY_CHECK>' --profile evidence.claim-boundary-check --skill isomer-rsch-nature-polishing-v2 --producer 'isomer-rsch-nature-polishing-v2' --consumer 'nature-polishing, write, review' --body-file <body-file>` |
| <SECTION_LOGIC_REBUILD> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.section-logic-rebuild` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<SECTION_LOGIC_REBUILD>' --profile draft.section-logic-rebuild --skill isomer-rsch-nature-polishing-v2 --producer 'isomer-rsch-nature-polishing-v2' --consumer 'nature-polishing, write' --body-file <body-file>` |
| <POLISHED_MANUSCRIPT_TEXT> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.polished-manuscript-text` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<POLISHED_MANUSCRIPT_TEXT>' --profile draft.polished-manuscript-text --skill isomer-rsch-nature-polishing-v2 --producer 'isomer-rsch-nature-polishing-v2' --consumer 'write, user' --body-file <body-file>` |
| <POLISHING_STYLE_QA> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.polishing-style-qa` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<POLISHING_STYLE_QA>' --profile report.polishing-style-qa --skill isomer-rsch-nature-polishing-v2 --producer 'isomer-rsch-nature-polishing-v2' --consumer 'nature-polishing, write' --body-file <body-file>` |
| <POLISHING_EVIDENCE_BLOCKER> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.polishing-evidence-blocker` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<POLISHING_EVIDENCE_BLOCKER>' --profile decision.polishing-evidence-blocker --skill isomer-rsch-nature-polishing-v2 --producer 'isomer-rsch-nature-polishing-v2' --consumer 'user, write, decision' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
