# Placeholder Bindings

This page binds the semantic objects in `references/placeholders.md` to Isomer Topic Workspace storage operations. Use these bindings when a pipeline object must become a durable record, structured payload, generated view, or queryable ref.

Use `isomer-cli ext research records` as the current transitional CRUD surface. Future native `project records ...` commands may replace these command shapes, but the semantic ids, producer, consumer, and profile metadata should remain stable.

When a Topic Actor creates or updates a record, add `--topic-actor <topic-actor-name>` and any known `--actor-kind`, `--runtime-kind`, `--controller-kind`, and `--adapter-ref` values. When a formal team agent creates or updates a record, include Agent Team Instance, Agent Instance, or Agent Workspace refs only when that formal context truly produced the record; do not fabricate those refs for Topic Actor work.

## Query-index metadata

When a structured payload has relationship facts, file outputs, or GUI facets, preserve them in the payload and pass explicit refs through `--relationships-json`, `--files-json`, and `--index-hints-json` when the producing skill knows them. Relationship metadata should name consumed, produced, routed, supported, superseded, summarized, or cited records; file metadata should name file role, semantic label, and source payload field or output pattern; facet metadata should leave ideas, route decisions, metrics, claims, artifact lists, and scalar facts in profile-backed payload sections so the query-index extractor can derive rows.

## Binding Rules

- Read `references/placeholders.md` first to understand the semantic id, meaning, producer, consumer, and kind.
- Choose the binding row with the exact semantic id; do not infer a nearby row by name similarity.
- Store exact semantic id, skill, producer, consumer, kind, format profile ref, payload file role, and generated view naming metadata on created records.
- Resolve generated view locations through the listed semantic label; do not invent hard-coded paths under the Topic Workspace.
- Validate any structured payload before writing it by running `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <profile> --payload-file <payload-file>`.

## Kind Defaults

| Kind | Storage Item | Record Kind | Default Label | Profile Prefix | Note |
| --- | --- | --- | --- | --- | --- |
| report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `report` | Store structured report payloads as Artifacts and link later Evidence Items, Decisions, or packages through metadata. |
| runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `control` | Use this for boards, checklists, route cursors, continuity notes, and other resumable control surfaces. |

## Placeholder Bindings

| Semantic id | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
| --- | --- | --- | --- | --- | --- | --- |
| `pipeline-terminal-report` | report | Artifact with a report profile | `artifact` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/report/pipeline-terminal-report/v1` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/report/pipeline-terminal-report/v1 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind artifact --semantic-id pipeline-terminal-report --format-profile isomer:deepsci/record-format/profile/report/pipeline-terminal-report/v1 --skill isomer-deepsci-pipeline --producer 'isomer-deepsci-pipeline at the end of a recipe run.' --consumer 'External controller, isomer-deepsci-decision, user.' --payload-file <payload-file> --render markdown --content-name pipeline-terminal-report.md` |
| `pipeline-run-record` | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/pipeline-run-record/v1` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/control/pipeline-run-record/v1 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id pipeline-run-record --format-profile isomer:deepsci/record-format/profile/control/pipeline-run-record/v1 --skill isomer-deepsci-pipeline --producer 'isomer-deepsci-pipeline during recipe execution.' --consumer 'External controller, future resume logic.' --payload-file <payload-file> --render markdown --content-name pipeline-run-record.md` |
| `pipeline-resume-packet` | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/pipeline-resume-packet/v1` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/control/pipeline-resume-packet/v1 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id pipeline-resume-packet --format-profile isomer:deepsci/record-format/profile/control/pipeline-resume-packet/v1 --skill isomer-deepsci-pipeline --producer 'isomer-deepsci-pipeline when a run pauses or blocks.' --consumer 'External controller, future isomer-deepsci-pipeline resume invocation.' --payload-file <payload-file> --render markdown --content-name pipeline-resume-packet.md` |
| `pipeline-recipe-context` | runtime state | View Manifest, Workflow Stage Cursor, or control Artifact | `view_manifest` | `topic.records.views` | `isomer:deepsci/record-format/profile/control/pipeline-recipe-context/v1` | `isomer-cli --print-json ext research records validate --topic <topic> --format-profile isomer:deepsci/record-format/profile/control/pipeline-recipe-context/v1 --payload-file <payload-file> && isomer-cli --print-json ext research records create --topic <topic> --record-kind view_manifest --semantic-id pipeline-recipe-context --format-profile isomer:deepsci/record-format/profile/control/pipeline-recipe-context/v1 --skill isomer-deepsci-pipeline --producer 'External controller invoking isomer-deepsci-pipeline.' --consumer 'isomer-deepsci-pipeline at recipe start.' --payload-file <payload-file> --render markdown --content-name pipeline-recipe-context.md` |
