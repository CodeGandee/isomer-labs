# Analysis Slice Record Template

Use this reference to record one follow-up analysis slice before campaign-level interpretation. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Identify the slice**. Record parent object, parent claim or gap, slice id, slice class, evidence question, intervention or inspection target, and why this slice matters now.
2. **Record fixed and changed conditions**. State controls, fixed conditions, metric or observable, comparison target, and what changed.
3. **Attach evidence**. Record evidence source, command or inspection basis, output pointers, metric values or observations, and resource or execution caveats.
4. **Classify the outcome**. Mark completed, partial, failed, blocked, infeasible, superseded, or read-only audit.
5. **Update the claim**. State claim update, comparability verdict, caveat, paper or review mapping when relevant, and next action.
6. **Keep slice boundaries clean**. Do not merge multiple interventions into one slice record unless the combined intervention is the tested object.

## Preferences

- Prefer one record per evidence-bearing slice (if a read-only audit answers the question, otherwise record it as an audit rather than a launched slice).
- Prefer semantic slice ids that can survive later write-back (if paper metadata exists, otherwise align ids with <ANALYSIS_WRITEBACK_MAP>).
- Prefer concrete metrics, observables, tables, examples, or rubrics over broad prose (if qualitative evidence is used, otherwise record the inspection basis).

## Constraints

- <ANALYSIS_SLICE_RECORD> must include question, intervention or inspection target, fixed conditions, metric or observable, evidence source, claim update, comparability verdict, and next action.
- A slice record must not claim direct support when comparison was non-comparable.
- A failed or infeasible slice must not be silently replaced by another slice without recording the non-success status.
- Multiple changed factors must not be interpreted as isolating one factor.

## Quality Gates

### Metrics

- Slice-record field coverage: fraction of slice id, class, parent object, evidence question, intervention or inspection target, fixed conditions, metric or observable, evidence path, claim update, comparability verdict, and next action fields completed; higher is better.
- Missing-evidence-path count: number of evidence-bearing slices without inspectable evidence paths or source records; lower is better.

### Checks

- Identity gate: parent object, parent claim or gap, slice id, slice class, and evidence question are present.
- Evidence gate: metric, observable, table, qualitative artifact, rubric, or inspection trace is recorded.
- Comparability gate: changed and fixed conditions are explicit.
- Outcome gate: status, claim update, caveat, and next action are stated.
- Reuse gate: later writing, decision, or experiment stages can understand what the slice proves, weakens, clarifies, or blocks.

## Template

### Slice Identity

- parent object:
- parent claim or gap:
- slice id:
- slice class:
- evidence question:
- why now:

### Execution and Evidence

- intervention or inspection target:
- fixed conditions:
- changed conditions:
- metric or observable:
- comparison target:
- evidence source:
- output pointers:
- resource or execution caveats:

### Interpretation

- status:
- claim update:
- comparability verdict:
- caveat:
- paper or review mapping:
- next action:
