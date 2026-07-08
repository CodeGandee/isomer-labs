## 1. Command Semantics and Service Boundaries

- [x] 1.1 Audit current `project toolboxes`, `project skill-callbacks`, and `project toolbox-params` handlers and identify shared service functions needed by high-level Toolbox installation.
- [x] 1.2 Decide and document the runtime-param default import policy for `project toolboxes install`, including whether defaults require an explicit option or are installed by default.
- [x] 1.3 Decide and document Topic Actor and Topic Agent Toolbox install behavior when the Toolbox declares callbacks but callback records only support Project and Research Topic scope.
- [x] 1.4 Refactor Toolbox manifest loading and validation so high-level install can reuse callback manifest validation, runtime-param bundle validation, source-path checks, and insertion-point validation without duplicating logic.

## 2. High-Level Toolbox Install

- [x] 2.1 Extend `project toolboxes install` so Project-scope installation validates the Toolbox manifest, upserts the Project Manifest `[[toolboxes]]` row, installs declared callback records at Project scope, applies the selected runtime-param default import policy, and reports effective status.
- [x] 2.2 Extend `project toolboxes install` so Research Topic installation validates the Toolbox manifest, upserts the Topic Workspace Manifest `[[toolboxes]]` row, installs declared callback records at Research Topic scope, applies the selected runtime-param default import policy, and reports effective status.
- [x] 2.3 Ensure high-level install preserves runtime params, runtime-param imports, callback records for other Toolboxes, and Toolbox registrations for other scopes.
- [x] 2.4 Add structured output fields for installed callback ids, Toolbox registration scope/status, runtime-param import status, skipped declarations, gated callbacks, unavailable insertion points, and diagnostics.

## 3. Lower-Level Primitive Commands

- [x] 3.1 Preserve `project skill-callbacks register` as the direct path for loose prompt, prompt-file, or skill-directory callback material that is not packaged as a Toolbox manifest.
- [x] 3.2 Preserve `project skill-callbacks install` as a lower-level callback-manifest refresh or repair primitive and ensure it does not install runtime-param default imports.
- [x] 3.3 Preserve `project toolbox-params` define, set, unset, import, get, list, explain, and validate behavior as direct runtime-param configuration primitives.
- [x] 3.4 Update CLI help text so `project toolboxes install` is described as the canonical Toolbox bundle install path and lower-level commands are described as primitives rather than a competing Toolbox install workflow.

## 4. Tests

- [x] 4.1 Add CLI tests showing `project toolboxes install` installs Toolbox registration and declared callback records at Project scope.
- [x] 4.2 Add CLI tests showing `project toolboxes install` installs Toolbox registration and declared callback records at Research Topic scope.
- [x] 4.3 Add tests for runtime-param default import policy during high-level Toolbox install, including skipped or explicit-default behavior.
- [x] 4.4 Add tests proving lower-level `skill-callbacks install` still refreshes callback records and preserves runtime-param rows/imports.
- [x] 4.5 Add tests for same `toolbox_id` from a different source, replacement diagnostics, gated Toolbox status, unavailable insertion points, and Topic Actor or Topic Agent scope behavior.

## 5. Documentation and Use Cases

- [x] 5.1 Update CLI reference docs to present `project toolboxes install` as the canonical directory install command.
- [x] 5.2 Update callback docs to describe `project skill-callbacks register` and `project skill-callbacks install` as lower-level callback primitives.
- [x] 5.3 Update runtime-param docs to describe `project toolbox-params` as direct configuration primitives that can be used with or without high-level Toolbox installation.
- [x] 5.4 Update Toolbox Creator Skill use cases so directory installation maps to high-level Toolbox install and loose callback/runtime-param work maps to primitives.

## 6. Validation

- [x] 6.1 Run `openspec validate unify-toolbox-install-cli --strict` and fix artifact or spec issues.
- [x] 6.2 Run `pixi run test` or the focused affected unit tests for CLI, Toolbox callbacks, and runtime params.
- [x] 6.3 Run `pixi run lint` and `pixi run typecheck` if implementation touches command handlers, project services, or models.
