# Verify Env Gate

Use this subcommand to run the desired command through Pixi and decide Topic Workspace environment readiness for a single agent or operator working in the selected Topic Workspace root, the Topic Main Development Repository, or a repo-specific working directory named by `topic.env.topic_setup_target_spec`. This is topic-scoped verification; per-Agent Workspace cwd verification is not checked here.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Workspace context | Require `project_root`, `research_topic_id`, `topic_workspace_dir`, `manifest_path_or_dir`, `manifest_path`, and `pixi_environment` from `resolve-topic-workspace`. Refuse to run if any value is missing, and tell the user to run `resolve-topic-workspace` first. |
| Topic env target spec | Require resolved `topic.env.topic_setup_target_spec` from `derive-env-gate`. Refuse to run if it is missing, and tell the user to run `derive-env-gate` first. |
| Topic-main and projection evidence | Require `ensure-topic-main-repository`, `ensure-topic-repos`, and `project-extern-repos` outputs when the target spec names topic-main, canonical external repos, or projected external repos. |
| Installed dependencies | Require an `install-topic-deps` result unless the prompt explicitly asks to verify an existing environment. In either case, check Pixi files before running verification commands. |
| Verification commands, expected results, resource check plan, and enclosure records | Read from the derived gate's `## Verification Commands`, `## Expected Results`, `## Resource Check Plan`, and enclosure records in `## Dependency Plan` and `## Execution Log`. Refuse to claim readiness if commands, expectations, resource checks for heavy commands, runtime wiring, or fallback records are missing or ambiguous. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context from `resolve-topic-workspace`, resolved `topic.env.topic_setup_target_spec`, topic-main/repo/projection predecessor outputs when required, and installed dependencies from `install-topic-deps`.
2. **Read the target spec**:
   - Extract `## Verification Commands`, `## Expected Results`, `## Resource Check Plan`, `## Blockers`, `## Repo Requirements`, `## Projection Requirements`, any `## Inferred Source Warnings`, and enclosure records for Pixi-managed dependencies, external runtime wiring, and topic-local fallbacks.
3. **Check Pixi files**:
   - Confirm the resolved `manifest_path`, the Topic Workspace `pixi.lock`, and `<topic-workspace-dir>/.pixi/` exist before reporting readiness.
   - The resolved manifest may be `pixi.toml` or Pixi-enabled `pyproject.toml`.
4. **Confirm verification commands are replayable**:
   - Each command must use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`.
   - When a command needs external runtime wiring, the target spec must record the exact variables, paths, sourced scripts, or activation commands before the command runs.
   - When the gate depends on package-specific runtime behavior, use the verification expectations recorded from `isomer-misc-pkg-specifics`.
5. **Check resources before heavy verification commands**:
   - Treat compilation, deep model inference, full dataset download, large archive extraction, broad test suites, multi-process training, and large GPU jobs as heavy.
   - Use lightweight read-only probes before heavy commands, including CPU load, available memory, available disk space, and GPU availability or active GPU processes when relevant.
   - Prefer the smallest proof that satisfies the gate: smoke tests, sample data, reduced parallelism, selected tests, dry-run, metadata check, skip, or defer.
   - If resources are insufficient, ambiguous, or already busy, do not run the heavy command. Report `blocked` or `not checked` with `resource_check_status: blocked` or `deferred`.
6. **Run verification commands through Pixi**:
   - Run from the Topic Workspace root unless the target spec specifies the resolved Topic Main Development Repository or a repo-specific working directory.
   - Do not rely on an activated shell, ambient Python environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script.
7. **Compare results to expected outputs** from the target spec.
8. **Update `topic.env.topic_setup_target_spec` `## Execution Log`**:
   - Include resource check evidence, conservative execution decisions, commands run, exit status, relevant output summary, enclosure records used, and pass/fail result.
9. **Report readiness**:
   - Use `ready` only when Pixi files exist, topic-main evidence is ready when required, required canonical repos exist, required projections are ready or explicitly blocked, inferred-source warnings are reported, enclosure records are complete, and all verification commands satisfy the expected results.
   - Otherwise report `failed` or `blocked`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `topic.env.topic_setup_target_spec`, parent guardrails, and user request, then execute the plan.

## Readiness Rules

- `ready`: all required Pixi files exist, topic-main and projection predecessor evidence is ready when required, all required repos exist, enclosure records are complete, and verification commands pass through recorded Pixi-scoped commands.
- `failed`: verification commands ran and did not satisfy expected results.
- `blocked`: predecessor artifacts, Pixi files, topic-main evidence, repo evidence, projection evidence, dependencies, enclosure records, permissions, or expected results are missing.
- `not checked`: verification was not requested or was intentionally deferred.

When `ready` depends on Pixi-mediated external runtime wiring or `.isomer-user-env/` fallback, include a warning in the final output naming the paths, scripts, variables, or fallback prefix and explaining that those pieces may need repair or reinstall if the Topic Workspace moves or the host runtime changes.

## Guardrails

- Do not claim readiness merely because `pixi install` succeeded.
- Do not claim package-specific runtime readiness from generic install success. Use the relevant package-specific checks from `isomer-misc-pkg-specifics` when the target spec names them.
- Do not claim per-agent cwd readiness from a topic-root command. If every `agent.workspace` cwd must prove a gate, report that per-agent readiness is not checked and name the Topic Workspace predecessor evidence produced by this verification.
- Do not claim readiness from ambient shell success. If a command only passes because of an already activated environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script, report `blocked` or `failed` and name the missing enclosure record.
- Do not require or verify `team-profile/`, Topic Agent Team Profile material, Agent Team Instance records, roles, or agent count before reporting environment readiness.
- Do not run live agent launch, Agent Instance creation, Topic Agent Team Profile materialization, GUI operation, or research decision commands as environment verification.
- Do not suppress warnings about inferred repo sources.
- Do not suppress warnings about external runtime wiring or topic-local user-space fallback.
- Do not run resource-heavy verification merely to make readiness look stronger. When a bounded smoke test is enough, run that. When the full command is required but the host is busy, low on memory or disk, out of GPU capacity, or otherwise uncertain, defer or block with resource evidence.
