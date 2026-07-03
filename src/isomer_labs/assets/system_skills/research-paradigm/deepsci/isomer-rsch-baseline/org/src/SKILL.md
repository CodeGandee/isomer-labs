---
name: baseline
description: Use when a quest needs to attach, import, reproduce, repair, verify, compare, or publish a baseline and its metrics.
skill_role: stage
---

# Baseline

Use this skill to secure one trustworthy comparator and then get out of the way.
The target is one accepted baseline line, not an endless reproduction diary.

## Match signals

Use `baseline` when:

- no credible baseline exists yet
- the current baseline is unverified or stale
- the user already has a baseline package that should be attached or imported
- a local code path or local service should be verified as the comparator
- a reproduction failed earlier and now needs repair
- the quest resumed and the baseline trust state is unclear

Do not use `baseline` when:

- a verified active baseline already exists and the next move is obviously `idea`, `experiment`, `write`, or `finalize`
- the baseline gate was already explicitly waived for the current route

## One-sentence summary

Secure the lightest trustworthy comparator, make the comparison contract explicit, then confirm, waive, or block the baseline and stop.

## Control workflow

1. Choose the current acceptance target and the lightest route that can satisfy it.
   Prefer `attach`, `import`, or `verify-local-existing` before full reproduction.
2. Make the comparator identity and core metric contract explicit.
   Record task, dataset, split, evaluation path, required metric ids, metric directions, source identity, and known deviations.
3. Collect only the evidence needed to establish comparability.
   Do not widen into broad codebase audit or heavy reruns unless the lighter route cannot be trusted.
4. Verify before acceptance.
   Check that outputs are real, metrics trace to real evidence, and the intended dataset/split and metric definitions match the contract.
   Explicitly verify the comparator and metric contract before treating the baseline gate as open.
5. Close the gate explicitly.
   Call `artifact.confirm_baseline(...)`, call `artifact.waive_baseline(...)`, or record an explicit blocker and next route.
   When an already accepted baseline needs a deliberate second-pass refresh after verified code, variant, or canonical metric changes, prefer `artifact.overwrite_baseline(...)` over pretending the update is just a first confirmation.

## AVOID / pitfalls

- Do not default to full source reproduction when reuse or verify-local-existing is already sufficient.
- Do not treat attach, import, or publish alone as baseline acceptance.
- Do not accept metrics that are fabricated, copied from the paper, or not traceable to real outputs, logs, or service responses.
- Do not silently normalize away deviations in dataset, split, metric definition, evaluation path, or source identity.
- Do not keep doing baseline work after the current acceptance target is already satisfied.
- Do not repeat the same failure class without new evidence, code changes, environment changes, or a route change.

## Constraints

- Routes, templates, filenames, smoke tests, and environment choices are tactics; the hard requirement is objective evidence sufficient to accept, waive, block, or switch the route.
- Do not treat templates, filenames, `uv`, smoke tests, detached runs, or the phase order as required paths.
- Durable records are required in substance, not in fixed filenames.
- `PLAN.md`, `CHECKLIST.md`, `setup.md`, `execution.md`, `verification.md`, `analysis_plan.md`, and `REPRO_CHECKLIST.md` are allowed compatibility surfaces, not mandatory success paths.
- `<baseline_root>/json/metric_contract.json` is the canonical accepted comparison contract.
- Accepted baselines still require `artifact.confirm_baseline(...)`.
- Waived baselines still require `artifact.waive_baseline(...)`.
- Attach/import/publish alone do not open the downstream gate.
- Later stages must not need to guess the active comparator, trusted metrics, or main caveats.

## Validation

Before `baseline` can end, all applicable checks should be true:

- comparator identity is explicit and stable enough to cite later
- task, dataset, split, evaluation path, required metric ids, metric directions, source identity, and known deviations are durably recorded
- trusted metric values or trusted output pointers trace to real files, logs, service responses, or source artifacts
- verification checked the intended dataset/split and metric definitions
- the accepted comparison contract exists at `<baseline_root>/json/metric_contract.json`
- the route ended in `artifact.confirm_baseline(...)`, `artifact.waive_baseline(...)`, or an explicit blocked state with next-step routing

## Interaction discipline

Follow the shared interaction contract injected by the system prompt.
Keep baseline updates brief unless trust state, blocker state, route, cost, or user-facing risk changed materially.

## Tool discipline

- **Do not use native `shell_command` / `command_execution` in this skill.**
- **All shell, CLI, Python, bash, node, git, npm, uv, and environment work must go through `bash_exec(...)`.**
- **For git work inside the current quest repository or worktree, prefer `artifact.git(...)` before raw shell git commands.**
- **If a generic git smoke test is needed outside the quest repo, use `bash_exec(...)` in an isolated scratch repository.**
- Use web search for discovering papers or repos, but use `artifact.arxiv(paper_id=..., full_text=False)` for actually reading a source arXiv paper when it exists.
- Set `full_text=True` only when the short form is insufficient.

## Authority and freedom

The agent owns the execution path.
It may choose the workspace layout, environment manager, command order, debugging route, smoke strategy, local paths, and whether the best route is attach, import, verify-local-existing, reproduce, or repair.

Ask the user only when the next move depends on a real scope, cost, permission, data-access, or scientific-preference decision that cannot be inferred from the quest contract.
Ordinary route, path, environment, and debugging choices are autonomous unless they change the accepted comparison meaning.

## Comparator-first rule

The baseline stage is comparator-first, not reproduction-first.
For `comparison_ready`, the default question is:

- what is the lightest trustworthy comparator?

not:

- how do I reproduce the whole source package most completely?

Default to the lightest baseline path that can still support a fair downstream comparison.
Default to a fast path when it can establish trust with less work.
Do not restart broad discovery or front-load a full codebase audit when the comparator, command path, and metric contract are already concrete.
When this applies, do not front-load a full codebase audit.
In that fast-path state, do not restart broad baseline discovery by default.
Do not require a fresh memory pass for every fast-path validation; use memory when it prevents repeated work or clarifies stale route state.
In short, do not require a fresh memory pass for every fast-path validation.
A bounded smoke test is usually helpful only when command path, environment viability, evaluator wiring, or output schema is still unclear.
Treat smoke/pilot work as a `0-2` default budget, and remember not to repeat an unchanged check without new evidence.
When resuming a previously blocked or ambiguous route, recover the relevant memory before trusting the old path again.

If runtime already exposes `requested_baseline_ref` or a matching `confirmed_baseline_ref`, default to reuse-and-verify.
Escalate to fuller audit, reproduction, or repair only when no concrete comparator, command path, or core comparability surface can be trusted yet.

For route examples and boundary cases, read `references/route-selection.md`, `references/artifact-flow-examples.md`, and `references/boundary-cases.md`.
Use `references/baseline-plan-template.md` and `references/baseline-checklist-template.md` when a baseline route is complex enough to need durable planning surfaces.

## Acceptance targets

- `comparison_ready`: the default target; one comparator is trustworthy enough for downstream comparison, and the core metric contract is durably recorded
- `paper_repro_ready`: the baseline is strong enough to support paper-facing reproduction or comparison claims
- `registry_publishable`: the baseline package is reusable and clean enough to publish as a durable baseline package
- `blocked`: the current route cannot clear the gate cleanly, and the next move is explicit
- `waived`: the quest must continue without a baseline, and the reason is durably recorded

Not every baseline needs paper-grade exact reproduction.
A verified attached, imported, or local-existing comparator can be enough when the acceptance target is only `comparison_ready`.

## Hard acceptance gates

Baseline success means later stages can compare against one accepted comparator without guessing task, data, split, metric, source, command or evaluation path, provenance, or caveats.

A baseline is successful only when all applicable gates are true:

- the comparator identity is explicit and stable enough for later stages to cite
- the task, dataset, split, evaluation path, required metric ids, metric directions, source identity, and known deviations are durably recorded
- trusted metric values or trusted output pointers are traceable to real files, logs, service responses, source artifacts, or an accepted registry/package record
- verification checked that the evidence came from the intended dataset/split and metric definitions
- the accepted comparison contract is written to `<baseline_root>/json/metric_contract.json`
- the baseline gate is opened with `artifact.confirm_baseline(...)`, or intentionally bypassed with `artifact.waive_baseline(...)`

Once a comparison-ready baseline is durably confirmed, baseline should usually stop immediately.
Once a comparison-ready baseline is durably confirmed, baseline should usually stop immediately and hand off to the next scientific step.
Any extra baseline work after that must name one explicit unresolved comparison risk it is meant to remove.

## Route success criteria

Choose the route that maximizes trust per unit time and compute; do not follow a fixed ritual.
Keep one dominant baseline route active at a time.
If a lighter route already satisfies the current acceptance target, stop there.

- `attach` succeeds when baseline identity, provenance, trusted outputs pointer, core metric contract, and accepted baseline artifact are explicit
- `import` succeeds when the package is materialized/readable inside the quest, `attachment.yaml` or equivalent provenance exists, and trusted outputs or metrics are traceable
- `verify-local-existing` succeeds when the concrete local path or service, exact command or evaluation endpoint, output location, required metrics, and core metric contract are verified
- `reproduce` succeeds when source identity, command or evaluation path, expected outputs, verification evidence, deviations, and metric contract are explicit
- `repair` succeeds when the broken point is identified, a bounded fix or route change is made, rerun or re-read evidence supports the new trust state, and the result is accepted or blocked

Prefer reuse over redundant reproduction, but prefer reproduction or repair when reuse would still leave the baseline incomparable.
Do not replace a working comparison-ready comparator with a heavier route merely because the heavier route feels cleaner or more complete.

## Objective evidence requirements

The final evidence should cover these facts before acceptance:

- comparator candidate and baseline id
- source paper, source repo, source commit/version/tag, local service identity, or registry/package identity as applicable
- task identity
- dataset identity and split contract
- evaluation script, evaluation endpoint, or evaluation path
- required metric keys for the current downstream comparison
- metric directions
- metric values or trusted output pointers
- environment and hardware facts that materially affect comparability
- known deviations from the paper, source package, local reference, or selected target
- verification verdict and caveats

Unless the user explicitly specifies otherwise, treat the original paper's evaluation protocol as the canonical starting point.
If later `experiment` work would still have to guess the comparison contract, the baseline is not ready.
For a compact verdict rubric, read `references/comparability-contract.md`.

## Verification

Verification is mandatory before baseline acceptance.

Verify:

- the run, service call, package import, or trusted-output inspection actually finished
- the reported metrics came from the intended dataset and split
- metric definitions and directions match the quest contract
- the result is comparable to the paper, source repo, local comparator, registry package, or selected target
- deviations are explicitly stated rather than silently normalized away

Classify the outcome as one of:

- `verified_match`
- `verified_close`
- `verified_diverged`
- `trusted_with_caveats`
- `broken`

Verification should explicitly separate likely implementation mismatch, environment mismatch, data or split mismatch, expected stochastic variance, and unexplained divergence when those distinctions matter.

## Core metric contract

Before declaring a baseline usable, make the core comparison contract explicit:

- task identity
- dataset identity and split contract
- evaluation script or evaluation path
- required metric keys for the current downstream comparison
- metric directions
- source commit or source package identity
- known deviations from the source reference

`<baseline_root>/json/metric_contract.json` is the canonical accepted comparison contract.
The comparison-ready minimum still requires `<baseline_root>/json/metric_contract.json`.
A core contract is enough to confirm a `comparison_ready` baseline; expand it later when paper claims, registry publication, or variant-heavy comparison need more coverage.

The accepted baseline artifact should include at least:

- `baseline_id`
- `baseline_kind`
- `path`
- `task`
- `dataset`
- `primary_metric`
- `metrics_summary`
- `environment`
- `source`
- `summary`

Metric-contract rules:

- keep `primary_metric` as the headline metric only; do not let it erase the rest of the comparison surface
- submit canonical `metrics_summary` as a flat top-level dictionary keyed by the paper-facing metric ids
- every canonical baseline metric entry should include `description`, either `derivation` or `origin_path`, and `source_ref`
- mark only the currently required canonical metrics as required; additional metrics can be added later or kept supplementary
- if the accepted baseline contract already needs multiple metrics, datasets, subtasks, or splits, record them in `<baseline_root>/json/metric_contract.json`
- if the paper reports both aggregate and per-dataset or per-task results, preserve both whenever feasible through `metrics_summary` plus structured rows rather than one cherry-picked scalar
- if the source package already has a richer leaderboard table, structured result file, or `json/metric_contract.json`, reuse that richer contract instead of hand-writing a thinner one that keeps only one averaged scalar
- `Result/metric.md` is optional temporary scratch memory only; reconcile against it before calling `artifact.confirm_baseline(...)`, but do not treat it as a required durable file
- for stable accepted payload shapes, read `references/artifact-payload-examples.md`

## Operational guidance

The main skill keeps the control surface in front.
For the longer operational notes, read `references/operational-guidance.md`.

- use it when you need the exact durable route record shape
- use it when you need detailed execution tactics or environment tactics
- use it when reuse or memory handling materially affects the route

## Negative cases and stop rules

Do not accept a baseline when:

- metrics are fabricated, copied, or paraphrased without provenance
- metrics are copied from a paper while the acceptance target requires local verification
- dataset, split, metric direction, or evaluation path is materially unknown
- outputs exist but cannot be tied to the intended command, source, comparator, package, or service
- a local run completed but used a materially different protocol without a recorded caveat
- source code was modified in a way that changes baseline scope without recording the deviation
- a package imports but trusted metrics or outputs are not traceable
- later experiment work would still need to guess the required baseline metric ids
- the same failure class reappears without new evidence, code changes, environment changes, or a route change

If the same failure class appears again without new evidence, code changes, environment changes, or a route change, stop looping and route through `repair`, `decision`, `blocked`, `waive`, or one bounded clarification.
Do not hide failures.
If blocked, record the class explicitly when possible:

- `missing_source`
- `missing_metric_contract`
- `environment_infeasible`
- `command_unknown`
- `run_failed`
- `verification_failed`

A blocked result must state:

- what failed
- what was tried
- which paths or logs show the issue
- whether the next best move is attach, import, retry, repair, reset, waive, or ask the user

Bounded autonomous fixes are acceptable only when they do not change confirmed scope, metrics, permissions, resource assumptions, or scientific meaning.
Reasonable bounded fixes include missing dependency installs, wrong dataset paths, permission fixes on scripts, obvious environment activation mistakes, and conservative batch-size reductions for OOM.

## Baseline id and variant rules

Keep baseline identifiers and variant names stable enough that later stages can cite the same comparator without guesswork.

- keep `baseline_id` short, stable, and filesystem-safe
- prefer one baseline id with stable variant names over many near-duplicate ids
- if multiple comparators exist, mark which one is the primary downstream baseline

## Exit criteria

Exit once one of these is durably true:

- a baseline is attached and accepted
- an imported baseline is accepted
- a verified local-existing comparator is accepted
- a reproduced baseline is verified and accepted
- a repaired baseline is verified and accepted
- a broken route has been declared blocked and a next decision is recorded
- a waiver decision explicitly leaves the baseline gate
- a route change is recorded because the previous route is no longer the best trust-per-cost path

Typical next anchors:

- `idea`
- `experiment` in tightly scoped follow-on cases
- `decision` if the baseline line remains contested

A good baseline pass leaves one trusted comparator, one explicit blocker, or one explicit route change, not a vague promise to keep rechecking baseline.
