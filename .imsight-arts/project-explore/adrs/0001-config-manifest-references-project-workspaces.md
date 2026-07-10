# Project Manifest References Topic Workspaces

Isomer Labs will keep platform configuration under the `.isomer-labs/` Project Config Directory, with a Project Manifest in that directory registering Research Topics, Research Topic Config files, and project-local Topic Workspaces that may live in arbitrary directories. Each Topic Workspace is scoped to one Research Topic and records that topic's Research Inquiries, Research Tasks, Runs, Artifacts, selected Topic Agent Team Profiles, and selected Agent Team Instances when delegated. This keeps the project root user-owned and flexible while giving the platform one durable configuration and discovery location for Research Topics, Research Topic Config refs, Research Inquiries, Research Tasks, Runs, Artifacts, and GUI-facing state.

## Status

accepted

## Considered Options

- Store all research state and workspaces inside one generated DeepScientist-style quest directory.
- Make each Run the primary object and attach Project and Topic Workspace references later.
- Use `.isomer-labs/` as the Project Config Directory and point to arbitrary project-local Topic Workspaces from a Project Manifest.

## Consequences

- The manifest becomes the authority for Research Topic Config registration and Topic Workspace discovery and must be validated before runs start.
- Workspace paths need clear relative-path rules, missing-workspace handling, and migration behavior.
- The GUI Backend and Operator Agent can resolve project state through a stable Project Config Directory without forcing all artifacts into one platform-owned directory.
