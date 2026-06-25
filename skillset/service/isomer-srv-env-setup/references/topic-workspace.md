# Topic Workspace Setup

Use this subcommand to run the full gate-driven setup flow for one Topic Workspace.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Resolve the Topic Workspace**. Load [resolve-workspace.md](resolve-workspace.md), execute its `## Workflow`, and carry forward its workspace context.
2. **Read the source gate**. Load [read-gate.md](read-gate.md), execute its `## Workflow`, and carry forward the source gate summary.
3. **Get required repos**. Load [get-repos.md](get-repos.md), execute its `## Workflow`, and carry forward repo paths, source warnings, and repo inspection notes.
4. **Derive the operational gate**. Load [derive-gate.md](derive-gate.md), execute its `## Workflow`, and carry forward `derived_gate_path`.
5. **Install dependencies**. Load [install-deps.md](install-deps.md), execute its `## Workflow`, and carry forward commands run and changed files.
6. **Verify the gate**. Load [verify-gate.md](verify-gate.md), execute its `## Workflow`, and use its result as the final readiness status.
7. **Report the combined result** using the parent skill's **Output Contract**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the linked subcommands, parent guardrails, and user request, then execute the plan.

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

- Run the subcommands in the order listed in **Workflow**; do not skip directly to dependency installation.
- Stop and report a blocker when any step reports a missing predecessor artifact.
- Keep all direct mutation scoped to the selected Topic Workspace Pixi environment and required repos under `repos/<repo-name>`.
