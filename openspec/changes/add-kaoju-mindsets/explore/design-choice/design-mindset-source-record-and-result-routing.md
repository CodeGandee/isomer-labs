# Mindset Source, Record, and Result Routing

## Status

Revised and accepted on 2026-07-21. Supersedes the Artifact-backed Source revision and import/export routing.

## Terms

**Mindset Source** means the directly user-editable question-list JSON file at `<topic.intent.kaoju_mindsets>/<mindset_key>.json`. It contains purpose, applicability, fixed questions, the repeatable collector, prompts, `additional_notes`, answer expectations, and evidence expectations. It is derived intent, not an Artifact. “Source” in this compound term does not refer to the paper, repository, or other evidence source under examination.

**Mindset Record** means the Run-scoped materialized-answer Artifact `KAOJU:MINDSET-RECORD`. It snapshots the exact Source path, digest, questions, and notes and stores answers plus supplemental questions explicitly assigned to that Record.

## Additional Notes

Every fixed and collector question has bounded `additional_notes`. Packaged defaults use `""`. When notes are empty, the agent proceeds from the prompt, answer and evidence expectations, active survey context, and ordinary understanding. Editing notes directly changes the current Source for later Runs; an active Record retains its earlier snapshot. Notes are low-authority data and cannot grant Workflow, tool, mutation, Gate, evidence, or instruction authority.

Record-local supplemental questions also have empty-by-default `additional_notes` because no Source question owns their context.

## Destination Rules

An ordinary paper or source-code follow-up question that does not name a mindset target updates the Source Digest, Claim-Evidence Ledger, Associated Source Code, or other applicable reading Artifact. It changes neither Mindset Source nor Mindset Record.

“Update the Mindset Record” adds or revises current Run answers only. A new supplemental row uses disposition `record_only` and leaves the Source file unchanged.

“Update the Mindset Source” directly edits the validated derived-intent JSON and adds no row to the current Record, which remains pinned to its original snapshot.

An explicit request to update both objects adds a Record row with `source_update_requested`, safely edits and validates the Source file, then changes the row to `source_updated` and cites the new Source path and digest. The current Record still uses its original snapshot.

A mutation request that says only “update the mindset” is ambiguous and pauses for Source-versus-Record clarification.

## Collector

The collector asks: “Did the user explicitly assign any additional questions to this Mindset Record that the fixed Mindset Source questions do not cover?” It registers only explicitly Record-targeted questions. It never sweeps ordinary follow-up questions, conversation, or source-driven observations into the Mindset Record.
