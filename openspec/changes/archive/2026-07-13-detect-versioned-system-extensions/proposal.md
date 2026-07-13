## Why

Project operators can declare optional system-skill extensions, but Isomer cannot currently tell whether a particular agent target has a complete, compatible installation. As DeepSci, Kaoju, and future extensions evolve independently across agent targets, static routing can recommend missing or obsolete skills and Project initialization can mistake one agent's installation for Project-wide availability.

## What Changes

- Add release-aligned skill versions to packaged skills through `agents/openai.yaml`; versions use the exact PEP 440 Isomer CLI release, including release candidates.
- Extend package-owned system-skill metadata with minimum compatible skill versions and validate packaged metadata consistency.
- Record each installed skill version in the target-root installation receipt and detect missing, malformed, drifted, obsolete, compatible-older, current, and newer-than-CLI installations.
- Add read-only, target-specific Project extension detection that reports evidence and repair advice without remembering declarations or mutating installations.
- Let Project initialization inspect deterministic Project-local agent skill roots and report detected extension advice without changing `[operator.system_extensions]`.
- Make the operator entrypoint consult declared and detected compatibility state before automatically routing to an optional extension.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `system-skill-installer-cli`: Add release-aligned per-skill versions, package-owned minimum compatibility metadata, receipt snapshots, and compatibility-aware status reporting.
- `operator-system-extension-declarations`: Add read-only, per-target detection and advice while preserving user-only declaration mutation.
- `isomer-cli-project-discovery`: Add advisory Project-local extension detection to Project initialization without automatic declarations.
- `isomer-op-entrypoint-skill`: Require extension availability and compatibility checks before automatic extension routing.

## Impact

This affects packaged skill metadata under `src/isomer_labs/assets/system_skills/`, the system-skill catalog and installer, Project system-extension commands, Project initialization output, operator entrypoint guidance, validation scripts, documentation, and focused unit tests. Version comparison will use PEP 440 semantics; if `packaging` is used at runtime it becomes a direct project dependency.
