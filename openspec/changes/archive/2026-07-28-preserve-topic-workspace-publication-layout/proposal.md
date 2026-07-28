## Why

Topic Workspace publication currently preserves selected research content but can relocate retained files into a synthetic export layout or expose the Topic Main Development Repository at the publication root. This breaks the expected relationship between a Topic Workspace and its published repository: a reader should find every retained source path at the same relative path and should see the complete sanitized Topic Workspace on the remote `main` branch.

## What Changes

- Require every retained Source Topic Workspace path to keep its exact relative path in the Topic Publication Copy; sanitization may change bytes and policy may omit a path, but publication may not relocate it.
- Keep Topic Main, selected Topic Actor Workspace and Agent Workspace snapshots, and registered reference repositories at their resolved Topic Workspace-relative paths as exact-commit submodules.
- **BREAKING**: Make remote `main` the only canonical sanitized Topic Workspace superproject branch, remove the legacy `topic-workspace/main` and source-style publication branches, and expose Topic Main plus its selected worktree snapshots through replaceable same-remote `components/...` branches mounted at their original paths.
- Record that Topic Actor Workspace and Agent Workspace snapshots derive from the Topic Main Git anchor without publishing machine-local worktree control data.
- Confine publication-only manifests and indexes to a reserved `.isomer-publication/` overlay. Keep only the required root `README.md` and Git-required `.gitmodules` as root-level generated exceptions.
- Preserve or sanitize root environment declarations, ignore policy, attributes, Topic Workspace Manifest, readiness summary, intent, and durable research records in place.
- Make the generated README link the latest eligible paper at its path-preserved published Artifact location instead of requiring a relocated duplicate.
- Treat the publication remote as a replaceable current-state snapshot rather than a publication-history archive, and validate the complete snapshot without relying on ancestry.
- State that the publication is an inspectable evidence and artifact snapshot, not a Topic Workspace backup or an automatic restoration mechanism.
- Add an exclusive-snapshot Publication Binding mode whose one-time acknowledgement authorizes later approved syncs to replace or delete every Git ref and tag on the dedicated remote without branch-specific destructive prompts.
- Detect output-path relocation, generated-path collisions, unexpected remote ownership, and incomplete snapshot replacement as blockers.
- Define migration for existing remotes whose `main`, `topic-workspace/main`, component refs, or default branch contain the old flattened, component-root, synthetic, or historical layouts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `topic-workspace-git-publication`: Add structural path preservation, current-state-only canonical `main` topology, same-remote `components/...` snapshot branches, reserved publication metadata, path-preserved latest-paper linking, and whole-snapshot remote replacement requirements.

## Impact

- Updates the Topic Workspace Git publication specification, operator skill guidance, Publication Binding and plan models, projection validation, README and manifest rendering, synchronization branch topology, and Topic Publication Copy recovery logic.
- Changes publication branch expectations and the locations of generated publication metadata.
- Requires focused unit, integration, skill-contract, and migration tests that compare Source Topic Workspace paths with published paths.
- Existing Source Topic Workspaces, Workspace Runtime, Topic Main history, and local worktree topology remain unchanged. Publication remote history and the legacy superproject branch are intentionally not preserved, operational Topic Workspace restoration remains manual, and changing the bound remote or snapshot mode requires new explicit acknowledgement.
