# Runtime Boundaries

`isomer-cli project init` creates Project config, the selected generated content root (`isomer-content/` by default or `--content-dir <content-dir>` when supplied), generated content-root policy files, and the Isomer-managed Houmao overlay at `.isomer-labs/.houmao/`. It must not create a Research Topic Config, Topic Workspace directory, or Workspace Runtime state.

`isomer-cli project topics create <topic-id> --statement "<research topic>"` is the explicit command that creates Research Topic Config, Project Manifest topic/workspace registrations, and the selected Topic Workspace directory. It must not create Workspace Runtime state.

`isomer-cli project runtime init` is the explicit command that creates or reopens `state.sqlite` and default runtime directories for the selected Topic Workspace.

`isomer-cli project runtime prepare` records Topic Environment Readiness. It does not install Pixi environments or silently repair dependency problems.

`isomer-cli project runtime validate --require-ready-readiness` checks launch-facing readiness without mutating runtime state.

Agent Team Instance creation, Houmao launch materialization, live launch, inspection, handoff, and stop operations are later explicit commands. Do not run them from Project initialization or read-only Project checks.
