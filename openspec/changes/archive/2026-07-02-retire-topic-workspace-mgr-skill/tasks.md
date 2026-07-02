## 1. Remove Retired Skill Surface

- [x] 1.1 Delete `skillset/operator/isomer-admin-topic-workspace-mgr/`, including `SKILL.md`, `agents/openai.yaml`, and any remaining references.
- [x] 1.2 Remove `operator/isomer-admin-topic-workspace-mgr` from `skillset/manifest.toml`.
- [x] 1.3 Update `skillset/operator/README.md` so it names `isomer-admin-topic-mgr` as the only initialized-topic manager and no longer describes an old-skill compatibility wrapper.

## 2. Replace Validation and Tests

- [x] 2.1 Remove `TOPIC_WORKSPACE_MANAGER_SKILL`, `TOPIC_WORKSPACE_MANAGER_WRAPPER_REQUIRED_TERMS`, `validate_topic_workspace_manager_wrapper`, and the wrapper validation call from `scripts/validate_skillsets.py`.
- [x] 2.2 Add `isomer-admin-topic-workspace-mgr` to removed-skill validation so operator validation fails if the old folder is present.
- [x] 2.3 Replace wrapper fixture helpers and wrapper-acceptance tests in `tests/unit/test_validate_skillsets.py` with tests that reject a revived `isomer-admin-topic-workspace-mgr` folder and ensure valid fixtures use only `isomer-admin-topic-mgr`.
- [x] 2.4 Ensure `pixi run validate-operator-skills` still validates the full `isomer-admin-topic-mgr` command set after wrapper removal.

## 3. Routing and Stale Reference Sweep

- [x] 3.1 Search active implementation, docs, skill, test, script, and main spec roots for `$isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-workspace-mgr`, and user-facing `Topic Workspace Manager` routing.
- [x] 3.2 Replace active routing references with `isomer-admin-topic-mgr` and scoped commands such as `actors-manage`, `actors-materialize`, `team-validate-workspaces`, or `env-install-packages`.
- [x] 3.3 Classify remaining references in archived OpenSpec material or historical rationale as historical, and do not present them as active routes.
- [x] 3.4 If `rename-topic-workspace-mgr-to-topic-mgr` is still unarchived, verify this implementation preserves its new `skillset/operator/isomer-admin-topic-mgr/` bundle and does not undo any pending rename work.

## 4. OpenSpec and Verification

- [x] 4.1 Run `openspec validate retire-topic-workspace-mgr-skill --strict`.
- [x] 4.2 Run `openspec validate rename-topic-workspace-mgr-to-topic-mgr --strict` if that change remains active.
- [x] 4.3 Run `pixi run validate-operator-skills`.
- [x] 4.4 Run `pixi run lint`.
- [x] 4.5 Run `pixi run test`.
- [x] 4.6 Report changed paths, validation results, remaining historical references, and any blockers.
