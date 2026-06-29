# Runtime Boundaries

`isomer-cli project init` creates Project config, the selected generated content root (`isomer-content/` by default or `--content-dir <content-dir>` when supplied), generated content-root policy files, and the Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`. It must not create a Research Topic Config, Topic Workspace directory, or Workspace Runtime state.

`isomer-cli project topics create <topic-id> --statement "<research topic>"` is the explicit command that creates Research Topic Config, Project Manifest topic/workspace registrations, and the selected Topic Workspace directory. It must not create Workspace Runtime state.

`isomer-cli project runtime init` is the explicit command that creates or reopens `state.sqlite` and records standard Topic Workspace visibility path plans for the selected Topic Workspace. `topic.repos.main` and `agent.workspace` are worker-facing Git surfaces prepared by topic and agent environment setup; `records/*` is owner-preserved topic record material, and `runtime/` is runtime support material. Runtime init must not create topic-main, Agent Workspace worktrees, root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` as normal worker-visible directories.

`isomer-cli project runtime prepare` records Topic Environment Readiness. It does not install Pixi environments or silently repair dependency problems.

`isomer-cli project runtime validate --require-ready-readiness` checks launch-facing readiness without mutating runtime state.

Agent Team Instance creation, Houmao launch materialization, live launch, inspection, handoff, and stop operations are later explicit commands. Do not run them from Project initialization or read-only Project checks.

Per-agent worktree preparation belongs to `isomer-srv-agent-env-setup` after topic env predecessor evidence exists. Project manager guidance should hand off cwd readiness to that service, and use `isomer-admin-topic-workspace-mgr` only for optional topology inspection, branch helper operations, boundary summaries, manual compatibility operations, and legacy diagnostics.
