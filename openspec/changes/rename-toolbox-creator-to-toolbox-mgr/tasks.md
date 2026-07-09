## 1. Packaged Skill Rename

- [x] 1.1 Rename `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-creator/` to `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr/`.
- [x] 1.2 Update the renamed skill's `SKILL.md` frontmatter, title, default help references, and user-facing wording from Toolbox Creator to Toolbox Manager where the broader owner is meant.
- [x] 1.3 Update `agents/openai.yaml` display name and default prompt to use `isomer-op-toolbox-mgr`.
- [x] 1.4 Update command pages so help output and examples use `isomer-op-toolbox-mgr` while preserving all existing command names.

## 2. Packaging and Documentation

- [x] 2.1 Replace `operator/isomer-op-toolbox-creator` with `operator/isomer-op-toolbox-mgr` in `src/isomer_labs/assets/system_skills/manifest.toml`.
- [x] 2.2 Update `src/isomer_labs/assets/system_skills/operator/README.md` to list and describe `isomer-op-toolbox-mgr`.
- [x] 2.3 Update pending `create-toolbox-creator-system-skill` artifacts and active feature design references that describe the active skill name, or mark the old name as superseded where historical context must remain.

## 3. Tests and Validation

- [x] 3.1 Update package asset tests to assert the manager path, frontmatter identity, command pages, and absence of the creator path in core discovery and materialization.
- [x] 3.2 Run the skill quick validator against `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr`.
- [x] 3.3 Run focused package asset tests for system-skill packaging.
- [x] 3.4 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, noting any unrelated dirty-tree failure separately.
  - Note: `pixi run lint` and `pixi run typecheck` passed. `pixi run test` ran and failed on unrelated dirty `web/read_model.py:933` file-size architecture check.
- [x] 3.5 Run `openspec validate rename-toolbox-creator-to-toolbox-mgr --strict`.
