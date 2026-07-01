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
| figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure` | Store exported figures and figure bundles as Artifacts; create Evidence Items for render inspection when needed. |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store report bodies as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |

## Placeholder Bindings

| Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| <PAPER_PRESENTATION_SOURCE_PACKET> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.paper-presentation-source-packet` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<PAPER_PRESENTATION_SOURCE_PACKET>' --profile evidence.paper-presentation-source-packet --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt' --body-file <body-file>` |
| <PAPER_TYPE_CLASSIFICATION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.paper-type-classification` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<PAPER_TYPE_CLASSIFICATION>' --profile decision.paper-type-classification --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt' --body-file <body-file>` |
| <CHINESE_PRESENTATION_PLAN> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.chinese-presentation-plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<CHINESE_PRESENTATION_PLAN>' --profile draft.chinese-presentation-plan --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt, user' --body-file <body-file>` |
| <PRESENTATION_FIGURE_SELECTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.presentation-figure-selection` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<PRESENTATION_FIGURE_SELECTION>' --profile decision.presentation-figure-selection --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt' --body-file <body-file>` |
| <PRESENTATION_ASSET_MANIFEST> | figure | Figure Artifact with optional render-inspection Evidence Item | `artifact` | `topic.records.artifacts` | `figure.presentation-asset-manifest` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PRESENTATION_ASSET_MANIFEST>' --profile figure.presentation-asset-manifest --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt, user' --body-file <body-file>` |
| <CHINESE_SLIDE_CONTENT> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.chinese-slide-content` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<CHINESE_SLIDE_CONTENT>' --profile draft.chinese-slide-content --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt, user' --body-file <body-file>` |
| <PPTX_DECK> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.pptx-deck` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PPTX_DECK>' --profile report.pptx-deck --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'user' --body-file <body-file>` |
| <PPTX_QA_REPORT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.pptx-qa-report` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PPTX_QA_REPORT>' --profile report.pptx-qa-report --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'user' --body-file <body-file>` |
| <PPTX_REVISION_LOG> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.pptx-revision-log` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<PPTX_REVISION_LOG>' --profile report.pptx-revision-log --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'user' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
