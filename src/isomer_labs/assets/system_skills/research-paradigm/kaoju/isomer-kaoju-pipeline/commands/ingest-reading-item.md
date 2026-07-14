# Ingest Reading Item

## Workflow

1. Resolve the exact Reading List item, version family, source class, requested inspection depth, and existing Artifact Library entry from the state DB.
2. Use `$isomer-kaoju-acquire` for artifact-library-first lookup. Acquire by source type and use an authorized online fallback only when local material cannot satisfy the accepted depth.
3. Preserve inaccessible sources as `kaoju:source-access-blocker`; never reconstruct missing evidence from snippets or memory.
4. Use `$isomer-kaoju-examine` to inspect the primary work and linked material. Record exact page, section, equation, figure, table, or immutable commit plus file and line locators.
5. Keep source statements, interpretation, provisional visual evidence, code findings, and executed behavior distinct. Verify provisional figure or table evidence before promotion.
6. Persist or revise `kaoju:artifact-library`, `kaoju:associated-source-code`, `kaoju:source-digest`, and `kaoju:claim-evidence-ledger` as applicable, then present them for approval or refinement.

## Owner, Inputs, and Outputs

Owners: `$isomer-kaoju-acquire` and `$isomer-kaoju-examine`. Inputs: Reading List ref and item id. Outputs: acquired-material, Source Digest, Claim-Evidence Ledger, associated-code, blocker, and provenance refs.

## Gates, Blockers, and Resume

Human acceptance governs claim-bearing digest output. Resume from lookup, acquire, inspect, verify-visual, refine, or approve using the recorded blocker and Run refs.
