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
| Verification commands, expected results, resource check plan, gate checklist, and enclosure records | Read from the derived gate's `## Gate Checklist`, `## Verification Commands`, `## Expected Results`, `## Resource Check Plan`, and enclosure records in `## Dependency Plan` and `## Execution Log`. Refuse to claim readiness if required checklist items, commands, expectations, operation classification evidence, bounded-run guidance for `heavy` or `unknown-risk`, generic best-effort fallback evidence when used, runtime wiring, fallback records, or bounded real-path coverage for each source-intent runnable target are missing or ambiguous. |
| Optional modifiers | None for this step. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require predecessor artifacts**:
   - Require workspace context from `resolve-topic-workspace`, resolved `topic.env.topic_setup_target_spec`, topic-main/repo/projection predecessor outputs when required, and installed dependencies from `install-topic-deps`.
2. **Read the target spec**:
   - Extract `## Gate Checklist`, `## Verification Commands`, `## Expected Results`, `## Resource Check Plan`, `## Blockers`, `## Repo Requirements`, `## Projection Requirements`, any `## Inferred Source Warnings`, and enclosure records for Pixi-managed dependencies, external runtime wiring, and topic-local fallbacks.
   - Treat every item under `## Gate Checklist` as required readiness work unless the target spec explicitly moved the item to a non-readiness diagnostic section.
   - Confirm every required checklist item has a pass condition, evidence source, and blocker condition.
   - Confirm that each source-intent runnable target has a matching verification command, bounded real-path command, or blocker. Do not accept a generic import, device-visibility, or repository-inspection smoke test as coverage for a requested build, inference, dataset, or benchmark path.
3. **Check Pixi files**:
   - Confirm the resolved `manifest_path`, the Topic Workspace `pixi.lock`, and `<topic-workspace-dir>/.pixi/` exist before reporting readiness.
   - The resolved manifest may be `pixi.toml` or Pixi-enabled `pyproject.toml`.
4. **Confirm verification commands are replayable**:
   - Each command must use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <command>`.
   - For profiler, tracer, debugger, memory-checker, and similar wrapper tools that execute a target command as a subprocess, Pixi must launch the wrapper tool. Accept `pixi run --manifest-path <manifest_path> --environment <pixi_environment> <wrapper-tool> ... <target-command>` and reject inverted commands shaped as `<wrapper-tool> pixi run ...`, such as `ncu pixi run ...`, `nsys profile pixi run ...`, `valgrind pixi run ...`, or `gdb --args pixi run ...`, unless the target spec records explicit local evidence that Pixi itself is the intended inspected process.
   - When a command needs external runtime wiring, the target spec must record the exact variables, paths, sourced scripts, or activation commands before the command runs.
   - When the gate depends on package-specific runtime behavior, use the verification expectations recorded from `isomer-misc-pkg-specifics`.
   - When a named package has no package-specific page, require the target spec to record `no package-specific rule` before using generic import, CLI, metadata, or smoke verification.
5. **Check resources before classified risky verification commands**:
   - Apply this when bounded-run tips classified a verification command as `heavy` or `unknown-risk`.
   - Treat the generated `## Resource Check Plan` and matching checklist item as the execution contract.
   - Confirm classification source, result, reason, resource dimensions, bounded-run guidance source, bounded command, expected result, and blocker condition.
   - If classification evidence or required bounded guidance is missing, report `blocked` and ask for `derive-env-gate` to repair the target spec before verification.
   - Use lightweight read-only probes before commands classified as `heavy` or `unknown-risk`, including CPU load, available memory, available disk space, and GPU availability or active GPU processes when relevant.
   - Run the smallest real command that exercises the essential path named by the source intent, such as fewer build jobs, selected kernel targets, tiny model or tensor shapes, sample data, reduced iterations, reduced batch size, selected tests, or short benchmark cases.
   - If resources are insufficient, ambiguous, or already busy, do not run an unrelated smoke test in place of the heavy path. Report `blocked` with `resource_check_status: blocked`, the capacity reason, and the bounded real-path command that would be run when capacity is available.
6. **Run verification commands through Pixi**:
   - Run from the Topic Workspace root unless the target spec specifies the resolved Topic Main Development Repository or a repo-specific working directory.
   - Do not rely on an activated shell, ambient Python environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script.
7. **Compare results to expected outputs** from the target spec and mark each relevant checklist item as checked only when the supporting command, path evidence, dependency evidence, resource probe, or expected-result comparison proves that item.
8. **Update `topic.env.topic_setup_target_spec` `## Execution Log`**:
   - Include resource check evidence, bounded real-path execution decisions, commands run, exit status, relevant output summary, enclosure records used, pass/fail result, and any required unchecked checklist item with its exact reason and next safe action.
9. **Report readiness**:
   - Use `ready` only when Pixi files exist, topic-main evidence is ready when required, required canonical repos exist, required projections are ready or explicitly blocked, inferred-source warnings are reported, enclosure records are complete, every required `## Gate Checklist` item is checked with supporting evidence, every source-intent runnable target is covered by a passed verification command or bounded real-path command, and all verification commands satisfy the expected results.
   - If any required checklist item is unchecked, report `blocked`, `failed`, or `not checked` with the exact checklist item, reason, and next safe action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from `topic.env.topic_setup_target_spec`, parent guardrails, and user request, then execute the plan.

## Readiness Rules

- `ready`: all required Pixi files exist, topic-main and projection predecessor evidence is ready when required, all required repos exist, enclosure records are complete, every required `## Gate Checklist` item is checked with supporting evidence, every source-intent runnable target is covered by a passed verification command or bounded real-path command, and verification commands pass through recorded Pixi-scoped commands.
- `failed`: a required checklist item was attempted through its matching command or check and did not satisfy expected results.
- `blocked`: predecessor artifacts, Pixi files, topic-main evidence, repo evidence, projection evidence, dependencies, enclosure records, permissions, expected results, or a required checklist item cannot be completed. Name the exact checklist item and blocker.
- `not checked`: verification was explicitly not requested. Do not use `not checked` to bypass a source-intent runnable target or unchecked checklist item during setup; report `blocked` when a required bounded real-path check cannot be run safely.

When `ready` depends on Pixi-mediated external runtime wiring or `.isomer-user-env/` fallback, include a warning in the final output naming the paths, scripts, variables, or fallback prefix and explaining that those pieces may need repair or reinstall if the Topic Workspace moves or the host runtime changes.

## Guardrails

- Do not claim readiness merely because `pixi install` succeeded.
- Do not claim package-specific runtime readiness from generic install success, solver success, package metadata, or generic import success. Use the relevant package-specific checks from `isomer-misc-pkg-specifics` when the target spec names them, or require explicit `no package-specific rule` evidence before falling back to generic verification.
- Do not claim per-agent cwd readiness from a topic-root command. If every `agent.workspace` cwd must prove a gate, report that per-agent readiness is not checked and name the Topic Workspace predecessor evidence produced by this verification.
- Do not claim readiness from ambient shell success. If a command only passes because of an already activated environment, global package, unrecorded PATH entry, unrecorded library path, or unrecorded sourced script, report `blocked` or `failed` and name the missing enclosure record.
- Do not require or verify `team-profile/`, Topic Agent Team Profile material, Agent Team Instance records, roles, or agent count before reporting environment readiness.
- Do not run live agent launch, Agent Instance creation, Topic Agent Team Profile materialization, GUI operation, or research decision commands as environment verification.
- Do not suppress warnings about inferred repo sources.
- Do not suppress warnings about external runtime wiring or topic-local user-space fallback.
- Do not run verification classified as `heavy` or `unknown-risk` at full scale merely to make readiness look stronger or because the generated bounded-run plan is incomplete. When a bounded real-path command is enough and it exercises the critical path named by the checklist item, run that. When the required source-intent path cannot be exercised safely even in bounded form, block with resource evidence and leave the checklist item unchecked. A simple smoke test that misses the essential code path is not enough to claim readiness.
- Do not mark a required checklist item complete with an unrelated weaker smoke test. If the user explicitly accepts a weaker check, record the user downgrade, original checklist item, weaker evidence, and limitation instead of presenting it as proof that the original critical path passed.
