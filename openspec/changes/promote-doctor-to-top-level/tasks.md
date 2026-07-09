## 1. CLI Command Surface

- [x] 1.1 Register `doctor` on the root `isomer-cli` group and remove `register_doctor_commands(project_group)`.
- [x] 1.2 Ensure `isomer-cli doctor --help` exposes read-only Project selector options and repeatable `--with-topic <research-topic-id>` filters.
- [x] 1.3 Ensure `isomer-cli project doctor` fails as an unknown Project subcommand with no compatibility alias.
- [x] 1.4 Update top-level command overview text and examples so `doctor` appears as a first-class command.

## 2. Doctor Diagnostics

- [x] 2.1 Ensure doctor always performs system-level checks for required Pixi and optional Houmao manager availability.
- [x] 2.2 Make Houmao diagnostics deterministic and non-fatal when `houmao-mgr` is missing, fails, times out, or returns unusable version output.
- [x] 2.3 Ensure doctor always attempts Project discovery and reports no-Project, discovered-Project, and invalid explicit selector outcomes.
- [x] 2.4 Implement default topic scanning for all manifest-registered active Research Topics and their registered or default Topic Workspaces when a Project exists and no `--with-topic` filter is supplied.
- [x] 2.5 Implement repeatable `--with-topic <research-topic-id>` filtering so one or more filters include only requested Research Topic ids.
- [x] 2.6 Report unknown or duplicate Research Topic id filters deterministically without crashing, and do not match Topic Workspace ids as a compatibility fallback.
- [x] 2.7 Replace singular JSON `topic` output with stable `topics: []` output and include Research Topic ids in per-topic payloads and topic-scoped check details.
- [x] 2.8 Confirm doctor remains read-only and does not create Pixi, Houmao, Workspace Runtime, Topic Workspace artifact, Run, or Agent Workspace state.

## 3. Usage Cleanup

- [x] 3.1 Replace non-archived docs references to `isomer-cli project doctor` or `project doctor` with `isomer-cli doctor` or `doctor` as appropriate.
- [x] 3.2 Update CLI examples and self-query usage strings from `project doctor` to `doctor`.
- [x] 3.3 Update packaged system skill assets and validation fixtures so agents recommend `isomer-cli doctor`.
- [x] 3.4 Update current OpenSpec specs or active deltas that describe CLI command surfaces so they no longer present `project doctor`.

## 4. Tests and Validation

- [x] 4.1 Update CLI unit tests to invoke `doctor` at top level.
- [x] 4.2 Add or update tests proving `project doctor` is removed and does not alias to root doctor.
- [x] 4.3 Add or update tests for required Pixi and optional Houmao host checks in JSON and text output.
- [x] 4.4 Add or update tests for default all-topic scanning and `--with-topic` filtered scanning.
- [x] 4.5 Add or update tests proving optional Houmao warnings do not make `ok` false, while required failures do.
- [x] 4.6 Run `openspec validate promote-doctor-to-top-level --strict`.
- [x] 4.7 Run `pixi run lint`, `pixi run typecheck`, and targeted CLI/unit tests.
