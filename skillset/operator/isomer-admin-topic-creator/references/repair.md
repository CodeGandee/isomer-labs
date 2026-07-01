# Repair

## Workflow

When this command is selected, execute the following steps in order.

1. Run `status` to locate the first blocked, stale, or inconsistent ladder stage.
2. Match the blocker to the owning command: `ensure-project`, `define-topic`, `register-topic`, `init-runtime`, `setup-topic-env`, `setup-actors`, `bootstrap-research`, or `start-manual-research`.
3. Reuse ready evidence and rerun only the selected repair stage after operator approval for mutation, without rerunning ready destructive or expensive stages.
4. After repair, rerun `status` and report whether `create` can continue.

If the user's task does not map cleanly to these steps, name the blocker and suggest the smallest command that can repair it.

## Guardrails

Do not delete, overwrite, reset, pull, reinitialize, or recreate existing repositories, Topic Actor Workspaces, runtime records, or start-pack records without explicit user instruction.
