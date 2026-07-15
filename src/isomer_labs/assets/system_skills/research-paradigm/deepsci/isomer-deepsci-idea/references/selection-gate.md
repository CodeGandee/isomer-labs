# Selection Gate And Handoff

Use this reference when choosing the final idea and preparing the handoff to experiment or optimize. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Score value and feasibility**. Score importance, novelty, feasibility, verifiability, report or paper potential, failure value, and boundary-changing potential.
2. **Apply FINER-style checks**. Confirm the route is feasible, interesting, meaningfully novel or valuable, acceptable under the Research Topic constraints, and relevant to an important bottleneck.
3. **Run the lightweight quality gate**. Score novelty, falsifiability, feasibility, evidence quality, and constraint fit on a zero to two scale.
4. **Assign an honest label**. Mark the route as `novel`, `incremental but valuable`, or `not sufficiently differentiated`.
5. **Check mechanism and falsification**. Require core hypothesis, mechanism sketch, strongest falsification experiment, anti-win condition, minimal validation, and abandonment condition.
6. **Prepare handoff fields**. Create DEEPSCI:SELECTED-HYPOTHESIS, DEEPSCI:SELECTED-IDEA-DRAFT, and DEEPSCI:IDEA-ROUTE-DECISION with metric key, expected direction, boundary condition, code-level plan, relation to literature, references, and next route.
7. **Route non-selected outcomes**. Create DEEPSCI:IDEA-BLOCKER-RECORD or a branch, reject, return-to-scout, baseline, decision, or optimize route when selection is not justified.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer `novel` routes when they remain feasible (if novelty is limited, otherwise require concrete incremental value).
- Prefer the best evidence-per-run route over the most exciting-sounding route.
- Prefer rejecting decorative tweaks unless the survey and current evidence show they are the highest-value surviving route.
- Prefer blocking or routing back to scout when literature coverage is too weak to judge novelty.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- A candidate with quality-gate total below seven out of ten must not be promoted without refinement.
- DEEPSCI:SELECTED-HYPOTHESIS must include a falsifiable claim tied to metric, expected direction, and boundary condition.
- DEEPSCI:SELECTED-IDEA-DRAFT must include citation markers and a standard-format reference list for papers that shaped the route.
- The selection gate must not promote a route with vague mechanism, vague falsification path, missing survey, or incomplete handoff contract.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Value-screen score: average or total score across importance, novelty, feasibility, verifiability, report or paper potential, failure value, and boundary-changing potential on the source 1-5 scale; higher is better.
- Lightweight quality total: sum of novelty, falsifiability, feasibility, evidence quality, and constraint fit on the source 0/1/2 scale; higher is better, and at least 7 out of 10 is required for promotion.
- Usable related-paper count: number of related and usable papers already covered by the survey before paper-ready promotion; higher is better until the usual 5-10 paper range is satisfied.

### Checks

- Value gate: the route passes importance, feasibility, verifiability, failure value, and relevance checks.
- Novelty gate: the route is `novel` or `incremental but valuable`, not `not sufficiently differentiated`.
- Evidence gate: literature, comparator evidence, and pre-idea draft support the selection.
- Handoff gate: the next stage can execute from DEEPSCI:SELECTED-HYPOTHESIS without guessing about metric, code touchpoints, falsification, abandonment, or references.
