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
| <DATA_AVAILABILITY_CONTEXT> | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control.data-availability-context` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --placeholder '<DATA_AVAILABILITY_CONTEXT>' --profile control.data-availability-context --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'nature-data' --body-file <body-file>` |
| <DATASET_INVENTORY> | evidence | Evidence Item with an Artifact body when the evidence needs rich content | `evidence_item` | `topic.records.artifacts` | `evidence.dataset-inventory` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<DATASET_INVENTORY>' --profile evidence.dataset-inventory --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'nature-data, write, finalize' --body-file <body-file>` |
| <DATA_ACCESS_CLASSIFICATION> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.data-access-classification` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<DATA_ACCESS_CLASSIFICATION>' --profile decision.data-access-classification --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'nature-data' --body-file <body-file>` |
| <REPOSITORY_STRATEGY> | handoff | Handoff packet Artifact, or Handoff Record when dispatching across agents | `artifact` | `topic.records.artifacts` | `handoff.repository-strategy` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<REPOSITORY_STRATEGY>' --profile handoff.repository-strategy --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'nature-data, finalize' --body-file <body-file>` |
| <DATA_AVAILABILITY_STATEMENT> | draft | Artifact with a draft profile | `artifact` | `topic.records.artifacts` | `draft.data-availability-statement` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<DATA_AVAILABILITY_STATEMENT>' --profile draft.data-availability-statement --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'write, finalize, user' --body-file <body-file>` |
| <DATASET_CITATION_ACTIONS> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.dataset-citation-actions` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<DATASET_CITATION_ACTIONS>' --profile report.dataset-citation-actions --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'write, finalize' --body-file <body-file>` |
| <FAIR_METADATA_AUDIT> | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report.fair-metadata-audit` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --placeholder '<FAIR_METADATA_AUDIT>' --profile report.fair-metadata-audit --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'nature-data, finalize' --body-file <body-file>` |
| <DATA_AVAILABILITY_BLOCKER> | decision | Decision Record | `decision_record` | `topic.records.artifacts` | `decision.data-availability-blocker` | `pixi run isomer-cli --print-json ext research records create --topic <topic> --record-kind decision_record --placeholder '<DATA_AVAILABILITY_BLOCKER>' --profile decision.data-availability-blocker --skill isomer-rsch-nature-data-v2 --producer 'isomer-rsch-nature-data-v2' --consumer 'user, decision, finalize' --body-file <body-file>` |

## Read, Update, and Archive Patterns

Use `pixi run isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'` to find prior records for a placeholder.

Use `pixi run isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-body` to inspect one stored record and its body when the body is text.

Use `pixi run isomer-cli --print-json ext research records update <record-id> --topic <topic> --record-kind <record-kind> --status <status> --placeholder '<PLACEHOLDER>' --body-file <body-file>` when the same semantic record receives a revised body or status.

Use `pixi run isomer-cli --print-json ext research records delete <record-id> --topic <topic> --reason <reason>` only to archive a superseded or invalid record. The command preserves body files by default.
