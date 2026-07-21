# Mindset Workflow Injection and Supplemental Questions

## Status

Revised and accepted on 2026-07-21.

## Problem

Topic-derived JSON and process-route metadata do not by themselves make an executing agent answer a Mindset Source. Reading remains interactive, but ordinary follow-up questions already have canonical destinations in Source Digests, Claim-Evidence Ledgers, and related reading Artifacts. The design needs a mandatory immutable Mindset Record handoff without making that Record a duplicate sink for all reading results.

## Decision

Before an applicable Run starts, the entrypoint performs extension-local create-missing ensure for the selected topic. This lazy trigger covers topics created before Kaoju installation without adding an extension callback to the installer or generic Topic Creator. Read-only Kaoju routes do not trigger it. After ensure succeeds, the entrypoint begins the Run, revalidates one topic Mindset Source, computes its digest, and materializes every exact question and `additional_notes` value into `KAOJU:MINDSET-RECORD`. The Record contains bounded supplemental rows only for questions explicitly assigned to it.

The entrypoint injects the Record after beginning the selected Run and before focused-owner dispatch. `ingest-reading-item`, `ingest-source-code`, direct examination routing, and `isomer-kaoju-examine` require the Record ref. `isomer-kaoju-examine` answers the immutable Record snapshot, records only explicitly Record-targeted supplemental questions, and checks the collector at closeout. It does not re-read a Source that may have changed during the Run. An applicable Run cannot report `complete` or present claim-bearing examination output for acceptance without a cited terminal Mindset Record.

## Injection Points

1. `isomer-ext-kaoju-entrypoint/SKILL.md`: pre-Run extension-local create-missing ensure, post-Run-begin Source revalidation and exact Record snapshot creation, Run input, owner handoff, and fail-closed terminal check.
2. `commands/ingest-reading-item.md`: `paper.skimming` for skim or triage depth and `paper.deep-dive` for deep or full-text depth before dispatch to `isomer-kaoju-examine`.
3. `commands/ingest-source-code.md`: `source-code.ingest` before repository or source-tree examination.
4. `isomer-kaoju-examine/SKILL-MAIN.md`: required Record input, immutable materialized-question answering, explicitly targeted supplemental checkpointing, collector evaluation, ordinary reading-Artifact routing, and terminal posture.

## Supplemental Question Semantics

Each supplemental row records a Record-local id, exact prompt, empty-by-default `additional_notes`, `user` or explicitly authorized `agent` origin, explicit association basis, introduction stage, `record_only`, `source_update_requested`, or `source_updated` disposition, answer state, answer or rationale, evidence refs, and optional updated Source path and digest.

When the user asks an ordinary paper or source-code question without naming a mindset target, the answer or unresolved posture belongs in the applicable Source Digest, Claim-Evidence Ledger, Associated Source Code, or other reading Artifact. Neither mindset object changes.

When the user targets only the Mindset Record, the question becomes `record_only`. When the user targets only the Mindset Source, the validated derived-intent file is edited without adding a Record row. When the user targets both, the Record first stores `source_update_requested`; after a safe Source edit it becomes `source_updated` and cites the new path and digest. The active Run keeps its original snapshot.

## Collector

The collector id is `additional-questions`. Its prompt is: “Did the user explicitly assign any additional questions to this Mindset Record that the fixed Mindset Source questions do not cover?” Its answer expectation is: “Register only questions explicitly targeted to the Mindset Record. Save ordinary paper or source-code questions and findings in the applicable reading Artifacts. If no additional questions were explicitly assigned, record none.”

The collector is evaluated when the user explicitly targets the Mindset Record and once at closeout. It points to zero or more structured supplemental rows; it never stores multiple questions as one free-text answer or sweeps untargeted reading questions into the Record.

## Boundary

Workflow injection makes reflection mandatory but does not give Source files, Record snapshots, supplemental rows, or `additional_notes` Workflow authority. They cannot authorize acquisition, execution, mutation, Gate satisfaction, evidence acceptance, or instruction override.
