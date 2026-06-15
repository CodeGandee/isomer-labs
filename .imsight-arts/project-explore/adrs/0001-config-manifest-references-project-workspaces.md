# Config Manifest References Project Workspaces

Isomer Labs will keep platform configuration under `.isomer-labs/`, with a TOML manifest in that directory referencing project-local workspaces that may live in arbitrary directories. This keeps the project root user-owned and flexible while giving the platform one durable control-plane location for discovering research threads, team runs, artifacts, and generated GUI state.

## Status

accepted

## Considered Options

- Store all research state and workspaces inside one generated quest directory.
- Make each team run the primary object and attach project/workspace references later.
- Use `.isomer-labs/` as the project control-plane directory and point to arbitrary project-local workspaces from a manifest.

## Consequences

- The manifest becomes the authority for workspace discovery and must be validated before runs start.
- Workspace paths need clear relative-path rules, missing-workspace handling, and migration behavior.
- The GUI and operator agent can resolve project state through a stable config directory without forcing all artifacts into one platform-owned workspace.
