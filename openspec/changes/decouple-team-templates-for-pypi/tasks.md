## 1. Team Repository Model and Parsing

- [x] 1.1 Add Team Repository manifest models for repository id, schema version, template entries, source paths, source kind, status, and diagnostics.
- [x] 1.2 Implement local `isomer-team-repo.toml` loading with path normalization and rejection of template paths that escape the Team Repository root.
- [x] 1.3 Add fixture Team Repository material that points at existing `deepsci-mini` and `deepsci-org` execplan packages without moving them into `src/`.

## 2. Template Discovery Refactor

- [x] 2.1 Remove `_REPO_ROOT`, `_BUILT_IN_DEEPSCI_ORG_SOURCE`, `_BUILT_IN_DEEPSCI_MINI_SOURCE`, and implicit built-in registrations from `src/isomer_labs/team_templates.py`.
- [x] 2.2 Refactor template discovery to merge Project-local registrations and explicitly configured Team Repository templates.
- [x] 2.3 Preserve validation for Project-local template registrations and allow Team Repository templates to resolve outside the Project root only through configured repository provenance.
- [x] 2.4 Update profile specialization and profile bundle materialization to consume resolved Project-local or Team Repository template sources without requiring core built-ins.

## 3. CLI Surface

- [x] 3.1 Add Team Repository list and inspect CLI commands with deterministic text and JSON output.
- [x] 3.2 Update `project team-templates list`, `inspect`, and `validate` to include Team Repository templates when configured.
- [x] 3.3 Update empty template-list output so it explains that reusable Agent Team definitions come from Project registrations or external Team Repositories.
- [x] 3.4 Add Project-facing registration or selection flow for choosing a Team Repository template before Topic Team Specialization.

## 4. PyPI Source and Metadata Boundary

- [x] 4.1 Add architecture tests that reject repository-root derivation and runtime references from `src/` to checkout-only directories such as `teams/`, `skillset/`, `tests/`, `openspec/`, `.imsight-arts/`, or `extern/`.
- [x] 4.2 Update source and public CLI examples to remove checkout-only fixture paths from PyPI-facing runtime text.
- [x] 4.3 Move development, documentation, lint, typecheck, and test-only dependencies out of default PyPI runtime dependencies while keeping Pixi tasks usable.
- [x] 4.4 Replace local-only package version metadata with a release-compatible version.

## 5. Tests and Fixtures

- [x] 5.1 Update CLI tests that expected `deepsci-mini` or `deepsci-org` as implicit built-ins to configure a fixture Team Repository explicitly.
- [x] 5.2 Add tests for missing, malformed, and path-escaping Team Repository manifests.
- [x] 5.3 Add tests for Project-local templates and Team Repository templates appearing together with stable source provenance.
- [x] 5.4 Add a package smoke test that imports `isomer_labs`, invokes the CLI entry point, lists schemas, and lists team templates without checkout-local `teams/` dependencies.

## 6. Documentation and Verification

- [x] 6.1 Document the Team Repository manifest shape and the migration from implicit DeepSci built-ins to external Team Repository configuration.
- [x] 6.2 Run `pixi run lint`.
- [x] 6.3 Run `pixi run typecheck`.
- [x] 6.4 Run `pixi run test`.
- [x] 6.5 Run `openspec status --change decouple-team-templates-for-pypi`.
