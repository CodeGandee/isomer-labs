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
isomer-cli system-skills install --target codex --scope user
```

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`, and every target-resolving operation requires `--target`. When `--scope` is omitted, `system-skills install` defaults to Project scope at the exact process working directory and does not search upward for Git or Isomer metadata. Explicit `--scope project` is equivalent, while `--scope user` is the only route to user-wide installation. `system-skills status`, `upgrade`, and `uninstall` require an explicit `--scope user|project`.

| Target | Project Scope | User Scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

The `all` target expands to all four logical targets and groups normalized identical roots before mutation. For example, Codex and generic project bindings produce one operation at `<cwd>/.agents/skills`.

Packaged skill names are reserved install slots in each target skill root. Every packaged skill stores the Isomer release version, including release candidates, in `agents/openai.yaml` at `metadata.version`. Successful mutations update `<skill-root>/isomer-labs-skill-manifest.json` with the Isomer package version, sorted target-scope bindings, source paths, projection modes, tracked skill names, and per-skill version snapshots. Receipt versions 1 and 2 remain readable as legacy evidence; the next authorized mutation migrates the root to version 3 with the effective target-scope binding. If a selected same-name path already exists, `system-skills install` preserves it unless `--force` is supplied.

Compatibility policy belongs to `src/isomer_labs/assets/system_skills/manifest.toml`. Each group declares `minimum_compatible_skill_version`, and an optional per-skill `minimum_compatible_version` overrides that floor. Status compares versions with PEP 440: older skills at or above the floor remain compatible, skills below the floor are obsolete, and skills newer than the CLI require a CLI upgrade before automatic routing. Legacy unversioned receipts remain readable but unverified until upgrade.

Use `system-skills upgrade` after installing a newer Isomer CLI package when packaged skills may have been renamed or removed. Upgrade reads the target-root manifest, refreshes the currently selected packaged skills, and removes stale manifest-tracked skill paths that are no longer in the selected set:

```bash
isomer-cli system-skills upgrade --target codex --scope project
isomer-cli system-skills upgrade --target codex --scope project --extension deepsci
isomer-cli system-skills upgrade --target codex --scope project --extension kaoju
```

## Migrating Existing Commands

An install without `--scope` now selects Project scope, and explicit `--scope project` remains equivalent. Use `--scope user` for user-wide installation. Status, upgrade, and uninstall remain scope-explicit.

The former exact-root override is no longer public. Migrate `--target kimi-code --home .kimi-code/skills` to `--target kimi-code` or `--target kimi-code --scope project`, and migrate `--target kimi-code --home ~/.kimi-code/skills` to `--target kimi-code --scope user`. Arbitrary plugin, extra, and custom roots do not map to a scope; use the host's native installation mechanism for those destinations. Explicit-root inspection remains available through `internals inspect-system-skill-root`.

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

Select `deepsci` for hypothesis-driven research that develops or evaluates a new route. Select `kaoju` for evidence-led literature and codebase surveys, including source examination, separately approved bounded source-code trials, genuine reproduction when the stronger contract is met, and controlled comparisons. Selecting one extension includes core skills and that family only; use the existing all-extensions selector or select both when an agent needs both families.

The CLI `ext` namespace owns native runtime and compatibility commands such as `ext research`, the DeepScientist compatibility adapter, and deterministic `ext kaoju paper` and `ext kaoju wiki` services. Packaged DeepSci and Kaoju agent-skill extensions are discovered under `system-skills extensions` and orchestrated through their installed entry skills. Kaoju research decisions start with `$isomer-kaoju-pipeline`; `ext kaoju paper template --kind content|latex` provides independent named content-template and LaTeX-template CRUD, concurrency, audit, migration, and working-copy exchange while the agent owns arbitrary tree preparation. Other `ext kaoju` commands validate canonical MyST, compose exact LaTeX stock, report drift, build PDFs, export, deploy, or launch already selected state.

Kaoju keeps its shared process, semantic, binding, and schema data under the extension implementation in `isomer_labs.kaoju`. Agents query that data through context-free `ext kaoju process show`, `ext kaoju bindings list`, and `ext kaoju bindings describe KAOJU:WHAT` commands. `isomer-kaoju-shared` retains common procedure guidance, and each producer's `artifact-bindings.md` is a concise non-authoritative bundle-local projection. Installation copies only manifest-listed skill directories; no skill depends on a sibling family-root contract directory. DeepSci and Kaoju durable artifact identities use exact uppercase `EXTENSION-NAME:WHAT` values.

Kaoju's optional extension contains fourteen skills. `isomer-kaoju-pipeline` routes ten user intents, while `isomer-kaoju-trial` owns bounded environment and code-trial work, `isomer-kaoju-reproduce` owns only genuine reproduction, and `isomer-kaoju-export` owns package-local wiki output. Skills query Workspace Runtime rather than scan directories for durable records. Repository work is deliberately different from Isomer-owned executable operations: the user or agent runs fit-for-purpose Git, provider, copy, or extraction commands outside Isomer, verifies source identity and the immutable result, calls `project repos register`, then records sanitized evidence with `project artifacts`. Isomer-owned package mutation, smoke, trial, document-build, and viewer operations may still cross registered Execution Adapter Command Requests. Houmao may implement launch, mailbox, gateway, inspection, or a Service Dispatch Form, but it remains an adapter detail and must not enter Kaoju schema or CLI terms.

`npx skills add` remains useful when testing a single source-checkout skill directory directly, but it is no longer the public recommended path for released Isomer packages. Repository-root discovery can still find repository-local OpenSpec development skills, so do not document repository-root `npx skills add CodeGandee/isomer-labs --skill isomer-op-entrypoint` as a packaged Isomer install path.

Keep each skill in the supported skill format. Workflow-oriented skills should present their workflow as ordered steps that an agent follows from start to finish, not as detached callback reminders.

When adding a new skill, update the README, the tutorial page for skill installation, and any CLI or packaging tests that assert packaged asset paths.
