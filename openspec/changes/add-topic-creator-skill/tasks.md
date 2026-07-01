## 1. Create Topic Creator Skill Bundle

- [x] 1.1 Create `skillset/operator/isomer-admin-topic-creator/` with `SKILL.md`, `agents/openai.yaml`, and a command-style workflow that defaults to `help`.
- [x] 1.2 Add `references/help.md` with what the skill does, required inputs, command functionalities, output contract, and guardrails.
- [x] 1.3 Add executable reference pages for `plan`, `create`, `ensure-project`, `define-topic`, `register-topic`, `init-runtime`, `setup-topic-env`, `setup-actors`, `bootstrap-research`, `start-manual-research`, `status`, and `repair`.
- [x] 1.4 Make `create` run the ordered initialization ladder and make `plan`, `status`, and `repair` explicitly idempotent and resumable.

## 2. Migrate User-Facing Topic Initialization Guidance

- [x] 2.1 Move the user-facing blank-state topic creation guidance from `isomer-admin-project-mgr`, `isomer-admin-topic-prepare`, and `isomer-admin-manual-research-session` into the new creator references.
- [x] 2.2 Preserve lower-level delegation to `isomer-admin-project-mgr`, `isomer-srv-topic-env-setup`, `isomer-admin-topic-workspace-mgr`, `isomer-rsch-workspace-mgr-v2`, and `isomer-admin-manual-research-session`.
- [x] 2.3 Define the manual-research-ready output contract with Project refs, Topic refs, `topic.repos.main`, Workspace Runtime, Topic Actor roster, actor cwd paths, bootstrap status, start-pack refs, blockers, and next action.

## 3. Mark Compatibility Skills Deprecated

- [x] 3.1 Add YAML frontmatter deprecation metadata to `isomer-admin-topic-prepare`, with `deprecated: true`, `replaced_by: isomer-admin-topic-creator`, direct-user-invocation scope, and a compatibility warning.
- [x] 3.2 Add YAML frontmatter deprecation metadata to `isomer-admin-manual-research-session`, with `deprecated: true`, `replaced_by: isomer-admin-topic-creator`, direct-user-invocation scope, and a compatibility warning.
- [x] 3.3 Update compatibility skill descriptions and help pages so direct users are guided to `isomer-admin-topic-creator` while delegated compatibility usage remains valid.

## 4. Update Operator Routing and Documentation

- [x] 4.1 Update `isomer-admin-project-mgr` routing, help, and subcommand guidance so blank-state topic creation and manual-research setup hand off to `isomer-admin-topic-creator`.
- [x] 4.2 Update `skillset/operator/README.md` to list `isomer-admin-topic-creator` as the topic initialization front door and describe deprecated compatibility skills.
- [x] 4.3 Update `skillset/manifest.toml` and `.kimi-code/skills/` symlink installation expectations so the new skill is included in the operator/core group.

## 5. Update Validation and Tests

- [x] 5.1 Update `scripts/validate_skillsets.py` so operator validation covers `isomer-admin-topic-creator` and accepts required deprecation metadata on compatibility skills.
- [x] 5.2 Update or add unit tests for topic creator command inventory, default help behavior, manual-research-ready contract terms, deprecation metadata, and Project Manager routing.
- [x] 5.3 Run `pixi run validate-operator-skills` and the relevant unit tests.
- [x] 5.4 Run `openspec validate add-topic-creator-skill --strict`.
