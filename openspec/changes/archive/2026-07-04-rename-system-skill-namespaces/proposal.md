## Why

The packaged system-skill catalog now exposes Isomer's skills as installable public interfaces, but the current `isomer-admin-*` and `isomer-rsch-*` names mix historical implementation language with active responsibility boundaries. Renaming the active namespaces makes the operator, service, misc, and domain-extension surfaces clearer before more extension families depend on the packaged skill contract.

## What Changes

- **BREAKING**: Rename active operator skill identities from `isomer-admin-*` to `isomer-op-*`, including folder names, `SKILL.md` frontmatter, agent metadata, manifest paths, direct invocation text, cross-skill routing, validators, tests, and active specs.
- **BREAKING**: Rename active DeepScientist-derived production research skills from `isomer-rsch-*` to `isomer-deepsci-*`, preserving the `research-paradigm/deepsci/` packaged root and the `[groups.deepsci]` manifest group.
- Keep `isomer-misc-*` as the public cross-domain helper namespace for stable helper interfaces such as bounded-run guidance, package specifics, NVIDIA tooling, and tool-pack resolution.
- Keep `isomer-srv-*` as the protected service-routed namespace for Service Team support skills; update their references to renamed operator and DeepSci skills where needed.
- Document the forward convention that domain extension families use `isomer-<extension-name>-<purpose>`, for example `isomer-deepsci-*`, while `isomer-misc-*` remains cross-domain helper infrastructure rather than a generic extension bucket.
- Do not add compatibility skill folders, aliases, or duplicate active shims for the old `isomer-admin-*` or `isomer-rsch-*` names.
- Preserve historical names inside archived OpenSpec changes and passive provenance/source-copy material such as `org/` and `migrate/` unless active validation treats a file as runtime guidance.

## Capabilities

### New Capabilities

- `system-skill-namespaces`: Defines the packaged system-skill namespace convention, active rename rules, extension family naming pattern, and compatibility policy.

### Modified Capabilities

- `operator-admin-skills`: Rename the active operator skill convention and inventory from `isomer-admin-*` to `isomer-op-*`.
- `research-paradigm-skills`: Rename the active production DeepSci skill convention and inventory from `isomer-rsch-*` to `isomer-deepsci-*`.
- `research-placeholder-bindings`: Update placeholder binding aggregation and validation so active DeepSci binding metadata, commands, producer, consumer, and `--skill` values use `isomer-deepsci-*`.
- `isomer-service-env-setup-skill`: Update service guidance and validation references that route package mutation, verification, or predecessor repair through renamed operator skills while preserving the `isomer-srv-*` service name.
- `isomer-agent-env-setup-service-skill`: Update service guidance and validation references that route repair or package-specific support through renamed operator skills while preserving the `isomer-srv-*` service name.
- `isomer-misc-tool-packs-skill`: Clarify that `isomer-misc-tool-packs` remains a public cross-domain helper, not a domain extension, and keep its helper routes aligned with the service and misc namespaces.
- `isomer-misc-pkg-specifics-skill`: Clarify that `isomer-misc-pkg-specifics` remains a public cross-domain helper consumed by service and operator skills.

## Impact

- Affected assets: `src/isomer_labs/assets/system_skills/` skill directories, `SKILL.md` frontmatter, `agents/openai.yaml`, local README files, placeholder binding pages, migration-facing active docs, and `manifest.toml`.
- Affected authoring view: repository-root `skillset/` symlinks continue pointing at packaged asset subtrees, but active folder names under those subtrees change.
- Affected validation: `scripts/validate_skillsets.py`, `scripts/validate_research_paradigm_skillset.py`, related unit tests, and active OpenSpec specs need updated expected names and stale-name checks.
- Affected user behavior: callers must use new active names such as `isomer-op-topic-mgr` and `isomer-deepsci-write`; old active invocations are intentionally unsupported after the rename.
- Affected package APIs: `isomer_labs.skills.system_assets` continues resolving manifest-listed paths, but the manifest entries change to the renamed folders.
