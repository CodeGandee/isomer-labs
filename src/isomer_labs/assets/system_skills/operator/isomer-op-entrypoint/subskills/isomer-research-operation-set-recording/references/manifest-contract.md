---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Operation Set Acceptance Manifest

## Boundary

Store the versioned manifest at `<operation-set>/.isomer-operation-set/manifest.json`. The coordinator ignores this reserved directory while inventorying files. Every other regular file must appear exactly once under `outputs`; Git ignore and tracking state do not affect the inventory.

Use schema version `isomer-operation-set-acceptance.v1`. Copy the stable `operation_set_id`, Topic and Topic Workspace ids, and worker identity from `inspect` or an explicit scaffold. Increase `revision` only when changing an already accepted manifest, and set `supersedes_receipt_id` to the earlier receipt.

## Shape

```json
{
  "schema_version": "isomer-operation-set-acceptance.v1",
  "operation_set_id": "operation-set-topic_actor-researcher-sets-run-1-...",
  "revision": 1,
  "research_topic_id": "topic-id",
  "topic_workspace_id": "topic-workspace-id",
  "worker": {"kind": "topic_actor", "name": "researcher"},
  "producer_skill": "isomer-deepsci-analysis",
  "lifecycle_refs": {"research_task_id": "task-id", "run_id": "run-id"},
  "outputs": [
    {
      "key": "analysis-payload",
      "path": "analysis.json",
      "digest": "sha256:<64 lowercase hex characters>",
      "size_bytes": 1234,
      "media_type": "application/json",
      "disposition": "record_payload",
      "record_key": "analysis"
    },
    {
      "key": "measurements",
      "path": "measurements.csv",
      "digest": "sha256:<64 lowercase hex characters>",
      "size_bytes": 456,
      "media_type": "text/csv",
      "disposition": "record_attachment",
      "record_key": "analysis"
    },
    {
      "key": "debug-log",
      "path": "debug.log",
      "digest": "sha256:<64 lowercase hex characters>",
      "size_bytes": 78,
      "disposition": "disposable",
      "reason": "Transient command trace with no research value."
    }
  ],
  "record_intents": [
    {
      "key": "analysis",
      "action": "create",
      "record_kind": "artifact",
      "semantic_id": "DEEPSCI:ANALYSIS-CAMPAIGN-SUMMARY",
      "scope_key": "campaign-main",
      "format_profile_ref": "<authoritative profile ref when structured>",
      "producer": "isomer-deepsci-analysis",
      "parents": [{"record_id": "parent-record-id", "lineage_kind": "derived_from", "parent_role": "analysis_input"}],
      "idea_effects_required": false
    }
  ]
}
```

## Output Dispositions

`record_payload` supplies the one body or structured payload for its named record intent. `record_attachment` creates an owner-preserved managed copy under the accepted record and stores the original relative path, digest, media type, operation-set id, and receipt id in the file metadata. `disposable` excludes the file from durable research state and requires a non-empty reason.

Do not assign more than one `record_payload` to an intent. An intent can own several attachments. Every durable output must name an existing `record_key`; a disposable output must not name one.

## Record Actions

Use `create` for a new durable record and supply `record_kind` plus all binding fields required by the current record contract. A root create requires `root_reason`; otherwise list immediate parents by durable `record_id` or `local_record_key`.

Use `revise` with `target_record_id` for a content-changing descendant. The canonical record service supplies the unique immediate `revision_of` parent and inherits record kind and compatible binding fields when omitted.

Use `reference` with `target_record_id` only for existing durable content. Acceptance verifies the staged output digest against the record payload, body, or indexed managed files and verifies any declared parents. It creates no duplicate record.

## Research Idea Effects

When the current Artifact Format Profile or producer contract marks the record as idea-bearing, set `idea_effects_required` and include the exact authored `research_idea_effects` object. Invoke `isomer-op-entrypoint->research-ideas` for its schema and validation rules. Record lineage in `parents` does not imply Idea Lineage, and the coordinator never synthesizes concept state from the payload.
