## Context

The current Kaoju contract makes a selected Mindset Source mandatory for paper and source-code examination. Before a concrete Run, the entrypoint invokes the topic creator in create-missing mode; after the Run begins, it snapshots the Source into `KAOJU:MINDSET-RECORD`; consumers and closeout fail when the Record is absent. This makes owner deletion or late Kaoju installation self-heal by mutation instead of expressing that the topic has no chosen mindset.

Mindset Sources are owner-editable derived intent, not Artifacts or workflow authority. The existing Run is already a Workspace Runtime lifecycle record stored in SQLite, and its `transition_metadata_json` persists typed procedure inputs and is preserved across checkpoints. The fallback can therefore record absence on the Run without creating a placeholder Artifact or adding a table.

## Goals / Non-Goals

**Goals:**

- Treat an absent selected Mindset Source file as a valid decision to run without mindset reflection.
- Persist one explicit, machine-readable mindset resolution on each applicable Run before focused-owner dispatch.
- Propagate verified absence through handoffs and closeout so later stages do not mistake a missing Record ref for orchestration failure.
- Keep invalid, unreadable, ambiguous, mismatched, or unsafe existing Source state fail-closed.
- Let future Runs use a Source added after an earlier Run recorded absence while preserving the historical Run posture.

**Non-Goals:**

- Create an empty, placeholder, or tombstone `KAOJU:MINDSET-RECORD` Artifact.
- Register Mindset Sources as Artifacts or add a new Artifact semantic id.
- Add a SQLite table or index for mindset availability.
- Fall back to packaged seed questions, conversation memory, or an unrelated topic.
- Make all topic-creation or explicit `create-topic` generation optional; those workflows still create requested Source files.
- Treat an invalid existing file as equivalent to an absent file.

## Decisions

### 1. Persist a typed resolution on the Run lifecycle record

An applicable Run stores one `mindset_resolution` object in `transition_metadata_json` after `project runs begin` and before focused-owner dispatch. It has one of two dispositions:

```text
recorded
  mindset_key
  source_semantic_label = topic.intent.kaoju_mindsets
  source_relative_path = <mindset_key>.json
  source_status = present
  record_status = available
  record_ref = <KAOJU:MINDSET-RECORD ref>

skipped_source_missing
  mindset_key
  source_semantic_label = topic.intent.kaoju_mindsets
  source_relative_path = <mindset_key>.json
  source_status = missing
  record_status = absent
  reason = source_missing
```

The skipped posture is database state, but it is not a Research Artifact. Storing it on the Run keeps the scope exact, survives checkpoints through the existing metadata merge behavior, and avoids inventing an answer document when no questions exist. A separate table was rejected because no cross-Run availability query or independent lifecycle is required.

### 2. Add `project runs resolve-mindset`

The typed command accepts one Run id and `--mindset-key`, plus exactly one of `--record-ref` or `--source-missing`. Recorded mode verifies that the referenced lifecycle record is a `KAOJU:MINDSET-RECORD` scoped to the same Run and that its snapshotted key matches. Missing mode resolves `topic.intent.kaoju_mindsets`, derives the deterministic direct-child path, and verifies that the file does not exist. A present but unreadable or invalid file cannot be recorded as missing.

The first successful resolution is immutable. An identical retry is idempotent; a different key, disposition, or Record ref fails. This mirrors Source snapshot immutability and prevents later stages from changing the reflection basis mid-Run.

The command also appends a verified Record ref to the Run's `input_refs` in recorded mode. Missing mode leaves `input_refs` unchanged because a synthetic ref would imply an object that does not exist.

### 3. Remove concrete-action lazy creation

Explicit Kaoju `create-topic` and explicit create-missing or repair requests continue to generate Sources from packaged defaults. Concrete research actions only select and inspect the deterministic Source for the chosen route. If that file is absent, they begin the Run, record `skipped_source_missing`, and proceed. This makes file absence meaningful and ensures topics created before Kaoju installation can operate without hidden mutation.

Read-only routes continue to report the missing posture without opening a Run. Existing invalid files remain repair blockers. The entrypoint never substitutes packaged defaults at execution time.

### 4. Pin absence for the whole Run

Once a Run records `skipped_source_missing`, every handoff carries the Run ref, mindset key, and skipped disposition. Consumers read the Run record and skip Mindset Record loading, question answering, collector checks, revisions, and terminal Record production. Ordinary Source Digest, Claim-Evidence Ledger, Associated Source Code, and other reading outputs remain unchanged.

If the Source appears later, the active Run remains skipped. A restarted or later Run re-resolves the filesystem and may materialize a Record. This is the absence equivalent of continuing to use an immutable Record snapshot after a Source edit.

### 5. Make closeout conditional on the persisted resolution

For `recorded`, the existing terminal Mindset Record rules remain mandatory. For `skipped_source_missing`, the Run may complete without a Mindset Record and the terminal report names the key, missing posture, and lack of Record ref. An applicable consumer that receives neither a verified Record ref nor a verified skipped resolution still pauses because an unrecorded omission is orchestration failure, not optionality.

## Risks / Trade-offs

- [Users may delete a Source accidentally and receive less reflective output] → Surface the skipped key and exact `create-topic` recovery route in Run status, handoffs, and terminal reports.
- [A caller may claim absence while a file exists] → Make the typed service resolve and verify the deterministic path before writing the Run marker.
- [A Source may appear after absence is recorded] → Pin the active Run posture and re-evaluate only for a restarted or later Run.
- [Existing skills may treat every absent Record as failure] → Update the public entrypoint, both ingestion commands, examine, shared mindset guidance, and README together, and cover both resolution branches in asset tests.
- [Arbitrary Run metadata could drift] → Centralize construction and validation in `KaojuRunService.resolve_mindset` and reject conflicting rewrites.

## Migration Plan

No SQLite migration is required because the new object lives in existing Run transition metadata. Existing Runs without `mindset_resolution` retain their historical meaning; applicable active Runs must resolve a posture before subsequent focused work. Rollback ignores the extra metadata, but Runs recorded as skipped would again fail the older skill closeout contract and should be completed before downgrading.

## Open Questions

None. Missing means the deterministic selected file does not exist; all other Source failures remain blocking.
