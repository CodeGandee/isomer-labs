# Project Manifest References Isomer Workspaces

Isomer Labs will keep platform configuration under the `.isomer-labs/` Project Config Directory, with a Project Manifest in that directory referencing project-local Isomer Workspaces that may live in arbitrary directories. Each Isomer Workspace is scoped to one Research Task, records a task handler, and may reference a selected Topic Agent Team Profile plus a selected Agent Team Instance after launch when delegated. This keeps the project root user-owned and flexible while giving the platform one durable configuration and discovery location for Research Threads, Research Tasks, Runs, Artifacts, and GUI-facing state.

## Status

accepted

## Considered Options

- Store all research state and workspaces inside one generated DeepScientist-style quest directory.
- Make each Run the primary object and attach Project and Isomer Workspace references later.
- Use `.isomer-labs/` as the Project Config Directory and point to arbitrary project-local Isomer Workspaces from a Project Manifest.

## Consequences

- The manifest becomes the authority for workspace discovery and must be validated before runs start.
- Workspace paths need clear relative-path rules, missing-workspace handling, and migration behavior.
- The GUI Backend and Operator Agent can resolve project state through a stable Project Config Directory without forcing all artifacts into one platform-owned directory.
