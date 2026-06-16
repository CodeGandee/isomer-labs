# Manifested Workspace Engine

Isomer Labs will use a manifested workspace engine as its primary architecture. A project-level Project Manifest at `.isomer-labs/manifest.toml` discovers arbitrary project-local Isomer Workspaces that back Research Threads, and each workspace owns its Workspace Runtime, file Artifacts, Agent Teams, workflow state, Gates, Run records, and generated View Manifests.

## Status

accepted

## Considered Options

- Manifested workspace engine.
- DeepScientist-compatible quest layer.
- Declarative research graph platform.

## Consequences

- Isomer can learn from DeepScientist without inheriting a pipeline-first quest model.
- The Agent Instance assigned to the coordinator Agent Role becomes the coordination boundary between user intent, team activity, durable state, and GUI-facing View Manifests.
- Team execution can create per-agent Agent Workspaces for concrete Agent Instances inside an Isomer Workspace. Their boundaries are advisory collaboration contracts, not filesystem-grade access control.
- Houmao can implement an Execution Adapter, but Isomer core state should remain provider-neutral.
- The first implementation should prioritize manifest validation, workspace discovery, team/workflow schemas, state migration, and view-manifest contracts before broad automation.
