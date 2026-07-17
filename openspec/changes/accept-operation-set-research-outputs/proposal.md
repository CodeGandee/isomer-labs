## Why

The incident documented in `context/issues/known/20260716-operation-set-outputs-not-recorded-in-db.md` predates the v0.4.0 Research Idea portfolio contract and the manual repair of the Flash Attention 4 Topic Workspace. Current Isomer already supports atomic durable-record creation, canonical record lineage, explicit `research_idea_effects`, and GUI-visible Research Ideas; the affected topic data no longer needs migration through this change.

The remaining systemic gap is at workflow closeout. A research operation can still finish with valuable reports, evidence, code, and notes left only in a worker output set because no machine-verifiable coordinator proves that every staged file was either accepted through the current record-and-idea transaction or intentionally discarded. This change prevents the historical omission from recurring; it does not replace the current data model or repair the already corrected topic.

## What Changes

- Add a provider-neutral Operation Set Acceptance contract that inventories every file in one resolved worker operation set and classifies it as a durable record payload, a durable record attachment, or explicitly disposable with a reason.
- Add `isomer-cli ext research operation-sets inspect`, `accept`, and `verify` commands. The commands validate path containment, file digests, record bindings, immediate record parents, and requested Research Idea effects before mutation, then apply a deterministic, resumable acceptance plan and persist an acceptance receipt.
- Implement the coordinator as a thin orchestration layer over the existing research-record create, revise, lineage, query-index, and atomic Research Idea mutation paths. It defines no replacement Research Idea schema, lifecycle vocabulary, decision model, lineage store, or GUI projection.
- Leave current Topic Workspace records and Research Ideas unchanged unless a caller explicitly accepts a selected operation set. Legacy inspection and repair remain opt-in tools, not an installation migration or a prerequisite for the already repaired Flash Attention 4 data.
- Treat acceptance as opt-out: an operation set cannot reach a complete receipt while a discovered material file lacks an accepted-record mapping or an explicit disposable disposition.
- Add a core `isomer-research-operation-set-recording` skill that guides inspection, manifest authoring, acceptance, verification, recovery from partial application, and legacy operation-set repair.
- Add a mandatory DeepSci closeout step after end callbacks. Production DeepSci skills that write operation-set files must return durable record refs and a complete acceptance receipt before reporting success; otherwise they pause with actionable diagnostics.
- Require `isomer-deepsci-pipeline` to validate each stage's accepted refs and receipt before handing outputs to the next stage or emitting `status: complete`.
- Extend packaged-skill and research-paradigm validation so missing closeout guidance, unverified terminal reports, and stale direct-file completion claims fail validation.

## Capabilities

### New Capabilities

- `operation-set-research-acceptance`: Defines operation-set manifests, exhaustive output dispositions, preview/apply/verify behavior, durable acceptance receipts, idempotent recovery, and coordination with record lineage and Research Idea effects.

### Modified Capabilities

- `worker-output-root-policy`: Requires every material operation output set to be reconciled at closeout instead of remaining an unclassified plain-file directory.
- `research-paradigm-skills`: Requires production DeepSci workflows and their validation harness to invoke and verify operation-set acceptance before successful completion.
- `isomer-deepsci-pipeline`: Requires stage handoffs and terminal reports to consume accepted durable refs and complete operation-set receipts rather than file paths alone.
- `isomer-op-entrypoint-skill`: Makes operation-set inspection, acceptance, verification, and repair discoverable through the focused recording skill and CLI family.
- `packaged-system-skills`: Adds the provider-neutral operation-set recording skill to the core packaged skill inventory.

## Impact

- Adds an additive Workspace Runtime acceptance-receipt model and migration, plus a research operation-set coordinator layered over the existing record and Research Idea stores.
- Adds a new `ext research operation-sets` CLI group while preserving all current `ext research records` and `ext research ideas` commands.
- Updates packaged core research-skill assets, DeepSci shared guidance, focused DeepSci workflows, pipeline recipes, operator routing indexes, documentation, and validators.
- Adds regression coverage proving that direct record creation, atomic `research_idea_effects`, canonical idea queries, and current GUI-facing contracts retain their v0.4.0 behavior, plus acceptance coverage for exhaustive manifests, path safety, dry-run planning, lineage ordering, idempotent replay, partial-apply recovery, optional legacy repair, and terminal completion gates.
- Introduces no external dependency, no Research Idea or GUI data-contract migration, and no automatic acceptance of existing worker output sets; legacy sets remain available for explicit inspection and repair.
