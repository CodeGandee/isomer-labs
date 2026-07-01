# Experiment Contract

Use this reference to fix one measured run before code or compute work starts. This page distills the source entrypoint's run-contract, planning, and readiness rules into native Isomer language. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Recover the ready context**. Gather selected hypothesis, accepted comparator basis, metric contract, current workspace, recent decisions, user constraints, and any prior incident or failure pattern into <EXPERIMENT_CONTEXT_BRIEF>.
2. **Classify the evidence target**. Choose `auxiliary/dev` or `main/test`, then choose `minimum`, `solid`, or `maximum` using `references/evidence-ladder.md`.
3. **Write the research contract**. State run id, research question, null hypothesis, alternative hypothesis, selected hypothesis, research type, research objective, and the observation that would answer the question.
4. **Freeze the comparison contract**. State comparator id or variant, dataset, split, required metric keys, primary metric, evaluator assumptions, expected outputs, stop condition, abandonment condition, compute budget, and strongest alternative hypothesis.
5. **Choose the planning surface**. Create <EXPERIMENT_PLAN> and <EXPERIMENT_CHECKLIST> for substantial, expensive, branch-sensitive, or long-running work; otherwise keep a compact contract that still preserves route, comparability boundary, command path, outputs, and fallback.
6. **Record material changes**. If the code path, comparability contract, runtime strategy, or execution route changes materially, revise <EXPERIMENT_CONTRACT> and <EXPERIMENT_PLAN> before spending more code or compute.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer one bounded research question over a broad execution agenda (if the request bundles several questions, otherwise keep the single route intact).
- Prefer the experiment package with the best balance of technical feasibility, research importance, and methodological rigor (if several packages are possible, otherwise use the selected route).
- Prefer a compact contract for lightweight runs (if the run is non-trivial, otherwise use the full plan and checklist templates).
- Prefer explicit falsification signals before execution (if the result would be ambiguous, otherwise state the route decision that each outcome would support).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <EXPERIMENT_CONTRACT> must exist before broad code edits, real compute, or a main comparison run.
- <EXPERIMENT_CONTRACT> must name the required metric keys and comparator basis.
- Dataset, split, metric definition, evaluator logic, and comparator recipe must not change silently.
- Required metric keys must not be replaced by supplementary metrics.
- A material contract change must be recorded before new compute or code work continues.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Contract field coverage: fraction of question, hypotheses, comparator, dataset, split, metric keys, primary metric, evaluator assumptions, outputs, stop condition, abandonment condition, budget, and alternative hypothesis recorded; higher is better.
- Material-change ambiguity count: number of code-path, comparability, runtime, or execution-route changes still unrecorded before compute or code work continues; lower is better.

### Checks

- Readiness check: selected hypothesis, accepted comparator basis, metric contract, and execution surface are explicit.
- Research check: question, null hypothesis, alternative hypothesis, selected hypothesis, expected answer signal, and strongest alternative hypothesis are stated.
- Comparability check: dataset, split, evaluator, primary metric, required metric keys, and comparator basis are fixed or deviations are named.
- Scope check: expected changed files, expected outputs, stop condition, abandonment condition, and budget are clear enough for execution.
- Planning check: <EXPERIMENT_PLAN> and <EXPERIMENT_CHECKLIST> exist when run complexity, cost, branch sensitivity, or duration requires them.
