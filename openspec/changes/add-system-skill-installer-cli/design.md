## Context

Official Isomer system skills already ship as package resources under `src/isomer_labs/assets/system_skills/` and are described by `manifest.toml`. Existing helpers can discover groups and materialize manifest-relative trees, but users still need external commands or manual copies to expose those skills to Claude Code, Codex, Kimi Code, or generic Open Agent Skills-compatible tooling.

Houmao has a similar `system-skills` CLI with list, status, install, and uninstall commands. Isomer should reuse that conceptual split, but keep the implementation tied to Isomer's packaged manifest and simpler installation needs.

## Goals / Non-Goals

**Goals:**
- Add a top-level `isomer-cli system-skills` command group.
- Install packaged Isomer skills into tool-specific skill roots as flat `<skill-name>/SKILL.md` directories.
- Support `claude-code`, `codex`, `kimi-code`, `generic`, and `all` targets.
- Preserve ownership metadata so status and uninstall can distinguish Isomer-owned projections from user-authored collisions.
- Document the installer as the recommended released-package path.

**Non-Goals:**
- Do not edit Claude, Codex, or Kimi settings files.
- Do not replace `npx skills add` as a valid external path for users who prefer it.
- Do not change the existing `materialize_system_skills()` contract that preserves manifest-relative package paths.
- Do not implement managed-launch policy or per-agent automatic sync in this change.

## Decisions

### Add a New Projection Module

Create a new module under `src/isomer_labs/skills/` that owns tool target resolution, flat projection, ownership markers, status discovery, install, and uninstall. Keep `system_assets.py` focused on package-resource discovery and manifest-relative materialization.

Alternative considered: extend `materialize_system_skills()`. Rejected because its output intentionally preserves `operator/isomer-op-entrypoint`, while agent tools expect direct skill directories such as `isomer-op-entrypoint`.

### Use Flat Skill Directory Names

Each installed skill directory is named after the skill folder name, such as `isomer-op-entrypoint`, even when its packaged source path is `operator/isomer-op-entrypoint`. This matches the skill name users invoke and the scanner shape used by current agent tools.

Alternative considered: preserve group folders under the tool root. Rejected because it risks scanners missing nested skills and forces users to remember package categories.

### Target Defaults

Resolve targets as follows:

| Target | Default destination |
| --- | --- |
| `claude-code` | `.claude/skills` relative to the current directory |
| `codex` | `$CODEX_HOME/skills` when set, else `~/.codex/skills` |
| `kimi-code` | `.kimi-code/skills` relative to the current directory |
| `generic` | `.agents/skills` relative to the current directory |
| `all` | expands to all concrete targets |

`--home` overrides the resolved skill root for a single concrete target only. `--home` with `--target all` is rejected.

Alternative considered: map Kimi through `KIMI_CODE_HOME`. Rejected by user decision; the Isomer contract should simply use `.kimi-code/skills`.

### Install Defaults to Core Skills

When no selectors are provided, `install` installs the `core` packaged group. Users can add extension skills with `--extension deepsci`, all extensions with `--all-extensions`, groups with `--group`, or named skills with `--skill`.

Alternative considered: install every packaged skill by default. Rejected because DeepSci and future extensions are optional method families, while core is the minimal operator/service/misc surface.

### Copy by Default, Symlink on Request

Use copy mode by default so installed skills work from released wheels and remain stable if the package location changes. Support `--mode symlink` for editable development and local iteration.

Alternative considered: symlink by default. Rejected because released packages should not depend on mutable package-resource paths or editable checkouts.

### Ownership Marker

Write an Isomer-owned marker inside each projected skill directory, for example `.isomer-system-skill.json`, containing schema version, skill name, packaged source path, install target, projection mode, and package version if available. Status uses this marker to classify installed, unmanaged collision, missing, and stale projections. Uninstall removes only directories with a valid Isomer marker unless `--force` is added in a future change.

Alternative considered: delete any matching skill directory by name. Rejected because users can own skills with colliding names.

## Risks / Trade-offs

- Tool discovery rules can change over time → Keep target paths small and documented; expose `--home` for explicit overrides.
- Symlink mode may point into an unavailable package path after upgrades → Default to copy and show projection mode in status.
- User-authored collisions may confuse installation → Refuse to overwrite directories without Isomer ownership metadata unless an explicit `--replace` flag is provided.
- `all` target can partially succeed if one target has a collision → Preflight selection first, then report per-target diagnostics without hiding successful installations.

## Migration Plan

1. Add the new CLI and projection module without changing existing package assets.
2. Update docs to recommend `isomer-cli system-skills install` for released installations.
3. Bump the package patch version before release because `v0.1.0` already exists.
4. Release through the existing GitHub release workflow; PyPI publish uses trusted publishing and GitHub Pages builds through `mkdocs build --strict`.
