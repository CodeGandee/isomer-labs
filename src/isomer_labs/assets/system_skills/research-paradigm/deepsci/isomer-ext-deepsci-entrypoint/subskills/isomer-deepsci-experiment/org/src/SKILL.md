---
name: experiment
description: Use when a quest is ready for a concrete implementation pass or a main experiment run tied to a selected idea and an accepted baseline.
skill_role: stage
---

# Experiment

Use this skill for the main evidence-producing runs of the quest.
The goal is to turn one selected route into one trustworthy measured result with the smallest valid amount of execution.

## Match signals

Use `experiment` when:

- a baseline is accepted
- an idea has been selected
- the evaluation contract is explicit
- the quest is ready for implementation and measurement rather than framing, route selection, or writing

Do not use `experiment` when:

- the baseline gate is unresolved
- the idea stage still has unresolved tradeoffs
- the main need is writing or follow-up analysis rather than a main run
- the real problem is still route choice, baseline recovery, or open-ended optimization rather than one bounded measured run

## One-sentence summary

Turn one selected route into one trustworthy measured result with the smallest valid amount of execution, then record and route from the evidence.

## Quick workflow

- Recover the selected idea, accepted baseline, metric contract, and current workspace before implementation.
- Keep the selected idea summarized in `1-2` sentences, then write a minimal code-change map before touching broad code.
- Define the null hypothesis, alternative hypothesis, research question, research type, research objective, experimental setup, experimental results, experimental analysis, and experimental conclusions as the run matures.
- Run only the checks needed to maximize valid evidence per unit time and compute.
- Use equivalence-preserving efficiency upgrades when they preserve baseline comparability; For `comparison_ready`, `verify-local-existing`, attach, or import should usually beat full reproduction.
- If an efficiency change affects baseline comparability, treat it as a real experiment change.
- Prefer one clean implementation pass and one real run over repeated half-runs when the route is already concrete.
- Implement according to the current `PLAN.md`; revise the plan before changing the route.
- implement according to the current `PLAN.md`
- Extra metrics are allowed, but missing required metrics are not.
- extra metrics are allowed, but missing required metrics are not
- If a useful non-canonical metric appears, record it as supplementary output rather than replacing the canonical comparator.
- In algorithm-first work, `experiment` is the execution surface of `optimize`, then results return to `optimize` or `decision` for frontier review.
- End with a concise `1-2` sentence outcome summary, `evaluation_summary`, `claim_update`, `baseline_relation`, `failure_mode`, and `next_action`.

## Required plan and checklist

Use `PLAN.md` and `CHECKLIST.md` when the run is non-trivial, expensive, or branch/worktree-sensitive.
If the plan or checklist is stale, revise `PLAN.md` before spending more code or compute.
Keep a rolling run log or rolling durable experiment log that captures command ids, output paths, metric changes, and blocker changes.

The planning surface should cover:

- selected idea summarized in `1-2` sentences
- minimal code-change map
- experiment tier: `auxiliary/dev` or `main/test`
- minimum -> solid -> maximum evidence target
- significance-testing plan when statistical claims are likely
- references/main-experiment-plan-template.md
- references/main-experiment-checklist-template.md

Incremental-recording rule: record the run contract early, update it as evidence arrives, and do not wait until the end to reconstruct what happened.

## Control workflow

1. Lock the run contract.
   Make explicit the research question, baseline reference, dataset/split, metric keys, stop condition, abandonment condition, and expected outputs.
2. Implement only the minimum hypothesis-bound change.
   Keep the baseline read-only and avoid unrelated cleanup or hidden scope expansion.
3. Run a bounded smoke or pilot only when the command path, output schema, or evaluator wiring are still unverified.
4. Execute and monitor the real run honestly.
   Preserve commands, configs, logs, outputs, comparability, and the last-known-good state.
5. Validate and record the result.
   Check metric completeness and comparability, then call `artifact.record_main_experiment(...)` and choose the next route.

## AVOID / pitfalls

- Do not confuse smoke or pilot success with main evidence.
- Do not silently change dataset, split, metric definition, evaluator logic, or baseline comparison recipe.
- Do not retry without a real route, code, command, environment, or evidence change.
- Do not claim success before durable outputs exist and `artifact.record_main_experiment(...)` succeeds.
- Do not record a durable main experiment from an idea branch, quest root branch, or paper branch as if that were the final result node.
- Do not disguise idea search or route revision as a routine rerun.
- Do not keep rerunning after the next route is already clear.

## Constraints

- All smoke tests, real runs, shell, CLI, Python, bash, node, git, npm, uv, and environment work must go through `bash_exec(...)`.
- For git work inside the current quest repository or worktree, prefer `artifact.git(...)` before raw shell git commands.
- Keep the accepted baseline reference read-only.
- If `active_baseline_metric_contract_json` exists, required baseline metric keys must still be covered unless a concrete deviation is durably recorded.
- Durable main experiments should land on their own `run/*` branch or an equivalent isolated run surface.
- If an active paper line or selected outline already exists, a recorded main experiment should be synchronized into the current paper contract instead of living only as a run artifact.
- In algorithm-first work, after each main run, return to `optimize` or `decision` for frontier review before launching another large run.
- Main-run evidence is not complete until `artifact.record_main_experiment(...)` succeeds.

## Validation

Before `experiment` can end, all applicable checks should be true:

- outputs correspond to the intended code and config
- required metric keys are present and finite
- baseline comparison is still comparable, or the deviation is explicit
- the claim is classified as `supported`, `refuted`, or `inconclusive`
- the run manifest includes exact command, config, seed, and environment snapshot
- `evaluation_summary` exists with the six stable fields the next stage needs
- if a paper line is active, the run is visible through the current paper contract rows rather than only through the run artifact
- `artifact.record_main_experiment(...)` succeeded
- the next route is explicit

## Interaction discipline

Follow the shared interaction contract injected by the system prompt.
Keep run updates brief unless the measured result, blocker state, or next route changed materially.
For ordinary active work, prefer a concise progress update once work has crossed roughly 6 tool calls with a human-meaningful delta, and do not drift beyond roughly 12 tool calls or about 8 minutes without a user-visible update.

## Tool discipline

- **Do not use native `shell_command` / `command_execution` in this skill.**
- **All smoke tests, real runs, shell, CLI, Python, bash, node, git, npm, uv, and environment work must go through `bash_exec(...)`.**
- **For git work inside the current quest repository or worktree, prefer `artifact.git(...)` before raw shell git commands.**
- **If a scratch repository or isolated test environment is needed, create and drive it through `bash_exec(...)`, not native shell tools.**

## Non-negotiable rules

- Do not fabricate metrics, logs, claims, or improvement narratives.
- Do not introduce a new dataset or silently change splits or evaluation protocol.
- Do not change metric definitions or evaluation logic unless the change is explicitly justified and durably recorded.
- Do not stop after a quick sanity run if the agreed goal is a real experiment.
- Do not claim success before durable artifacts exist and the acceptance gate passes.
- Implement the claimed mechanism, not a convenient shortcut that changes the theory.
- Keep the baseline reference read-only.
- Avoid asking the user to fix the environment unless there is no credible agent-side path left.
- After each `artifact.record_main_experiment(...)`, route from the measured result instead of stopping at “run finished”.

## Truth sources

Use:

- idea-stage outputs
- baseline artifacts
- current codebase and configs
- recent decisions
- task and metric contract
- shell logs and generated outputs from the actual run
- `bash_exec` session ids, progress markers, and exported logs from the actual run
- the selected idea handoff contract
- incident or failure-pattern memory from earlier runs

Do not claim run success without durable outputs.

## Required durable outputs

A meaningful experiment pass should leave behind:

- a run directory under `artifacts/experiment/<run_id>/` or the quest-equivalent canonical location
- durable command, config, and log pointers
- exported shell log, typically `bash.log`
- a run artifact with explicit deltas versus baseline
- a decision about what should happen next

For the exact run-manifest fields, checklist template, and detailed recording contract, use the references listed below.

## Evidence ladder note

Use `references/evidence-ladder.md` when deciding whether the current package is merely executable, solid enough to carry the main claim, or already in the stage where broader polish is justified.

The default ladder is:

- `minimum`: executable and comparable
- `solid`: strong enough to carry the main claim
- `maximum`: broader supporting polish after the main claim is already credible

Do not spend for `maximum` before the line is at least `solid`.

## Planning note

Use quest or workspace planning files only when they help control a non-trivial run.
Otherwise keep the run contract small and move to the first decisive execution step.

## Operational guidance

The main skill keeps the control surface in front.
For the longer operational notes, read the references:

- `references/main-experiment-plan-template.md`
- `references/main-experiment-checklist-template.md`
- `references/execution-playbook.md`
- `references/operational-guidance.md`

Use them when:

- the run contract is non-trivial
- the long-running protocol or monitoring cadence matters
- the exact manifest, artifact, memory, or charting rules matter

## Run-quality rules

A credible main run should satisfy:

- comparable against baseline
- method change is knowable from code and config
- metric source is durable
- outcome can be explained by the intended intervention or its failure
- commands, configs, and seeds are reconstructable
- environment context is reconstructable
- later readers can trace code and diff context to command, logs, and metrics

If the result is confounded, say so directly.

## Acceptance gate

Before marking the run complete, verify all of the following:

- all required baseline metric keys are present
- the reported comparison contract still matches `active_baseline_metric_contract_json` when that file exists
- metric values are finite numbers
- claim-to-metric traceability is recorded
- run manifest includes exact command, config, seed, and environment snapshot
- the summary states go or no-go and why
- artifacts are sufficient for another stage to reconstruct the run

If these checks fail, record the run as partial or blocked rather than pretending it is complete.

## Failure and blocked handling

A failed main run is still useful if it is explained well.

Record:

- what was attempted
- where the failure occurred
- whether the failure was methodological or infrastructural
- what retry, branch, or reset is justified
- the single best next action

Prefer a primary failure type such as:

- `data_contract_mismatch`
- `resource_exhausted`
- `numeric_instability`
- `implementation_bug`
- `evaluation_pipeline_failure`
- `external_dependency_blocked`
- `direction_underperforming`

Also classify the broader failure layer when possible:

- implementation
- evaluation
- environment
- direction

Blocked experiment states commonly include missing baseline reference, unknown metric contract, environment failure, run failure before metrics, or metrics that are not comparable.
When results are suspicious, fix the subset and seeds, isolate preprocessing/model/training/evaluation one by one, compare intermediate outputs on the same inputs, and run the cheapest discriminative check before another full retry.

## Exit criteria

Exit the experiment stage once one of the following is durably true:

- a main run is completed and recorded
- the run failed and the blocker is durably recorded
- the next step is clearly `analysis-campaign`, `write`, another `experiment`, `optimize`, or `reset`

A good experiment pass leaves one interpretable result or one explicit blocker, not another vague promise to rerun later.
