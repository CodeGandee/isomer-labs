# Placeholder Bindings

This page binds the placeholders in `migrate/placeholders.md` to Isomer Topic Workspace storage operations. Keep the placeholders in workflow prose; use this page when a placeholder must become a durable record, body, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the placeholder tokens, producer, consumer, and profile metadata should remain stable.

## Binding Rules

- Read `migrate/placeholders.md` first to understand the placeholder meaning, producer, consumer, and kind.
- Choose the binding row with the exact placeholder token; do not infer a nearby row by name similarity.
- Store exact placeholder, skill, producer, consumer, kind, and profile metadata on created records.
- Resolve body locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- For paper-line presentation outputs, use profiles such as `presentation.source-packet`, `presentation.plan`, `presentation.asset-manifest`, `presentation.slide-content`, `package.presentation.pptx-deck`, `presentation.qa-report`, and `presentation.revision-log` on existing generic semantic labels; do not add paper-specific top-level labels.
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
| <PAPER_PRESENTATION_SOURCE_PACKET> | evidence | Presentation source-packet Evidence Item | `evidence_item` | `topic.records.artifacts` | `presentation.source-packet` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --semantic-label topic.records.artifacts --placeholder '<PAPER_PRESENTATION_SOURCE_PACKET>' --profile presentation.source-packet --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt' --body-file <body-file> --content-name paper-presentation-source-packet.json --metadata-json '{"paper_surface":"presentation_source_packet"}'` |
| <PAPER_TYPE_CLASSIFICATION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.paper-type-classification` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PAPER_TYPE_CLASSIFICATION>' --profile decision.paper-type-classification --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt' --body-file <body-file> --metadata-json '{"paper_surface":"paper_type_classification"}'` |
| <CHINESE_PRESENTATION_PLAN> | draft | Chinese presentation plan Artifact | `artifact` | `topic.records.artifacts` | `presentation.plan` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<CHINESE_PRESENTATION_PLAN>' --profile presentation.plan --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt, user' --body-file <body-file> --content-name chinese-presentation-plan.md --metadata-json '{"paper_surface":"chinese_presentation_plan"}'` |
| <PRESENTATION_FIGURE_SELECTION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.presentation-figure-selection` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --semantic-label topic.records.artifacts --placeholder '<PRESENTATION_FIGURE_SELECTION>' --profile decision.presentation-figure-selection --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt' --body-file <body-file> --metadata-json '{"paper_surface":"presentation_figure_selection"}'` |
| <PRESENTATION_ASSET_MANIFEST> | figure | Presentation asset manifest Artifact | `artifact` | `topic.records.artifacts` | `presentation.asset-manifest` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PRESENTATION_ASSET_MANIFEST>' --profile presentation.asset-manifest --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt, user' --body-file <body-file> --content-name presentation-asset-manifest.json --metadata-json '{"paper_surface":"presentation_asset_manifest"}'` |
| <CHINESE_SLIDE_CONTENT> | draft | Chinese slide content Artifact | `artifact` | `topic.records.artifacts` | `presentation.slide-content` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<CHINESE_SLIDE_CONTENT>' --profile presentation.slide-content --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'nature-paper2ppt, user' --body-file <body-file> --content-name chinese-slide-content.md --metadata-json '{"paper_surface":"chinese_slide_content"}'` |
| <PPTX_DECK> | report | PPTX deck package Artifact | `artifact` | `topic.records.artifacts` | `package.presentation.pptx-deck` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PPTX_DECK>' --profile package.presentation.pptx-deck --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'user' --body-file <body-file> --content-name pptx-deck.json --metadata-json '{"paper_surface":"pptx_deck"}'` |
| <PPTX_QA_REPORT> | report | PPTX QA report Artifact | `artifact` | `topic.records.artifacts` | `presentation.qa-report` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PPTX_QA_REPORT>' --profile presentation.qa-report --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'user' --body-file <body-file> --content-name pptx-qa-report.md --metadata-json '{"paper_surface":"pptx_qa_report"}'` |
| <PPTX_REVISION_LOG> | report | PPTX revision log Artifact | `artifact` | `topic.records.artifacts` | `presentation.revision-log` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-label topic.records.artifacts --placeholder '<PPTX_REVISION_LOG>' --profile presentation.revision-log --skill isomer-rsch-nature-paper2ppt-v2 --producer 'isomer-rsch-nature-paper2ppt-v2' --consumer 'user' --body-file <body-file> --content-name pptx-revision-log.md --metadata-json '{"paper_surface":"pptx_revision_log"}'` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
