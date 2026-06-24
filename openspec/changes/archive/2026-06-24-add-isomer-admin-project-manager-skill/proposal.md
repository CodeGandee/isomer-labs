## Why

Operators currently have a Topic Team Specialization skill, but they do not have a matching Project lifecycle skill that explains and drives Isomer Project setup, validation, topic inspection, runtime preparation, and Houmao bootstrap. This gap showed up when an agent correctly failed to resolve `.isomer-labs/` and then mixed stale guidance with an incomplete project-init path.

`isomer-cli init` also creates only the Isomer Project files today. Because Isomer relies on Houmao for agent-team construction and management, Project initialization should create the Project-level Houmao overlay at the same time, while still keeping Workspace Runtime state and live agent launch outside init.

## What Changes

- Add `skillset/operator/isomer-admin-project-mgr/` as the operator/admin skill for initializing, inspecting, validating, and preparing an Isomer Project.
- Give the new skill a lean skill-creator bundle shape: `SKILL.md`, `agents/openai.yaml`, local `references/*.md` subcommand pages, no `evals/`, and no auxiliary docs.
- Format the skill in the Imsight style: near-top numbered `## Workflow`, short local subcommands, detail pages with their own numbered workflows, and a freeform fallback.
- Include subcommands for help, project initialization, project checks, topic and workspace listing, context inspection, runtime initialization, runtime preparation, and handoff to topic-team specialization when a Domain Agent Team Template needs to be adapted for a Research Topic.
- Make empty invocation of `isomer-admin-project-mgr` default to `help`.
- Keep required support knowledge self-contained inside the new skill directory instead of depending on `.imsight-arts/`, `docs/`, `extern/`, or absolute local paths.
- Modify `isomer-cli init` so a successful initialization creates or validates both the Isomer Project configuration and the Project-level Houmao overlay, normally at `<project-root>/.houmao/`.
- Ensure `isomer-cli init` reports deterministic Houmao bootstrap diagnostics and does not claim success when the required Houmao Project overlay cannot be initialized.
- Preserve existing side-effect boundaries: `init` must not create Workspace Runtime databases or directories, Agent Workspaces, adapter launch material, mailboxes, managed agents, or live Houmao sessions.

## Capabilities

### New Capabilities

- `isomer-admin-project-manager-skill`: Defines the `isomer-admin-project-mgr` operator skill bundle, local project-management subcommands, Imsight workflow formatting, self-contained references, no-prompt help behavior, and validation requirements.

### Modified Capabilities

- `isomer-cli-project-discovery`: Changes Project initialization so `isomer-cli init` initializes both Isomer Project config and the Project-level Houmao overlay while preserving runtime and launch boundaries.
- `houmao-cli-adapter-layer`: Clarifies that Project-level Houmao bootstrap is a supported CLI-backed Project setup operation distinct from per-Agent Team Instance adapter launch materialization.

## Impact

- Affected skill files: new `skillset/operator/isomer-admin-project-mgr/SKILL.md`, `skillset/operator/isomer-admin-project-mgr/agents/openai.yaml`, and `skillset/operator/isomer-admin-project-mgr/references/*.md`.
- Affected skillset docs and validators: `skillset/operator/README.md`, `scripts/validate_skillsets.py`, and related tests should recognize and validate the new operator skill.
- Affected CLI code: `src/isomer_labs/init_project.py`, `src/isomer_labs/cli/app.py`, and related Houmao command invocation surfaces.
- Affected tests and docs: `tests/unit/test_isomer_cli.py`, `tests/unit/test_houmao_cli_adapter.py` where needed, `docs/getting-started.md`, `docs/isomer-cli.md`, `docs/houmao-adapter.md`, and troubleshooting docs.
- Affected behavior: fresh `isomer-cli init` runs require a working Houmao CLI boundary or a resolvable local Houmao checkout so the Project-level Houmao overlay can be initialized alongside `.isomer-labs/`.
