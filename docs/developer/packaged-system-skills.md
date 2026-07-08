# Packaged System Skills

System skills live under `src/isomer_labs/assets/system_skills/` and are packaged with the Python distribution. They teach agents how to operate Isomer projects, create research intent, manage topic workspaces, use DeepSci workflows, and route tasks through the operator entrypoint.

Public installation should use `npx skills add` against a specific skill directory in the repository:

```bash
npx skills add https://github.com/CodeGandee/isomer-labs/tree/main/src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint --agent codex --yes
```

Core operator skills include `isomer-op-entrypoint` for informed routing and `isomer-op-welcome` for first-time project orientation. Optional extension skills include the DeepSci skills under `research-paradigm/deepsci/`.

This command shape has been verified against `npx skills add` for both local filesystem skill directories and GitHub tree URLs. Prefer direct skill-directory URLs over a repository root install until the repository exposes a dedicated skills catalog.

Repository-root discovery currently finds the repository-local OpenSpec development skills, not packaged system skills under `src/isomer_labs/assets/system_skills/`. Do not document `npx skills add CodeGandee/isomer-labs --skill isomer-op-entrypoint` until a skills-facing catalog or root-level system-skill export exists.

Keep each skill in the supported skill format. Workflow-oriented skills should present their workflow as ordered steps that an agent follows from start to finish, not as detached callback reminders.

When adding a new skill, update the README, the tutorial page for skill installation, and any CLI or packaging tests that assert packaged asset paths.
