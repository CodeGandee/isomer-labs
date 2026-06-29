## 1. Dependency Manifest

- [x] 1.1 Create `skillset/operator/isomer-admin-topic-team-specialize/references/step-dependencies.json`.
- [x] 1.2 Record every public procedural subcommand with step id, display name, kind, required predecessor artifacts or inputs, produced artifacts or outputs, mutation notes, recovery conditions, and unrecoverable blockers.
- [x] 1.3 Record canonical predecessor edges and conditional edges needed for full `fast-forward`, inclusive targeted recovery, and exclusive targeted recovery.
- [x] 1.4 Keep the manifest at the domain level; do not encode file-existence checks, fixed workspace paths, Project Manifest mutation logic, or service implementation details.

## 2. Query Script

- [x] 2.1 Add `skillset/operator/isomer-admin-topic-team-specialize/scripts/query_step_dependencies.py` using only the Python standard library.
- [x] 2.2 Implement `validate` to check required fields, unknown step ids, invalid edges, malformed manifest data, and dependency cycles.
- [x] 2.3 Implement `path --target <subcommand> --include-target` and `path --target <subcommand> --exclude-target`.
- [x] 2.4 Implement `prereqs`, `produces`, `blockers`, and `explain` queries.
- [x] 2.5 Support human-readable output for agent use and `--json` output for validation and future tooling.

## 3. Skill Documentation

- [x] 3.1 Update `SKILL.md` so Targeted Fast-Forward Recovery tells agents to query `scripts/query_step_dependencies.py` for dependency paths.
- [x] 3.2 Update `references/fast-forward.md` so full and targeted fast-forward path computation comes from the query script.
- [x] 3.3 Update procedural subcommand pages to remove repeated long recovery chains and refer to the query script for inclusive and exclusive recovery paths.
- [x] 3.4 Preserve local prose for each subcommand's purpose, local evidence requirements, produced outputs, safety blockers, and information the agent must not invent.
- [x] 3.5 Update `references/help.md` to mention the centralized dependency contract and query helper.

## 4. Validation

- [x] 4.1 Update `scripts/validate_skillsets.py` to verify the manifest and query script exist for `isomer-admin-topic-team-specialize`.
- [x] 4.2 Update `scripts/validate_skillsets.py` to run the query script's `validate` command or equivalent structural checks.
- [x] 4.3 Update `scripts/validate_skillsets.py` to verify the manifest covers all procedural subcommands and that key docs route dependency-path questions through the query script.
- [x] 4.4 Update `tests/unit/test_validate_skillsets.py` for the centralized dependency contract and stale duplicated-path failure cases.

## 5. Verification

- [x] 5.1 Run `openspec validate centralize-topic-team-step-dependencies --strict`.
- [x] 5.2 Run `pixi run python scripts/validate_skillsets.py --scope operator`.
- [x] 5.3 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 5.4 Run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize`.
- [x] 5.5 Run `pixi run python scripts/validate_docs.py`.
