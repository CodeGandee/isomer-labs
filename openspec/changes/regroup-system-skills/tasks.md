## 1. Catalog and Identity Model

- [ ] 1.1 Add exact catalog fixtures for the three public packs and the 20 core, 21 DeepSci, and 13 Kaoju protected members, including scoped member names and preserved logical ids.
- [ ] 1.2 Add `SystemSkillPack` and `SystemSkillCapability` models that keep public identity, protected logical identity, nested source path, and invocation designator as separate fields.
- [ ] 1.3 Implement `isomer-skillset-manifest.v3` parsing for pack metadata, public commands, protected members, areas, dependencies, aliases, callback stages, and compatibility floors.
- [ ] 1.4 Reject duplicate identities, noncanonical invocation designators, invalid `isomer-ext-<extension-id>-entrypoint` names, escaped member paths, alias conflicts, unknown dependencies, and dependency cycles with deterministic diagnostics while allowing separately declared same-name commands and protected members.
- [ ] 1.5 Add catalog lookup APIs for public pack name, extension id, protected logical id, legacy alias, scoped member name, and canonical invocation designator.
- [ ] 1.6 Add deterministic protected dependency-closure resolution that supports cross-pack edges and returns each member's private-projection source metadata.
- [ ] 1.7 Retain read-only parsing support for manifest v2 fixtures where migration or compatibility tests need the old flat catalog.

## 2. Package the Three Public Skill Trees

- [ ] 2.1 Rewrite `src/isomer_labs/assets/system_skills/manifest.toml` as manifest v3 with `isomer-op-entrypoint`, `isomer-ext-deepsci-entrypoint`, and `isomer-ext-kaoju-entrypoint` as the only public packs.
- [ ] 2.2 Move the eight non-welcome core operator owner bundles below `operator/isomer-op-entrypoint/subskills/` while preserving their full logical-id folder and frontmatter names.
- [ ] 2.3 Move `isomer-op-welcome` below the core pack and make its accepted orientation routines available through the public entrypoint's help and visible start-path commands.
- [ ] 2.4 Move the five `isomer-srv-*` bundles below the core pack and register their `topic-env`, `agent-env`, `package-repo`, `houmao`, and `topic-service` scoped routes.
- [ ] 2.5 Move the four `isomer-misc-*` and two research-recording bundles below the core pack and register their six protected shared routes.
- [ ] 2.6 Rename the DeepSci pipeline bundle to `isomer-ext-deepsci-entrypoint`, retain its eight public pass commands plus help, and register `isomer-deepsci-pipeline` only as a legacy alias.
- [ ] 2.7 Move all 21 non-pipeline `isomer-deepsci-*` bundles below the DeepSci public pack and add the declared scoped member routes without changing their research method contracts.
- [ ] 2.8 Rename the Kaoju pipeline bundle to `isomer-ext-kaoju-entrypoint`, retain its accepted public command groups plus help, and register `isomer-kaoju-pipeline` only as a legacy alias.
- [ ] 2.9 Move all 13 non-pipeline `isomer-kaoju-*` bundles below the Kaoju public pack while preserving trial versus reproduction and every existing evidence boundary.
- [ ] 2.10 Remove obsolete top-level packaged skill directories after their content is present in the owning pack, and add checks that no compatibility shim directory remains.
- [ ] 2.11 Audit each routable unit by resource ownership: retain every moved capability that owns private entrypoint metadata, commands, references, scripts, assets, templates, or other support files as a self-contained subskill, and retain procedures that use their containing bundle's resources as direct or nested commands.

## 3. Invocation and Skill Validation

- [ ] 3.1 Update all three public entrypoints to support `$<entrypoint> use <subcommand> to <task>`, task-only route selection, empty-invocation help, and route-and-proceed behavior.
- [ ] 3.2 Replace active cross-skill prose routes with catalog-declared bare protected-member designators such as `isomer-op-entrypoint->project` and `isomer-ext-kaoju-entrypoint->trial`; put `()` on every actual command component, including parent generators in chains such as `isomer-ext-kaoju-entrypoint->manage-survey()->list()`.
- [ ] 3.3 Add the exact standard `skill_invocation_notation` frontmatter value to every active page that uses an object designator.
- [ ] 3.4 Update protected `agents/openai.yaml` prompts to point ordinary users at the owning public entrypoint while retaining the logical-id display identity needed for private projection.
- [ ] 3.5 Extend skill validation to enumerate public packs and protected members recursively from manifest v3 and validate identity, current-template structure, resources, and release versions.
- [ ] 3.6 Validate that each parent route table and invocation designator resolves to the declared capability kind, protected-member entrypoints are bare paths, every command component has `()`, every child command is declared by its immediate parent, no command chain returns to a bare component, same-name command and member routes remain distinguishable, and no undeclared nested skill exists.
- [ ] 3.7 Add active-guidance validation that rejects direct `$<protected-logical-id>` user prompts outside migration text and logical-id CLI fields.
- [ ] 3.8 Add flat private-projection fixtures that prove a selected protected bundle and its dependency closure work without parent or sibling filesystem access.
- [ ] 3.9 Add family checks that require DeepSci and Kaoju shared procedures to route through their protected `shared` member instead of sibling paths or duplicated process text, and reject a command that claims an independent private resource root instead of using its containing bundle.

## 4. Catalog Consumers, Callbacks, and Private Projection

- [ ] 4.1 Change callback insertion-point metadata to key targets by logical id and return owning pack, nested path, scoped member, and invocation designator in discovery and explained output.
- [ ] 4.2 Normalize old DeepSci and Kaoju pipeline callback targets to the new public entrypoint ids while leaving historical stored provenance unchanged.
- [ ] 4.3 Keep compact callback resolution payloads unchanged and verify that each protected member still applies its own begin and end callbacks by logical id.
- [ ] 4.4 Update Skill Binding Projection resolution helpers to map preserved logical ids through the catalog without storing pack filesystem layout in provider-neutral bindings.
- [ ] 4.5 Add the protected capability and dependency-closure API used by Topic Actor, Agent Role, Agent Profile, and Service Agent private projection.
- [ ] 4.6 Update the Isomer-Houmao adapter to project nested protected source paths with stable logical identity for intended roles and to include every declared dependency.
- [ ] 4.7 Update DeepSci and Kaoju extension-query payloads, process contracts, and artifact/source metadata to report the new public entry skill and protected member mapping.
- [ ] 4.8 Add tests for logical-id lookup, legacy alias normalization, callback target validation, stage-specific callback execution, and selective projection closure.

## 5. Pack-Based Installation and Receipts

- [ ] 5.1 Refactor installer selection records so core, extension, all-extension, public-skill, protected-logical-id, and legacy pipeline selectors resolve to complete public packs.
- [ ] 5.2 Emit deprecation diagnostics for protected or legacy `--skill` selectors and prevent ordinary selection from projecting a protected member beside its parent.
- [ ] 5.3 Refactor copy and symlink installation to project each selected public pack as one top-level unit with its complete nested tree.
- [ ] 5.4 Add `isomer-labs-skill-manifest.v4` receipt models and serialization for public pack records and their protected logical-id, relative-path, invocation, and version inventory.
- [ ] 5.5 Retain v1 through v3 receipt readers and report their tracked flat paths as legacy evidence without inventing nested pack integrity.
- [ ] 5.6 Update status to verify public projection mode, entrypoint metadata, every declared protected member, nested versions, resource integrity, and aggregate compatibility.
- [ ] 5.7 Update uninstall to remove a receipt-owned public pack as one unit, refuse single-member removal, and preserve unrelated or untracked paths.
- [ ] 5.8 Implement staged legacy upgrade that validates destination conflicts and complete new packs before writing v4 and removing only obsolete receipt-tracked top-level paths.
- [ ] 5.9 Make failed staging preserve the old receipt and projections, and make partial stale cleanup report exact retained paths and repair guidance.
- [ ] 5.10 Update list and extension discovery JSON and text output to distinguish public packs, protected members, commands, aliases, dependencies, and compatibility evidence.
- [ ] 5.11 Add copy, symlink, force, conflict, status, uninstall, v3-to-v4 upgrade, partial-cleanup, and untracked-path preservation tests.

## 6. Inspection and Operator Workflows

- [ ] 6.1 Update explicit-root inspection to parse v4 receipts and verify each public pack's protected nested inventory without recursively classifying ambient siblings.
- [ ] 6.2 Change live-inventory classification so a public name yields `entrypoint_seen`, legacy flat names yield legacy member observations, and neither proves complete pack integrity.
- [ ] 6.3 Update deterministic inspection output and compatibility status fields for pack coverage, missing protected logical ids, receipt drift, and entrypoint-only evidence.
- [ ] 6.4 Update protected System Skill Manager routines to use Project declarations, v4 receipts, explicit-root evidence, and limited live inventory in the accepted order.
- [ ] 6.5 Update protected System Skill Manager installation and repair flows to converge on public packs, managed migration, Project declaration, and post-install host refresh.
- [ ] 6.6 Update core welcome, skill maps, routing references, and extension recovery to name `isomer-ext-deepsci-entrypoint` and `isomer-ext-kaoju-entrypoint` and never advertise protected skills directly.
- [ ] 6.7 Add inspection and operator-workflow tests for complete packs, missing nested members, legacy flat installations, declaration-only state, entrypoint-only state, and refresh-pending state.

## 7. Documentation, Release Metadata, and Verification

- [ ] 7.1 Update the packaged skill README, developer system-skill guide, namespace guide, installation guide, CLI reference, and migration notes for the three public packs and protected visibility semantics.
- [ ] 7.2 Document all 54 protected logical-id to scoped-member mappings, dependency-closure behavior, callback identity, private projection, the resource-ownership test for command versus subskill form, nested command generator semantics, and the distinction between protected visibility and security.
- [ ] 7.3 Document managed v3-to-v4 receipt migration, safe stale cleanup, rollback behavior, deprecated selectors, and the required agent-host refresh or new session.
- [ ] 7.4 Update public examples to use `$isomer-op-entrypoint`, `$isomer-ext-deepsci-entrypoint`, or `$isomer-ext-kaoju-entrypoint` with the accepted `use <subcommand> to <task>` form.
- [ ] 7.5 Update every packaged public and protected `agents/openai.yaml` metadata version to exactly match `project.version` without changing the compatibility floor unless policy requires it.
- [ ] 7.6 Run `pixi run validate-skills` and fix all recursive layout, identity, invocation-notation, resource-boundary, route, callback, dependency, and version diagnostics.
- [ ] 7.7 Run targeted unit and integration tests for catalog loading, materialization, installer CLI, receipts, inspection, callbacks, extension queries, and Isomer-Houmao private projection.
- [ ] 7.8 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run python -c "import isomer_labs"`, then record the final validation evidence.
- [ ] 7.9 Run strict OpenSpec validation and confirm the implementation satisfies every public-pack, protected-routing, migration, and compatibility scenario before requesting archive.
