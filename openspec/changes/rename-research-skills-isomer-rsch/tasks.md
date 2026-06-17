## 1. Rename Map and Folder Moves

- [x] 1.1 Build and review the complete rename map from `isomer-labs-research-<purpose>` to `isomer-rsch-<purpose>` for all research-paradigm skill folders.
- [x] 1.2 Rename every active folder under `skillset/research-paradigm/` according to the map.
- [x] 1.3 Confirm no old active skill folders remain under `skillset/research-paradigm/`.

## 2. Skill Metadata and Internal Links

- [x] 2.1 Update every renamed skill's `SKILL.md` frontmatter `name:` to match the new folder name.
- [x] 2.2 Update relative links from stage and companion skills to the shared skill so they point to `../isomer-rsch-shared/SKILL.md`.
- [x] 2.3 Preserve the self-contained `analysis` skill references and manifest after the folder rename.
- [x] 2.4 Update any `agents/openai.yaml` manifest default prompts or skill names that still use `isomer-labs-research-*`.

## 3. Documentation and Role Mapping

- [x] 3.1 Update `skillset/README.md` to document the `isomer-rsch-<purpose>` convention.
- [x] 3.2 Update `skillset/research-paradigm/README.md` with the renamed folder list and shared-skill guidance.
- [x] 3.3 Update `teams/deepsci-org/source/team-design.md` role mappings to list `isomer-rsch-*` skills.
- [x] 3.4 Search active docs and skill files outside `openspec/changes/archive/` for `isomer-labs-research-` and update remaining active references.

## 4. Spec and Validation

- [x] 4.1 Validate each renamed skill folder has `SKILL.md`.
- [x] 4.2 Validate each `SKILL.md` frontmatter `name:` matches its `isomer-rsch-*` folder.
- [x] 4.3 Validate manifests under renamed skills still match the current skill names and prompts.
- [x] 4.4 Run the existing source-runtime coupling scan and confirm remaining matches are provenance, mapping, or explicit rejection notes only.
- [x] 4.5 Run the concrete DeepScientist-style path/API scan and confirm unsettled equivalents remain marked with `[[tbd-surface:<id>]]`.
- [x] 4.6 Run `openspec validate rename-research-skills-isomer-rsch` and confirm the change is valid.
