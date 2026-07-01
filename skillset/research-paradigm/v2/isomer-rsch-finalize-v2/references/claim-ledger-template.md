# Claim Ledger Template

Use this reference to classify final claim status. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **List important claims**. Include supported claims, partial claims, weakened claims, failed claims, deferred claims, and claims intentionally not made.
2. **Classify status**. Mark each claim as supported, partially supported, unsupported, or deferred.
3. **Attach evidence and caveats**. Record evidence pointers, caveats, comparability limits, safe-to-surface status, and whether the claim may appear in summary, writing, publication, or handoff material.
4. **Preserve downgrade history**. If a claim moved from supported to partial, partial to unsupported, promising to abandoned, or draft-ready to evidence-gap, record what changed and why.
5. **State recommendation**. Give the final recommendation for each claim: surface, narrow, defer, reject, or revisit.

## Preferences

- Prefer honest partial or unsupported labels over optimistic claim smoothing.
- Prefer preserving weakened claims with downgrade history over silently deleting them.
- Prefer evidence pointers over broad claim prose when later agents may need to inspect support.

## Constraints

- <CLAIM_LEDGER> must classify every important claim as supported, partially supported, unsupported, or deferred.
- Each claim must include evidence, caveats, safe-to-surface status, and recommendation.
- Claims that were once believed and later weakened must preserve the belief-change reason.
- Unsupported claims must not appear in final summary as supported findings.

## Quality Gates

### Metrics

- Claim classification coverage: fraction of important supported, partial, weakened, failed, deferred, and intentionally unmade claims classified with status, evidence, caveats, surface-safety, and recommendation; higher is better.
- Missing downgrade-history count: number of weakened claims without a recorded belief-change reason; lower is better.

### Checks

- Claim coverage: every important outcome and major negative result is represented.
- Evidence traceability: each claim has inspectable evidence or a clear absence of support.
- Caveat quality: claim limits are concrete enough to prevent overclaiming.
- Surface safety: future writing or handoff work can tell which claims are safe to use.
