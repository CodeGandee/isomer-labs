# Operational Guidance

Use this reference when the experiment route needs the longer planning, environment, artifact, memory, or charting notes rather than the main control surface in `SKILL.md`.

## Planning surfaces

Use quest or workspace planning files only when they help control a non-trivial run; otherwise keep the run contract small and move to the first decisive execution step.

## Required plan and checklist

Before substantial implementation work or a real main run, create a quest-visible `PLAN.md` and `CHECKLIST.md`.

- Use `references/main-experiment-plan-template.md` as the canonical structure for `PLAN.md`.
- Use `references/main-experiment-checklist-template.md` as the canonical structure for `CHECKLIST.md`.
- `PLAN.md` and `CHECKLIST.md` are the canonical planning-and-control surface before and during execution.
- `PLAN.md` should lead with the selected idea summarized in `1-2` sentences and include the baseline and comparability rules, safe efficiency levers, minimal code-change map, smoke or pilot path, full-run path, fallback options, monitoring and sleep rules, expected outputs, and a revision log.
- Once the route is concrete, implement according to the current `PLAN.md`.
- If the code path, comparability contract, runtime strategy, or execution route changes materially, revise `PLAN.md` before spending more code or compute.

## Working-boundary rules

Only modify the active quest workspace for this experiment line.

- treat the accepted baseline workspace as read-only
- do not derive branch or worktree assumptions from guesswork
- keep all durable outputs inside the quest
- if the runtime gives an explicit worktree path, use it exactly

## Resource note

Respect explicit resource limits and record real environment or dependency constraints, but do not stop the run early just to over-document them.

## Resource and environment rules

- Follow the explicit resource assignment if one exists.
- If GPU assignment is explicit, respect it exactly and record it in the run manifest.
- Do not silently consume extra GPUs or broaden resource scope.
- Capture enough environment information that the run can later be reconstructed.
- If a new dependency appears necessary, record it as a risk and prefer a fallback if possible.

## Required durable outputs

A meaningful experiment pass should leave behind:

- a run directory under `artifacts/experiment/<run_id>/` or the quest-equivalent canonical location
- `artifact_manifest.json`, `run_manifest.json`, `metrics.json`, and `summary.md`
- `metrics.md` and `runlog.summary.md` for durable main runs
- durable command, config, and log pointers
- exported shell log, typically `bash.log`
- a run artifact with explicit deltas versus baseline
- a decision about what should happen next

Recommended additional files:

- `claim_validation.md`
- environment snapshot files such as Python version, package freeze, and GPU info when applicable
- a live execution note or rolling run log when the experiment spans multiple implementation or execution steps

`run_manifest.json` should capture at least:

- `run_id`
- quest or branch context
- baseline reference or commit
- full commands
- config paths and key resolved hyperparameters
- dataset identifier or version
- seeds
- environment snapshot paths
- start time, end time, and final status

If a command needed for environment capture is unavailable, record that gap in the manifest and summary.

## Memory rules

Stage-start requirement:

- begin every experiment pass with `memory.list_recent(scope='quest', limit=5)`
- then run at least one experiment-relevant `memory.search(...)` before reopening a previously tested command path or retrying an old run

Stage-end requirement:

- if the run produced a durable lesson, incident pattern, comparability caveat, or route-changing outcome, write at least one `memory.write(...)` before leaving the stage

## Memory note

Use memory only to avoid repeating known failures or to preserve reusable experiment lessons; the canonical run record belongs in `artifact`.

## Artifact rules

- use `progress` for long-running execution updates
- use `artifact.record_main_experiment(...)` for each meaningful completed main experiment
- use `report` for suspicious-result investigations or analysis-rich summaries when they materially help the next route
- use `decision` for continue / branch / analysis / write / reset / stop
- use `approval` when an explicit user approval is captured for an expensive or risky run change
- use `artifact.checkpoint(...)` when code evolution is meaningful and should be preserved in Git
- after a meaningful experiment checkpoint or completion, emit `artifact.interact(kind='progress' | 'milestone', ...)` so the user sees the concrete result and next step

## Connector-facing chart requirements

When this stage produces connector-facing charts or milestone-facing visuals, keep the palette aligned with the system prompt Morandi plotting template.

- `sage-clay` should be the primary positive or accepted-result color
- `mist-stone` should be the neutral comparison or baseline color
- `dust-rose` should be the restrained caution or limitation accent when needed
- keep light paper-style backgrounds close to `#F3EEE8`
- use calm connector-safe palettes such as `sage-clay`, `mist-stone`, and `dust-rose`
- highlight only the decisive delta; do not color every series as if they are equally important
- stay aligned with the system prompt rather than inventing a new local visual language for each chart
