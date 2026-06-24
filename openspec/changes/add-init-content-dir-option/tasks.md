## 1. CLI and Initialization Plumbing

- [x] 1.1 Add a `--content-dir` option to the `isomer-cli project init` command registration and carry it through CLI options into `_cmd_init`.
- [x] 1.2 Update `initialize_project` to accept an optional content directory input while preserving the existing omitted-option default of `isomer-content/`.
- [x] 1.3 Add shared helper logic to resolve the selected content root, derive `<content-dir>/topic-ws`, and render project-relative manifest path defaults when possible.
- [x] 1.4 Update generated Project Manifest text so custom initialization writes `isomer_content_root = "<content-dir>"` and `topic_workspace_base_dir = "<content-dir>/topic-ws"`.
- [x] 1.5 Update initialization text and JSON output so custom content root and derived Topic Workspace paths are reported deterministically.

## 2. Safety and Failure Behavior

- [x] 2.1 Validate `--content-dir` before filesystem mutation, rejecting values outside the Project root.
- [x] 2.2 Reject content roots inside `.isomer-labs/`, equal to `.isomer-labs/`, equal to `.houmao/`, or producing a derived Topic Workspace base inside Project bootstrap/config directories.
- [x] 2.3 Ensure existing-manifest refusal does not create or modify the selected content root.
- [x] 2.4 Ensure Houmao bootstrap failure does not leave the selected content root, content-root policy files, or derived Topic Workspace directory behind.
- [x] 2.5 Preserve explicit legacy Project Manifest paths and existing path-default validation behavior outside fresh initialization.

## 3. Documentation and Operator Skills

- [x] 3.1 Update `skillset/operator/isomer-admin-project-mgr` `init-project`, help, CLI-boundary, concept, and guardrail references to describe `--content-dir <content-dir>`.
- [x] 3.2 Update local operator skill validation rules and fixtures if they assert fresh init command shapes or required generated-content terms.
- [x] 3.3 Update user docs that describe `isomer-cli project init`, generated content roots, Topic Workspace defaults, path previews, and workflow examples.
- [x] 3.4 Update service or support skill examples that describe Topic Workspace Pixi manifest paths if they need to mention custom content roots.

## 4. Tests

- [x] 4.1 Add CLI init tests for `--content-dir custom-content` with default and explicit Research Topic ids.
- [x] 4.2 Add tests asserting custom init creates `<content-dir>/README.md`, `<content-dir>/.gitignore`, and `<content-dir>/topic-ws/<topic-id>/`.
- [x] 4.3 Add tests asserting generated manifest `[paths]` values match the selected content root and derived Topic Workspace base.
- [x] 4.4 Add tests for invalid `--content-dir` values outside the Project root, inside `.isomer-labs/`, and colliding with `.houmao/`.
- [x] 4.5 Add tests asserting existing-manifest refusal and Houmao bootstrap failure leave no custom content-root material behind.
- [x] 4.6 Add or update operator-skill validation tests for project-manager custom content directory guidance.

## 5. Validation

- [x] 5.1 Run `openspec validate add-init-content-dir-option --strict`.
- [x] 5.2 Run `pixi run python -m unittest tests.unit.test_isomer_cli`.
- [x] 5.3 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 5.4 Run `pixi run validate-operator-skills`.
- [x] 5.5 Run `pixi run lint` and `pixi run test`.
