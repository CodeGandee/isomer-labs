# Runtime Boundaries

`isomer-cli project init` creates Project config, the selected generated content root (`isomer-content/` by default or `--content-dir <content-dir>` when supplied), generated content-root policy files, and the Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`. It must not create a Research Topic Config, Topic Workspace directory, or Workspace Runtime state.

`isomer-cli project topics create <topic-id> --statement "<research topic>"` is the explicit command that creates Research Topic Config, Project Manifest topic/workspace registrations, and the selected Topic Workspace directory. It must not create Workspace Runtime state.

`isomer-cli project runtime init` is the explicit command that creates or reopens `state.sqlite` and the standard Topic Workspace visibility layout for the selected Topic Workspace: `repos/topic-main` and `agents/<agent-name>` are worker-facing Git surfaces, `records/*` is owner-preserved topic record material, and `runtime/` is runtime support material. It must not create root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` as normal worker-visible directories.

`isomer-cli project runtime prepare` records Topic Environment Readiness. It does not install Pixi environments or silently repair dependency problems.

`isomer-cli project runtime validate --require-ready-readiness` checks launch-facing readiness without mutating runtime state.

Agent Team Instance creation, Houmao launch materialization, live launch, inspection, handoff, and stop operations are later explicit commands. Do not run them from Project initialization or read-only Project checks.

Per-agent worktree preparation belongs to `isomer-admin-topic-workspace-mgr`. Project manager guidance should hand off worktree setup, owner branch checks, `isomer-managed/` support paths, generated links, and visibility diagnostics instead of duplicating Git worktree instructions.
