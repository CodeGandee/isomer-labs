# Manifested Workspace Engine

Isomer Labs will use a manifested workspace engine as its primary architecture. A project-level Project Manifest at `.isomer-labs/manifest.toml` discovers arbitrary project-local Isomer Workspaces for Research Tasks. Each Isomer Workspace owns its Workspace Runtime, file Artifacts, task-handler identity, selected Agent Team Instance reference when delegated, workflow state, Gates, Run records, and generated View Manifests.

## Status

accepted

## Considered Options

- Manifested workspace engine.
- DeepScientist-compatible quest layer.
- Declarative research graph platform.

## Consequences

- Isomer can learn from DeepScientist without inheriting a pipeline-first quest model.
- The Operator Agent becomes the human-facing coordination boundary between user intent, team activity, durable state, and GUI-facing View Manifests.
- Team execution can create per-agent Agent Workspaces for concrete Agent Instances inside an Isomer Workspace. Their boundaries are advisory collaboration contracts, not filesystem-grade access control.
- Houmao can implement an Execution Adapter, but Isomer core state should remain provider-neutral.
- The first implementation should prioritize manifest validation, workspace discovery, Agent Team Template and Agent Team Instance contracts, state migration, View Manifest contracts, GUI component registry contracts, AG-UI envelope contracts, and `isomer-cli` access to built-in artifacts before broad automation.
