# Runtime Boundaries

`isomer-cli init` creates Project config, the first Research Topic Config, the first Topic Workspace directory, and the Project-level Houmao overlay. It must not create Workspace Runtime state.

`isomer-cli runtime init` is the explicit command that creates or reopens `state.sqlite` and default runtime directories for the selected Topic Workspace.

`isomer-cli runtime prepare` records Topic Environment Readiness. It does not install Pixi environments or silently repair dependency problems.

`isomer-cli runtime validate --require-ready-readiness` checks launch-facing readiness without mutating runtime state.

Agent Team Instance creation, Houmao launch materialization, live launch, inspection, handoff, and stop operations are later explicit commands. Do not run them from Project initialization or read-only Project checks.
