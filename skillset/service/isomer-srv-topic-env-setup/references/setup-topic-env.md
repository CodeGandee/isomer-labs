# Setup Topic Env

Use this subcommand to run the full gate-driven development environment setup flow for one Topic Workspace. The setup target is the command set one agent or operator needs to run the research from the selected Topic Workspace, the Topic Main Development Repository, or a repo-specific working directory named by the target spec; Topic Agent Team Profile material and Agent Team Instance structure are not prerequisites.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| `subcommand` | Use this page when the prompt names `setup-topic-env`, or when the prompt describes concrete Topic Workspace setup without naming another subcommand. |
| `setup_mode` | Use `fast-forward` for `fast-forward`, `fast-foward`, `auto`, `automatic`, or equivalent direct-execution wording. Use `step-by-step` for `step-by-step`, `manual`, `interactive`, confirmation, or equivalent user-controlled wording. Default to `fast-forward` for concrete setup tasks unless the prompt asks to inspect, decide, or proceed carefully. |
| Project root | Use the provided path or current working directory; it must resolve to an Isomer Project root containing `.isomer-labs/manifest.toml`. |
| Research Topic or Topic Workspace selector | Read a Research Topic id, Topic Workspace ref, or Topic Workspace path from the prompt or Project Manifest context. Ask only when several topics remain plausible. |
| `topic_workspace_dir`, `semantic_paths`, `manifest_path_or_dir`, `manifest_path`, `pixi_environment` | Resolve through `resolve-status` before any later step mutates or verifies Pixi state. `semantic_paths` must include setup labels such as `topic.repos.main`, `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, and `topic.runtime`; `manifest_path_or_dir` may be an explicit file target, an explicit directory target, or the implicit Topic Workspace directory default; `manifest_path` is Pixi's resolved manifest path. |
| Topic env source intent | Resolve `topic.intent.topic_env_requirements` when deriving from user-authored source intent. Under `isomer-default.v1`, this defaults to `<topic-workspace-dir>/intent/src/topic-env-gate.md`; `read-env-gate` must confirm it exists before source-intent-derived readiness can be claimed. |
| Topic env target spec | Resolve `topic.env.topic_setup_target_spec`, or accept an explicit manual target spec file, prompt, or context. Under `isomer-default.v1`, the label defaults to `<topic-workspace-dir>/intent/derived/isomer-env-gate.md`; `derive-env-gate` must create, update, normalize, or validate it before install or verification. |

When asking for missing input, separate `Required` values from `Optional` modifiers. If no optional inputs apply, say `Optional: none for this setup run.`

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Select execution mode** from the prompt:
   - Use `fast-forward` mode for `fast-forward`, `fast-foward`, `auto`, `automatic`, `just do it`, `fully setup`, or equivalent direct-execution wording.
   - Use `step-by-step` mode for `step-by-step`, `manual`, `interactive`, `ask me`, `confirm before each step`, or equivalent user-controlled wording.
   - If the prompt gives a concrete setup task but no mode, default to `fast-forward` unless the prompt asks to inspect, decide, or proceed carefully.
2. **Run the setup chain** in this fixed order:
   - Run `resolve-status`, `read-env-gate` when deriving from source intent, `derive-env-gate`, `ensure-topic-main-repository`, `ensure-topic-repos`, `project-extern-repos`, `install-topic-deps`, and `verify-env-gate`.
   - If an explicit target spec is supplied, `derive-env-gate` validates that spec and records its source instead of requiring `read-env-gate`.
   - Preserve every source-intent runnable target through the chain. Operations that `isomer-misc-bounded-run-tips` classifies as `heavy` or `unknown-risk` must become bounded real-path setup and verification commands, not generic smoke tests that miss the requested build, inference, dataset, or benchmark path.
3. **In `fast-forward` mode**, load each referenced subcommand page, execute its `## Workflow`, and carry forward its outputs to the next step without pausing for optional consent.
4. **In `step-by-step` mode**, pause before each step:
   - Explain what will happen and why.
   - Present an option table from **Manual Choice**.
   - State the recommended option after the table.
   - Wait for the user to choose.
   - Execute only the chosen action, then report the result before offering the next step.
5. **Stop on blockers** in either mode:
   - Stop when a step reports missing required inputs, missing predecessor artifacts, unsafe ambiguity, out-of-scope requests, or a failed precondition.
6. **Report the combined result** using the parent skill's **Essential Output** by default and **Complete Output** when requested:
   - Include `subcommand`, selected `mode`, step results, topic-main Git state, Isomer-managed namespace posture, projection metadata, resource check status, bounded real-path decisions, commands run, changed files, enclosure strategy, external runtime wiring, topic-local fallbacks, Topic Workspace readiness status, `per_agent_readiness_status: not checked` when relevant, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the linked subcommands, parent guardrails, mode rules, and user request, then execute the plan.

## Step Order

| Order | Step | Reference | Carry Forward |
| --- | --- | --- | --- |
| 1 | Resolve the Topic Workspace | [resolve-status.md](resolve-status.md) | Project root, Research Topic, Topic Workspace, semantic setup paths, Pixi binding, and blockers. |
| 2 | Read the source intent | [read-env-gate.md](read-env-gate.md) | `topic.intent.topic_env_requirements` metadata, source intent summary, runnable target, repo hints, and blockers. Skip only when an explicit manual target spec is supplied. |
| 3 | Derive or validate the target spec | [derive-env-gate.md](derive-env-gate.md) | `topic.env.topic_setup_target_spec` metadata, target spec source, repository requirements, projection access intent, dependency plan, enclosure strategy, resource check plan, verification commands, and blockers. |
| 4 | Ensure Topic Main Development Repository | [ensure-topic-main-repository.md](ensure-topic-main-repository.md) | Topic-main Git state, owner branch posture, Isomer-managed namespace posture, changed files, commands run, and blockers. |
| 5 | Ensure canonical external repos | [ensure-topic-repos.md](ensure-topic-repos.md) | Repo paths, source warnings, inspection notes, read-only existing-repo evidence, and blockers. |
| 6 | Project external repos into topic-main | [project-extern-repos.md](project-extern-repos.md) | Projection paths, projection access intent, projection manifest metadata, changed files, and blockers. |
| 7 | Install dependencies | [install-topic-deps.md](install-topic-deps.md) | Commands run, changed Pixi files, external runtime wiring, topic-local fallbacks, install results, and blockers. |
| 8 | Verify the gate | [verify-env-gate.md](verify-env-gate.md) | Gate execution results, resource check evidence, bounded real-path decisions, enclosure warnings, topic-main/projection readiness evidence, and final readiness status. |

## Fast-Forward Mode

Run the steps in **Step Order** directly. Do not pause for optional user consent between steps. Stop only when a step reports a blocker, a required input is missing, the next action is unsafe or ambiguous, or the user request leaves the service-safe boundary.

## Step-by-Step Mode

Before each step:

1. Name the next step and status the current state.
2. Explain why the step is needed before later setup can be correct.
3. Present a Markdown table with columns `Option`, `Explain`, and `Pros and Cons`.
4. After the table, write `Recommended: <option> - <reason>. This is recommended because <why>.` Use the option name exactly as shown in the table.
5. Ask the user to choose an option, then stop and wait.

After the user chooses, execute one chosen action, report the result, and then offer the next step with a new option table.

Use this default option set when there are no meaningful alternatives:

| Option | Explain | Pros and Cons |
| --- | --- | --- |
| A | Proceed with the next step. | Pros: keeps setup moving and preserves the required order. Cons: may reveal blockers that require user repair. |
| B | Stop before this step. | Pros: safest when the next action is uncertain. Cons: leaves setup incomplete. |

Recommended: A - Proceed with the next step. This is recommended because the workflow needs this artifact or action before later setup can be correct.

When there are meaningful alternatives, replace or add rows for those alternatives. Examples include candidate repo sources, package-source choices, repair routes for missing gate files, or whether to stop after a blocker. Keep the recommendation outside the table.

## Expected Result

Successful setup leaves the selected Topic Workspace with:

```text
<topic-workspace-dir>/
  .pixi/
  .gitignore
  pixi.toml
  pixi.lock
  .isomer-user-env/   # only when topic-local fallback is needed
  repos/
    topic-main/          # default `topic.repos.main`; prepared by topic env setup
      isomer-managed/
        tracked/
          manifests/
            extern-projections.toml
        topic-owned/
          readonly/
            extern/
          writable/
            extern/
    extern/              # default canonical non-main `topic.repos.*` repositories
      <repo-label-path>/
  intent/
    src/
      topic-env-gate.md        # default binding for topic.intent.topic_env_requirements
    derived/
      isomer-env-gate.md       # default binding for topic.env.topic_setup_target_spec
```

Readiness means the desired command from the resolved `topic.env.topic_setup_target_spec` runs successfully through recorded Pixi-scoped commands for a single agent or operator working in the selected Topic Workspace root, the resolved Topic Main Development Repository, or a repo-specific working directory named by the target spec. It also means required topic-main setup, canonical external repos, and external projections are ready or explicitly blocked. It does not merely mean that Pixi files exist, it does not mean a command passed because the ambient shell already had a global tool, activated environment, PATH entry, library path, or sourced script, and it does not mean a Topic Agent Team Profile, per-Agent Workspace cwd, or live Agent Team Instance is ready. A generic smoke test can support diagnostics but cannot replace bounded real-path verification of each source-intent runnable target.

Example for CUDA kernel setup: if the source intent requires building a baseline kernel and running a baseline benchmark, the target spec should identify the local GPU with `nvidia-smi`, compile only that host architecture, cap build parallelism such as `MAX_JOBS=1`, build a selected baseline kernel or extension rather than all release artifacts, and run a tiny benchmark case with a short input shape and few iterations. If that bounded real path cannot run safely, report a blocker with resource evidence instead of marking readiness ready.

If the caller needs every Agent Workspace cwd verified, report `per_agent_readiness_status: not checked` and list the ready Topic Workspace predecessor evidence that a separate agent readiness workflow can consume. That predecessor evidence includes the ready Topic Workspace Pixi binding, resolved `topic.env.topic_setup_target_spec`, Topic Main Development Repository Git state, Isomer-managed namespace posture, projection metadata, enclosure records, commands run, changed files, and blockers when present. Do not read `topic.intent.agent_env_requirements` or trigger agent env setup from this topic-scoped flow.

The Topic Workspace `.gitignore` may include a default `tmp/` entry as the `isomer-default.v1` binding for the resolved `topic.tmp` label. Report `topic.tmp` when Workspace Path Resolution can resolve it, and preserve the literal `tmp/` ignore entry for default Topic Workspace posture. `tmp/` material is local, ignored, disposable, not shared, and not durable evidence unless another accepted contract promotes it. Add `.pixi/` and `.git/`, add `.isomer-user-env/` only when topic-local fallback is used, and do not add an `extern/orphan` ignore rule from this skill.

## Guardrails

- Run the subcommands in the order listed in **Step Order**; do not skip directly to dependency installation.
- Stop and report a blocker when any step reports a missing predecessor artifact.
- Do not require `team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Team Instances, Agent Workspace plans, roles, or agent count before running this setup chain.
- Keep all direct mutation scoped to the selected Topic Workspace Pixi environment, the resolved Topic Main Development Repository Isomer-managed namespace, missing required canonical external repos at resolved non-main `topic.repos.*` paths, and external projections under `isomer-managed/topic-owned/{readonly,writable}/extern/`.
- Carry resource check status, enclosure strategy, external runtime wiring, topic-local fallback warnings, and enclosure blockers from `derive-env-gate`, `install-topic-deps`, and `verify-env-gate` into the combined result.
- Do not mutate an existing repo during `ensure-topic-repos`; later setup or verification steps may only run commands against existing repos when the derived gate explicitly requires those commands.
- Do not read `topic.intent.agent_env_requirements`, write `topic.env.agent_setup_target_spec`, create Agent Workspace worktrees, or claim per-agent cwd readiness from this topic-scoped flow.
