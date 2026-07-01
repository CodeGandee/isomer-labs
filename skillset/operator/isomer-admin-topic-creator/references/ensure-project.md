# Ensure Project

## Workflow

When this command is selected, execute the following steps in order.

1. Resolve the Project root from the user's prompt or current working directory.
2. If `.isomer-labs/` and Project Manifest state are missing and the user approves mutation, delegate Project bootstrap to `isomer-admin-project-mgr init-project` or `isomer-cli project init`.
3. If Project state exists, delegate read-only health checks to `isomer-admin-project-mgr check-project`, `isomer-cli project validate`, or `isomer-cli project doctor`.
4. Report Project root, Project Manifest path, generated content root, Isomer-managed Houmao overlay status, blockers, and next command.

If the user's task does not map cleanly to these steps, ask whether the user wants Project initialization, read-only diagnosis, or a specific Project root.

## Guardrails

Do not create a Research Topic, Topic Workspace, Workspace Runtime, Topic Actor, Agent Workspace, Houmao launch material, mailbox, gateway, or start pack in this command.
