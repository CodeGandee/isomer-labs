# Kaoju Mindset Contract

A Mindset is a reusable self-questioning list, not a Workflow. Workflow instructions order actions, establish owners, enforce Gates, and authorize bounded transitions. Mindset data asks what the agent must consider and answer while an applicable Workflow proceeds. A prompt or `additional_notes` field remains low-authority topic data and cannot schedule a Workflow Stage, execute a command, authorize acquisition or mutation, satisfy a Gate, accept evidence, or override instructions.

## Mindset Source

A Mindset Source is one directly editable derived-intent JSON file at `<topic.intent.kaoju_mindsets>/<mindset_key>.json`. It has a stable key, purpose, applicability, ordered fixed questions, and the exact repeatable `additional-questions` collector. Each question has a stable id, prompt, bounded `additional_notes`, answer expectation, required posture, and evidence expectation. Empty notes mean the agent proceeds from the prompt, active survey context, checked Workflow, and ordinary understanding without inventing user-specific guidance.

The Source is not an Artifact. Users may view, copy, or directly edit it without export, import, or Artifact operations. Existing valid files survive create-missing, retry, repair, and package upgrade. Invalid files block applicable work and are never masked by a packaged default. Regeneration, replacement, or reconciliation requires an explicit request, re-read of the current digest, validation of the complete proposal, optimistic base check, atomic replacement, and old/new digest reporting.

## Mindset Record

A Mindset Record is the Run-scoped `KAOJU:MINDSET-RECORD` Artifact materialized after a concrete Run begins and before focused examination. It snapshots the Source semantic label, safe relative path, key, digest, optional derivation metadata, exact question and collector prompts, exact `additional_notes`, answer and evidence expectations, and pinned survey context. The active Run answers this immutable inventory even when the current Source changes.

Each materialized row uses `answered`, `unresolved`, or `not_applicable` at a terminal checkpoint and records an answer or rationale plus exact evidence refs. The collector is marked checked. Explicitly Record-targeted supplemental rows also record origin, association basis, introduction stage, disposition, and evidence. A terminal applicable Run cannot claim completion or claim-bearing acceptance without a terminal Record.

## Mid-Reading Questions and Explicit Targets

Ordinary user questions asked while reading a paper or source tree remain in Source Digest, Claim-Evidence Ledger, Associated Source Code, or another applicable reading Artifact. They do not become Mindset Record rows by default. The repeatable collector asks only whether the user explicitly assigned additional questions to that Record.

Apply explicit targets as follows:

| Target | Effect |
| --- | --- |
| Source only | Directly validate and edit the current topic Source; add no active Record row. |
| Record only | Add the bounded supplemental row and use `record_only`; preserve the current Source. |
| Both | Add the Record row, move `source_update_requested` to `source_updated`, and record the new Source relative path and digest while the active Record retains its original snapshot. |

Clarify a bare request to “update the mindset” when the requested mutation makes Source versus Record material. Conflicting, impossible, or unauthorized questions remain unresolved or not applicable with rationale.
