# Evidence Ladder

Use this reference to choose an evidence target proportional to the claim. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Classify the run role**. Mark the run as `auxiliary/dev` when it clarifies parameters, settings, mechanisms, or diagnostics; mark it as `main/test` when it carries the core comparison.
2. **Choose the ladder level**. Use `minimum` for executable and comparable evidence, `solid` for evidence strong enough to carry the main claim, and `maximum` for broader polish after credibility exists.
3. **Match effort to the current claim**. Spend first on comparability and claim-carrying evidence; defer broad polish until the result is at least solid.
4. **Separate supplementary signals**. Keep non-canonical metrics, diagnostics, and exploratory checks as supplementary evidence unless the contract has explicitly changed.
5. **Reassess after the run**. Use the observed metrics, caveats, and uncertainty to decide whether the next route is analysis, writing, optimization/frontier review, another experiment, reset, stop, or explicit decision.

## Preferences

- Prefer `minimum` evidence first when the execution path or comparability is still uncertain (if the path is already verified, otherwise move toward `solid`).
- Prefer `solid` evidence before writing or claim promotion (if the result is only executable, otherwise keep it as a partial signal).
- Prefer `maximum` polish only after the main claim is credible (if the claim is not yet solid, otherwise use resources on the decisive gap).
- Prefer marking auxiliary evidence as auxiliary (if it cannot carry the main claim, otherwise state why it is main evidence).

## Constraints

- Main-claim promotion must not proceed from smoke, pilot, or non-comparable evidence.
- Maximum-level polish must not consume the run before minimum and solid gates are satisfied.
- Supplementary metrics must not replace required comparator metrics.
- Evidence level should be downgraded when metrics are incomplete, non-finite, unstable, or not traceable to outputs.

## Quality Gates

### Metrics

- Evidence level: achieved evidence level on the source minimum, solid, maximum ladder; higher is better only after the comparison contract is preserved.
- Claim-critical gap count: number of unresolved main-result, robustness, sensitivity, or claim-critical follow-up gaps still blocking the target evidence level; lower is better.

### Checks

- Level clarity: the run is labeled `auxiliary/dev` or `main/test`, and `minimum`, `solid`, or `maximum`.
- Minimum gate: commands finish, required outputs exist, and the comparison remains comparable.
- Solid gate: required metrics are complete and traceable, caveats are bounded, and the result can support or refute the selected hypothesis.
- Maximum gate: extra ablations, robustness checks, figures, or polish add claim-level value rather than masking missing main evidence.
- Route gate: the chosen next route follows from the evidence level and claim status.
