# Method Brief Template

Use this reference to shape <METHOD_BRIEF> or <CANDIDATE_BRIEF> fields before ranking or promotion. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the candidate**. Give one short title and candidate id when available.
2. **State bottleneck and limitation**. Explain the concrete bottleneck and why the current line or baseline is not already solving it.
3. **State mechanism and family**. Describe the intervention and classify its mechanism family.
4. **Classify change layer**. Use `Tier1` for local optimization/training detail, `Tier2` for representation or component change, and `Tier3` for paradigm or system-level shift.
5. **Record source lens and keep-unchanged contract**. State whether it comes from baseline refinement, orthogonal mechanism, failure repair, transfer, objective shift, or search widening, and what must stay fixed.
6. **Record expected gain, implementation surface, risks, foundation, promote-now status, and next target**.

## Preferences

- Prefer concrete bottlenecks over generic performance goals (if the bottleneck is unclear, otherwise return to brief shaping).
- Prefer explicit mechanism family and change layer (if classification is hard, otherwise explain uncertainty).
- Prefer expected gain tied to measurable evidence (if gain is qualitative, otherwise state observable).
- Prefer `promote_now: no` when the brief lacks comparability or mechanism clarity.

## Constraints

- <METHOD_BRIEF> must not omit keep-unchanged conditions.
- Change layer and mechanism family must not be left implicit.
- Implementation surface must distinguish local, moderate, and broad scope.
- Promotion status must include why.

## Quality Gates

### Metrics

- Brief-field coverage: fraction of title, bottleneck, limitation, mechanism, family, change layer, source lens, keep-unchanged contract, expected gain, implementation surface, risk, foundation, promote-now status, and next target completed; higher is better.
- Implicit-comparability count: number of method briefs missing keep-unchanged conditions despite expected comparison or promotion; lower is better.

### Checks

- Bottleneck gate: limitation is concrete.
- Mechanism gate: intervention, family, and change layer are explicit.
- Comparability gate: keep-unchanged contract is present.
- Evidence gate: expected gain and next target are measurable or observable.
- Promotion gate: promote-now status is justified.

## Template

### Title

- candidate title:

### Bottleneck

- bottleneck:
- why current line is limited:

### Mechanism

- intervention:
- mechanism family:
- change layer:
- source lens:

### Comparability

- keep unchanged:
- expected gain:

### Implementation

- likely files or modules:
- change scope:
- risks:

### Foundation and Next Target

- source branch, run, or baseline:
- why this foundation:
- promote now:
- next target:
