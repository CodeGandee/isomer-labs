# Packaged System Skills

System skills live under `src/isomer_labs/assets/system_skills/` and are packaged with the Python distribution. They teach agents how to operate Isomer projects, create research intent, manage topic workspaces, use DeepSci workflows, and route tasks through the operator entrypoint.

Released-package installation should use `isomer-cli system-skills install`, which reads packaged resources from the installed Python package and projects flat skill directories into supported agent-tool skill roots:

```bash
isomer-cli system-skills install --target codex
isomer-cli system-skills install --target codex --extension deepsci
isomer-cli system-skills install --target codex --extension kaoju
```

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`. Target defaults are `.claude/skills` for Claude Code, `$CODEX_HOME/skills` or `~/.codex/skills` for Codex, `.kimi-code/skills` for Kimi Code, and `.agents/skills` for the generic Open Agent Skills-compatible projection.

Packaged skill names are reserved install slots in each target skill root. Installation no longer writes per-skill ownership markers; instead, successful mutations update `<skill-root>/isomer-labs-skill-manifest.json` with the Isomer package version, target, source paths, projection modes, and tracked skill names. If a selected same-name path already exists, `system-skills install` preserves it unless `--force` is supplied.

Use `system-skills upgrade` after installing a newer Isomer CLI package when packaged skills may have been renamed or removed. Upgrade reads the target-root manifest, refreshes the currently selected packaged skills, and removes stale manifest-tracked skill paths that are no longer in the selected set:

```bash
isomer-cli system-skills upgrade --target codex
isomer-cli system-skills upgrade --target codex --extension deepsci
isomer-cli system-skills upgrade --target codex --extension kaoju
```

Core operator skills include `isomer-op-entrypoint` for informed routing and `isomer-op-welcome` for first-time project orientation. Optional extension skills include the DeepSci family under `research-paradigm/deepsci/` and the Kaoju survey family under `research-paradigm/kaoju/`.

Select `deepsci` for hypothesis-driven research that develops or evaluates a new route. Select `kaoju` for evidence-led literature and codebase surveys, including source examination, first-hand paper-method trials, and controlled comparisons. Selecting one extension includes core skills and that family only; use the existing all-extensions selector or select both when an agent needs both families.

`npx skills add` remains useful when testing a single source-checkout skill directory directly, but it is no longer the public recommended path for released Isomer packages. Repository-root discovery can still find repository-local OpenSpec development skills, so do not document repository-root `npx skills add CodeGandee/isomer-labs --skill isomer-op-entrypoint` as a packaged Isomer install path.

Keep each skill in the supported skill format. Workflow-oriented skills should present their workflow as ordered steps that an agent follows from start to finish, not as detached callback reminders.

When adding a new skill, update the README, the tutorial page for skill installation, and any CLI or packaging tests that assert packaged asset paths.
