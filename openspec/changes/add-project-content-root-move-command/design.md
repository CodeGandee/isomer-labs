## Context

Project initialization can create a generated content root at `isomer-content/` or at a user-selected `--content-dir`. The Project Manifest records `[paths].isomer_content_root`, `[paths].topic_workspace_base_dir`, and explicit `[[topic_workspaces]].path` entries. Runtime commands can then create `state.sqlite`, path plans, adapter manifests, Pixi environments, and other files under a Topic Workspace.

Today, changing the generated content root after initialization is manual. The user must move directories and edit `.isomer-labs/manifest.toml`, and it is easy to accidentally rewrite or delete files that Isomer does not own. The relocation feature needs a tight ownership boundary: update Isomer-managed names and manifests, move Isomer-managed content containers, and warn when internal runtimes may still contain old paths.

## Goals / Non-Goals

**Goals:**

- Provide a dry-run-first command for changing the configured generated content root of an existing Project.
- Move only Isomer-managed content entries: content-root policy files and registered Topic Workspace directories that live inside the old content root.
- Rewrite Project Manifest path defaults and registered Topic Workspace paths that point inside the old content root.
- Preserve unknown files and directories under the old content root, report them as unmanaged leftovers, and avoid implicit whole-root moves.
- Warn users that Pixi environments, installed package metadata, runtime DB records, adapter runtime material, logs, and stored path plans may still reference old paths and may need reinstall or reinitialization.

**Non-Goals:**

- Do not rewrite `state.sqlite`, path plans, adapter runtime records, logs, package metadata, virtual environments, installed libraries, lockfiles, or generated code internals.
- Do not provide arbitrary path migration for user-managed directories outside the generated content root.
- Do not merge conflicting destination content in the first version.
- Do not replace Project cleanup. Cleanup remains the removal workflow; relocation changes configured paths and moves managed content entries.

## Decisions

### Use a nested Project command

The command surface will be `isomer-cli project content-root move --to <content-dir> --dry-run` and `isomer-cli project content-root move --to <content-dir> --yes`. This keeps the command under the existing Project namespace and makes the target noun explicit.

Alternative considered: `isomer-cli project paths move-content-root`. That shape fits path tooling but reads like generic path migration. The feature is specifically about the generated content root, so a `content-root` subgroup is clearer.

### Require a valid Project Manifest

Relocation will require a valid `.isomer-labs/manifest.toml`. The manifest is the authority for current content root, Topic Workspace registrations, and paths to rewrite.

Alternative considered: allow missing or malformed manifest recovery. That would blur relocation with cleanup or repair. The safe recovery path remains explicit cleanup and reinitialization.

### Move managed entries, not the whole root

The planner will identify managed entries under the old content root:

- generated `README.md`
- generated `.gitignore`
- registered Topic Workspace directories whose resolved paths are inside the old content root

The executor will move those entries to the new content root and preserve their relative paths. Unknown entries stay in the old root and appear in the plan as unmanaged leftovers.

Alternative considered: rename the entire old content root to the new path. That is simple but would move unknown user files and any unrelated local material, violating the ownership boundary.

### Rewrite manifest paths by old-root containment

The manifest update will set `[paths].isomer_content_root` to the requested new content root and set `[paths].topic_workspace_base_dir` to `<new-content-root>/topic-ws` when the old value was inside or derived from the old content root. Each registered Topic Workspace path that resolves inside the old content root will be rewritten to the same relative path under the new content root. Workspace paths outside the old content root remain unchanged and are reported as skipped manifest updates.

Alternative considered: rewrite every Topic Workspace path to the new default base. That would unexpectedly move explicitly custom workspace locations.

### Warn, but do not repair runtimes

The command will always warn that moving content can break internal runtimes. When the planner sees `state.sqlite`, `.pixi/`, `pixi.toml`, `pyproject.toml`, adapter runtime material, or other known runtime markers inside moved Topic Workspaces, it will include concrete warnings. The executor will not modify runtime DBs, path plans, Pixi environments, installed package metadata, or adapter runtime records.

Alternative considered: rewrite stored path plans and common environment files. That cannot cover the variety of installed libraries and generated runtime state reliably, and a partial repair would look safer than it is.

### Plan before mutation

Dry-run output and confirmed execution will use the same relocation plan. Without `--yes`, the command remains non-mutating. With `--yes`, execution validates the destination, creates needed destination parents, moves planned managed entries, writes the manifest atomically, and removes old directories only when they become empty.

Alternative considered: write the manifest first. That makes failures harder to recover because the manifest may point at content that has not moved.

## Risks / Trade-offs

- Runtime material may break after relocation -> The command prints explicit warnings and leaves reinstall or runtime reinitialization to the user.
- Moving managed Topic Workspace directories can still contain unknown nested files -> Registered Topic Workspaces are Isomer-managed containers; the command moves the container but does not rewrite or inspect every internal runtime file.
- Partial filesystem failure can leave some managed entries moved before the manifest rewrite -> Execution should attempt rollback for moved entries before returning an error, and diagnostics should report any remaining partial state.
- Destination conflicts can block legitimate moves -> The first version should refuse conflicting paths instead of merging; users can clean or choose a fresh destination before rerunning.
- Manifest formatting may change if a TOML writer is used -> Keep output deterministic and preserve semantic content; exact formatting preservation is secondary to a valid manifest.

## Migration Plan

This is an additive CLI feature. Existing Projects keep their current content root until a user explicitly runs the relocation command. Rollback is manual: run another relocation from the new content root back to the old root after resolving any warnings or conflicts. Runtime environments that break after the move should be reinstalled or reinitialized in their Topic Workspace.

## Open Questions

- Should the command expose a recovery-only `--manifest-only` mode later for advanced users who already moved content by hand? This is intentionally outside the first version.
- Should detection of runtime markers remain warning-only forever, or should a future runtime command offer explicit reinitialization after relocation?
