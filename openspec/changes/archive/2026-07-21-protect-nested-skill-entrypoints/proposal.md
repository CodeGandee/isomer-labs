## Why

Codex and other agent hosts recursively discover every nested file named `SKILL.md`, so protected subskills and preserved source snapshots inside an installed public skill pack can be registered as unintended top-level skills. The Imsight authoring contract currently requires the same filename for public skills and parent-scoped subskills, which makes the declared protection boundary depend on host-specific scan behavior.

## What Changes

- **BREAKING** Rename authored parent-scoped subskill entrypoints from `SKILL.md` to `SKILL-MAIN.md`; keep `SKILL.md` exclusively for host-discoverable skill roots.
- Teach `imsight-agent-skill-handling` and both bundled Imsight style-guide surfaces to create, locate, inspect, format, migrate, test, and route subskills through `SKILL-MAIN.md` while continuing to accept `SKILL.md` for top-level skills.
- Audit every `imsight-*` skill bundle and rename nested preserved source entrypoints to a non-discoverable provenance filename so recursive scanners do not expose them.
- Migrate all 53 packaged Isomer protected capabilities to `SKILL-MAIN.md`, keep the six public welcome and execution entrypoints on `SKILL.md`, and make each public execution entrypoint explicitly load only its selected protected member's `SKILL-MAIN.md`.
- Update packaged-asset resolution, validation, installation, inspection, documentation, and tests to enforce the role-aware filename contract.
- Preserve selective Agent Role behavior by promoting a deliberately flattened protected private projection from `SKILL-MAIN.md` to top-level `SKILL.md`; full public-pack materialization keeps nested members non-discoverable.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `imsight-subskill-routing-guidance`: Define `SKILL-MAIN.md` as the recursive subskill entrypoint and require parent routers and authoring workflows to resolve it explicitly.
- `protected-system-skill-routing`: Make filename-based non-discovery part of the protected-member boundary and define explicit parent loading and flattened private-projection promotion.
- `packaged-system-skills`: Change packaged protected asset resolution and materialization from nested `SKILL.md` files to role-aware entrypoint filenames while preserving public installation and private projection behavior.
- `packaged-system-skill-template-format`: Validate public `SKILL.md`, protected `SKILL-MAIN.md`, and the absence of recursively discoverable undeclared `SKILL.md` files.

## Impact

The change affects `extern/orphan/houmao-agents/skillset/imsight-skills`, packaged assets under `src/isomer_labs/assets/system_skills`, system-skill asset and installer helpers, validation scripts, unit tests, OpenSpec path assertions, and developer documentation. Existing consumers that directly open a protected bundle's `SKILL.md` must use `SKILL-MAIN.md` or a role-aware resolver; public skill roots and ordinary user-authored standalone skills remain unchanged.
