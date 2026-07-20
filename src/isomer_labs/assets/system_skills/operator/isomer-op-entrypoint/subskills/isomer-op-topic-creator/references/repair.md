# Repair

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Run `status` to locate the first blocked, stale, or inconsistent ladder stage.
2. Match the blocker to the owning subcommand: `ensure-project`, `resolve-topic-input`, `register-topic`, `create-research-intent`, `init-runtime`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, or `finalize`.
3. Reuse ready evidence and rerun only the selected repair stage after operator approval for mutation, without rerunning ready destructive or expensive stages.
4. After repair, rerun `status` and report ready, verified, skipped, stale, and blocked state without routing to a next research command.

If the user's task does not map cleanly to these steps, name the blocker and suggest the smallest subcommand that can repair it.

## Guardrails

- DO NOT delete, overwrite, reset, pull, reinitialize, or recreate existing repositories, Topic Actor Workspaces, runtime records, or summary evidence without explicit user instruction.
