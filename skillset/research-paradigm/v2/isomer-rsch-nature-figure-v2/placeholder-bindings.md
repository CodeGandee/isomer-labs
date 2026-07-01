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
| evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence` | Create an Evidence Item record and attach the body or source summary through the resolved topic records label. |
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store exported figures and figure bundles as Artifacts; create Evidence Items for render inspection when needed. |
| handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff` | Use `project handoffs` for live agent-to-agent dispatch; use this binding for durable handoff packets and acceptance criteria. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <NATURE_FIGURE_BACKEND_CHOICE> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.nature-figure-backend-choice` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<NATURE_FIGURE_BACKEND_CHOICE>' --profile decision.nature-figure-backend-choice --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2 or user' --consumer 'nature-figure' --body-file <body-file>` |
| <NATURE_FIGURE_CONTRACT> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.nature-figure-contract` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<NATURE_FIGURE_CONTRACT>' --profile handoff.nature-figure-contract --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'nature-figure, write, finalize' --body-file <body-file>` |
| <NATURE_FIGURE_RUNTIME_CHECK> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.nature-figure-runtime-check` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<NATURE_FIGURE_RUNTIME_CHECK>' --profile report.nature-figure-runtime-check --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'nature-figure, user' --body-file <body-file>` |
| <NATURE_PANEL_EVIDENCE_MAP> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.nature-panel-evidence-map` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<NATURE_PANEL_EVIDENCE_MAP>' --profile evidence.nature-panel-evidence-map --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'nature-figure, review' --body-file <body-file>` |
| <NATURE_FIGURE_ARCHETYPE> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.nature-figure-archetype` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<NATURE_FIGURE_ARCHETYPE>' --profile decision.nature-figure-archetype --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'nature-figure' --body-file <body-file>` |
| <NATURE_EXPORT_CONTRACT> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.nature-export-contract` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<NATURE_EXPORT_CONTRACT>' --profile handoff.nature-export-contract --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'nature-figure, finalize' --body-file <body-file>` |
| <NATURE_FIGURE_EXPORT_BUNDLE> | figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure.nature-figure-export-bundle` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<NATURE_FIGURE_EXPORT_BUNDLE>' --profile figure.nature-figure-export-bundle --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'write, finalize, user' --body-file <body-file>` |
| <NATURE_FIGURE_QA_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.nature-figure-qa-report` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<NATURE_FIGURE_QA_REPORT>' --profile report.nature-figure-qa-report --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'nature-figure, review, finalize' --body-file <body-file>` |
| <NATURE_FIGURE_BLOCKER> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.nature-figure-blocker` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<NATURE_FIGURE_BLOCKER>' --profile decision.nature-figure-blocker --skill isomer-rsch-nature-figure-v2 --producer 'isomer-rsch-nature-figure-v2' --consumer 'user, decision' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
