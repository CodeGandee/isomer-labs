## 1. Split the Install Scope Contract

- [x] 1.1 Add an install-specific target option decorator in `src/isomer_labs/cli/commands/system_skills.py` that keeps `--target` required and gives `--scope` a visible `project` default.
- [x] 1.2 Keep `status`, `upgrade`, and `uninstall` on the existing required-scope option contract, and preserve their failure-before-mutation behavior when `--scope` is omitted.
- [x] 1.3 Pass the effective install scope through the existing target resolver, installer, projection, binding, and receipt paths without adding a second default inside those layers.
- [x] 1.4 Update install help and extension discovery output so the Project-default form omits `--scope`, while user-wide install and non-install operations show an explicit scope.

## 2. Add CLI Regression Coverage

- [x] 2.1 Add a CLI test that runs `system-skills install` without `--scope` from a temporary working directory and verifies that it creates Project-scoped bindings and receipts only under that directory.
- [x] 2.2 Verify that omitted scope and explicit `--scope project` resolve the same concrete target roots for individual targets and `--target all`, including target deduplication.
- [x] 2.3 Verify that Project scope uses the exact current working directory from a nested path and does not discover an ancestor Git or Isomer root.
- [x] 2.4 Preserve explicit `--scope user` installation and verify that user-scoped roots are mutated only when the user scope is supplied.
- [x] 2.5 Verify that install help displays the Project default, `--target` remains required, unsupported legacy options remain rejected, and `status`, `upgrade`, and `uninstall` still reject omitted scope without mutation.
- [x] 2.6 Update structured and human-readable extension discovery tests to expect the short Project-default install command and the explicit-scope status command.

## 3. Update Packaged System Skill Guidance

- [x] 3.1 Update the packaged system skill manager source and references to explain that direct CLI install defaults to Project scope, while the manager continues to pass its selected scope explicitly and user-wide install always names `user`.
- [x] 3.2 Update system skill validation rules and fixtures so they accept and require the new default guidance, reject stale claims that install always requires `--scope`, and preserve explicit-scope guidance for the other operations.
- [x] 3.3 Regenerate or refresh any tracked packaged skill projections affected by the source changes and verify that installed symlink and materialized forms expose the same instructions.

## 4. Update Documentation and Release Notes

- [x] 4.1 Update the README with the short Project-scoped install form, an explicit user-scoped example, and the exact-current-working-directory rule.
- [x] 4.2 Update the quickstart, CLI reference, manual validation guide, and packaged system skill documentation so install defaults to Project scope while status, upgrade, and uninstall require explicit scope.
- [x] 4.3 Update generated or registered CLI examples and documentation validation fixtures so the short install form is accepted and stale universal required-scope guidance is rejected.
- [x] 4.4 Add an Unreleased changelog entry describing the new install default, the clean distinction for user scope, and the exact directory that Project installation mutates.

## 5. Validate the Change

- [x] 5.1 Run focused system-skill CLI, resolver, installer, discovery, packaged-skill, and documentation tests.
- [x] 5.2 Run repository skill and documentation validation, including all supported packaged skill scopes.
- [x] 5.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 5.4 Build and install the distribution in an isolated environment, then smoke-test omitted-scope install from outside the repository and verify that only the current Project target root changes.
- [x] 5.5 Search for stale guidance that says every system-skill install requires `--scope`, and run strict OpenSpec validation for this change.
