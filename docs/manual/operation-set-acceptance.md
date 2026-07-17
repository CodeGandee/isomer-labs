# Operation Set Acceptance

Operation Set Acceptance closes the boundary between plain files under a Topic Actor or Agent worker-output set and durable research records. A file is not a durable Artifact, Evidence Item, managed attachment, or Research Idea realization merely because it exists, appears in Git, renders correctly, or was described in a terminal response.

Use `isomer-cli ext research operation-sets` to inventory one resolved worker operation set, preview its complete persistence plan, apply the plan with a resumable receipt, and verify every promised durable effect.

## Completion Contract

Every regular material file outside the reserved `.isomer-operation-set/` control directory must have exactly one manifest disposition:

| Disposition | Meaning |
| --- | --- |
| `record_payload` | The file supplies the body or structured payload for one durable record intent. |
| `record_attachment` | The file is copied into owner-preserved managed storage under one accepted record. |
| `disposable` | The file has no durable research value, and the manifest records a concrete reason. |

An applicable closeout succeeds only when apply returns a `complete` receipt and a separate verify call succeeds. A workflow may report `closeout: not_applicable` only when it opened no operation set, wrote no material plain files, and can name the durable record refs it used or created. A missing set, forgotten path, or unclassified file is a paused closeout, not `not_applicable`.

## Inspect, Preview, Apply, and Verify

Resolve exactly one Topic Actor or Agent boundary. The operation-set path must be inside the selected worker's current output root.

```bash
isomer-cli --print-json ext research operation-sets inspect <operation-set-path> \
  --topic <topic-id> \
  --topic-actor <topic-actor-name>
```

Use `--agent <agent-name>` instead for a formal Agent Workspace. Inspection is read-only unless `--write-scaffold` is present. A scaffold is visibly incomplete, is written only under `.isomer-operation-set/manifest.json`, and never overwrites an existing manifest.

Complete the manifest, then run acceptance without `--apply`. Preview performs whole-plan validation without mutating records, managed files, or receipts.

```bash
isomer-cli --print-json ext research operation-sets accept <manifest-path> \
  --topic <topic-id> \
  --topic-actor <topic-actor-name>
```

Review the ordered actions, expected record ids, managed-copy destinations, canonical parents, authored Research Idea effects, expected receipt id, and diagnostics. Apply only the unchanged valid plan:

```bash
isomer-cli --print-json ext research operation-sets accept <manifest-path> \
  --topic <topic-id> \
  --topic-actor <topic-actor-name> \
  --apply
```

Verify by receipt id or by operation-set id, which selects its latest receipt revision:

```bash
isomer-cli --print-json ext research operation-sets verify <receipt-or-operation-set-id> \
  --topic <topic-id>
```

Verification is read-only. It checks exhaustive dispositions, staged and managed digests, record queryability, canonical record lineage, exact promised Research Idea effects, and receipt scope. It never repairs missing state.

## Manifest Schema

The manifest is strict JSON with schema version `isomer-operation-set-acceptance.v1`. Unknown fields, duplicate keys or paths, invalid digests, path traversal, symlinks, special files, missing dispositions, and unresolved record dependencies fail preflight.

```json
{
  "schema_version": "isomer-operation-set-acceptance.v1",
  "operation_set_id": "operation-set-topic-actor-researcher-run-1",
  "revision": 1,
  "research_topic_id": "topic-id",
  "topic_workspace_id": "topic-workspace-id",
  "worker": {
    "kind": "topic_actor",
    "name": "researcher"
  },
  "producer_skill": "isomer-deepsci-analysis",
  "lifecycle_refs": {
    "research_task_id": "task-id",
    "run_id": "run-id"
  },
  "outputs": [
    {
      "key": "analysis-payload",
      "path": "analysis.json",
      "digest": "sha256:<64-lowercase-hex-characters>",
      "size_bytes": 1234,
      "media_type": "application/json",
      "disposition": "record_payload",
      "record_key": "analysis"
    },
    {
      "key": "measurements",
      "path": "measurements.csv",
      "digest": "sha256:<64-lowercase-hex-characters>",
      "size_bytes": 456,
      "media_type": "text/csv",
      "disposition": "record_attachment",
      "record_key": "analysis"
    },
    {
      "key": "debug-log",
      "path": "debug.log",
      "digest": "sha256:<64-lowercase-hex-characters>",
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
      "format_profile_ref": "<authoritative-profile-ref>",
      "producer": "isomer-deepsci-analysis",
      "parents": [
        {
          "record_id": "parent-record-id",
          "lineage_kind": "derived_from",
          "parent_role": "analysis_input"
        }
      ],
      "idea_effects_required": false
    }
  ]
}
```

Use `create` for a new record and provide its authoritative binding fields. A root create needs `root_reason`; otherwise it names immediate durable parents by `record_id` or an earlier `local_record_key`. Use `revise` with `target_record_id`; the canonical record service supplies the unique `revision_of` parent. Use `reference` only when a named existing record already owns content whose managed digest can be verified.

When an Artifact Format Profile or producer contract makes an output idea-bearing, set `idea_effects_required` and provide the exact authored `idea_effects` object accepted by the current research-record transaction. The coordinator does not infer idea identity, facets, lifecycle transitions, decision options, generations, realizations, or Idea Lineage Edges.

## Managed Attachments

Accepted attachments are copied from the staging set into an owner-preserved record directory. The managed file index retains the original relative path, digest, size, media type, operation-set id, and receipt id. Durable queries use the managed path, so later worker cleanup does not break the record.

Acceptance rechecks staged size and digest immediately before each action and checks the copied digest before installing a managed file. A destination that already contains different bytes is a conflict. A matching destination is reused idempotently.

## Receipt Status and Recovery

| Status | Meaning |
| --- | --- |
| `applying` | Apply started and item progress is being recorded. |
| `partial` | At least one item failed or remains pending; earlier committed records remain durable. |
| `complete` | Every item committed and immediate verification succeeded. |
| `superseded` | A later explicit manifest revision completed and preserves this earlier receipt for audit. |

For a transient failure, correct only the external prerequisite and rerun the same `accept <manifest-path> --apply` command with the unchanged manifest. Completed items are verified and reused; pending items resume without duplicate records, attachments, lineage, or idea effects.

If an output, disposition, binding, parent, or authored effect must change after partial apply, create a higher manifest `revision` and set `supersedes_receipt_id` to the earlier receipt. Preview and apply the new revision. Do not edit receipt rows or delete earlier committed records.

A paused handoff should include the operation-set root, manifest path and digest, receipt id and status, completed and failed intent keys, accepted record refs, diagnostic codes, the first unresolved owner action, and the exact resume command.

## Three Independent Boundaries

Git tracking, research-record lineage, and Research Idea lineage are independent:

- Git says whether bytes belong to a repository history. It does not create a research record or prove semantic acceptance.
- Record lineage names immediate durable record parents such as `derived_from`, `follow_up_to`, or `revision_of`.
- Research Idea lineage describes conceptual derivation, selection, merge, follow-up, or subsumption between canonical ideas.

The acceptance manifest authors record parents and passes explicit Research Idea effects through the existing atomic record transaction. It never derives one lineage layer from the other.

## Legacy Read-Only Audit and Optional Repair

The historical Flash Attention 4 recovery had six operation sets containing an idea-exploration report, two benchmark reports, predictor validation, predictor code, and a SASS note. A safe legacy audit starts with read-only inspection of each named set, then compares its digests with the already recovered record payloads, managed files, record-lineage query, and Research Idea query. Do not scan every worker root or mutate the repaired topic as part of installation or validation.

For a similarly shaped unrepaired topic:

1. Run `operation-sets inspect` without `--write-scaffold` and preserve the deterministic inventory.
2. Query candidate records and their lineage through `ext research records list` and `ext research records lineage query`.
3. Query canonical concepts through `ext research ideas query` and `ext research ideas graph`; record lineage alone does not prove idea realization or Idea Lineage.
4. If durable records already own matching bytes, author explicit `reference` intents and preview them. Acceptance verifies existing record scope and managed digests rather than creating duplicates.
5. If a record is missing, author a supported `create` or `revise` intent with authoritative binding fields, immediate parents, and explicit idea effects when required.
6. Apply only after review, then verify the receipt. Preserve the old operation-set paths as provenance, not as durable attachment locators.

The current Flash Attention 4 records were repaired manually before this feature. They are an audit example, not automatic migration input.
