# Packaged System Skills

System skills live under `src/isomer_labs/assets/system_skills/` and are packaged with the Python distribution. They teach agents how to operate Isomer projects, create research intent, manage topic workspaces, use DeepSci workflows, and route tasks through the operator entrypoint.

Discover optional packaged agent-skill extensions before installation. The focused inspection output includes the manifest-owned description, entry skill, public commands, packaged skills, and install and status command shapes:

```bash
isomer-cli system-skills extensions list
isomer-cli system-skills extensions show deepsci
isomer-cli system-skills extensions show kaoju
```

Released-package installation should use `isomer-cli system-skills install`, which reads packaged resources from the installed Python package and projects flat skill directories into supported agent-tool skill roots:

```bash
isomer-cli system-skills install --target codex
isomer-cli system-skills install --target codex --extension deepsci
isomer-cli system-skills install --target codex --extension kaoju
```

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`. Target defaults are `.claude/skills` for Claude Code, `$CODEX_HOME/skills` or `~/.codex/skills` for Codex, `.kimi-code/skills` for Kimi Code, and `.agents/skills` for the generic Open Agent Skills-compatible projection.

Packaged skill names are reserved install slots in each target skill root. Every packaged skill stores the Isomer release version, including release candidates, in `agents/openai.yaml` at `metadata.version`. Successful mutations update `<skill-root>/isomer-labs-skill-manifest.json` with the Isomer package version, target, source paths, projection modes, tracked skill names, and per-skill version snapshots. If a selected same-name path already exists, `system-skills install` preserves it unless `--force` is supplied.

Compatibility policy belongs to `src/isomer_labs/assets/system_skills/manifest.toml`. Each group declares `minimum_compatible_skill_version`, and an optional per-skill `minimum_compatible_version` overrides that floor. Status compares versions with PEP 440: older skills at or above the floor remain compatible, skills below the floor are obsolete, and skills newer than the CLI require a CLI upgrade before automatic routing. Legacy unversioned receipts remain readable but unverified until upgrade.

Use `system-skills upgrade` after installing a newer Isomer CLI package when packaged skills may have been renamed or removed. Upgrade reads the target-root manifest, refreshes the currently selected packaged skills, and removes stale manifest-tracked skill paths that are no longer in the selected set:

```bash
isomer-cli system-skills upgrade --target codex
isomer-cli system-skills upgrade --target codex --extension deepsci
isomer-cli system-skills upgrade --target codex --extension kaoju
```

The internal inspection namespace lets version-aligned system skills inspect one agent-supplied root or classify a host-supplied live inventory without knowing receipt filenames, schemas, or extension membership:

```bash
isomer-cli --print-json internals inspect-system-skill-root --skill-root /explicit/agent/skill-root --category extensions
isomer-cli --print-json internals inspect-system-skill-root --skill-root /explicit/agent/skill-root --extension kaoju
isomer-cli --print-json internals classify-system-skill-inventory --skill-name isomer-kaoju-pipeline --skill-name isomer-kaoju-shared
```

Both commands are read-only, return `mutated: false`, and use `isomer-internal-system-skill-inspection.v1`. Root inspection reads only the supplied root. It reports current or legacy receipt state, real-directory and symlink projections, broken links, unmanaged same-name directories, complete or partial family coverage, and version compatibility. Inventory classification maps only names supplied by the current host; optional paths remain descriptive input and are not scanned.

Within an initialized Project, direct detection accepts only explicit skill roots. With no root, it reports catalog and declaration state without filesystem discovery:

```bash
isomer-cli --print-json project system-extensions detect
isomer-cli --print-json project system-extensions detect --skill-root /explicit/agent/skill-root
```

Direct `project init`, low-level `system-skills install`, and internal inspection do not register extensions. The core `isomer-op-system-skill-mgr` skill adds operator-aware automation because the working agent knows its own project-scope roots and live inventory. It trusts Project declarations first, then complete compatible Isomer receipts in host-supplied roots, then complete live-inventory families. During operator-controlled Project initialization, explicit reconciliation, extension installation, or a concrete extension-use request, it remembers complete extensions additively unless the user opts out. It never forgets a declaration because another agent exposes a different inventory.

Core operator skills include `isomer-op-entrypoint` for informed routing, `isomer-op-system-skill-mgr` for extension management, and `isomer-op-welcome` for first-time project orientation. Optional extension skills include the DeepSci family under `research-paradigm/deepsci/` and the Kaoju survey family under `research-paradigm/kaoju/`.

Project declarations are authoritative claimed state, not proof that every current agent host can load the extension. A declared-but-unavailable route is stale user-controlled state and receives repair advice without automatic removal. Receipt and projection compatibility remains advisory beneath a declaration. Newly installed skills may require a new turn, thread, or host-native reload; operator workflows report `host_refresh_required` instead of claiming current-session activation.

Select `deepsci` for hypothesis-driven research that develops or evaluates a new route. Select `kaoju` for evidence-led literature and codebase surveys, including source examination, first-hand paper-method trials, and controlled comparisons. Selecting one extension includes core skills and that family only; use the existing all-extensions selector or select both when an agent needs both families.

The CLI `ext` namespace owns native runtime and compatibility commands such as `ext research` and the DeepScientist compatibility adapter. Packaged DeepSci and Kaoju agent-skill extensions are discovered under `system-skills extensions` and invoked through their installed entry skills. Kaoju therefore starts with `$isomer-kaoju-pipeline`; there is no `isomer-cli ext kaoju` command group.

Kaoju packages its storage-neutral semantic registry in `isomer-kaoju-shared/references/artifact-semantics.md` and concrete producer contracts in each producer's `artifact-bindings.md`. Installation must preserve both. The family-neutral research format schema, template, and Kaoju profile catalog ship as Python package assets independently of the skill projection. DeepSci placeholder binding pages and profile refs remain unchanged.

`npx skills add` remains useful when testing a single source-checkout skill directory directly, but it is no longer the public recommended path for released Isomer packages. Repository-root discovery can still find repository-local OpenSpec development skills, so do not document repository-root `npx skills add CodeGandee/isomer-labs --skill isomer-op-entrypoint` as a packaged Isomer install path.

Keep each skill in the supported skill format. Workflow-oriented skills should present their workflow as ordered steps that an agent follows from start to finish, not as detached callback reminders.

When adding a new skill, update the README, the tutorial page for skill installation, and any CLI or packaging tests that assert packaged asset paths.
