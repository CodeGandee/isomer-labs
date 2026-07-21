## Context

Agent hosts such as Codex recursively discover files named exactly `SKILL.md` below configured skill roots. Isomer public packs intentionally contain protected subskills, and Imsight authoring guidance currently models those subskills as ordinary nested skill folders with their own `SKILL.md`. The filesystem therefore contradicts the parent-only routing contract even though manifests, invocation designators, and documentation call the members protected.

The migration crosses two repositories. Houmao Agents owns the general Imsight skill-writing contract and the `imsight-*` authored skill suite. Isomer Labs owns package assets, role-aware catalog metadata, complete public-pack installation, selective protected projection, validation, and system-skill documentation. Existing top-level standalone skills and callback `skill_dir` sources remain host-discoverable and continue to use `SKILL.md`.

## Goals / Non-Goals

**Goals:**

- Make filename-based host discovery match the declared public-versus-protected skill boundary.
- Give authors and agents a deterministic, backward-readable way to locate top-level and nested entrypoints.
- Migrate every packaged Isomer protected member and every nested skill-shaped source snapshot that could be recursively discovered.
- Preserve public-pack installation, explicit parent routing, validation, compatibility inspection, and selective Agent Role projection.
- Add regression checks that fail when a protected package member or nested provenance copy reintroduces `SKILL.md`.

**Non-Goals:**

- Change skill invocation designators, logical ids, pack manifests, workflows, gates, callbacks, or output contracts.
- Claim that protected files are secret or inaccessible to an agent that receives the complete pack.
- Change standalone user-authored skills, Toolbox callback skill directories, Houmao-owned top-level skills, or external source repositories.
- Depend on a Codex configuration switch or a fixed recursive scan-depth implementation detail.

## Decisions

### Use Role-Aware Entrypoint Filenames

Host-discoverable roots use `SKILL.md`. Parent-scoped subskills use `SKILL-MAIN.md`. Preserved upstream entrypoint snapshots under provenance trees use `SKILL-SOURCE.md` because they are evidence, not executable entrypoints.

The Imsight grammar notice and authoring workflows will state that a parent-selected subskill loads `SKILL-MAIN.md`; readers may accept nested `SKILL.md` only as legacy input during inspection or migration. New creation and formatting output must use the role-canonical filename, and a folder containing both candidate entrypoints is invalid.

This role distinction is preferable to relying on scan depth, hidden directories, symlinks, or host configuration because the pack remains safe under any recursive exact-`SKILL.md` scanner.

### Keep Public Pack Layout and Manifest Schema Stable

The manifest already distinguishes public skill paths from protected capability paths, so the filename can be derived from catalog role without adding another manifest field. Public records resolve `SKILL.md`; capability records resolve `SKILL-MAIN.md`. A shared package helper will return the role-canonical entrypoint so callers do not concatenate a filename themselves.

Complete pack materialization copies the package tree without renaming nested entrypoints. The resulting host root contains only the public welcome and entrypoint `SKILL.md` files as discoverable Isomer skills.

### Promote Deliberately Flattened Private Projections

Selective Agent Role projection changes a protected member from a nested parent-owned object into an intentionally exposed top-level bundle in a private skill root. During that materialization only, Isomer copies `SKILL-MAIN.md` as `SKILL.md` at the flattened destination and records the actual copied path. Dependencies receive the same treatment because each is an intentionally selected member of that bounded projection.

The package source stays canonical and unchanged. This projection-time promotion preserves current host discovery without weakening complete public-pack protection.

### Validate the Boundary at Source and Materialized Surfaces

Manifest-aware validation will select entrypoint filenames by record kind, validate the same structural and metadata rules for both names, require every protected member to have `SKILL-MAIN.md`, and reject protected `SKILL.md` files. A recursive public-pack check will allow `SKILL.md` only at declared public roots and will reject nested provenance copies or undeclared bundles that use the discovery filename.

Focused unit tests will cover package lookup, complete materialization, private-projection promotion, identity/version inspection, installation and upgrade status, routing guidance, and the no-nested-`SKILL.md` invariant. Research-paradigm and general skillset validators will use the same role-aware entrypoint helper or equivalent record-aware path selection.

### Migrate References Semantically

References to active protected entrypoints become `SKILL-MAIN.md`. References to public or standalone entrypoints remain `SKILL.md`. References to preserved upstream snapshots become `SKILL-SOURCE.md`. Generic callback `skill_dir` contracts remain `SKILL.md` because callbacks are standalone supplemental sources rather than parent-scoped subskills.

The three public execution entrypoints will explicitly instruct agents to resolve a selected manifest member below `subskills/<logical-id>/`, load only its `SKILL-MAIN.md` and required local resources, and then follow that member's full contract.

## Risks / Trade-offs

- [External tooling assumes every skill directory contains `SKILL.md`] → Provide a role-aware resolver, update all in-repository callers and tests, and retain legacy-input recognition in the authoring guide.
- [Private projections stop being discoverable] → Promote only flattened private projection entrypoints back to `SKILL.md` and test the resulting directory shape.
- [Blind text replacement changes public skills or callback contracts] → Derive the protected inventory from the manifest, rename only those paths, and audit remaining `SKILL.md` files by role.
- [Archived source snapshots remain recursively discoverable] → Rename nested provenance entrypoints to `SKILL-SOURCE.md` and update their local links and migration notes.
- [A running agent host caches the old inventory] → Keep existing refresh/restart guidance; installation success does not claim current-session rediscovery.
- [Older third-party subskills still use `SKILL.md`] → Inspection and migration guidance may read the legacy name, but formatting and creation normalize parent-scoped output to `SKILL-MAIN.md`.

## Migration Plan

1. Update the Imsight authoring contract, grammar notice, layout examples, and all affected subcommand workflows.
2. Rename nested provenance copies in the `imsight-*` suite and verify that each suite member has exactly one top-level `SKILL.md` and no deeper discovery filename.
3. Add role-aware Isomer entrypoint helpers and private-projection promotion.
4. Rename all manifest-declared protected package entrypoints and nested provenance snapshots, then update parent routing instructions and active references.
5. Update validators, installation and inspection code, tests, documentation, and OpenSpec path contracts.
6. Run focused unit and validation suites, then the repository lint, typecheck, and unit test commands when feasible.

Rollback restores the old filenames and callers together. A mixed package in which callers and assets disagree is invalid and must not be released.

## Open Questions

None. `SKILL-MAIN.md` is the canonical authored subskill filename, `SKILL-SOURCE.md` is the canonical non-executable provenance filename, and projection-time promotion is limited to deliberately flattened private roots.
