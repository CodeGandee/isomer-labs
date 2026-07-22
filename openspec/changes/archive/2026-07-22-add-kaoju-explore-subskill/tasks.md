## 1. Contract and manifest updates

- [x] 1.1 Add `isomer-kaoju-explore` to `protected_members` and `skills` in `src/isomer_labs/kaoju/resources/survey-process.v2.json`
- [x] 1.2 Add `exploration_procedures: ["explore"]` to `src/isomer_labs/kaoju/resources/survey-process.v2.json`
- [x] 1.3 Add `exploration_procedures` field to `KaojuContract` in `src/isomer_labs/kaoju/contracts.py` and load it from the JSON resource
- [x] 1.4 Update hardcoded counts in `src/isomer_labs/kaoju/contracts.py`: 13 protected members → 14, 14 skills → 15, and add `exploration_procedures` with one entry while keeping survey intents at 10
- [x] 1.5 Add `isomer-kaoju-explore` to the kaoju `protected_members` list in `src/isomer_labs/assets/system_skills/manifest.toml`
- [x] 1.6 Add a `capabilities` entry for `isomer-kaoju-explore` in `src/isomer_labs/assets/system_skills/manifest.toml`
- [x] 1.7 Add `explore` to the `public_commands` of `isomer-ext-kaoju-entrypoint` in `src/isomer_labs/assets/system_skills/manifest.toml`

## 2. Entrypoint command surface

- [x] 2.1 Add `explore` to the protected subskills table in `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/SKILL.md`
- [x] 2.2 Add an `## Exploration Procedures` section to `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/SKILL.md`
- [x] 2.3 Create `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/commands/explore.md` as a thin orchestration page
- [x] 2.4 Add the `explore` row to `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-welcome/references/show-command-map.md`

## 3. Explore subskill

- [x] 3.1 Create `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/isomer-kaoju-explore/agents/openai.yaml` with version `0.4.0`
- [x] 3.2 Create `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/isomer-ext-kaoju-entrypoint/subskills/isomer-kaoju-explore/SKILL-MAIN.md` with overview, workflow, subcommand routing, output contract, and guardrails
- [x] 3.3 Create the default `auto` subcommand page under `subskills/isomer-kaoju-explore/commands/auto.md`
- [x] 3.4 Create the `help` subcommand page under `subskills/isomer-kaoju-explore/commands/help.md`
- [x] 3.5 Create placeholder subcommand pages for `directions`, `reading-list`, `intake`, `comparison`, `trial`, `paper`, and `wiki`
- [x] 3.6 Ensure no `artifact-bindings.md` is created in the explore subskill

## 4. Tests

- [x] 4.1 Update `tests/unit/test_kaoju_contracts.py`: protected count 13 → 14, skills count 14 → 15
- [x] 4.2 Update `tests/unit/test_system_skill_assets.py`: kaoju capabilities 13 → 14, total capabilities 53 → 54, total protected 53 → 54, kaoju subskill directories 13 → 14, kaoju protected members length 13 → 14
- [x] 4.3 Update `tests/unit/test_system_skill_assets.py` expected public commands to include `explore` from `exploration_procedures`
- [x] 4.4 Update `tests/unit/test_kaoju_skill_assets.py` COMMANDS set and section assertions for the new `## Exploration Procedures` section
- [x] 4.5 Run `pixi run test tests/unit/test_kaoju_contracts.py tests/unit/test_kaoju_skill_assets.py tests/unit/test_system_skill_assets.py` and fix failures

## 5. Validation

- [x] 5.1 Run `pixi run lint` and resolve any issues
- [x] 5.2 Run `pixi run typecheck` and resolve any issues
- [x] 5.3 Run the full unit test suite with `pixi run test`
