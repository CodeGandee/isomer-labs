## 1. Skill Bundle

- [x] 1.1 Create `src/isomer_labs/assets/system_skills/operator/isomer-op-switch-identity/SKILL.md` with valid frontmatter, `Use when...` description, overview, when-to-use guidance, concise numbered workflow, freeform fallback, output contract, and common mistakes.
- [x] 1.2 Create `agents/openai.yaml` for `isomer-op-switch-identity` with matching display name, short description, default prompt, and manual invocation policy consistent with operator skills.
- [x] 1.3 Add command detail pages under `commands/` for `switch`, `act-as`, `status`, `reset`, and `help`.
- [x] 1.4 Ensure the skill creates no empty `references/`, `assets/`, or `scripts/` directories.

## 2. Switch Identity Behavior

- [x] 2.1 Document target parsing for Topic Actor and Agent switches, including blockers for ambiguous target kind or name.
- [x] 2.2 Document semantic path resolution commands for `topic.actors.workspace` and `agent.workspace`.
- [x] 2.3 Document one-task switch behavior and persistent session switch behavior.
- [x] 2.4 Document `act-as` behavior that executes one following prompt under the target identity and then restores the previous identity posture.
- [x] 2.5 Document that switched shell commands default to the resolved actor or agent workspace cwd.
- [x] 2.6 Document reset behavior that clears persistent switched identity posture.
- [x] 2.7 Document provenance guardrails that prevent fabricated Topic Actor process, Agent Instance, Houmao launch, or Execution Adapter claims.

## 3. Inventory and Documentation

- [x] 3.1 Add `operator/isomer-op-switch-identity` to `src/isomer_labs/assets/system_skills/manifest.toml`.
- [x] 3.2 Update operator skillset documentation or welcome skill-map guidance to list `isomer-op-switch-identity`.
- [x] 3.3 Confirm the `skillset/operator` symlink exposes the new packaged skill path.

## 4. Validation and Tests

- [x] 4.1 Update `scripts/validate_skillsets.py` to require and validate `isomer-op-switch-identity`.
- [x] 4.2 Add unit tests that accept a valid switch-identity skill fixture.
- [x] 4.3 Add unit tests that reject missing command pages, missing `act-as` one-prompt restore guidance, missing persistent-switch guidance, missing cwd discipline, directory-scanning target resolution, and fabricated Agent Instance or Houmao execution claims.
- [x] 4.4 Run `python scripts/validate_skillsets.py --scope operator`.

## 5. Verification

- [x] 5.1 Run `pixi run lint`.
- [x] 5.2 Run `pixi run typecheck`.
- [x] 5.3 Run `pixi run test`.
- [x] 5.4 Run `openspec validate add-operator-switch-identity-skill --strict`.
