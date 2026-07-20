# Research Outline Template

Use this reference when idea work needs a durable research-outline style note before selecting or defending a final direction. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Write an executive summary**. State purpose, current result, dataset characteristics, core algorithm, major limitations, and performance gap.
2. **Analyze the codebase**. Name major modules, data flow, key classes or functions, dependencies, computational hotspots, evaluation pipeline, and improvement-potential ratings.
3. **Analyze dataset and metrics**. State dataset constraints, metric direction, evaluation contract, and success criteria.
4. **Formulate the problem**. Add notation, objective, constraints, complexity or theoretical limits when relevant, and three to five subproblems.
5. **Characterize baselines**. Treat baseline methods as special cases or constrained solutions, naming extension potential and theoretical gaps.
6. **List directions**. Produce exactly five actionable directions when the space is broad enough, each with challenge, approach, implementation sketch, metrics, risks, and claim boundary.
7. **Record infrastructure constraints**. Include runtime, compute, queue, data, and repository constraints that affect feasibility.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer an outline-style note when the Research Topic needs a serious plan artifact (if the task is tiny, otherwise keep the outline light).
- Prefer direct code and metric grounding over abstract method prose.
- Prefer exactly five directions only when the search space is broad enough (if the space is tiny, otherwise state why fewer directions are enough).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:RESEARCH-OUTLINE-NOTE must not replace literature survey or selected-idea handoff records.
- Direction entries must include both conceptual thrust and repo-grounded translation.
- Baseline characterization must not ignore the accepted comparator basis.
- The outline should not force a paper structure when the route is only an algorithm-first optimization brief.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Decomposed sub-problem count: number of decomposed sub-problems in the outline; closer to 3-5 is better.
- Direction count: number of proposed research directions when the space is broad enough; closer to exactly 5 is better.

### Checks

- Grounding gate: the outline links objective, code, data, metric, comparator, and constraints.
- Direction gate: candidate directions are actionable and not only slogans.
- Feasibility gate: each direction includes implementation surface, success metric, risk, and abandonment cue.
- Planning gate: the note clarifies what evidence future experiment or writing stages must maintain.
