# Placeholder Bindings

This page binds the semantic objects in `references/placeholders.md` to Isomer Topic Workspace storage operations. Use these bindings when a pipeline object must become a durable record, structured payload-file record or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the semantic ids, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

Every structured payload file must include non-empty top-level `title` and `summary` strings. If the payload contains idea-bearing entries that can become canonical Research Ideas, each accepted idea object must include its own non-empty `title` and `summary`; labels, candidate ids, and aliases may be present but do not replace those display fields.

## Canonical lineage metadata

When a durable record is produced from prior durable records, pass immediate parents through `--parents-json`, choose `--lineage-kind`, and add `--generation-id` plus `--generation-purpose` for sibling candidate passes. Use `revision_of` only through `ext research records revise <record-id>` when accepted content changes; use `--relationships-json`, `--files-json`, and `--index-hints-json` only for non-lineage query metadata.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name evidence, citations, file materialization, support links, summaries, routes, or other non-canonical refs; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `references/placeholders.md` first to understand the semantic id, meaning, producer, consumer, and kind.
- Choose the binding row with the exact semantic id; do not infer a nearby row by name similarity.
- Store exact semantic id, skill, producer, consumer, kind, format profile ref, payload file role, and payload file and optional export metadata on created records.
- Inspect stored payloads with `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload`.
- Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.
- Validate any structured payload before writing it by running `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <profile> --payload-file <payload-file>`.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Semantic id | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| `DEEPSCI:PIPELINE-TERMINAL-REPORT` | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/pipeline-terminal-report/v2` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/report/pipeline-terminal-report/v2 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id DEEPSCI:PIPELINE-TERMINAL-REPORT --format-profile isomer:deepsci/record-format/profile/report/pipeline-terminal-report/v2 --skill isomer-ext-deepsci-entrypoint --producer 'isomer-ext-deepsci-entrypoint at the end of a recipe run.' --consumer 'External controller, isomer-deepsci-decision, user.' --payload-file <payload-file>` |
| `DEEPSCI:PIPELINE-RUN-RECORD` | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/pipeline-run-record/v2` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/control/pipeline-run-record/v2 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id DEEPSCI:PIPELINE-RUN-RECORD --format-profile isomer:deepsci/record-format/profile/control/pipeline-run-record/v2 --skill isomer-ext-deepsci-entrypoint --producer 'isomer-ext-deepsci-entrypoint during recipe execution.' --consumer 'External controller, future resume logic.' --payload-file <payload-file>` |
| `DEEPSCI:PIPELINE-RESUME-PACKET` | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/pipeline-resume-packet/v2` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/control/pipeline-resume-packet/v2 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id DEEPSCI:PIPELINE-RESUME-PACKET --format-profile isomer:deepsci/record-format/profile/control/pipeline-resume-packet/v2 --skill isomer-ext-deepsci-entrypoint --producer 'isomer-ext-deepsci-entrypoint when a run pauses or blocks.' --consumer 'External controller, future isomer-ext-deepsci-entrypoint resume invocation.' --payload-file <payload-file>` |
| `DEEPSCI:PIPELINE-RECIPE-CONTEXT` | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/pipeline-recipe-context/v2` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/control/pipeline-recipe-context/v2 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id DEEPSCI:PIPELINE-RECIPE-CONTEXT --format-profile isomer:deepsci/record-format/profile/control/pipeline-recipe-context/v2 --skill isomer-ext-deepsci-entrypoint --producer 'External controller invoking isomer-ext-deepsci-entrypoint.' --consumer 'isomer-ext-deepsci-entrypoint at recipe start.' --payload-file <payload-file>` |
