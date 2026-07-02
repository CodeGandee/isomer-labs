## Why

Most skills under `skillset/*` are installed into agents that run outside this repository, so examples such as `pixi run isomer-cli ...` are wrong for those users. Non-dev skills must assume `isomer-cli` is installed as a global `uv` tool and call it directly, while `skillset/dev` may keep repo-local Pixi commands for repository maintenance.

## What Changes

- Replace `pixi run isomer-cli ...` command guidance in non-dev skills with direct `isomer-cli ...` command guidance.
- Keep `skillset/dev/**` exempt because developer skills operate inside this repository and may use Pixi for repo-local validation or migration work.
- Update operator/service/research skill docs, including v2 `placeholder-bindings.md`, so CRUD examples use global `isomer-cli`.
- Update skill validators and tests to reject `pixi run isomer-cli` under non-dev skill paths and to preserve direct `isomer-cli` command shapes.
- Keep repository docs, scripts, tests, and OpenSpec artifacts free to mention Pixi when they describe repo-local development; the user-facing skill contract is the scoped target.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `operator-admin-skills`: Operator skills outside `skillset/dev` must use direct `isomer-cli` command examples and validation must reject `pixi run isomer-cli` in active operator skills.
- `isomer-admin-project-manager-skill`: Project Manager command guidance must present `isomer-cli project ...` directly because the skill is installed into external operator agents.
- `research-placeholder-bindings`: Placeholder binding CRUD command rows must use direct `isomer-cli ext research records ...` commands.
- `research-paradigm-skills`: Research v2 skills and their binding docs must call global `isomer-cli` directly for extension, record, and bootstrap operations.
- `isomer-service-env-setup-skill`: Service skills outside `skillset/dev` must use direct `isomer-cli` examples when they describe Project or Topic Workspace operations.

## Impact

- Affected skill files: `skillset/operator/**`, `skillset/service/**`, `skillset/research-paradigm/**`, and any other non-dev skill paths that mention `pixi run isomer-cli`.
- Excluded skill files: `skillset/dev/**`.
- Affected validators and tests: skillset validation should gain a non-dev forbidden-command check and unit coverage.
- No runtime Python API change is expected; this is a skill documentation and validation contract change.
