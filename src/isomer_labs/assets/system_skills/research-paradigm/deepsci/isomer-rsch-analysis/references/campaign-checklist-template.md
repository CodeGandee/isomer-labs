# Analysis Evidence Gate Checklist

Use this reference as a compact acceptance-boundary checklist when it helps. It is optional; the hard requirement is durable, unambiguous launched slices, evidence boundaries, blockers, and next routes. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Identify the current frontier**. Record parent object, parent claim or gap, route, campaign id if any, next slice or blocker, active uncertainty, and the next route if the gate clears or fails.
2. **Apply the resource gate**. Check device, memory, storage, wall-clock, dependency, credential, and service limits when they affect design; tag each planned slice as runnable now, runnable with downscope, or blocked by resources.
3. **Apply the evidence gate**. Confirm each launched slice has an outcome or monitoring path, evidence-bearing fields, claim update, comparability verdict, and visible non-success states.
4. **Apply the comparability gate**. Check that the main comparison contract is preserved or deviations are labeled as generalization, stress test, boundary, failure analysis, or non-comparable evidence.
5. **Apply the paper or review gate**. Verify paper-ready or reviewer-facing slices map to write-back targets and that stale paper contracts are treated as blockers.
6. **Close out honestly**. Summarize the strongest evidence boundary, classify the parent claim, and record the next route.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a checklist only when it reduces ambiguity (if the analysis is tiny, otherwise keep the gate in the route record).
- Prefer explicit blocked high-value slices over silent omission (if a slice is infeasible, otherwise tag it).
- Prefer closeout categories that separate strengthened, weakened, narrowed, abandoned, and ambiguous outcomes (if the evidence is mixed, otherwise state that).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <ANALYSIS_CAMPAIGN_CHECKLIST> must not replace slice records.
- The current frontier must be explicit before additional slices are launched.
- Paper or review closeout must not be marked complete when write-back targets are stale or missing.
- Closeout must not hide null, negative, failed, partial, blocked, infeasible, or contradictory findings.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Checklist completion: fraction of objective, resource, evidence, comparability, paper/review, and closeout checklist items satisfied or explicitly waived; higher is better.
- Unresolved route item count: number of checklist items whose failure would change continue, write, experiment, idea, decision, stop, or blocker routing; lower is better.

### Checks

- Frontier gate: next slice, aggregation, blocker, or route decision is explicit.
- Resource gate: planned slices are screened against current limits.
- Evidence gate: launched slices have durable outcomes, evidence fields, claim updates, and comparability verdicts.
- Comparability gate: preserved or changed comparison contracts are labeled correctly.
- Paper gate: writing-facing outputs map to current paper or review targets.
- Closeout gate: strongest boundary, claim status, and next route are recorded.

## Template

### Identity

- parent object:
- parent claim or gap:
- route:
- campaign id:

### Current Frontier

- [ ] next slice, aggregation, blocker, or route decision is explicit
- [ ] active uncertainty is written as a concrete question
- [ ] next route is known if this gate clears or fails

### Resource Gate

- [ ] current device, memory, storage, dependency, credential, service, and wall-clock limits are explicit when they affect campaign design
- [ ] planned slices have been screened as runnable now, runnable with downscope, or blocked by resources
- [ ] blocked high-value slices are recorded explicitly rather than silently dropped
- [ ] the current frontier is prioritized by soundness gain under the real resource budget

### Evidence Gate

- [ ] parent claim, paper gap, reviewer item, rebuttal item, or decision being tested is explicit
- [ ] each launched slice has a durable outcome or active monitoring path
- [ ] evidence-bearing slices record question, intervention or inspection target, fixed conditions, metric or observable, and evidence source
- [ ] claim update and comparability verdict are explicit
- [ ] null, negative, partial, failed, blocked, infeasible, superseded, or contradictory findings are visible
- [ ] campaign-level interpretation is backed by per-slice evidence

### Comparability Gate

- [ ] baseline or main comparison contract is preserved, or deviation is recorded
- [ ] new dataset, split, metric, or protocol changes are labeled as generalization, stress test, boundary, failure analysis, or non-comparable evidence
- [ ] additional comparators do not overwrite the canonical comparator basis

### Paper or Review Gate

- [ ] paper-ready or reviewer-facing slices map to outline, paper matrix, evidence ledger, section, claim, table, reviewer item, or rebuttal item
- [ ] if a writing-facing slice is complete, the write-back target is updated or the stale contract is recorded as a blocker

### Blocked Boundary

- [ ] if blocked, the failure class is explicit
- [ ] if blocked, tried steps and evidence sources are recorded
- [ ] if blocked, next best move is continue, redesign, return to experiment, return to idea, write, decision, stop, or reset

### Closeout

- [ ] strongest evidence boundary is summarized
- [ ] main claim is classified as strengthened, weakened, narrowed, abandoned, or still ambiguous
- [ ] next route recorded explicitly
