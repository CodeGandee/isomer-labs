# Packaged System Skills

Isomer distributes three public system-skill packs. Each pack is one top-level host installation unit with protected capabilities nested below `subskills/`.

| Pack | Public Skill | Contents |
| --- | --- | --- |
| Core | `isomer-op-entrypoint` | 20 protected operator, service, shared-support, and research-recording capabilities |
| DeepSci | `isomer-ext-deepsci-entrypoint` | 21 protected hypothesis-driven research capabilities |
| Kaoju | `isomer-ext-kaoju-entrypoint` | 13 protected evidence-led survey capabilities |

Ordinary users invoke only these public skills. The accepted prompt form is `$<entrypoint> use <subcommand> to <task>`. A concrete task-only invocation is also valid, and an empty invocation selects help.

```text
$isomer-op-entrypoint use project to validate this Project
$isomer-ext-deepsci-entrypoint use empirical-pass to test the selected hypothesis
$isomer-ext-kaoju-entrypoint use build-reading-list to assemble evidence for the survey
```

Protected means parent-routed and omitted from ordinary top-level host discovery. It does not mean encrypted, unreadable, or authorization-protected. Any agent that receives a complete public pack can read its nested files. Use selective private projection when an Agent Role should receive fewer capabilities.

## Installation

Discover the package catalog before installation:

```bash
isomer-cli system-skills list
isomer-cli system-skills extensions list
isomer-cli system-skills extensions show deepsci
isomer-cli system-skills extensions show kaoju
```

Install the core pack or core plus one extension pack:

```bash
isomer-cli system-skills install --target codex
isomer-cli system-skills install --target codex --extension deepsci
isomer-cli system-skills install --target codex --extension kaoju
isomer-cli system-skills install --target codex --all-extensions
isomer-cli system-skills install --target codex --scope user --extension deepsci
```

Extension selection includes the core pack. Copy and symlink modes always project a selected public pack as one complete top-level directory. They never place a protected member beside its parent.

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`. When `--scope` is omitted, installation defaults to Project scope at the exact process working directory. `--scope user` is the only user-wide installation route. Status, upgrade, and uninstall require an explicit `--scope user|project`.

| Target | Project Scope | User Scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

The `all` target expands to all concrete targets and deduplicates identical physical roots. The installer does not provide an arbitrary path override. Use a host-native mechanism for plugin, extra, or custom destinations.

`--skill <public-entrypoint>` selects its complete pack. During the migration window, a protected logical id or old pipeline alias is accepted as a deprecated selector and resolves to its complete owning pack. It does not install the named protected capability alone. `uninstall` refuses protected-member removal because a managed public pack is the ownership unit.

## Manifest and Identity Layers

`src/isomer_labs/assets/system_skills/manifest.toml` uses `isomer-skillset-manifest.v3`. It separates four identity layers:

1. Public skill identity names the host-discoverable installation unit.
2. Pack id names the catalog and receipt unit: `core`, `deepsci`, or `kaoju`.
3. Protected logical id remains stable for callbacks, Skill Binding Projection, provenance, compatibility selectors, and private projection.
4. Scoped member name and invocation designator describe parent routing without replacing the logical id.

The nested source path is package layout, not provider-neutral identity. Bindings and durable records store logical ids rather than pack filesystem paths.

## Protected Capability Map

The manifest is authoritative. This table documents all 54 current mappings.

| Pack | Protected Logical ID | Member | Invocation Designator |
| --- | --- | --- | --- |
| `core` | `isomer-op-welcome` | `welcome` | `isomer-op-entrypoint->welcome` |
| `core` | `isomer-op-project-mgr` | `project` | `isomer-op-entrypoint->project` |
| `core` | `isomer-op-gui-mgr` | `gui` | `isomer-op-entrypoint->gui` |
| `core` | `isomer-op-switch-identity` | `identity` | `isomer-op-entrypoint->identity` |
| `core` | `isomer-op-system-skill-mgr` | `system-skills` | `isomer-op-entrypoint->system-skills` |
| `core` | `isomer-op-toolbox-mgr` | `toolbox` | `isomer-op-entrypoint->toolbox` |
| `core` | `isomer-op-topic-creator` | `topic-create` | `isomer-op-entrypoint->topic-create` |
| `core` | `isomer-op-topic-mgr` | `topic-manage` | `isomer-op-entrypoint->topic-manage` |
| `core` | `isomer-op-topic-team-specialize` | `topic-team` | `isomer-op-entrypoint->topic-team` |
| `core` | `isomer-srv-topic-env-setup` | `topic-env` | `isomer-op-entrypoint->topic-env` |
| `core` | `isomer-srv-agent-env-setup` | `agent-env` | `isomer-op-entrypoint->agent-env` |
| `core` | `isomer-srv-resolve-pkg-repo` | `package-repo` | `isomer-op-entrypoint->package-repo` |
| `core` | `isomer-srv-houmao-interop` | `houmao` | `isomer-op-entrypoint->houmao` |
| `core` | `isomer-srv-topic-service-agent-support` | `topic-service` | `isomer-op-entrypoint->topic-service` |
| `core` | `isomer-misc-bounded-run-tips` | `bounded-run` | `isomer-op-entrypoint->bounded-run` |
| `core` | `isomer-misc-nvidia-tools` | `nvidia` | `isomer-op-entrypoint->nvidia` |
| `core` | `isomer-misc-pkg-specifics` | `package-specifics` | `isomer-op-entrypoint->package-specifics` |
| `core` | `isomer-misc-tool-packs` | `tool-packs` | `isomer-op-entrypoint->tool-packs` |
| `core` | `isomer-research-idea-recording` | `research-ideas` | `isomer-op-entrypoint->research-ideas` |
| `core` | `isomer-research-operation-set-recording` | `operation-sets` | `isomer-op-entrypoint->operation-sets` |
| `deepsci` | `isomer-deepsci-analysis` | `analysis` | `isomer-ext-deepsci-entrypoint->analysis` |
| `deepsci` | `isomer-deepsci-baseline` | `baseline` | `isomer-ext-deepsci-entrypoint->baseline` |
| `deepsci` | `isomer-deepsci-decision` | `decision` | `isomer-ext-deepsci-entrypoint->decision` |
| `deepsci` | `isomer-deepsci-experiment` | `experiment` | `isomer-ext-deepsci-entrypoint->experiment` |
| `deepsci` | `isomer-deepsci-figure-polish` | `figure-polish` | `isomer-ext-deepsci-entrypoint->figure-polish` |
| `deepsci` | `isomer-deepsci-finalize` | `finalize` | `isomer-ext-deepsci-entrypoint->finalize` |
| `deepsci` | `isomer-deepsci-idea` | `idea` | `isomer-ext-deepsci-entrypoint->idea` |
| `deepsci` | `isomer-deepsci-nature-data` | `nature-data` | `isomer-ext-deepsci-entrypoint->nature-data` |
| `deepsci` | `isomer-deepsci-nature-figure` | `nature-figure` | `isomer-ext-deepsci-entrypoint->nature-figure` |
| `deepsci` | `isomer-deepsci-nature-paper2ppt` | `nature-paper2ppt` | `isomer-ext-deepsci-entrypoint->nature-paper2ppt` |
| `deepsci` | `isomer-deepsci-nature-polishing` | `nature-polishing` | `isomer-ext-deepsci-entrypoint->nature-polishing` |
| `deepsci` | `isomer-deepsci-optimize` | `optimize` | `isomer-ext-deepsci-entrypoint->optimize` |
| `deepsci` | `isomer-deepsci-paper-outline` | `paper-outline` | `isomer-ext-deepsci-entrypoint->paper-outline` |
| `deepsci` | `isomer-deepsci-paper-plot` | `paper-plot` | `isomer-ext-deepsci-entrypoint->paper-plot` |
| `deepsci` | `isomer-deepsci-rebuttal` | `rebuttal` | `isomer-ext-deepsci-entrypoint->rebuttal` |
| `deepsci` | `isomer-deepsci-review` | `review` | `isomer-ext-deepsci-entrypoint->review` |
| `deepsci` | `isomer-deepsci-science` | `science` | `isomer-ext-deepsci-entrypoint->science` |
| `deepsci` | `isomer-deepsci-scout` | `scout` | `isomer-ext-deepsci-entrypoint->scout` |
| `deepsci` | `isomer-deepsci-shared` | `shared` | `isomer-ext-deepsci-entrypoint->shared` |
| `deepsci` | `isomer-deepsci-workspace-mgr` | `workspace` | `isomer-ext-deepsci-entrypoint->workspace` |
| `deepsci` | `isomer-deepsci-write` | `write` | `isomer-ext-deepsci-entrypoint->write` |
| `kaoju` | `isomer-kaoju-acquire` | `acquire` | `isomer-ext-kaoju-entrypoint->acquire` |
| `kaoju` | `isomer-kaoju-audit` | `audit` | `isomer-ext-kaoju-entrypoint->audit` |
| `kaoju` | `isomer-kaoju-compare` | `compare` | `isomer-ext-kaoju-entrypoint->compare` |
| `kaoju` | `isomer-kaoju-discover` | `discover` | `isomer-ext-kaoju-entrypoint->discover` |
| `kaoju` | `isomer-kaoju-examine` | `examine` | `isomer-ext-kaoju-entrypoint->examine` |
| `kaoju` | `isomer-kaoju-export` | `export` | `isomer-ext-kaoju-entrypoint->export` |
| `kaoju` | `isomer-kaoju-frame` | `frame` | `isomer-ext-kaoju-entrypoint->frame` |
| `kaoju` | `isomer-kaoju-reproduce` | `reproduce` | `isomer-ext-kaoju-entrypoint->reproduce` |
| `kaoju` | `isomer-kaoju-shared` | `shared` | `isomer-ext-kaoju-entrypoint->shared` |
| `kaoju` | `isomer-kaoju-synthesize` | `synthesize` | `isomer-ext-kaoju-entrypoint->synthesize` |
| `kaoju` | `isomer-kaoju-trial` | `trial` | `isomer-ext-kaoju-entrypoint->trial` |
| `kaoju` | `isomer-kaoju-workspace-mgr` | `workspace` | `isomer-ext-kaoju-entrypoint->workspace` |
| `kaoju` | `isomer-kaoju-write` | `write` | `isomer-ext-kaoju-entrypoint->write` |

## Invocation Grammar

A skill or subskill component is bare. A command component always has `()`.

```text
isomer-op-entrypoint
isomer-op-entrypoint->project
isomer-op-entrypoint->project->init-project()
isomer-ext-kaoju-entrypoint->manage-survey()->list()
isomer-ext-kaoju-entrypoint->manage-paper-template()->file()->put()
```

Parent commands act as object generators. In `skill->cmd_parent()->cmd_child()`, the child is the invoked subcommand declared by `cmd_parent()`; the chain does not execute the parent's standalone terminal workflow first. Once a command component appears, a later bare component is invalid. A command and subskill may share a name because `X->Y()` names the command and `X->Y` names the subskill.

Use private resource ownership to decide how to author a capability. A unit that owns its own `SKILL.md` metadata, `agents/`, scripts, references, templates, assets, or another private resource root is a protected subskill. A procedure that uses only resources owned by its containing bundle is a command, including a parent command with child commands. Triggers or workflow importance do not override this resource-boundary test.

## Dependency Closure and Private Projection

Each protected capability declares logical-id dependencies. Catalog resolution returns the selected capabilities and their transitive closure in deterministic order, including cross-pack dependencies. It also returns each member's owning pack, nested source path, scoped member, and invocation designator.

Ordinary installation ignores that selective surface and installs complete public packs. Internal Agent Role, Agent Profile, Topic Actor, and Service Agent adapters may instead project only a requested protected capability closure. The Isomer-Houmao adapter materializes each selected nested bundle as a flat logical-id directory in the role-private skill root, without granting parent or sibling filesystem access, and writes projection metadata that records the pack, nested source, invocation designator, dependencies, and binding reference.

Provider-neutral Skill Binding Projection continues to store logical ids. It does not store the nested package layout.

## Callback Identity

Callback registration, resolution, and stored provenance continue to target protected logical ids such as `isomer-deepsci-scout`. Callback insertion-point discovery and explained output add the owning pack, nested path, scoped member, and invocation designator. Each protected member resolves its own `begin` and `end` callbacks at the same workflow boundaries after the public parent routes to it.

Old pipeline callback targets normalize to `isomer-ext-deepsci-entrypoint` or `isomer-ext-kaoju-entrypoint` for current resolution. Historical stored provenance remains unchanged.

## Receipts, Status, and Migration

Managed roots use `isomer-labs-skill-manifest.v4`. Each receipt record represents one public pack and includes its public name, pack id, source path, projection mode, package and skill versions, extension id, and ordered protected inventory. Every protected inventory row records logical id, relative nested path, invocation designator, and version.

Status verifies the public entrypoint, projection mode, receipt identity, every protected member identity and version, missing members, extra protected paths, and compatibility. A top-level name alone cannot make a pack complete.

Readers retain v1 through v3 support as legacy flat evidence. They report tracked paths and candidate owner packs without inventing nested integrity. Use managed upgrade to migrate:

```bash
isomer-cli system-skills upgrade --target codex --scope project
isomer-cli system-skills upgrade --target codex --scope project --extension deepsci
isomer-cli system-skills upgrade --target codex --scope project --extension kaoju
```

Upgrade validates destination conflicts, stages complete new packs, validates their material, and writes receipt v4 before removing old paths. If staging or validation fails, the old receipt and projections remain intact. Cleanup removes only exact obsolete top-level paths tracked by the old receipt. Untracked lookalike directories are preserved. A cleanup failure returns exact `stale_retained` paths, `migration_status=partial_cleanup`, and repair guidance while retaining bounded legacy evidence in receipt v4.

After install or upgrade, refresh the agent host or start a new session. A running host may cache old skill discovery, so file and receipt success do not prove current-session activation.

See [System Skill Migration](system-skill-migration.md) for the operator migration checklist.

## Explicit Inspection

Version-aligned skills can inspect a host-supplied root or a host-supplied name inventory without embedding provider paths:

```bash
isomer-cli --print-json internals inspect-system-skill-root --skill-root /explicit/agent/skill-root --category extensions
isomer-cli --print-json internals inspect-system-skill-root --skill-root /explicit/agent/skill-root --extension kaoju
isomer-cli --print-json internals classify-system-skill-inventory --skill-name isomer-ext-kaoju-entrypoint
```

These read-only commands return `mutated: false` and use `isomer-internal-system-skill-inspection.v2`. Explicit-root inspection can verify v4 receipt and nested pack integrity, report legacy flat receipt rows, and leave ambient top-level siblings unclassified. Live inventory is deliberately limited: a public name yields `entrypoint_seen`, and old protected names yield legacy observations. Neither proves complete protected coverage.

Project declarations are authoritative routing intent, not current-host integrity evidence. The protected system-skill manager evaluates Project declaration, current v4 receipt, explicit-root integrity, and limited live inventory in that order. It registers only verified current-v4 complete packs.

## Namespace Rules

Reserve these public forms:

- `isomer-op-entrypoint` is the sole public core pack.
- `isomer-ext-<extension-id>-entrypoint` is the public form for an optional extension pack.

Protected logical ids retain responsibility-oriented forms such as `isomer-op-*`, `isomer-srv-*`, `isomer-misc-*`, `isomer-research-*`, `isomer-deepsci-*`, and `isomer-kaoju-*`. Do not use `isomer-ext-*` for protected helpers or arbitrary capability buckets. Do not add top-level compatibility shim folders for protected ids or the old pipeline aliases.

## Authoring and Release Checks

Every public pack and protected member remains a complete skill bundle and must resolve its local resources without parent or sibling access. Shared family procedures route through the family's protected `shared` member rather than duplicated prose or sibling paths.

All 57 `agents/openai.yaml` files carry `metadata.version` equal to `project.version`, including release candidates. `minimum_compatible_skill_version` is a separate compatibility floor and changes only when support policy changes.

Run these checks before release:

```bash
pixi run validate-skills
pixi run lint
pixi run typecheck
pixi run test
pixi run python -c "import isomer_labs"
```
