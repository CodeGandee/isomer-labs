# Doctor is Read-only

`isomer-cli doctor` will be a read-only diagnostic command. It checks required dependencies such as Pixi, Project-level Pixi configuration, topic-specific Pixi environment refs, version requirements, lock/readiness signals, and launch preconditions, but it does not install environments, create Workspace Runtime records, or mutate Topic Workspaces.

## Status

accepted

## Considered Options

- Keep `doctor` read-only and add a separate preparation command for environment and runtime mutation.
- Let `doctor --fix` prepare Pixi environments or repair readiness state.
- Make `doctor` always prepare missing topic environments.
- Defer all environment setup to Service Requests during Houmao launch.

## Consequences

- `doctor` can run safely in CI, local preflight, and pre-launch inspection without surprising side effects.
- A future preparation command such as `workspaces prepare` or `runtime prepare` should perform Pixi install/readiness work, create Workspace Runtime readiness records, and record provenance.
- Service Requests remain the durable surface for user-visible environment repair or setup mutation that creates Artifacts or changes dependency, runtime, workspace, or environment state.
- Milestone 4 can separate diagnostics from mutation while still preparing topic environment readiness before Milestone 5 starts real Houmao launch.
