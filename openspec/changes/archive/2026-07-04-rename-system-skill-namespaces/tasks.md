## 1. Inventory and Scope

- [x] 1.1 Record the active skill inventory from `src/isomer_labs/assets/system_skills/manifest.toml` and confirm the expected operator, misc, service, and DeepSci entries before moving folders.
- [x] 1.2 Classify active runtime guidance paths versus passive historical paths, including `org/`, `migrate/`, archived OpenSpec changes, and provenance notes.
- [x] 1.3 Run focused searches for `isomer-admin-`, `isomer-rsch-`, `isomer-srv-`, and `isomer-misc-` across active assets, validators, tests, docs, and active specs to establish the rename worklist.

## 2. Rename Packaged Skill Folders

- [x] 2.1 Move active operator folders under `src/isomer_labs/assets/system_skills/operator/` from `isomer-admin-*` to the matching `isomer-op-*` names.
- [x] 2.2 Move active production DeepSci folders under `src/isomer_labs/assets/system_skills/research-paradigm/deepsci/` from `isomer-rsch-*` to the matching `isomer-deepsci-*` names.
- [x] 2.3 Confirm `isomer-misc-*` folders under `misc/` and `isomer-srv-*` folders under `service/` remain stable.
- [x] 2.4 Verify the repository-root `skillset/` authoring view still resolves to the packaged asset subtrees after the folder moves.

## 3. Rewrite Active Skill Identities

- [x] 3.1 Update every renamed operator `SKILL.md` frontmatter `name`, direct invocation text, cross-skill route, and local README reference to use `isomer-op-*`.
- [x] 3.2 Update every renamed DeepSci `SKILL.md` frontmatter `name`, shared-skill route, local README reference, and research workflow handoff to use `isomer-deepsci-*`.
- [x] 3.3 Update every affected `agents/openai.yaml` `interface.display_name` and `interface.default_prompt` to invoke the renamed skill.
- [x] 3.4 Update active placeholder binding pages so `--skill`, producer, consumer, and workspace-manager references use `isomer-deepsci-*`.
- [x] 3.5 Update active service guidance so user-facing package mutation, verification, and topic-management routes use `isomer-op-topic-mgr` while service skill names remain `isomer-srv-*`.
- [x] 3.6 Preserve old names only in passive provenance, source-copy, migration, or archived-change contexts.

## 4. Update Manifest, Docs, and Specs

- [x] 4.1 Update `src/isomer_labs/assets/system_skills/manifest.toml` so manifest-listed paths use `isomer-op-*`, stable `isomer-misc-*`, stable `isomer-srv-*`, and `isomer-deepsci-*`.
- [x] 4.2 Update packaged system-skill README files to describe the final active inventory and the `isomer-<extension-name>-<purpose>` convention.
- [x] 4.3 Update active OpenSpec specs under `openspec/specs/` to reflect the renamed operator and DeepSci skill contracts.
- [x] 4.4 Update active design notes and context docs that describe current skill call graphs, leaving archived changes and passive historical notes unchanged unless they are presented as current guidance.

## 5. Update Validators and Tests

- [x] 5.1 Update `scripts/validate_skillsets.py` expected operator skill constants, manifest checks, stale-name diagnostics, and fixture expectations for `isomer-op-*`.
- [x] 5.2 Update `scripts/validate_research_paradigm_skillset.py` expected DeepSci inventory, shared-skill registry paths, placeholder binding checks, and stale-name diagnostics for `isomer-deepsci-*`.
- [x] 5.3 Update unit tests that read skill paths or assert skill names, including manual research topic skill tests, system skill asset tests, DeepSci extension tests, and validator tests.
- [x] 5.4 Add or update tests that fail active `isomer-admin-*` and `isomer-rsch-*` invocations outside explicitly passive or historical paths.

## 6. Validate and Close

- [x] 6.1 Run focused stale-name searches and confirm active runtime guidance has no old `isomer-admin-*` or `isomer-rsch-*` invocations.
- [x] 6.2 Run `pixi run validate-skills` and `pixi run validate-research-skills`.
- [x] 6.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 6.4 Run `openspec status --change rename-system-skill-namespaces` and confirm the change is apply-ready or complete according to the workflow stage.
