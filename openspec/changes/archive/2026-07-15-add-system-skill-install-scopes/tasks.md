## 1. Target and Scope Resolution

- [x] 1.1 Add typed `user` and `project` scope values plus target-scope binding and physical-destination models to the system-skill installer.
- [x] 1.2 Replace the `home` resolver input with required scope resolution for every target using the design matrix and current-working-directory semantics.
- [x] 1.3 Honor `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, and `KIMI_CODE_HOME` for their specified user roots, including empty-value fallbacks and user expansion.
- [x] 1.4 Expand `all` into concrete bindings, group normalized identical skill roots, and preserve deterministic target and root ordering.
- [x] 1.5 Add resolver unit tests for every target-scope pair, environment override, nested current working directory, and shared-root deduplication.

## 2. Scope-Aware Receipts and Results

- [x] 2.1 Introduce `isomer-labs-skill-manifest.v3` with sorted target-scope bindings while retaining safe v1 and v2 parsing as legacy evidence.
- [x] 2.2 Update receipt writes to merge compatible bindings for an existing physical root and migrate legacy receipts only during an authorized mutation.
- [x] 2.3 Update install, status, upgrade, and uninstall result models to expose scope, resolved root, and all bindings without duplicating physical-root operations.
- [x] 2.4 Add receipt tests for v3 round trips, multi-binding roots, later binding merges, legacy scope remaining unknown during status, and mutation-driven v2 migration.
- [x] 2.5 Verify install and upgrade still preserve untracked paths and projection modes when binding metadata changes.

## 3. CLI Contract

- [x] 3.1 Remove `--home` and add required `--scope user|project` to `system-skills install`, `status`, `upgrade`, and `uninstall`.
- [x] 3.2 Pass grouped physical destinations through each command and update JSON and human renderers to identify scope and target bindings.
- [x] 3.3 Update extension discovery install and status command templates to include explicit target and scope placeholders.
- [x] 3.4 Add CLI tests for missing scope, rejected `--home`, user and project resolution, `all` root deduplication, and scope-aware human and JSON output.
- [x] 3.5 Update existing system-skill command tests and fixtures so every target-resolving invocation supplies an explicit scope.

## 4. Operator System-Skill Management

- [x] 4.1 Revise `isomer-op-system-skill-mgr` workflow and installation references to call the scoped installer without `--home` or guessed paths.
- [x] 4.2 Make project scope the Project Operator default, require explicit intent for user-wide installation, and block installation when the concrete host target is unknown.
- [x] 4.3 Preserve explicit-root verification by reading the installed root from CLI output and keep detection and live-inventory guidance provider-neutral.
- [x] 4.4 Update operator-skill validators and tests to require scoped installation guidance and reject stale `--home` instructions.

## 5. Documentation and Migration

- [x] 5.1 Update the README, quickstart, developer packaged-system-skills guide, and CLI reference with the target-scope path matrix and required command syntax.
- [x] 5.2 Add migration examples for prior implicit defaults and `--home` commands, including the loss of arbitrary public install-root support.
- [x] 5.3 Search packaged skills, documentation, tests, and examples for stale target-resolving commands that omit `--scope` or still use `--home`, and update each owned occurrence.

## 6. Validation

- [x] 6.1 Run focused system-skill resolver, installer, receipt, CLI, inspection, and operator-skill test modules.
- [x] 6.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 6.3 Run strict OpenSpec validation for `add-system-skill-install-scopes` and record any intentional compatibility boundary in the change artifacts.
