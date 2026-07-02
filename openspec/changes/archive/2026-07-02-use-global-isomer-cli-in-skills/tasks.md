## 1. Update Non-Dev Skill Command Guidance

- [x] 1.1 Scan `skillset/**` excluding `skillset/dev/**` for `pixi run isomer-cli` command guidance.
- [x] 1.2 Replace exact `pixi run isomer-cli` prefixes with `isomer-cli` in non-dev operator, service, misc, and research-paradigm skill files.
- [x] 1.3 Preserve legitimate Pixi commands that describe Topic Workspace or research environment setup and do not invoke Isomer's own CLI.
- [x] 1.4 Confirm `skillset/dev/**` is unchanged by the replacement.

## 2. Update Validation and Tests

- [x] 2.1 Add skillset validation that rejects `pixi run isomer-cli` under non-dev skill paths.
- [x] 2.2 Add or update unit tests for the forbidden non-dev pattern and the `skillset/dev/**` exemption.
- [x] 2.3 Update existing test fixtures or expected command strings from `pixi run isomer-cli` to direct `isomer-cli` where the fixture represents non-dev skills.

## 3. Verify

- [x] 3.1 Run `pixi run validate-operator-skills`.
- [x] 3.2 Run the relevant skillset validator unit tests.
- [x] 3.3 Run `openspec validate use-global-isomer-cli-in-skills --strict`.
