## 1. Relocation Planning

- [x] 1.1 Add a Project content-root relocation module with plan/result data structures for old root, new root, managed moves, manifest updates, skipped entries, unmanaged leftovers, diagnostics, warnings, and mutation flags.
- [x] 1.2 Implement Project Manifest loading for relocation using existing Project discovery and validation authority, refusing missing or malformed manifests.
- [x] 1.3 Implement destination path validation for project scope, Project root collision, `.isomer-labs/` collision, `.houmao/` collision, symlink roots, and destination conflicts.
- [x] 1.4 Implement managed-entry planning for generated `README.md`, generated `.gitignore`, and registered Topic Workspace directories inside the old content root.
- [x] 1.5 Implement unmanaged-leftover detection for old-root entries that relocation will not move.
- [x] 1.6 Implement runtime warning detection for moved workspaces containing markers such as `state.sqlite`, `.pixi/`, Pixi files, adapter runtime material, logs, or stored runtime paths.

## 2. Manifest Rewrite and Execution

- [x] 2.1 Implement manifest update generation for `[paths].isomer_content_root`, `[paths].topic_workspace_base_dir`, and moved `[[topic_workspaces]].path` entries while preserving external registered workspace paths.
- [x] 2.2 Implement confirmed execution that creates destination parents, applies planned managed moves, writes the updated manifest atomically, and removes old directories only when they become empty.
- [x] 2.3 Add failure handling that reports partial state and attempts rollback for managed moves completed before a manifest-write failure.
- [x] 2.4 Ensure execution never opens or rewrites `state.sqlite`, stored path plans, Pixi environments, installed package metadata, adapter runtime records, logs, or generated runtime internals.

## 3. CLI Surface

- [x] 3.1 Add the nested `isomer-cli project content-root move --to <content-dir> --dry-run` and `isomer-cli project content-root move --to <content-dir> --yes` command surface.
- [x] 3.2 Wire relocation output into the standard text renderer and versioned `--print-json` wrapper.
- [x] 3.3 Update Project help so `project content-root` and `project content-root move` appear with the expected controls.
- [x] 3.4 Ensure missing `--to`, invalid destinations, missing confirmation, and discovery failures produce deterministic diagnostics.

## 4. Project Manager Skill

- [x] 4.1 Add `skillset/operator/isomer-admin-project-mgr/references/move-content.md` with dry-run-first relocation guidance, confirmation rules, unmanaged-leftover behavior, and runtime breakage warnings.
- [x] 4.2 Update project-manager skill help and CLI boundary references to include `move-content` and the canonical `isomer-cli project content-root move` command shapes.
- [x] 4.3 Ensure project-manager guidance does not tell operators to hand-edit `.isomer-labs/manifest.toml` for supported relocation workflows.

## 5. Tests and Validation

- [x] 5.1 Add unit tests for dry-run planning, non-mutating behavior without `--yes`, valid-manifest requirement, and deterministic plan payloads.
- [x] 5.2 Add unit tests for path safety refusals, symlink refusal, destination conflict refusal, and external registered workspace preservation.
- [x] 5.3 Add unit tests for confirmed managed moves, manifest rewrites, unmanaged-leftover preservation, and empty old-directory cleanup.
- [x] 5.4 Add unit tests proving runtime DBs, path plans, Pixi environments, adapter runtime material, and logs are not rewritten by relocation.
- [x] 5.5 Add CLI tests for help text, JSON output, Project discovery from child directories, `--root`, `--manifest`, missing `--to`, dry-run, and confirmed execution.
- [x] 5.6 Add skill tests or file assertions for the new project-manager `move-content` subcommand and updated help.
- [x] 5.7 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
