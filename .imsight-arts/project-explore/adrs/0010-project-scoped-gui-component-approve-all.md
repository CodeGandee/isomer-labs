# Project-Scoped GUI Component Approve-All

Isomer Labs will support a project-scoped approve-all mode for agent-generated Executable GUI Components. When the human user enables approve-all through the Operator Agent, any registered Executable GUI Component in the Project that passes validation can load without per-component approval until approve-all is revoked.

## Status

accepted

## Considered Options

- Scope approve-all to the current GUI Backend session.
- Scope approve-all to one Isomer Workspace and selected Agent Team Instance.
- Scope approve-all to the whole Project until revoked.

## Consequences

- Approve-all state belongs to the Project, not to one browser session or one Isomer Workspace.
- The GUI Backend and Operator Agent must surface approve-all status clearly because it changes the trust posture for all agent-generated Executable GUI Components in the Project.
- Revocation should stop new loads of unapproved Executable GUI Components. Already loaded components should be marked stale or require reload under the new approval state.
- Project-scoped approve-all does not bypass component registration, manifest validation, sandbox policy, compatibility checks, or AG-UI publisher authentication.
