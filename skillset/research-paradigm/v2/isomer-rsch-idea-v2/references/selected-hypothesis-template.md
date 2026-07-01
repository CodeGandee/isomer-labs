# Selected Hypothesis Template

Use this reference to create the selected route handoff after `references/selection-gate.md` passes. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Name the selected object**. Give <SELECTED_HYPOTHESIS> a stable id, two-sentence pitch, and one falsifiable claim.
2. **Tie the claim to measurement**. Include metric key, expected direction, boundary condition, minimal experiment, and abandonment condition.
3. **Explain mechanism and alternatives**. State the mechanism sketch, strongest alternative hypothesis, strongest objection, and anti-win condition.
4. **Bind to evidence**. Reference <LITERATURE_SURVEY_REPORT>, <RELATED_WORK_MAP>, closest prior work, comparator evidence, and <PRE_IDEA_DRAFT>.
5. **Prepare the draft**. Create <SELECTED_IDEA_DRAFT> with SCQA or pyramid structure, citation markers, standard-format references, code-level plan, and risks.
6. **Choose next route**. Create <IDEA_ROUTE_DECISION> for experiment, optimize, scout, baseline, decision, branch, reject, or blocker.

## Preferences

- Prefer one falsifiable claim over a bundle of loosely related ideas (if multiple claims survive, otherwise record a branch or decision route).
- Prefer citation-supported motivation and mechanism over casual paper mentions (if citation style is unspecified, otherwise use one consistent standard style).
- Prefer `continue_line` style routing for a child of the current route and branch-style routing for sibling alternatives when the runtime supports lineage semantics.

## Constraints

- <SELECTED_HYPOTHESIS> must include id, pitch, hypothesis, mechanism, expected effect, comparator relation, risk, falsification, minimal test, abandonment condition, citations, and next route.
- <SELECTED_IDEA_DRAFT> must cite papers that shaped the mechanism, motivation, novelty check, or claim boundary.
- The selected route must not omit the strongest alternative hypothesis or strongest likely objection.
- The selected route must not be submitted before the literature survey and pre-idea draft gates are satisfied.

## Quality Gates

### Metrics

- Handoff-field coverage: fraction of id, pitch, hypothesis, mechanism, expected effect, comparator relation, risk, falsification, minimal test, abandonment condition, citations, and next route recorded; higher is better.
- Missing alternative count: number of selected-route handoffs without strongest alternative hypothesis, strongest likely objection, or anti-win condition; lower is better.

### Checks

- Handoff completeness: the next stage can run from the handoff without reconstructing metric, code surface, prior work, falsifier, or abandon rule.
- Citation quality: references are standard-format and tied to actual route-shaping papers.
- Claim quality: the claim is falsifiable, scoped, and tied to the accepted comparator basis.
- Route quality: <IDEA_ROUTE_DECISION> explains why the next stage is experiment, optimize, scout, baseline, decision, branch, reject, or blocked.
