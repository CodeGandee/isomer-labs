# Execution Playbook

Use this reference when the experiment route needs the full execution checklist rather than the short control surface in `SKILL.md`.

## 1. Define the run contract

Before implementation or execution, state:

- `run_id`
- experiment tier: `auxiliary/dev` or `main/test`
- research question
- null hypothesis
- alternative hypothesis
- hypothesis
- baseline id or variant
- metric targets
- expected changed files
- expected outputs
- stop condition
- compute or runtime budget
- minimal experiment
- abandonment condition
- strongest alternative hypothesis
- exact metric keys that will decide success or failure

Prefer to write this contract first in `PLAN.md` using `references/main-experiment-plan-template.md`, then keep the current execution state visible in `CHECKLIST.md` using `references/main-experiment-checklist-template.md`.

For substantial runs, also record the following seven experiment fields early and keep them updated during execution:

1. research question
2. research type
3. research objective
4. experimental setup
5. experimental results
6. experimental analysis
7. experimental conclusions

If the run contract changes materially later, record the change durably.

Treat the run contract as a research-question contract, not only an execution checklist.
Before coding, be able to explain:

- why this run is the best current route rather than the main alternatives
- what observation would count as a real answer to the research question
- what result would force a downgrade, retry, or route change
- what confounder would make the run non-comparable even if it finishes successfully

If multiple candidate experiment packages exist, prefer the one with the best balance of technical feasibility, research importance, and methodological rigor.
Do not choose a package only because it sounds ambitious.

For paper-facing lines, default to this evidence ladder:

- `auxiliary/dev`
  - clarify parameters, settings, mechanisms, or diagnostics
- `main/test`
  - carry the core comparison the paper will rely on
- `minimum -> solid -> maximum`
  - first make the result executable and comparable
  - then make it strong enough to carry the claim
  - only then spend effort on broader supporting polish

## 2. Run a preflight check

Before editing or executing:

- confirm the dataset path, version, and split contract
- confirm the baseline metrics reference
- if durable state exposes `active_baseline_metric_contract_json`, read that JSON file before planning commands or comparisons
- treat `active_baseline_metric_contract_json` as the default authoritative baseline comparison contract unless you record a concrete reason to override it
- confirm the selected idea claim and code-level plan
- look up prior incidents or repeated failure patterns when available
- confirm output directories and naming
- confirm that the intended run still matches the current quest decision

If a repeated failure pattern already exists, apply the mitigation first and record that choice.

Also confirm before comparison work:

- the baseline verification is trustworthy enough
- the planned comparison still uses the same metric contract
- the metric keys and primary metric still match `active_baseline_metric_contract_json` when that file is available
- every main experiment submission still covers all required baseline metric ids from `active_baseline_metric_contract_json`; extra metrics are allowed, but missing required metrics are not
- the required baseline metrics still use the same evaluation code and metric definitions; if an extra evaluator is genuinely necessary, record it as supplementary output rather than replacing the canonical comparator
- if the run is `main/test` and superiority is likely to be claimed, define the significance-testing plan before execution rather than after seeing the numbers
- if `Result/metric.md` was used during the run, treat it as optional scratch memory only and reconcile it against the final submitted metrics before `artifact.record_main_experiment(...)`

Before you begin a substantial run, send a concise threaded `artifact.interact(kind='progress', ...)` update naming:

- the run contract you are about to execute
- the main evidence it is testing
- the expected durable outputs
- the next checkpoint for reporting back

## 2.1 Diagnostic mode trigger

Switch from ordinary execution mode into diagnosis mode when any of the following becomes true:

- two retries in a row add no new evidence or no interpretable delta
- the baseline gap is much larger than expected and the cause is unclear
- the metrics are suspiciously strong, suspiciously identical to baseline, or highly unstable
- logs, checkpoints, or intermediate outputs conflict with the claimed behavior

In diagnosis mode:

- stop brute-force retrying
- prefer the smallest discriminative test that can separate competing hypotheses
- resolve obvious environment or data-contract issues before launching another comparison run
- make the diagnosis goal explicit: explain the behavior, not just "try something else"

## 3. Confirm the execution workspace

The normal experiment workspace is the current active idea worktree returned by `artifact.submit_idea(...)`.

- do not create a fresh manual branch for the main experiment unless recovery or debugging truly requires it
- implement and run inside the current active idea workspace
- if the idea package changes materially before execution, submit a new durable idea branch with `artifact.submit_idea(mode='create', lineage_intent='continue_line'|'branch_alternative', ...)` instead of silently mutating the old node
- after a real main run finishes, record it with `artifact.record_main_experiment(...)` before moving to analysis or writing
- once that durable main result exists, treat the branch as a fixed round node; a later new optimization round should usually compare foundations and create a new `continue_line` child branch or `branch_alternative` sibling-like branch
- after `artifact.record_main_experiment(...)`, if QQ milestone media is enabled and the metrics are stable enough to summarize honestly, prefer one concise summary PNG over multiple attachments

## 4. Implement the minimum required change

Implementation rules:

- keep the change hypothesis-bound
- prefer small, explainable edits
- avoid unrelated cleanup during a main run
- record which files matter for later review
- preserve theory fidelity between the idea claim and the code change
- add robustness checks when the mechanism risks NaN, inf, or unstable behavior
- implement according to the current `PLAN.md` instead of repeatedly improvising a new method after each small observation
- avoid repeated code churn between the smoke test and the real run unless the smoke test exposes a specific problem that the next change is meant to fix

Prefer to complete one experiment cleanly before expanding to the next, unless parallel execution is explicitly justified and isolated.
For substantial experiment packages, the default is one experiment at a time, with each one reaching a recoverable recorded state before the next begins.

Retry-delta discipline:

- unless the current state is completely non-executable, change only one major variable per retry
- if broader recovery is unavoidable, record exactly which layer changed: data, preprocessing, model, objective, optimization, evaluation, or environment
- before each retry, state the expected effect and the fastest falsification signal
- if the retry produced no interpretable delta, do not treat it as meaningful evidence about the underlying research hypothesis
- if the retry does not change the hypothesis, code path, command path, or evidence surface, stop rerunning and route through `decision`
- if the same failure class appears again without a real route or evidence change, stop looping and route through `decision`

## 5. Execute the run

Run with auditable commands and durable outputs.

Execution rules:

- use non-interactive commands
- prefer `bash_exec` instead of ephemeral shell invocations
- use the intended dataset and split
- keep logs durable
- report progress for long runs
- avoid silent metric-definition changes
- do not drift away from `active_baseline_metric_contract_json` silently when that file exists
- avoid silently changing the baseline comparison recipe
- run the full agreed evaluation, not only a smoke test

You may do a quick sanity run first, but if the stage goal is a real experiment you must continue to the real evaluation unless the run is blocked and recorded.

Pilot-before-scale rule:

- start with a bounded pilot only when the modification is non-trivial and that pilot resolves a real execution uncertainty
- use the pilot to catch implementation mistakes early
- record pilot outcomes explicitly
- do not mistake pilot success for final evidence

Incremental-recording rule:

- do not wait until the end to reconstruct the run from memory
- update the durable run note after:
  - contract definition
  - important code changes
  - pilot validation
  - full execution checkpoints
  - post-run analysis
- update `CHECKLIST.md` alongside those durable notes so the current execution frontier is obvious without replaying the whole log
- include timestamps when they materially help reconstruction
- preserve failed attempts, anomalies, and partial outcomes rather than overwriting them
- a durable run memory or note should explicitly record whether the current state is `success`, `partial`, or `failure`
- when available, include `idea_id`, `branch`, and `run_id`

Last-known-good rule:

- keep track of the most recent state that was executable, comparable, and explainable
- when a new attempt breaks that state, debug forward from the last-known-good point instead of stacking more speculative edits on top of the broken state
- if the last-known-good state is unclear, reconstruct it before spending more budget on new hypotheses

## 5.1 Long-running command protocol

For commands that may run longer than a few minutes:

- if command paths, outputs, or basic metrics are still unverified, execute one bounded smoke test or pilot first
- keep smoke or pilot budget at `0-2` for the current experiment pass
- treat smoke work as a `0-2` budget rather than as a mandatory separate phase
- allow a second smoke or pilot only after a real code, command, environment, or evaluator change
- once the path is verified, launch the real run with `bash_exec(mode='detach', ...)` and normally leave `timeout_seconds` unset for that long run
- monitor through durable logs rather than only live terminal output
- `bash_exec(mode='read', id=...)` returns the full rendered log when it is 2000 lines or fewer; for longer logs it returns the first 500 lines plus the last 1500 lines and a hint to inspect omitted sections with `start` and `tail`
- if the middle of a long saved log matters, inspect that omitted region with `bash_exec(mode='read', id=..., start=..., tail=...)`
- use `bash_exec(mode='list')` and `bash_exec(mode='read', id=..., tail_limit=..., order='desc')` to monitor or revisit managed commands while focusing on the newest evidence first
- after the first read, prefer `bash_exec(mode='read', id=..., after_seq=last_seen_seq, tail_limit=..., order='asc')` so later checks only fetch new evidence
- if you need to recover ids or sanity-check the active session ordering, use `bash_exec(mode='history')`
- launch important runs with a structured `comment` such as `{stage, goal, action, expected_signal, next_check}`
- use `silent_seconds`, `progress_age_seconds`, `signal_age_seconds`, and `watchdog_overdue` from `bash_exec(mode='list'|'read', ...)` as your default watchdog signals
- use an explicit wait-and-check loop such as:
  - wait about `60s`, then inspect logs
  - wait about `120s`, then inspect logs
  - wait about `300s`, then inspect logs
  - wait about `600s`, then inspect logs
  - wait about `1800s`, then inspect logs
  - then keep checking about every `1800s` while the run is still active
- if needed, use an explicit bounded wait such as `bash_exec(command='sleep 60', mode='await', timeout_seconds=70)` or `bash_exec(mode='await', id=..., wait_timeout_seconds=1800)` between checks
- canonical sleep choice:
  - if you only need wall-clock waiting between checks, use `bash_exec(command='sleep N', mode='await', timeout_seconds=N+buffer, ...)`
  - keep a real buffer on that sleep timeout; do not set `timeout_seconds` exactly equal to `N`
  - if you are waiting on an already running managed session, prefer `bash_exec(mode='await', id=..., wait_timeout_seconds=1800)` instead of starting a new sleep command
  - if that bounded await returns while the session is still `running`, treat that as expected managed-monitoring behavior; read the log, judge forward progress, and then decide whether another `1800s` wait is justified
- after every completed sleep or await cycle, inspect logs first; only send `artifact.interact(kind='progress', ...)` when the user-visible state, frontier, blocker status, or ETA materially changed
- after the first meaningful signal and then at real checkpoints such as completion, recovery, blocker, or a materially widened comparable surface, keep those progress updates going rather than waiting silently
- if the run is clearly invalid, wedged, or superseded, stop it with `bash_exec(mode='kill', id=..., wait=true, timeout_seconds=...)`; if it must die immediately, add `force=true`, record the reason, fix the issue, and relaunch cleanly
- do not report completion until logs and output files both confirm completion
- when you control the run code, prefer a throttled `tqdm` progress reporter and concise structured progress markers when feasible

Always preserve the managed `bash_exec` log and export it into the experiment artifact directory when the run artifact is written.

## 5.2 Progress marker protocol

If the run emits progress markers, keep them concise and machine-readable instead of narrating every low-level update in chat.
When a real checkpoint is reached, include the estimated next reply time and `next_reply_at` when that is honestly knowable.

## 6. Validate the outputs

After the run, verify:

- outputs correspond to the intended code and config
- metrics are complete and interpretable
- comparison to baseline is fair
- any failure mode or confounder is visible
- required metric keys are present and finite
- the result can be mapped back to the original claim
- the summary states a clear go or no-go recommendation

Create a durable claim-validation record that maps:

- claim
- metric key
- expected direction
- observed result
- verdict:
  - `supported`
  - `refuted`
  - `inconclusive`

Also verify baseline comparability before claiming deltas:

- was the baseline verification stable?
- was the evaluation path the same?
- are the compared metric keys identical?
- if the run is claim-carrying, are the significance results or uncertainty estimates strong enough for main-text use?
- do known caveats make the delta weaker than it first appears?

## 7. Record the run

Every meaningful main run must be recorded through `artifact.record_main_experiment(...)`.

That call is responsible for writing:

- `experiments/main/<run_id>/RUN.md`
- `experiments/main/<run_id>/RESULT.json`
- the durable `run` artifact payload
- baseline comparisons
- breakthrough status derived by the system

`artifact.record_main_experiment(...)` should include at least:

- `run_id`
- title
- hypothesis
- setup
- execution
- results
- conclusion
- baseline reference
- `metrics_summary`
- `metric_rows` when available
- the metric contract actually used
- verdict
- evidence paths
- changed files
- relevant config paths when applicable
- `evaluation_summary` with exactly these six fields:
  - `takeaway`
  - `claim_update`
  - `baseline_relation`
  - `comparability`
  - `failure_mode`
  - `next_action`

Use `evaluation_summary` as the short structured judgment layer on top of the longer narrative fields:

- `takeaway`: one sentence the next reader can reuse directly
- `claim_update`: `strengthens`, `weakens`, `narrows`, or `neutral`
- `baseline_relation`: `better`, `worse`, `mixed`, or `not_comparable`
- `comparability`: `high`, `medium`, or `low`
- `failure_mode`: `none`, `implementation`, `evaluation`, `environment`, or `direction`
- `next_action`: the immediate route such as `continue`, `revise_idea`, `analysis_campaign`, `write`, or `stop`

After `artifact.record_main_experiment(...)` succeeds, do not assume the same branch should absorb the next round by default.
Interpret the measured result first, then either:

- launch analysis from this branch, or
- compare candidate foundations and create the next child research branch

Use `artifact.create_analysis_campaign(...)` only when the extra slices have clear academic or claim-level value relative to their resource cost.
If the main need is simply to continue optimization from a measured result, prefer a new durable child idea branch instead of an expensive analysis package by reflex.
If the extra work should happen on an older durable branch rather than the current head, first switch the runtime back there with `artifact.activate_branch(...)`, then launch the analysis campaign from that activated workspace.

When `artifact.record_main_experiment(...)` succeeds, send a richer threaded `artifact.interact(kind='milestone', ...)` update rather than a generic one-line progress ping.
Lead that milestone with a concise `1-2` sentence outcome summary before expanding into more detail.
That milestone should state:

- the research question that was tested
- the primary result and baseline delta
- whether the run supports, weakens, or leaves the idea inconclusive
- the main caveat or confidence note that still matters
- the exact recommended next move

Do not treat a main run as durably complete until `artifact.record_main_experiment(...)` succeeds.

Recommended per-run documentation fields:

1. research question
2. research type
3. research objective
4. experimental setup
5. experimental results
6. experimental analysis
7. experimental conclusions

For durable main runs, these seven fields should be progressively filled as the run advances, not only at final packaging time.
For lightweight runs, a shorter summary is acceptable if the route remains obvious and the result is still durably recorded.

`RUN.md` should make it easy for later stages to answer:

- what changed?
- how can this run be reproduced?
- what are the main results?
- why did it work or fail?
- what should happen next?

Recording rules:

- record results incrementally, not only at the end
- include timestamps when helpful
- include failed attempts, partial runs, and unexpected outcomes
- do not leave placeholder sections for later if the information is already known
- report exactly what happened, not what you hoped would happen

## 8. Decide the next move

The experiment stage should normally end with one of:

- continue the current line
- branch a new line
- launch an analysis campaign
- move to writing
- reset or stop

Do not let the stage end without an explicit next direction.
If analysis is selected, record why the expected information gain is strong enough to justify the added compute, time, or annotation budget.
