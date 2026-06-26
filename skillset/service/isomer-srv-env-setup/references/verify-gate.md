# Verify Gate

Use this subcommand to run the desired command through Pixi and decide Topic Workspace environment readiness.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path`, and `pixi_environment` from `resolve-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-workspace` first. |
| Derived gate | Require `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` from `derive-gate`. Refuse to run if it is missing, and tell the user to run `derive-gate` first. |
| Installed dependencies | Require an `install-deps` result unless the prompt explicitly asks to verify an existing environment. In either case, check Pixi files before running verification commands. |
| Verification commands, expected results, and enclosure records | Read from the derived gate's `## Verification Commands`, `## Expected Results`, and enclosure records in `## Dependency Plan` and `## Execution Log`. Refuse to claim readiness if commands, expectations, runtime wiring, or fallback records are missing or ambiguous. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-workspace`, `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`, and installed dependencies from `install-deps`.
2. **Read `isomer-env-gate.md`** and extract `## Verification Commands`, `## Expected Results`, `## Blockers`, any `## Inferred Source Warnings`, and enclosure records for Pixi-managed dependencies, external runtime wiring, and topic-local fallbacks.
3. **Check Pixi files**. Confirm `<topic-workspace-dir>/pixi.toml`, `<topic-workspace-dir>/pixi.lock`, and `<topic-workspace-dir>/.pixi/` exist before reporting readiness.
4. **Confirm verification commands are replayable**. Each command must use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`. When a command needs external runtime wiring, the derived gate must record the exact variables, paths, sourced scripts, or activation commands before the command runs.
5. **Run verification commands through Pixi**. Run from the Topic Workspace root unless the derived gate specifies a repo-specific working directory. Do not rely on an activated shell, ambient Python environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script.
6. **Compare results to expected outputs** from `isomer-env-gate.md`.
7. **Update `isomer-env-gate.md`** `## Execution Log` with commands run, exit status, relevant output summary, enclosure records used, and pass/fail result.
8. **Report readiness** as `ready` only when Pixi files exist, required repos exist, inferred-source warnings are reported, enclosure records are complete, and all verification commands satisfy the expected results. Otherwise report `failed` or `blocked`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `isomer-env-gate.md`, parent guardrails, and user request, then execute the plan.

## Readiness Rules

- `ready`: all required Pixi files exist, all required repos exist, enclosure records are complete, and verification commands pass through recorded Pixi-scoped commands.
- `failed`: verification commands ran and did not satisfy expected results.
- `blocked`: predecessor artifacts, Pixi files, repos, dependencies, enclosure records, permissions, or expected results are missing.
- `not checked`: verification was not requested or was intentionally deferred.

When `ready` depends on Pixi-mediated external runtime wiring or `.isomer-user-env/` fallback, include a warning in the final output naming the paths, scripts, variables, or fallback prefix and explaining that those pieces may need repair or reinstall if the Topic Workspace moves or the host runtime changes.

## Guardrails

- Do not claim readiness merely because `pixi install` succeeded.
- Do not claim readiness from ambient shell success. If a command only passes because of an already activated environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script, report `blocked` or `failed` and name the missing enclosure record.
- Do not run live agent launch, Agent Instance creation, GUI operation, or research decision commands as environment verification.
- Do not suppress warnings about inferred repo sources.
- Do not suppress warnings about external runtime wiring or topic-local user-space fallback.
