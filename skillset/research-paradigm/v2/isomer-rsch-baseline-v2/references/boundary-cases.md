# Baseline Boundary Cases

Use this reference when the baseline route is not blocked but the success boundary still feels fuzzy. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Separate comparison-ready from paper-repro-ready**. Accept comparison-ready when downstream work can compare without guessing, and reserve paper-repro-ready for paper-facing reproduction or publication needs.
2. **Handle trusted-with-caveats honestly**. Accept caveats only when they do not silently change comparison meaning.
3. **Reject weak-provenance metrics**. Route to verify-local-existing, reproduce, or blocker when numbers cannot be tied to real outputs, service responses, source records, or package evidence.
4. **Clarify local paths before full reproduction**. Check evaluation entrypoint, output location, split, and metric contract before escalating.
5. **Avoid heavier-but-not-more-trustworthy routes**. Do not replace a working comparison-ready comparator unless the heavier route removes a named risk.
6. **Stop repeated no-evidence failures**. Record blocker, switch route, repair, waive, or route through decision when failure repeats without new information.

## Preferences

- Prefer comparison-ready when the next scientific step only needs fair comparison (if paper claims or registry publication require more, otherwise expand).
- Prefer caveated acceptance over false exactness (if caveats do not change comparison meaning, otherwise block or repair).
- Prefer clarifying concrete local evidence before reproducing from scratch (if path and metrics stay ambiguous, otherwise reproduce).
- Prefer stopping repeated failures over another unchanged retry (if no new evidence exists, otherwise change route).

## Constraints

- Comparison-ready must still include a durable core metric contract.
- Trusted-with-caveats must not hide dataset, split, metric, evaluation, or source-identity changes.
- Imported metrics with weak provenance must not be accepted.
- A heavier route must not be chosen only because it feels cleaner.
- Repeated failure with no new evidence must not continue silently.

## Quality Gates

### Metrics

- Boundary-case classification coverage: fraction of comparison-ready, trusted-with-caveats, weak-provenance, local-path, heavier-route, and repeated-failure cases classified with an explicit route; higher is better.
- Weak-provenance metric count: number of imported or local metric values accepted without real outputs, services, source records, or package records; lower is better.

### Checks

- Comparison gate: downstream work can compare without guessing task, split, metric, or comparator identity.
- Caveat gate: caveats are explicit and do not change comparison meaning.
- Provenance gate: metrics tie to real outputs, services, source records, or package records.
- Local path gate: entrypoint, output location, split, and metric contract are checked before full reproduction.
- Stop gate: repeated failures route to blocker, repair, waiver, decision, or route switch.

## Boundary Cases

- Comparison-ready but not paper-repro-ready: acceptable for downstream comparison when exact paper setup, broader variant tables, or reusable packaging are not needed yet.
- Trusted with caveats: acceptable when the main comparator remains honest and the caveat is explicit.
- Imported metrics with weak provenance: not acceptable without real evidence.
- Local path exists but exact comparator is unclear: inspect entrypoint, output, split, and metric contract before reproduction.
- Route feels cleaner but not more trustworthy: heavier route is justified only by a named unresolved risk.
- Repeated failure with no new evidence: stop looping and route.
