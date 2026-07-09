## Why

System-skill installation currently uses per-skill hidden marker files to decide whether an installed skill is Isomer-owned. That marker model is awkward for symlink installs because marker writes can pass through the symlink into the packaged source directory, and it does not give the target skill root a coherent record of which Isomer CLI version installed which skill set.

## What Changes

- **BREAKING**: Treat packaged system-skill install names as the ownership boundary. A path under the target skill root with the same name as a packaged Isomer system skill is considered the Isomer projection for that skill.
- Remove per-skill `.isomer-system-skill.json` marker creation, reading, and ownership decisions from system-skill install, status, and uninstall behavior.
- Add an installed-root manifest named `isomer-labs-skill-manifest.json` under each target skill root. The manifest records the Isomer CLI/package version, target, installed skill names, source paths, projection modes, and update time for the root.
- Add `--force` to `isomer-cli system-skills install` so users can explicitly replace an existing same-name path when they want destructive refresh behavior.
- Add `isomer-cli system-skills upgrade` so a later Isomer CLI version can refresh installed skills and remove manifest-tracked stale skills that were renamed or deleted from the selected packaged skill set.
- Make copy and symlink projection modes switch cleanly by removing the existing same-name path and recreating it in the requested mode.
- Preserve selection safety: install, status, and uninstall only operate on selected packaged skill names under the resolved target skill root.
- Update CLI output, tests, and documentation to describe name-based ownership, root manifest tracking, forced replacement behavior, and upgrade behavior.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `system-skill-installer-cli`: Change ownership detection from hidden per-skill marker files to packaged skill names plus a target-root install manifest, add forced replacement semantics, require copy/symlink mode switching to work without writing marker files into installed or packaged skill directories, and add root-manifest-backed skill upgrade behavior.

## Impact

- Affected CLI: `isomer-cli system-skills install`, `status`, `uninstall`, and new `upgrade`.
- Affected package code: `src/isomer_labs/skills/installer.py` and `src/isomer_labs/cli/commands/system_skills.py`.
- Affected tests: system-skill installer unit tests and CLI tests for install/status/uninstall JSON and text output.
- Affected docs: manual CLI reference and packaged-system-skills developer documentation.
