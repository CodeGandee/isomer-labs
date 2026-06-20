# Milestone 4 Prepares Topic Environment Readiness

Milestone 4 will verify explicit Project Manifest topic Pixi environment bindings and prepare topic-specific Pixi environment readiness before real Houmao launch, then record the resolved environment use, readiness status, and provenance in Workspace Runtime. It may create Agent Team Instance records in a prepared or pending-launch lifecycle state, but Houmao launch material, mailbox refs, gateway refs, managed-agent ids, and live handoff traffic remain Milestone 5 concerns.

## Status

accepted

## Considered Options

- Validate Pixi and topic environment refs without preparing environments.
- Prepare topic Pixi environment readiness and record it in Workspace Runtime before launch.
- Require full topic smoke commands before Agent Team Instance records are valid.
- Defer all environment preparation to the Service Team during Houmao launch.

## Consequences

- `isomer-cli doctor` and Workspace Runtime preparation commands should expose Project Manifest environment binding and readiness diagnostics before an Execution Adapter starts Houmao-backed agents.
- Agent Team Instance records can be created and reopened without live Houmao refs, as long as their lifecycle state makes the launch boundary explicit.
- Environment setup, dependency repair, or compatibility fixes that mutate state should be recorded as Service Requests, support Artifacts, and Provenance Records.
- Milestone 5 can assume Milestone 4 has already resolved Project Manifest topic environment bindings and readiness, then focus on mapping prepared Isomer records to Houmao launch and inspection surfaces.
