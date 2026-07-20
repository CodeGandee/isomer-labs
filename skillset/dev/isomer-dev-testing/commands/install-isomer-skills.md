# Install Isomer Skills

## Overview

Sync Isomer skills into the local AI coding tool skill roots under the current checkout. This is a development-time projection: packaged system skills are refreshed through the Isomer CLI, existing development skills from `skillset/dev/` are preserved and refreshed, explicitly requested development skills are added, and development skills are removed only when the user explicitly requests removal.

## Workflow

1. **Resolve the checkout and CLI**.
   - Use the user-supplied path or find the Isomer Labs repository root from the current directory.
   - Confirm `pyproject.toml` declares project name `isomer-labs` and that `isomer-cli` is available through the Pixi environment (`pixi run isomer-cli --version`).
2. **Select targets**.
   - Default to `--target all` so every known tool root (`.agents/`, `.claude/`, `.codex/`, `.kimi-code/`) is reconciled.
   - If the user names specific tools or directories, map them to CLI targets. See **Target Mapping**.
3. **Select projection mode**.
   - Default to `--mode symlink` so tool skill roots stay in sync with the source skills and do not go stale.
   - Use `--mode copy` only when the user explicitly asks for copy-mode projection.
4. **Determine packaged extension coverage**.
   - Default to core only (no extension flag).
   - If the user names one or more extensions (`deepsci`, `kaoju`), pass `--extension <id>` for each.
   - If the user explicitly says `all`, pass `--all-extensions`.
5. **Determine development skills**.
   - Enumerate existing top-level entries in every selected tool skill root whose names match immediate children of `skillset/dev/` that contain `SKILL.md`. Treat these as the existing development-skill set even when the current request does not name them.
   - If the user names specific `skillset/dev/` skills to add or refresh (for example, `isomer-dev-testing`), resolve each source folder at `skillset/dev/<skill-name>/` and require `SKILL.md`.
   - If the user says `all dev skills`, enumerate every immediate child of `skillset/dev/` that contains a `SKILL.md` and add it to the requested development-skill set.
   - Build the desired development-skill set from the existing set plus explicitly requested additions. Subtract a skill only when the user explicitly asks to remove or uninstall that skill, or explicitly asks to remove all development skills.
6. **Capture preflight state**.
   - For each selected target, run `pixi run isomer-cli --print-json system-skills status --target <target> --scope project <extension-args>` and list the tool skill root (`ls -la <tool-dir>/skills/`).
   - Record packaged skill names, existing development-skill entries, their link targets or directory types, and any diagnostics.
7. **Refresh packaged system skills**.
   - Run `pixi run isomer-cli system-skills upgrade --target <target> --scope project <mode-arg> <extension-args>` for each selected target.
   - If `upgrade` reports that no manifest exists yet, first run `pixi run isomer-cli system-skills install --target <target> --scope project <mode-arg> --force <extension-args>`.
8. **Preserve, install, or update development skills**.
   - For each selected target, preserve every existing development skill unless the user explicitly requested its removal.
   - For each preserved or explicitly requested development skill backed by a symlink, ensure the link points to the absolute `<checkout>/skillset/dev/<skill-name>/` source path. Repair broken, relative, or outdated links when the source exists.
   - Add each explicitly requested development skill that is absent by creating an absolute symlink to its source folder.
   - If an existing development-skill entry is a real directory, preserve it and ask before replacing it with a symlink or copy.
9. **Apply explicit development-skill removals**.
   - Remove only the development skills that the user explicitly asked to remove or uninstall.
   - Do not treat an existing development skill as stale merely because the current request omits its name.
   - Leave all non-Isomer entries untouched. Let the packaged system-skill CLI and its manifest manage obsolete packaged projections.
10. **Verify and report**.
   - Run `pixi run isomer-cli --print-json system-skills status --target <target> --scope project <extension-args>` again.
   - List each tool skill root and confirm that every remaining `isomer-*` entry is a symlink.
   - Report which skills were preserved, added, refreshed, or explicitly removed per target.

If the request does not map cleanly to these steps, use the native planning tool to build a bounded plan from the selected targets, projection mode, extension choices, and dev skill names, then execute the plan.

## Target Mapping

| User reference | CLI `--target` | Tool skill root |
| --- | --- | --- |
| `.agents/`, `generic` | `generic` | `<checkout>/.agents/skills/` |
| `.claude/`, `claude-code` | `claude-code` | `<checkout>/.claude/skills/` |
| `.codex/`, `codex` | `codex` | `<checkout>/.codex/skills/` |
| `.kimi-code/`, `kimi-code` | `kimi-code` | `<checkout>/.kimi-code/skills/` |
| `all` | `all` | all of the above |

## Projection Mode

Default to `--mode symlink` for both packaged system skills and development skills. Symlink projection keeps tool skill roots in sync with the source skills and avoids stale copies. Use `--mode copy` only when the user explicitly requests it.

## Scope Selection

Default to `--scope project` so installations are anchored to the resolved checkout and do not affect user-wide tool configuration. Use `--scope user` only after explicit user request.

## Packaged Extension Coverage

Default to core only. Add extension coverage only when the user explicitly names one or more extensions (`deepsci`, `kaoju`) or explicitly says `all`. For named extensions, pass `--extension <id>` for each. For `all`, pass `--all-extensions`. Never install extension packs that the user did not request.

## Development Skill Coverage

Development skills under `skillset/dev/` are direct projections managed outside the packaged system-skill manifest. Preserve development skills already present in selected tool skill roots and refresh their symlinks when their checkout sources exist. Add absent development skills only when the user names one or more folders or says `all dev skills`. Omission from the current request is not removal intent; remove a development skill only when the user explicitly asks to remove or uninstall it.

## Failure Handling

- If a target tool directory does not exist and the CLI does not create it, create the parent directory manually and retry.
- If `upgrade` fails because the target has no prior manifest, fall back to `install --force`.
- If a requested dev skill source folder does not exist or lacks `SKILL.md`, skip it and report the omission.
- If an existing development-skill entry has no matching source folder, preserve it and report that it could not be refreshed.
- If a status check shows non-symlink `isomer-*` projections after the sync, report them as verification failures and ask the user before replacing real directories.

## Output Contract

Return a concise natural-language summary. State the resolved checkout, selected targets, scope, packaged extensions covered, and development-skill intent. List preserved, added, refreshed, and explicitly removed skills per target. Note any verification failures, unresolved development skills, skipped development skills, or skipped targets.

## Common Mistakes

- Defaulting to `--all-extensions` and installing deepsci or kaoju packs the user never requested. Only include extensions when named or when the user explicitly says `all`.
- Treating an omitted development skill as stale and removing it without explicit user intent.
- Preserving an existing development-skill symlink without refreshing an outdated or broken target when the matching checkout source exists.
- Confusing `install` with `upgrade`. Use `upgrade` for refresh-and-remove-obsolete packaged skills; use `install --force` only when the target has no manifest or the user explicitly requests a force reinstall.
- Defaulting to `--mode copy` and creating stale projections. Prefer `--mode symlink` unless the user explicitly asks for copies.
- Using `--scope user` without explicit user intent.

## Guardrails

- DO NOT remove non-Isomer skills or non-manifest-tracked directories from tool skill roots.
- DO preserve existing development skills unless the user explicitly requests their removal.
- DO refresh existing development-skill symlinks to their matching current-checkout sources when available.
- DO NOT replace a real skill directory with a symlink or copy without user confirmation.
- DO NOT install packaged skills from outside the resolved Isomer Labs checkout.
- DO NOT commit the generated manifest or symlinked tool skill roots as part of this procedure.
