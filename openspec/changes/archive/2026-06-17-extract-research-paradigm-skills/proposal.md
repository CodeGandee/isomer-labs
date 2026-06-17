## Why

The current DeepScientist-derived team design names stage roles, but the reusable research behavior still lives in DeepScientist skill bundles that include quest-specific APIs, paths, and runtime assumptions. Extracting those behaviors into generic project skills gives future research agents a portable research paradigm without depending on the DeepScientist workspace model.

## What Changes

- Add a reusable research-paradigm skillset under `skillset/research-paradigm/`.
- Convert DeepScientist stage and companion behavior into generic `isomer-labs-research-*` skill bundles.
- Separate research judgment from DeepScientist-specific concepts such as `quest`, `artifact.*`, `memory.*`, `bash_exec(...)`, DeepXiv, branch/worktree assumptions, and completion APIs.
- Define a shared vocabulary based on Isomer Labs concepts, including Research Thread, Research Task, Isomer Workspace, Workspace Runtime, Run, Artifact, Evidence Item, Decision Record, Gate, Operator Agent, Agent Role, Agent Instance, and Agent Workspace.
- Mark unsettled concrete paths, filenames, commands, runtime APIs, storage locations, and generated artifact layouts as `yet-to-be-determined` instead of guessing defaults.
- Map generic research agents to the extracted skills so `teams/deepsci-org` can move from DeepScientist-specific specialists to portable research roles.
- Preserve source provenance and license notices for copied or adapted references, templates, assets, and publication helpers.

## Capabilities

### New Capabilities

- `research-paradigm-skills`: Portable research-stage skills and agent role mappings derived from the DeepScientist skill analysis, with DeepScientist workspace specifics removed.

### Modified Capabilities

- None.

## Impact

- Adds skill bundles under `skillset/research-paradigm/`.
- May update `skillset/README.md` to document the research-paradigm subtree.
- May update `teams/deepsci-org/source/team-design.md` or companion team docs to reference generic research agents and installed skills instead of DeepScientist-specific skill sources.
- Uses existing project documentation under `context/explore/deepscientist-skill-analysis/`, `context/explore/deepscientist-system-explain.md`, and `teams/deepsci-org/source/team-design.md` as source material.
- Does not change Python package code, runtime APIs, or Pixi configuration.
