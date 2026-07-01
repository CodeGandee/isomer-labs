# Comparability Contract

Use this reference to define the comparison basis that later work must not guess. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Record comparator identity**. State baseline id, variant when relevant, source paper, source repository, source commit or package version, local service identity, registry/package identity, and provenance.
2. **Record task and data contract**. State task identity, dataset identity, split contract, evaluation path, expected outputs, and any direct-comparison limits.
3. **Record metric contract**. State required metric ids, metric directions, primary metric, supplementary metrics, derivation or origin path, and source reference for each canonical metric.
4. **Record deviations and caveats**. Name known differences from paper, source package, local reference, registry package, service behavior, environment, or selected target.
5. **Classify the verdict**. Use verified match, verified close, verified diverged, trusted with caveats, broken, waived, or blocked.
6. **Prepare handoff fields**. Ensure <COMPARABILITY_CONTRACT> and <BASELINE_PAYLOAD_RECORD> are sufficient for downstream idea, experiment, analysis, or decision work.

## Preferences

- Prefer the original paper's evaluation protocol as the starting point (if the user specifies another comparator, otherwise record that route).
- Prefer a core contract for comparison-ready baselines (if paper claims, registry publication, or variant-heavy comparison need more coverage, otherwise expand).
- Prefer richer existing structured results over a thinner hand-written scalar (if a leaderboard, result file, or metric contract exists, otherwise summarize minimally).
- Prefer preserving both aggregate and per-dataset or per-task metrics when the source reports both (if feasible, otherwise record the missing coverage).

## Constraints

- <COMPARABILITY_CONTRACT> must include task, dataset, split, evaluation path, required metric ids, metric directions, source identity, known deviations, and caveats.
- The primary metric must not erase the rest of the comparison surface.
- Supplementary metrics must not replace required canonical metrics.
- If downstream experiment work would still need to guess required metric ids or directions, the baseline is not ready.
- A caveat must not hide a different dataset split, evaluation script, source identity, or comparison meaning.

## Quality Gates

### Metrics

- Core contract field coverage: fraction of comparator identity, task, dataset, split, evaluation path, required metric keys, metric directions, source identity, known deviations, and caveats recorded; higher is better.
- Downstream-guesswork count: number of comparator, metric, provenance, or caveat questions later stages would still need to infer; lower is better.

### Checks

- Identity gate: comparator id, variant, source, and provenance are stable enough to cite.
- Data gate: task, dataset, split, evaluation path, and expected outputs are explicit.
- Metric gate: required metric ids, directions, primary metric, supplementary metrics, and derivation or origin paths are recorded.
- Deviation gate: known differences and caveats are visible.
- Verdict gate: verified match, verified close, verified diverged, trusted with caveats, broken, waived, or blocked is justified by evidence.
- Handoff gate: later stages can compare without guessing.
