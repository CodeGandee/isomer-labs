## Context

The packaged system-skill installer projects selected skills from `src/isomer_labs/assets/system_skills/` into tool-specific skill roots such as Codex and Claude Code. Current ownership detection depends on `.isomer-system-skill.json` inside each installed skill directory. That works for copied directories, but it is a poor fit for symlink projection because writing a marker below the symlink path writes into the symlink target, which can be the packaged source checkout.

The user intent is simpler: packaged system skills have reserved public names. A path named `isomer-op-entrypoint` under a resolved skill root is the install slot for that packaged skill, and the installer should not need a hidden file inside each skill to prove it. The target root still needs one coherent install manifest so future `isomer-cli` versions can know which skills an older version installed and can clean up renamed or deleted skill paths during an explicit upgrade.

## Goals / Non-Goals

**Goals:**

- Use packaged skill names as the ownership and install-slot boundary for `system-skills install`, `status`, `uninstall`, and `upgrade`.
- Remove per-skill marker-file creation and marker-file-dependent behavior.
- Maintain `isomer-labs-skill-manifest.json` at the installed skill root.
- Add `--force` to make destructive replacement explicit.
- Add an explicit `system-skills upgrade` path that uses the installed-root manifest to refresh current skills and remove stale manifest-tracked skill names.
- Support projection mode switching, including replacing an existing copied directory with a symlink and replacing an existing symlink with a copied directory.
- Keep operations scoped to selected packaged skill names under the resolved target skill root.

**Non-Goals:**

- Do not add a compatibility layer for old per-skill marker files.
- Do not preserve same-name custom user skills during `uninstall`; same-name paths are reserved by packaged Isomer skill names after this breaking change.
- Do not change packaged skill selection, target resolution, or extension inclusion rules.
- Do not change Toolbox callback registration or user callback semantics.

## Decisions

1. **Name-based ownership replaces per-skill marker files.**

   A selected packaged skill record already has a unique install name. The installer will treat `<skill-root>/<skill-name>` as the sole projection path for that skill. Status can report the skill as installed when that path exists, and uninstall can remove that path when the skill is selected.

   Alternative considered: move marker files to a sidecar directory outside symlinks. This avoids symlink write-through, but it keeps a second ownership database that can drift from the visible skill root.

2. **The target skill root gets one install manifest.**

   The installer will write `<skill-root>/isomer-labs-skill-manifest.json` after successful install, upgrade, or uninstall operations. The manifest should include a schema version, target name, skill root path, Isomer package/CLI version, update timestamp, projection mode requested for the operation, and one record per Isomer-installed skill with skill name, source path, and projection mode. The manifest is root-level state, not a per-skill ownership marker.

   Alternative considered: keep no install metadata at all. That is too weak for version upgrades because the current package cannot infer old names that were renamed or deleted after installation.

3. **Destructive install requires `--force`.**

   If the selected destination path already exists, normal install should report that the path already exists and leave it untouched. With `--force`, install removes the existing file, symlink, or directory at exactly that selected destination before projecting the packaged skill in the requested mode.

   Alternative considered: always overwrite same-name paths because names are reserved. Requiring `--force` is clearer for users and keeps accidental refreshes from deleting local edits.

4. **Projection mode is a requested end state.**

   `--mode copy` creates a real directory. `--mode symlink` creates a symlink to the packaged skill source when the package resource is filesystem-backed. With `--force`, the installer switches between these states by removing the existing selected path and recreating it.

   Alternative considered: only switch modes when the previous install has matching metadata. That depends on the marker model this change removes.

5. **Status should report path shape plus root manifest context.**

   Status output should derive `projection_mode` from the filesystem where possible: symlink means `symlink`, directory means `copy`, file or other path kind means an invalid projection. It should also report root manifest metadata when present so users can see which Isomer CLI/package version last updated the target skill root.

6. **Upgrade uses the manifest to remove stale installed skills.**

   `system-skills upgrade` will read `isomer-labs-skill-manifest.json`, resolve the current selected packaged skill set, remove previously manifest-tracked skill paths that are no longer in the selected set, and install or refresh the current selected set. It should only delete stale paths that appear in the root manifest, so unrelated files under the skill root remain untouched.

   Alternative considered: make `install --force` also remove stale manifest entries. Keeping stale deletion behind an explicit `upgrade` command makes the destructive version-migration intent clearer.

## Risks / Trade-offs

- Same-name custom skills become replaceable and removable by system-skill commands. Mitigation: this is an intentional breaking change; docs should state that packaged Isomer skill names are reserved install slots.
- The root manifest can drift if users manually edit the skill root. Mitigation: status should derive current path existence from the filesystem and treat manifest data as install history, while upgrade deletes only manifest-tracked stale paths.
- Symlink projection depends on packaged resources being filesystem-backed. Mitigation: keep the existing error when symlink mode cannot resolve a concrete packaged source path.
- Removing per-skill marker-file compatibility can leave old markers inside existing copied directories. Mitigation: after the change, marker files are ignored and disappear on the next forced copy refresh.
