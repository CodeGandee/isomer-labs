# Setup for Topic Workspace

Use this subcommand to run the full gate-driven setup flow for one Topic Workspace.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Select execution mode** from the prompt. Use `fast-forward` mode for `fast-forward`, `fast-foward`, `auto`, `automatic`, `just do it`, `fully setup`, or equivalent direct-execution wording. Use `step-by-step` mode for `step-by-step`, `manual`, `interactive`, `ask me`, `confirm before each step`, or equivalent user-controlled wording. If the prompt gives a concrete setup task but no mode, default to `fast-forward` unless the prompt asks to inspect, decide, or proceed carefully.
2. **Run the setup chain** in this fixed order: `resolve-workspace`, `read-gate`, `ensure-repos`, `derive-gate`, `install-deps`, and `verify-gate`.
3. **In `fast-forward` mode**, load each referenced subcommand page, execute its `## Workflow`, and carry forward its outputs to the next step without pausing for optional consent.
4. **In `step-by-step` mode**, before each step, explain what will happen and why, present an option table from **Manual Choice**, state the recommended option after the table, wait for the user to choose, execute only the chosen action, then report the result before offering the next step.
5. **Stop on blockers** in either mode when a step reports missing required inputs, missing predecessor artifacts, unsafe ambiguity, out-of-scope requests, or a failed precondition.
6. **Report the combined result** using the parent skill's **Output Contract**, including `subcommand`, selected `mode`, step results, commands run, changed files, readiness status, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the linked subcommands, parent guardrails, mode rules, and user request, then execute the plan.

## Step Order

| Order | Step | Reference | Carry Forward |
| --- | --- | --- | --- |
| 1 | Resolve the Topic Workspace | [resolve-workspace.md](resolve-workspace.md) | Project root, Research Topic, Topic Workspace, Pixi binding, and blockers. |
| 2 | Read the source gate | [read-gate.md](read-gate.md) | Source gate summary, runnable target, repo hints, and blockers. |
| 3 | Ensure required repos | [ensure-repos.md](ensure-repos.md) | Repo paths, source warnings, inspection notes, and blockers. |
| 4 | Derive the operational gate | [derive-gate.md](derive-gate.md) | `derived_gate_path`, dependency plan, verification commands, and blockers. |
| 5 | Install dependencies | [install-deps.md](install-deps.md) | Commands run, changed Pixi files, install results, and blockers. |
| 6 | Verify the gate | [verify-gate.md](verify-gate.md) | Gate execution results and final readiness status. |

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
  pixi.toml
  pixi.lock
  repos/
    <repo-name>/
  user-intent/
    src/
      env-gate.md
    derived/
      isomer-env-gate.md
```

Readiness means the desired command from `isomer-env-gate.md` runs successfully through the Topic Workspace Pixi environment. It does not merely mean that Pixi files exist.

## Guardrails

- Run the subcommands in the order listed in **Step Order**; do not skip directly to dependency installation.
- Stop and report a blocker when any step reports a missing predecessor artifact.
- Keep all direct mutation scoped to the selected Topic Workspace Pixi environment and missing required repos under `repos/<repo-name>`.
- Do not mutate an existing repo during `ensure-repos`; later setup or verification steps may only run commands against existing repos when the derived gate explicitly requires those commands.
