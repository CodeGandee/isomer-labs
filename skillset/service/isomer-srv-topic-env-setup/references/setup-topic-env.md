# Setup Topic Env

Use this subcommand to run the full gate-driven development environment setup flow for one Topic Workspace. The setup target is the command set one agent or operator needs to run the research from the selected Topic Workspace; Topic Agent Team Profile material and Agent Team Instance structure are not prerequisites.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| `subcommand` | Use this page when the prompt names `setup-topic-env`, or when the prompt describes concrete Topic Workspace setup without naming another subcommand. |
| `setup_mode` | Use `fast-forward` for `fast-forward`, `fast-foward`, `auto`, `automatic`, or equivalent direct-execution wording. Use `step-by-step` for `step-by-step`, `manual`, `interactive`, confirmation, or equivalent user-controlled wording. Default to `fast-forward` for concrete setup tasks unless the prompt asks to inspect, decide, or proceed carefully. |
| Project root | Use the provided path or current working directory; it must resolve to an Isomer Project root containing `.isomer-labs/manifest.toml`. |
| Research Topic or Topic Workspace selector | Read a Research Topic id, Topic Workspace ref, or Topic Workspace path from the prompt or Project Manifest context. Ask only when several topics remain plausible. |
| `topic_workspace_dir`, `semantic_paths`, `manifest_path_or_dir`, `manifest_path`, `pixi_environment` | Resolve through `resolve-topic-workspace` before any later step mutates or verifies Pixi state. `semantic_paths` must include setup labels such as `topic.main_repo`, `topic.records`, and `topic.runtime`; `manifest_path_or_dir` may be an explicit file target, an explicit directory target, or the implicit Topic Workspace directory default; `manifest_path` is Pixi's resolved manifest path. |
| `env_gate_path` | Use `<topic-workspace-dir>/user-intent/src/env-gate.md`; `read-env-gate` must confirm it exists before readiness can be claimed. |
| `derived_gate_path` | Use `<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md`; `derive-env-gate` must create or update it before install or verification. |

When asking for missing input, separate `Required` values from `Optional` modifiers. If no optional inputs apply, say `Optional: none for this setup run.`

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Select execution mode** from the prompt. Use `fast-forward` mode for `fast-forward`, `fast-foward`, `auto`, `automatic`, `just do it`, `fully setup`, or equivalent direct-execution wording. Use `step-by-step` mode for `step-by-step`, `manual`, `interactive`, `ask me`, `confirm before each step`, or equivalent user-controlled wording. If the prompt gives a concrete setup task but no mode, default to `fast-forward` unless the prompt asks to inspect, decide, or proceed carefully.
2. **Run the setup chain** in this fixed order: `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate`.
3. **In `fast-forward` mode**, load each referenced subcommand page, execute its `## Workflow`, and carry forward its outputs to the next step without pausing for optional consent.
4. **In `step-by-step` mode**, before each step, explain what will happen and why, present an option table from **Manual Choice**, state the recommended option after the table, wait for the user to choose, execute only the chosen action, then report the result before offering the next step.
5. **Stop on blockers** in either mode when a step reports missing required inputs, missing predecessor artifacts, unsafe ambiguity, out-of-scope requests, or a failed precondition.
6. **Report the combined result** using the parent skill's **Output Contract**, including `subcommand`, selected `mode`, step results, commands run, changed files, enclosure strategy, external runtime wiring, topic-local fallbacks, readiness status, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the linked subcommands, parent guardrails, mode rules, and user request, then execute the plan.

## Step Order

| Order | Step | Reference | Carry Forward |
| --- | --- | --- | --- |
| 1 | Resolve the Topic Workspace | [resolve-topic-workspace.md](resolve-topic-workspace.md) | Project root, Research Topic, Topic Workspace, semantic setup paths, Pixi binding, and blockers. |
| 2 | Read the source gate | [read-env-gate.md](read-env-gate.md) | Source gate summary, runnable target, repo hints, and blockers. |
| 3 | Ensure required repos | [ensure-topic-repos.md](ensure-topic-repos.md) | Repo paths, source warnings, inspection notes, and blockers. |
| 4 | Derive the operational gate | [derive-env-gate.md](derive-env-gate.md) | `derived_gate_path`, dependency plan, enclosure strategy, verification commands, and blockers. |
| 5 | Install dependencies | [install-topic-deps.md](install-topic-deps.md) | Commands run, changed Pixi files, external runtime wiring, topic-local fallbacks, install results, and blockers. |
| 6 | Verify the gate | [verify-env-gate.md](verify-env-gate.md) | Gate execution results, enclosure warnings, and final readiness status. |

## Fast-Forward Mode

Run the steps in **Step Order** directly. Do not pause for optional user consent between steps. Stop only when a step reports a blocker, a required input is missing, the next action is unsafe or ambiguous, or the user request leaves the service-safe boundary.

## Step-by-Step Mode

Before each step:

1. Name the next step and summarize the current state.
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
  repos/                 # default `topic.main_repo` parent for independent setup repos
    <repo-name>/
  user-intent/
    src/
      env-gate.md
    derived/
      isomer-env-gate.md
```

Readiness means the desired command from `isomer-env-gate.md` runs successfully through recorded Pixi-scoped commands for a single agent or operator working in the selected Topic Workspace. It does not merely mean that Pixi files exist, it does not mean a command passed because the ambient shell already had a global tool, activated environment, PATH entry, library path, or sourced script, and it does not mean a Topic Agent Team Profile, per-Agent Workspace cwd, or live Agent Team Instance is ready.

If the caller needs every Agent Workspace cwd verified, route that downstream work to `isomer-srv-agent-env-setup`. That service consumes the ready Topic Workspace Pixi binding, `user-intent/src/agent-env-gate.md`, Topic Main Repository topology, authoritative Agent Names, and resolved `agent.workspace` paths, then writes `user-intent/derived/isomer-agent-env-gate.md`.

The Topic Workspace `.gitignore` may include a default `tmp/` entry only as part of the downstream `topic.tmp` label posture. `tmp/` material is local, ignored, disposable, not shared, and not durable evidence unless another accepted contract promotes it. Add `.pixi/` and `.git/`, add `.isomer-user-env/` only when topic-local fallback is used, and do not add an `extern/orphan` ignore rule from this skill.

## Guardrails

- Run the subcommands in the order listed in **Step Order**; do not skip directly to dependency installation.
- Stop and report a blocker when any step reports a missing predecessor artifact.
- Do not require `team-profile/`, Topic Agent Team Profile material, Topic Team Instantiation Packets, Agent Team Instances, Agent Workspace plans, roles, or agent count before running this setup chain.
- Keep all direct mutation scoped to the selected Topic Workspace Pixi environment and missing required repos under the resolved topic repository root.
- Carry enclosure strategy, external runtime wiring, topic-local fallback warnings, and enclosure blockers from `derive-env-gate`, `install-topic-deps`, and `verify-env-gate` into the combined result.
- Do not mutate an existing repo during `ensure-topic-repos`; later setup or verification steps may only run commands against existing repos when the derived gate explicitly requires those commands.
- Do not read `user-intent/src/agent-env-gate.md`, write `user-intent/derived/isomer-agent-env-gate.md`, create Agent Workspace worktrees, or claim per-agent cwd readiness from this topic-scoped flow.
