## Context

Fresh Project initialization now creates several Project-scoped surfaces: `.isomer-labs/` for Project config, `.houmao/` for the Project-level Houmao overlay, and a selected generated content root with Topic Workspace material. `isomer-cli project init` correctly refuses to overwrite an existing `.isomer-labs/manifest.toml`, but the user-facing recovery path is manual deletion. That is too blunt because some surfaces are generated policy files, some are discovery authority, some are runtime records, and some may contain user-authored topic material.

The cleanup command should be the inverse of Project bootstrap only where ownership is clear. It should make deletion explicit, previewable, and partial, while keeping the default posture conservative enough that an existing `isomer-content/` with user files is not accidentally removed.

## Goals / Non-Goals

**Goals:**

- Add a Project-scoped `isomer-cli project cleanup` command for removing selected Isomer-managed Project material.
- Support deterministic dry-run plans for every cleanup part and every destructive operation.
- Require explicit confirmation for actual filesystem deletion.
- Support partial cleanup by part so users can unblock `project init`, reset runtime state, remove a Houmao overlay, or remove selected Topic Workspace material without destroying unrelated content.
- Use Project Manifest data as the cleanup authority when a valid manifest exists.
- Support bounded cleanup when the manifest is missing or malformed, especially for `.isomer-labs/`, `.houmao/`, and explicit/default content-root policy files.
- Preserve `isomer-cli project init` overwrite refusal and keep force-overwrite out of init.

**Non-Goals:**

- Do not stop live Houmao agents, close mailboxes, revoke gateways, or clean external service state.
- Do not migrate or rewrite Project Manifests.
- Do not guarantee removal of arbitrary user-created files under a generated content root unless the user selects an explicit purge mode.
- Do not infer Research Topics by scanning unregistered directories as authoritative state.
- Do not delete paths outside the Project root or delete the Project root itself.

## Decisions

### Use one Project-scoped cleanup command with repeatable parts

The public command shape should be:

```bash
isomer-cli project cleanup --part <part> [--part <part> ...] [--topic <topic-id>] [--all-topics] [--content-dir <content-dir>] [--dry-run | --yes]
```

Supported parts should be:

| Part | Planned removal |
| --- | --- |
| `bootstrap` | Project config, Project-level Houmao overlay, known content-root policy files, and known init-created empty/default Topic Workspace directories |
| `project-config` | `.isomer-labs/` |
| `houmao-overlay` | `.houmao/` |
| `content-policy` | `<content-root>/README.md` and `<content-root>/.gitignore` |
| `topic-workspace` | selected Topic Workspace directories |
| `runtime` | selected Workspace Runtime files and runtime-owned directories under a Topic Workspace |
| `content-root` | the selected generated content root only when explicit purge mode is enabled |

Alternative considered: separate commands such as `cleanup config`, `cleanup runtime`, and `cleanup content`. A single command with repeatable parts keeps the deletion planner and JSON output uniform, and makes it easier to combine cleanup actions in one reviewed plan.

### Default to planning, require `--yes` for mutation

`--dry-run` should always produce a removal plan and mutate nothing. If neither `--dry-run` nor `--yes` is supplied, the command should behave as a dry run and report that no files were removed. Actual deletion requires `--yes`.

Alternative considered: require either `--dry-run` or `--yes` and fail otherwise. Defaulting to a dry run is friendlier for operators and still preserves a non-destructive default.

### Plan first, then delete

Cleanup must resolve every target and build the full removal plan before removing the first file. This matters because deleting `.isomer-labs/` first can destroy the Project Manifest data needed to locate custom content roots and Topic Workspaces.

Alternative considered: stream deletion as each target is discovered. That is simpler but produces partial-deletion failures that are harder to audit and recover from.

### Use the strongest available authority for paths

If a valid Project Manifest exists, cleanup should use its path defaults, Research Topic registrations, and Topic Workspace registrations. If the manifest exists but cannot be parsed, cleanup may still plan removal of `.isomer-labs/`, `.houmao/`, and a selected content root from `--content-dir` or the built-in default `isomer-content/`. If no manifest exists, cleanup should require an explicit `project --root <root>` selector or use the current directory as the root with a diagnostic that authority is limited.

Alternative considered: scan `isomer-content/topic-ws/` for topics when the manifest is missing. That would blur the existing rule that unregistered directories are not authoritative Research Topics, so it should be allowed only as filesystem removal by explicit path/content-root selection, not as topic discovery.

### Treat content-root purge as a stronger operation

The ordinary content cleanup behavior should remove known managed paths and then remove empty parent directories where safe. Deleting the whole selected content root should require `--part content-root --purge-content-root --yes`, and the plan should warn when the root contains files outside known managed paths.

Alternative considered: let `--part content-root --yes` remove the whole tree directly. That is risky because the previous initialization design allows an existing content root, so it may contain user-owned files that predate Isomer.

### Keep symlink and bounds behavior conservative

Every planned path must resolve inside the Project root and must not equal the Project root. For symlinks, cleanup should either remove the symlink entry itself when it is the exact planned target or refuse the target; it must not recursively follow a symlink into another tree.

Alternative considered: resolve symlinks and delete the destination when in-bounds. That makes the command harder to reason about and can surprise users who expected only Project-local entries to be removed.

### Keep Houmao cleanup filesystem-only

`houmao-overlay` cleanup removes the Project-level `.houmao/` overlay directory. It must not stop running Houmao agents or assume external Houmao runtime state is gone. If live cleanup is needed later, it should be a separate command with live-state inspection and confirmation.

Alternative considered: invoke Houmao stop/cleanup operations automatically. That would mix local filesystem cleanup with live managed-agent operations and break the bounded project cleanup contract.

## Risks / Trade-offs

- Unknown user files under the generated content root may be left behind → Preserve them by default, report them in the plan, and require explicit purge for whole-root deletion.
- Malformed manifests limit cleanup authority → Allow cleanup of obvious bootstrap surfaces and explicit content roots, but do not infer topics or custom workspace paths from broken config.
- Users may expect `bootstrap` to return a directory to a pristine pre-Isomer state → Document that `bootstrap` removes known Isomer-managed surfaces and preserves unknown files unless purge is requested.
- Deleting runtime material can make adapter manifests and records disappear together → Keep `runtime` cleanup scoped to the selected Topic Workspace and require dry-run/confirmation like all destructive parts.
- The command can delete a lot of files when multiple parts are selected → Emit a stable plan with part, path, kind, existence, action, and warnings before deletion.

## Migration Plan

Fresh behavior is additive. Existing Projects keep current initialization and validation behavior. Users who need to reinitialize can run `isomer-cli project cleanup --part bootstrap --dry-run`, review the plan, then run the same command with `--yes` before running `isomer-cli project init` again.

Rollback for the feature is to keep using manual deletion; no durable schema migration is required. If a cleanup run removes files unintentionally, recovery depends on VCS or filesystem backup, so dry-run and conservative purge rules are the main protection.

## Open Questions

- Resolved by the Project namespace refactor: cleanup should use the Project-scoped `isomer-cli project cleanup` command shape.
- Should `bootstrap` include `content-policy` by default when the content root contains unknown files? The safer behavior is to remove only policy files and empty managed directories, then report remaining files.
