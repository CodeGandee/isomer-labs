## 1. Installer Behavior

- [x] 1.1 Remove `.isomer-system-skill.json` marker constants, marker writing, marker reading, and marker-dependent ownership checks from `src/isomer_labs/skills/installer.py`.
- [x] 1.2 Add target-root manifest load/write helpers for `<skill-root>/isomer-labs-skill-manifest.json` with schema version, target, skill root, Isomer CLI/package version, update timestamp, and tracked skill records.
- [x] 1.3 Change install behavior so an existing selected `<skill-root>/<skill-name>` path is preserved and reported unless `force=True`.
- [x] 1.4 Add force replacement behavior that removes exactly the selected destination path before projecting the packaged skill.
- [x] 1.5 Keep symlink removal non-recursive so switching from symlink to copy unlinks the symlink without deleting the packaged source.
- [x] 1.6 Derive installed status and projection mode from destination path shape by packaged skill name, and include target-root manifest metadata or warnings when present.
- [x] 1.7 Change uninstall behavior to remove selected packaged skill paths by name, report removed or absent paths without marker checks, and update the target-root manifest.
- [x] 1.8 Implement upgrade behavior that reads the target-root manifest, removes manifest-tracked stale skill paths no longer in the selected packaged set, refreshes current selected skills, preserves recorded projection mode by default, and writes the updated manifest.

## 2. CLI Surface and Output

- [x] 2.1 Add `--force` to `isomer-cli system-skills install` and pass it into the installer.
- [x] 2.2 Add `isomer-cli system-skills upgrade` with target, selection, and projection-mode options, preserving recorded mode unless a mode override is supplied.
- [x] 2.3 Update install result models and JSON/text rendering to report preserved existing paths, forced replacements, and manifest updates.
- [x] 2.4 Update status result models and JSON/text rendering to remove unmanaged-collision fields, report invalid projection path shapes deterministically, and show target-root manifest metadata or warnings.
- [x] 2.5 Update uninstall result models and JSON/text rendering to remove preserved-unmanaged fields and report manifest updates.
- [x] 2.6 Add upgrade result models and JSON/text rendering for refreshed skills, stale removed skills, preserved existing paths if any, projection modes, and manifest updates.

## 3. Tests

- [x] 3.1 Update system-skill installer unit tests for markerless copy install, markerless symlink install, existing path preservation without force, and forced replacement.
- [x] 3.2 Add tests for force switching copy to symlink and symlink to copy.
- [x] 3.3 Add tests for target-root manifest creation, manifest updates on uninstall, status behavior with valid and invalid manifests, and absence of per-skill marker writes for symlinks.
- [x] 3.4 Add tests for upgrade refreshing selected skills, removing manifest-tracked stale names, preserving untracked paths, preserving recorded projection mode, and honoring explicit mode override.
- [x] 3.5 Update CLI tests for `--force` help, `upgrade` help, JSON output shape, status output, uninstall output, and upgrade output.
- [x] 3.6 Remove or revise tests that expect unmanaged collisions or per-skill marker files.

## 4. Documentation and Validation

- [x] 4.1 Update manual CLI reference and packaged-system-skills developer docs to describe name-based reserved install slots, the target-root manifest, `--force`, and `system-skills upgrade`.
- [x] 4.2 Run `openspec validate simplify-system-skill-install-ownership --strict`.
- [x] 4.3 Run targeted unit tests for the installer and CLI.
- [x] 4.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
