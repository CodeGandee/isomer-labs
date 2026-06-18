## Why

The research-paradigm skills still mark many ordinary file, path, and workspace locations as TBD even though the manifested workspace design already says Agent Team Instance work belongs inside declared Topic Workspaces and per-agent Agent Workspaces. This change settles the default workspace path contract, keeps actual placement controlled by workspace planning, and lets Execution Adapters use environment variables as launch-time overrides without making skills invent paths.

## What Changes

- Define a workspace path resolution contract with deterministic precedence: recorded workspace plan, Execution Adapter environment overrides, Project Manifest defaults, then built-in defaults.
- Establish default project-local layout roots for Topic Workspaces, Workspace Runtime files, Run records, Artifact classes, View Manifests, logs, and Agent Workspaces.
- Define the supported `ISOMER_*` environment variables that adapters may export for the current Project, Topic Workspace, Run, Agent Workspace, and derived roots.
- Require resolved paths to be canonicalized, validated against Project boundaries by default, and recorded in Workspace Runtime or Provenance Records before downstream work depends on them.
- Update research-paradigm skill contracts so stage skills request semantic Artifact kinds and workspace scopes instead of using path TBD placeholders for ordinary resolved locations.

## Capabilities

### New Capabilities

- `workspace-path-resolution`: Default layout, override precedence, validation, and durable recording for Project, Topic Workspace, Workspace Runtime, Run, Artifact, View Manifest, log, and Agent Workspace paths.

### Modified Capabilities

- `research-paradigm-skills`: Research-stage skills consume the workspace path resolution contract and narrow path TBD usage to genuinely unsettled surfaces outside the resolved workspace layout.

## Impact

- Affected docs and design references: `.imsight-arts/project-explore` workspace-engine design material and any new design notes that capture accepted path-resolution rules.
- Affected skillset files: `skillset/research-paradigm/isomer-rsch-shared` and the local `isomer-research-contract.md` copies used by stage and companion skills.
- Affected validation: searches and checks for `[[tbd-surface:path-*]]`, hard-coded source runtime paths, and unresolved ordinary workspace paths.
- No new runtime dependency is required for this planning change; implementation should remain compatible with the existing Pixi project layout and future `isomer-cli` path validation.
