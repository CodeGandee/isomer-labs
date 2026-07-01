# Init Runtime

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require a registered Research Topic and Topic Workspace from `register-topic`.
2. Inspect Workspace Runtime status for the selected topic.
3. If runtime is missing and mutation is approved, delegate to `isomer-admin-project-mgr init-runtime` or `isomer-cli project runtime init`.
4. Validate runtime status enough for topic preparation, research record use, Topic Actor audit/provenance records, and later readiness checks.
5. Report runtime status, commands run, blockers, and readiness state.

If the user's task does not map cleanly to these steps, explain whether the blocker is missing topic registration, missing mutation approval, or invalid runtime state.

## Guardrails

Do not create launch-facing adapter material, Agent Team Instances, Houmao agents, mailboxes, or gateways.
