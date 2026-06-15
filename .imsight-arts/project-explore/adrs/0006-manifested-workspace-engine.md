# Manifested Workspace Engine

Isomer Labs will use a manifested workspace engine as its primary architecture. A project-level `.isomer-labs/manifest.toml` file discovers arbitrary project-local workspaces, and each workspace owns its SQLite control plane, file artifacts, team definitions, workflow state, decision gates, and generated view manifests.

## Status

accepted

## Considered Options

- Manifested workspace engine.
- DeepScientist-compatible quest layer.
- Declarative research graph platform.

## Consequences

- Isomer can learn from DeepScientist without inheriting a pipeline-first quest model.
- The operator agent becomes the coordination boundary between user intent, team activity, durable state, and GUI-facing view manifests.
- The first implementation should prioritize manifest validation, workspace discovery, team/workflow schemas, state migration, and view-manifest contracts before broad automation.
