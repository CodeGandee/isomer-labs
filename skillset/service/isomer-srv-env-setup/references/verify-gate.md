# Verify Gate

Use this subcommand to run the desired command through Pixi and decide Topic Workspace environment readiness.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path`, and `pixi_environment` from `resolve-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-workspace` first. |
| Derived gate | Require `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` from `derive-gate`. Refuse to run if it is missing, and tell the user to run `derive-gate` first. |
| Installed dependencies | Require an `install-deps` result unless the prompt explicitly asks to verify an existing environment. In either case, check Pixi files before running verification commands. |
| Verification commands and expected results | Read from the derived gate's `## Verification Commands` and `## Expected Results` sections. Refuse to claim readiness if either section is missing or ambiguous. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**: workspace context from `resolve-workspace`, `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`, and installed dependencies from `install-deps`.
2. **Read `isomer-env-gate.md`** and extract `## Verification Commands`, `## Expected Results`, `## Blockers`, and any `## Inferred Source Warnings`.
3. **Check Pixi files**. Confirm `<topic-workspace-dir>/pixi.toml`, `<topic-workspace-dir>/pixi.lock`, and `<topic-workspace-dir>/.pixi/` exist before reporting readiness.
4. **Run verification commands through Pixi** using `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`. Run from the Topic Workspace root unless the derived gate specifies a repo-specific working directory. Do not rely on an activated shell or ambient Python environment.
5. **Compare results to expected outputs** from `isomer-env-gate.md`.
6. **Update `isomer-env-gate.md`** `## Execution Log` with commands run, exit status, relevant output summary, and pass/fail result.
7. **Report readiness** as `ready` only when Pixi files exist, required repos exist, inferred-source warnings are reported, and all verification commands satisfy the expected results. Otherwise report `failed` or `blocked`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `isomer-env-gate.md`, parent guardrails, and user request, then execute the plan.

## Readiness Rules

- `ready`: all required Pixi files exist, all required repos exist, and verification commands pass.
- `failed`: verification commands ran and did not satisfy expected results.
- `blocked`: predecessor artifacts, Pixi files, repos, dependencies, permissions, or expected results are missing.
- `not checked`: verification was not requested or was intentionally deferred.

## Guardrails

- Do not claim readiness merely because `pixi install` succeeded.
- Do not run live agent launch, Agent Instance creation, GUI operation, or research decision commands as environment verification.
- Do not suppress warnings about inferred repo sources.
