## Context

Isomer has three related but separate sources of extension information. The packaged system-skill catalog says which extensions and member skills exist, the Project Manifest records user-declared operator extensions, and each target skill root may contain an `isomer-labs-skill-manifest.json` installation receipt plus projected skill directories. Only callback insertion-point discovery currently consumes Project declarations, receipts carry only the Isomer package version, and operator routing names optional extensions statically.

Different agent targets can have different extensions or versions installed. Claude Code, Kimi Code, and generic targets use Project-local roots, while Codex uses `$CODEX_HOME/skills` or `~/.codex/skills`. Project initialization cannot infer which target will later act as operator and must not turn one target's filesystem state into a Project-wide declaration.

Codex currently ignores unknown top-level fields in `agents/openai.yaml`, so an Isomer-owned `metadata.version` field is compatible while remaining directly readable by Isomer. The release version in `pyproject.toml` and installed package metadata uses PEP 440 and can include release candidates.

## Goals / Non-Goals

**Goals:**

- Give every packaged Isomer skill one release-aligned version in `agents/openai.yaml`.
- Define compatibility floors in the package-owned system-skill catalog rather than in user declarations or installed skill content.
- Preserve per-skill versions in installation receipts and diagnose installation drift and compatibility per target.
- Provide read-only Project extension detection and initialization advice without automatic declaration, installation, upgrade, or removal.
- Prevent the operator entrypoint from automatically selecting an optional extension whose relevant target is unavailable or incompatible.

**Non-Goals:**

- Do not auto-write `[operator.system_extensions]` from detection.
- Do not choose a Project-wide operator target.
- Do not make Codex or another agent host interpret skill versions.
- Do not introduce third-party extension registries or relax the packaged-catalog requirement for extension ids.
- Do not solve the separate Kaoju managed-dataset owner handoff.

## Decisions

### Store the Skill Version Only in `agents/openai.yaml`

Each packaged skill carries `metadata.version = "<release>"` in `agents/openai.yaml`. The value exactly matches the Isomer CLI/package release that ships the source skill, including candidates such as `0.3.0rc1`. `SKILL.md` frontmatter remains unchanged. Isomer validators parse the YAML metadata and require valid PEP 440 plus equality with the source package version.

The version is a release provenance marker, not an independent semantic version for the skill. A release process updates every packaged skill version even when a skill's prose did not change. This makes a copied installation attributable to one Isomer release and avoids divergent version schemes.

Alternative considered: duplicate the version in `SKILL.md` frontmatter. This adds a second source of truth and conflicts with current repository contracts that restrict some frontmatter to `name` and `description`.

### Keep Compatibility in the Package-Owned Catalog

Each system-skill group declares a `minimum_compatible_skill_version`, and an optional per-skill metadata value can override the group floor. The current package reads the installed skill version and compares it with the floor using PEP 440 ordering. The runtime dependency on `packaging` is declared directly.

For CLI version `C`, installed skill version `S`, and minimum `M`, detection classifies `S < M` as obsolete and incompatible, `M <= S < C` as compatible older, `S == C` as current, and `S > C` as newer than the CLI with compatibility unknown. Newer-than-CLI installations are not automatically routed because an older CLI may lack commands required by the newer skill. Release candidates follow normal PEP 440 ordering.

Alternative considered: require exact equality with the CLI version. This would reject compatible older skills and force needless upgrades. Alternative considered: embed `requires_cli` in each installed skill. That lets detached content assert compatibility and weakens the package-owned authority.

### Snapshot Per-Skill Version in Installation Receipts

The target-root receipt records `skill_version` for every tracked skill. A new receipt schema version requires this field, while readers continue to accept the legacy schema and classify its records as unversioned until upgrade. Detection compares the receipt snapshot with the projected `agents/openai.yaml`; disagreement is receipt drift and does not count as verified compatibility.

The receipt's package version remains useful release context but is not substituted for a missing skill version because manually preserved or overwritten paths can differ from the package that last wrote the receipt.

### Detect Per Target and Never Declare Automatically

`isomer-cli project system-extensions detect` performs a read-only inspection. It reports catalog membership, Project declaration state, target, root, receipt evidence, entry-skill and member-skill coverage, per-skill versions, aggregate compatibility, diagnostics, and exact install, upgrade, remember, or CLI-upgrade advice. It never mutates the Project Manifest or skill roots.

Without explicit targets, Project detection inspects only deterministic Project-local roots for Claude Code, Kimi Code, and generic agents. Codex inspection requires an explicit target because its root is user-global. Results stay separated by target and are never collapsed into a Project-wide installed boolean.

Project initialization performs the same Project-local read-only inspection before completing and includes the observations in its result. It can advise `project system-extensions remember <id>` but does not run it.

Alternative considered: seed declarations from a valid receipt. This incorrectly promotes one machine and target's observation into shared Project state.

### Gate Automatic Entrypoint Routing on Effective Availability

The entrypoint checks Project declaration state and target-specific detection before automatically selecting an optional extension. Ready and compatible-older states may route. Missing, partial, unversioned, malformed, drifted, obsolete, or newer-than-CLI states produce repair advice instead. A direct user invocation remains explicit intent, but the entrypoint still reports compatibility blockers rather than pretending the route is ready.

## Risks / Trade-offs

- [Every release updates many YAML files] → Provide a mechanical release/version synchronization command or validator-backed update step and test exact equality with the package version.
- [A manually edited skill can retain the same version] → Receipt comparison detects many replacements but is not content integrity; a future digest field can strengthen verification without changing this version contract.
- [Legacy receipts and skills lack versions] → Accept legacy receipts read-only, report `unversioned`, and advise `system-skills upgrade`.
- [The active agent session may not reload newly installed files] → Detection reports filesystem availability only and advises session reload when routing still cannot load a detected skill.
- [A newer skill may happen to work with an older CLI] → Treat it as unknown unless a future package compatibility rule explicitly permits it; the conservative action is CLI upgrade.

## Migration Plan

1. Add `packaging` as a direct dependency and extend catalog models with compatibility floors.
2. Add the current release version to every packaged skill `agents/openai.yaml` and extend validators.
3. Introduce a backward-compatible receipt reader and write the new per-skill version receipt schema on install or upgrade.
4. Add target-specific detection and Project CLI output.
5. Add Project initialization observations and operator entrypoint routing guidance.
6. Update documentation and tests. Existing Project declarations remain unchanged; rollback can ignore the new YAML field and continue reading legacy receipts.

## Open Questions

None for this change. Third-party extension discovery remains a separate future design.
