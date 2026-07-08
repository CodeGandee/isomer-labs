## 1. Project Settings Openable Model

- [x] 1.1 Add a `Settings` project explorer node with `openable_item_id` set to `project:settings`.
- [x] 1.2 Add a project settings openable descriptor that resolves to a `Project Settings` tab and `settings` component.

## 2. Workbench Settings UI

- [x] 2.1 Add a `settings` Dockview component and `ProjectSettingsPanel`.
- [x] 2.2 Add an Appearance section with a `Global Theme` selector for `system`, `light`, and `dark` using the existing theme provider.
- [x] 2.3 Add a topbar settings button that opens `project:settings`.
- [x] 2.4 Allow the Dockview host to render when project-level settings are opened without a selected topic.

## 3. Tests and Validation

- [x] 3.1 Add backend or frontend tests for the settings openable descriptor and explorer item.
- [x] 3.2 Add frontend tests for the theme selector behavior.
- [x] 3.3 Run targeted GUI tests and project validation for the changed areas.
