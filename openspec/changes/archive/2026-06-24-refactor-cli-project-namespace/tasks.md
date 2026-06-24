## 1. Project Command Registration

- [x] 1.1 Add a root-level `project` Click group with group-level `--root`, `--project` compatibility alias, and `--manifest` selectors.
- [x] 1.2 Move Project lifecycle commands `init`, `validate`, `doctor`, and `cleanup` when present under `isomer-cli project`.
- [x] 1.3 Move Project topic/context/path command groups under `isomer-cli project`: `topics`, `workspaces`, `context`, and `paths`.
- [x] 1.4 Move Project runtime command group under `isomer-cli project runtime`.
- [x] 1.5 Move Project team/template/profile/handoff command groups under `isomer-cli project`: `team-instances`, `team-templates`, `team-profiles`, and `handoffs`.
- [x] 1.6 Keep genuinely global commands, including `schemas list`, at the root command surface.
- [x] 1.7 Keep root-level `--print-json` working for nested Project commands such as `isomer-cli --print-json project validate`.

## 2. Discovery and Initialization Semantics

- [x] 2.1 Preserve existing parent-directory Project discovery for `isomer-cli project <subcmd>` when no explicit selector is supplied.
- [x] 2.2 Ensure `isomer-cli project --root <project-root> <subcmd>` and `isomer-cli project --manifest <manifest-path> <subcmd>` override cwd and environment discovery.
- [x] 2.3 Preserve supported environment fallbacks when no explicit selector or cwd-discovered Project applies.
- [x] 2.4 Add a nested-init preflight so `isomer-cli project init` refuses to initialize inside an existing ancestor Project and reports that ancestor.
- [x] 2.5 Preserve fresh initialization behavior, custom `--content-dir`, generated content defaults, and Houmao bootstrap behavior under `isomer-cli project init`.

## 3. Compatibility and Cleanup Coordination

- [x] 3.1 Decide whether legacy root-level Project command forms are removed immediately or retained as hidden compatibility aliases with deprecation guidance.
- [x] 3.2 If aliases are retained, ensure root help does not present them as canonical and new docs do not use them.
- [x] 3.3 Align the active `add-project-cleanup-command` change with this namespace by updating its artifacts or implementing cleanup only as `isomer-cli project cleanup`.
- [x] 3.4 Update CLI output command labels if needed so JSON remains deterministic after command names move under `project`.

## 4. Documentation and Operator Skill

- [x] 4.1 Update `docs/isomer-cli.md` to describe the root/global command surface and the `isomer-cli project` command group.
- [x] 4.2 Update getting-started, workflow, runtime/files, troubleshooting, and Houmao-adapter docs to use canonical `isomer-cli project ...` examples for Project-scoped commands.
- [x] 4.3 Update `skillset/operator/isomer-admin-project-mgr` help, init/check/list/context/runtime/cleanup references, CLI-boundary examples, output contract, and guardrails to use `isomer-cli project ...`.
- [x] 4.4 Update operator skill validation rules and fixtures to require project-namespace command examples and reject root-level Project command examples as canonical guidance.

## 5. Tests

- [x] 5.1 Update CLI help tests so root help lists `project` and global commands, and `isomer-cli project --help` lists Project-scoped commands.
- [x] 5.2 Update CLI invocation tests from root-level Project commands to canonical `project` command forms.
- [x] 5.3 Add tests that `isomer-cli project <subcmd>` discovers an ancestor `.isomer-labs/manifest.toml` from nested cwd.
- [x] 5.4 Add tests for explicit `project --root` and `project --manifest` selector precedence.
- [x] 5.5 Add tests that `project init` refuses nested initialization under an ancestor Project.
- [x] 5.6 Add tests that root-level global `schemas list` remains available without an active Project.
- [x] 5.7 Add compatibility alias tests if legacy root-level Project command forms are retained.
- [x] 5.8 Add or update operator-skill validation tests for canonical `isomer-cli project ...` guidance.

## 6. Validation

- [x] 6.1 Run `openspec validate refactor-cli-project-namespace --strict`.
- [x] 6.2 Run `pixi run python -m unittest tests.unit.test_isomer_cli`.
- [x] 6.3 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 6.4 Run `pixi run validate-operator-skills`.
- [x] 6.5 Run `pixi run lint` and `pixi run test`.
