## 1. Manifest v4 and Catalog Model

- [x] 1.1 Add `isomer-skillset-manifest.v4` constants and public-skill role records to the packaged system-skill catalog while retaining read-only v3 parsing for migration fixtures.
- [x] 1.2 Refactor `SystemSkillPack` to expose an ordered public-skill inventory and one designated execution entrypoint without treating the entrypoint path or commands as the complete public pack.
- [x] 1.3 Parse and validate globally unique public names and paths, exactly one `welcome` and one `entrypoint` per current pack, canonical core and extension role names, and an `entry_skill` that resolves to the entrypoint-role record.
- [x] 1.4 Keep protected capability paths and invocation designators anchored below the designated entrypoint, and reject welcome-owned or top-level duplicates of protected logical ids.
- [x] 1.5 Extend identity normalization and lookup so any public welcome or entrypoint resolves to its owning pack and role while protected ids, invocation designators, dependencies, and legacy aliases retain their current meanings.
- [x] 1.6 Update group, extension, materialization, package-resource, and compatibility views to enumerate both public skill paths in manifest order while retaining entrypoint-focused compatibility accessors where needed.
- [x] 1.7 Update callback insertion-point catalog construction so entrypoint and protected targets retain current ownership, public welcomes expose no insertion points, and returned metadata distinguishes public role from protected member.
- [x] 1.8 Add catalog and materialization unit tests for valid public pairs, missing or duplicate roles, invalid extension names, identity collisions, protected path anchoring, copy output, and manifest v3 compatibility parsing.

## 2. Public Welcome Skill Assets

- [x] 2.1 Move the historical core welcome bundle from `isomer-op-entrypoint/subskills/isomer-op-welcome` to the public sibling `operator/isomer-op-welcome` and remove its protected capability declaration and `welcome` route-table row.
- [x] 2.2 Revise core welcome metadata, workflow, common commands, output contract, and guardrails for independent newcomer use and public `$isomer-op-welcome` invocation.
- [x] 2.3 Author the core typical-use-case guidance for Project, Topic, manual research, formal Agent Team, GUI, identity, system-skill extension, Toolbox, and environment-support patterns, including exact entrypoint examples and mutation boundaries.
- [x] 2.4 Add core `show-command-map` guidance that covers every current `isomer-op-entrypoint` public command once, while retaining `show-extensions` and the four established start-path routines.
- [x] 2.5 Create the self-contained public `isomer-ext-deepsci-welcome` bundle with common welcome commands, curated hypothesis, empirical, experiment, analysis, paper, revision, rebuttal, polish, and readiness patterns, and a complete DeepSci entrypoint command map.
- [x] 2.6 Create the self-contained public `isomer-ext-kaoju-welcome` bundle with common welcome commands, curated landscape, reading-list, framing, evidence-intake, comparison, code, trial, paper, and wiki patterns, and a complete Kaoju entrypoint command map.
- [x] 2.7 Update core, DeepSci, and Kaoju entrypoints so empty invocation, `help`, and retained welcome-style commands delegate read-only output to the public sibling welcome for at least one minor release without copying welcome resources.
- [x] 2.8 Replace active `isomer-op-entrypoint->welcome` references with `$isomer-op-welcome`, route extension learning to extension welcomes, and keep concrete work routed to the corresponding execution entrypoint.
- [x] 2.9 Audit each welcome bundle for self-contained one-level references, current Isomer domain language, representative routing cues rather than claimed magic keywords, and no direct protected-skill invocation.
- [x] 2.10 Update all packaged skill `agents/openai.yaml` metadata and align every packaged skill version, including the three welcomes, with `project.version` under the release rule.

## 3. Manifest Asset and Pack Discovery

- [x] 3.1 Convert `assets/system_skills/manifest.toml` to schema v4 with explicit public-skill records for the six public skills and remove core welcome from `protected_members` and `[[capabilities]]`.
- [x] 3.2 Preserve the existing execution entrypoint command inventories, protected member order, dependency edges, aliases, callback stages, compatibility floors, and extension ids during the manifest conversion.
- [x] 3.3 Update packaged READMEs, route indexes, extension indexes, validation configuration, expected inventories, and system-skill maps to describe welcome and entrypoint as two public roles per pack.
- [x] 3.4 Update system-skill list and extension discovery data models and human-readable output to show ordered public role records, designated entrypoint, entrypoint commands, and protected summaries.
- [x] 3.5 Update Project extension reporting and system-skill-manager guidance to distinguish welcome-seen, entrypoint-seen, Project-declared, and integrity-verified evidence without requiring welcome for routing intent.
- [x] 3.6 Add CLI and catalog tests for list, extension list/show, JSON role records, public invocations, and absence of the old protected welcome designator.

## 4. Receipt v5 and Pack-Atomic Installation

- [x] 4.1 Define `isomer-labs-skill-manifest.v5` receipt dataclasses for one pack record with ordered public projection records and protected entrypoint-member records.
- [x] 4.2 Implement v5 receipt serialization, parsing, ownership maps, validation, deterministic ordering, and conservative read-only support for v1-v4 receipts.
- [x] 4.3 Refactor installer selection records so group, extension, welcome, entrypoint, protected, and legacy selectors resolve to complete packs while preserving requested-selector diagnostics.
- [x] 4.4 Refactor staging to project and recursively validate every public skill in a pack before changing live destinations, for both copy and symlink modes.
- [x] 4.5 Make install conflict detection, force replacement, backups, commit, receipt writing, and rollback operate atomically across the welcome and entrypoint siblings.
- [x] 4.6 Extend status models and output with per-public-role identity, version, compatibility, projection mode, receipt ownership, and aggregate pack verification alongside protected-member integrity.
- [x] 4.7 Make uninstall resolve either public name to the owning pack, report both affected paths, remove only receipt-owned public projections, and update the v5 receipt atomically without following symlinks.
- [x] 4.8 Implement managed v4-to-v5 upgrade that stages the new welcome sibling and refreshed entrypoint, validates both, replaces the compacted entrypoint, and writes v5 before stale cleanup.
- [x] 4.9 Extend legacy flat-receipt migration to reuse receipt-owned top-level core welcome paths, preserve and block on untracked public-welcome conflicts, and remove only supported receipt-tracked obsolete paths.
- [x] 4.10 Add rollback and partial-cleanup diagnostics for failures during multi-public commit, receipt write, or post-commit legacy cleanup.
- [x] 4.11 Update install, status, upgrade, and uninstall human and JSON renderers to report pack outcomes plus individual public projections without presenting them as independently mutable units.
- [x] 4.12 Add installer and receipt tests for default core selection, extension selection, welcome and entrypoint selectors, copy and symlink pairs, conflicts, force, status incompleteness, uninstall, v1-v4 parsing, v4 migration, flat migration, rollback, and stale-path safety.

## 5. Inspection and Integration Surfaces

- [x] 5.1 Update explicit-root inspection to correlate v5 public projection records, report welcome and entrypoint evidence separately, and require both plus protected integrity for verified pack coverage.
- [x] 5.2 Update live-inventory classification to recognize public welcome and entrypoint roles independently while keeping name-only observations unverified.
- [x] 5.3 Update internal inspection schemas, deterministic output, ambient-path classification, and diagnostics for multi-public packs and v4 legacy evidence.
- [x] 5.4 Audit callback commands, Skill Binding Projection, artifact identity, Houmao adapter projection, and protected private-projection APIs so they continue to use the designated entrypoint and stable protected logical ids rather than the welcome skill.
- [x] 5.5 Update DeepSci and Kaoju package contracts and tests only where public pack metadata is surfaced, while keeping process registries, artifact producers, pass commands, and protected execution identities entrypoint-owned.
- [x] 5.6 Add inspection and integration tests for complete public pairs, welcome-only and entrypoint-only observations, v5 ownership drift, protected-name observations, extension declaration output, and deterministic ordering.

## 6. Welcome and Pack Validation

- [x] 6.1 Extend manifest-aware skill discovery to classify public welcomes, public entrypoints, and protected subskills from manifest v4 and recursively validate every active bundle.
- [x] 6.2 Add common welcome validation for canonical identity, metadata, allowed implicit orientation triggers, workflow shape, common commands, read-only posture, public handoffs, self-contained resources, output contract, and negative-only guardrails.
- [x] 6.3 Validate each typical-use-case row for a one-sentence use condition, routing cues, required context, canonical route, exact invocation example, expected action, mutation posture, and next step without requiring verbatim source metadata.
- [x] 6.4 Validate each welcome command map against its sibling entrypoint's manifest command inventory for exact, unique, current coverage.
- [x] 6.5 Add pack-specific category checks for core platform patterns, DeepSci production-research patterns, and Kaoju evidence-led survey patterns.
- [x] 6.6 Reject active welcome guidance that invokes protected logical ids directly, uses the retired `isomer-op-entrypoint->welcome` designator, duplicates entrypoint execution procedure, or claims example phrases are mandatory parser keywords.
- [x] 6.7 Update entrypoint validation to require independent welcome delegation, reject a protected welcome member, and preserve all existing execution, protected routing, callback, run-to, and retired-route checks.
- [x] 6.8 Update validator tests and fixtures for valid welcome pairs, missing resources, bad role metadata, incomplete use cases, command drift, protected-route leaks, duplicate ownership, and unrelated existing family rules.

## 7. Documentation, Migration Guidance, and Release Notes

- [x] 7.1 Update installation, quickstart, packaged system-skill, extension, and command-reference documentation to present welcome-first onboarding and direct entrypoint execution as separate supported paths.
- [x] 7.2 Add representative core, DeepSci, and Kaoju examples that pair natural-language routing cues with deterministic public commands and explain prerequisites and mutation posture.
- [x] 7.3 Document complete-pack selector behavior, v5 receipts, v4 and flat migration, conflict handling, managed upgrade, and the required agent-host refresh or new session.
- [x] 7.4 Update documentation validation so public names, roles, command examples, and protected-route exclusions are checked against manifest v4.
- [x] 7.5 Update `CHANGELOG.md` with the three independent welcome skills, multi-public pack installation, receipt v5 migration, compatibility delegation, and newcomer workflow guidance.

## 8. Verification

- [x] 8.1 Run focused catalog, system-assets, installer, receipt, inspection, CLI, Kaoju-contract, callback, validator, and documentation unit tests and fix all regressions.
- [x] 8.2 Run `pixi run validate-skills` and confirm all public welcomes, entrypoints, protected subskills, command maps, versions, and local references pass.
- [x] 8.3 Run copy and symlink installation smoke tests for core-only, each named extension, all extensions, current v4 upgrade, and one supported flat-receipt migration in temporary target roots.
- [x] 8.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test` from the repository root.
- [x] 8.5 Build or inspect installed package resources without relying on the repository layout and verify all six public skills materialize with self-contained active resources.
- [x] 8.6 Run `openspec validate add-independent-pack-welcome-skills --strict` and reconcile the implementation, delta specs, design, and completed task checklist before handoff.
