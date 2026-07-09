## 1. Toolbox Manager Guidance

- [x] 1.1 Update `isomer-op-toolbox-mgr/SKILL.md` to state that Toolbox skills default to routed or manual invocation, not implicit auto-invocation.
- [x] 1.2 Update `author-toolbox-source` layout examples to scaffold `agents/openai.yaml` beside Toolbox skill `SKILL.md` files.
- [x] 1.3 Update `author-toolbox`, `convert-skill`, `insert-callback`, and `edit-callback-declarations` guidance to prefer prompt-file routers that name Toolbox skill, subcommand, and purpose.
- [x] 1.4 Update help and output guidance so created or converted callback material reports routed/manual/supplemental invocation posture.

## 2. Existing Toolbox Skills

- [x] 2.1 Add `agents/openai.yaml` with `allow_implicit_invocation: false` to each `gpu-analytic-*-prior` skill.
- [x] 2.2 Ensure each GPU prior skill metadata default prompt says the skill is used when routed by a Toolbox callback prompt or manually invoked.
- [x] 2.3 Check GPU callback prompt files still explicitly name prior skill, subcommand, and purpose.

## 3. Validation

- [x] 3.1 Search active Toolbox Manager and Toolbox assets for wording that implies automatic Toolbox skill invocation by default.
- [x] 3.2 Validate OpenSpec change artifacts.
- [x] 3.3 Run focused asset or metadata checks for Toolbox prior `agents/openai.yaml` files.
