## Why

Isomer system skills are packaged with the Python distribution, but users still need to install them into each coding-agent surface by remembering tool-specific directories or external `npx skills add` commands. A first-party `isomer-cli system-skills` surface makes released packages self-contained for Claude Code, Codex, Kimi Code, and generic Open Agent Skills-compatible setups.

## What Changes

- Add a top-level `isomer-cli system-skills` command group with `list`, `status`, `install`, and `uninstall` subcommands.
- Support target tools `claude-code`, `codex`, `kimi-code`, `generic`, and `all`.
- Project packaged Isomer skills as flat skill directories named by skill id, while preserving source metadata for ownership-safe status and uninstall.
- Select skills by core group, extension id, all extensions, or explicit skill name.
- Default install to the core group unless selectors are provided.
- Support copy and symlink projection modes, with copy as the default.
- Document the installer in README and public docs so users can install the released CLI through `uv` and install packaged skills through `isomer-cli`.

## Capabilities

### New Capabilities
- `system-skill-installer-cli`: User-facing CLI commands for installing packaged Isomer system skills into supported coding-agent skill directories.

### Modified Capabilities
- None.

## Impact

- Affected CLI modules: `src/isomer_labs/cli/app.py`, `src/isomer_labs/cli/commands/`, and likely new or existing handlers.
- Affected skill asset code: `src/isomer_labs/skills/`.
- Affected docs: `README.md`, `docs/tutorial/quickstart.md`, `docs/developer/packaged-system-skills.md`, and `docs/manual/cli-reference.md`.
- Affected tests: unit coverage for target resolution, projection ownership, CLI help, install, status, and uninstall.
