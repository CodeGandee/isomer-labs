## 1. Project Initialization Layout

- [x] 1.1 Add shared constants or helpers for `isomer-content`, `isomer-content/topic-ws`, content-root README text, and content-root `.gitignore` text.
- [x] 1.2 Update `initialize_project` so new Projects create `isomer-content/`, `isomer-content/README.md`, `isomer-content/.gitignore`, and `isomer-content/topic-ws/<topic-id>/`.
- [x] 1.3 Update generated Project Manifest text to include `[paths]` defaults for `isomer_content_root = "isomer-content"` and `topic_workspace_base_dir = "isomer-content/topic-ws"`.
- [x] 1.4 Update init command text and JSON payloads when needed so initialization reports the new Topic Workspace path and content root without claiming runtime creation.
- [x] 1.5 Ensure Houmao bootstrap failure and existing-manifest refusal do not leave new `isomer-content/` material behind.

## 2. Path Resolution and Validation

- [x] 2.1 Update Workspace Path Resolution built-in defaults so the generated content root resolves to `<project>/isomer-content/`.
- [x] 2.2 Update default Topic Workspace base and derived Topic Workspace paths to use `<project>/isomer-content/topic-ws/<topic-id>/` when no explicit registration or manifest path default overrides them.
- [x] 2.3 Add support for the `isomer_content_root` Project Manifest path default while preserving existing `topic_workspace_base_dir` behavior and aliases.
- [x] 2.4 Update `project paths preview` to include the generated content root surface and keep preview side-effect free.
- [x] 2.5 Add validation for `isomer_content_root` and `topic_workspace_base_dir` so they resolve inside the Project root, and reject `isomer_content_root` inside `.isomer-labs/`.
- [x] 2.6 Confirm explicit existing Topic Workspace registrations such as `topic-workspaces/<topic-id>` still validate and are not rewritten.

## 3. Operator Skills and Documentation

- [x] 3.1 Update `skillset/operator/isomer-admin-project-mgr` references so init-project, concepts, help, and output guidance name `isomer-content/` and `isomer-content/topic-ws/<topic-id>/`.
- [x] 3.2 Update `skillset/operator/isomer-admin-topic-team-specialize/references/init-topic.md` so clear topics without explicit output directories derive a provisional seed under the effective Topic Workspace base.
- [x] 3.3 Update topic-team specialization workflow or help text where it still says missing output directory must always prompt the user.
- [x] 3.4 Update repository docs and examples that describe default Topic Workspace paths, Project init output, path preview output, runtime files, and content-root Git policy.
- [x] 3.5 Update any local skill validation rules or fixture text that hard-code `topic-workspaces/<topic-id>` as the default created by init.

## 4. Tests and Fixtures

- [x] 4.1 Update CLI init tests to assert `isomer-content/README.md`, `isomer-content/.gitignore`, and `isomer-content/topic-ws/<topic-id>/`.
- [x] 4.2 Add or update tests for the generated `.gitignore` policy so only `README.md` and `.gitignore` are unignored by default.
- [x] 4.3 Update path preview and Workspace Path Resolution tests for the generated content root and new default Topic Workspace base.
- [x] 4.4 Add validation tests for bad `isomer_content_root` values outside the Project root or inside `.isomer-labs/`.
- [x] 4.5 Update fixture manifests, docs tests, and operator-skill tests affected by the default layout change.

## 5. Validation

- [x] 5.1 Run `openspec validate add-isomer-content-default-layout --strict`.
- [x] 5.2 Run `pixi run python -m unittest tests.unit.test_isomer_cli`.
- [x] 5.3 Run `pixi run python -m unittest tests.unit.test_validate_skillsets`.
- [x] 5.4 Run `pixi run validate-operator-skills`.
- [x] 5.5 Run `pixi run lint` and `pixi run test`.
