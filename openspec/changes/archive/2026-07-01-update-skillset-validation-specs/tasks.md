## 1. Spec and Inventory Alignment

- [x] 1.1 Update implementation-facing skillset inventory docs to list preserved v1 skills and the expanded v2 skill set, including paper-writing, review, rebuttal, plotting, figure-polish, and Nature-facing companion skills.
- [x] 1.2 Remove or replace stale v2-core-only expectations, including any wording that says v2 excludes paper-production skills.
- [x] 1.3 Confirm migrated companion-skill layout docs distinguish active resources from `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, provenance, and license material.

## 2. Validator Scope and Rules

- [x] 2.1 Add or refine file-role classification in `scripts/validate_research_paradigm_skillset.py` for active guidance, provenance, migration notes, source analysis, source copies, passive templates, license notices, deferred-resource notes, active references, active scripts, and active assets.
- [x] 2.2 Update default allow zones and `validation.toml` handling so `migrate/**`, `org/analysis/**`, `org/src/**`, top-level source-analysis material, passive templates, provenance files, license files, and deferred-resource notes do not receive active-guidance diagnostics.
- [x] 2.3 Align expected v1 and v2 skill inventories with the current skillset layout, either through validator constants or a config-backed inventory that unit tests assert.
- [x] 2.4 Make local reference validation report missing concrete `references/`, `assets/`, and `scripts/` links while accepting placeholder path patterns such as `references/packages/<package_id>.md` and `scripts/<script>.py`.
- [x] 2.5 Validate `[[tbd-surface:<id>]]`, `[[rsch-object:<id>]]`, and angle-bracket migration placeholders against the appropriate shared or skill-local registry.
- [x] 2.6 Preserve v2 storage-binding deferral checks for active text while allowing explicitly optional source-compatible bridge examples and non-active migration/provenance notes.

## 3. Unit Tests

- [x] 3.1 Update `tests/unit/test_validate_research_paradigm_skillset.py` fixtures so the minimal valid skillset covers preserved v1 skills and the expanded v2 inventory.
- [x] 3.2 Add tests proving migrated companion-skill `migrate/`, `org/analysis/`, `org/src/`, passive `templates/`, provenance, license, and deferred-resource paths are classified without active-guidance false positives.
- [x] 3.3 Add tests proving the same stale terms, source paths, runtime API terms, or resolved placeholders still fail when they appear in active `SKILL.md` or active references.
- [x] 3.4 Add tests for concrete broken local references versus accepted placeholder path patterns.
- [x] 3.5 Add tests for angle-bracket migration placeholder registration and existing v2 `[[rsch-object:<id>]]` registration.
- [x] 3.6 Add tests that storage-binding diagnostics still fire for active v2 concrete Artifact, host API, or source-runtime storage requirements.

## 4. Documentation and Verification

- [x] 4.1 Update `skillset/research-paradigm/README.md`, `skillset/research-paradigm/PROVENANCE.md`, and related skillset docs if their skill inventory, migration-state, or validation-scope descriptions are stale.
- [x] 4.2 Run `pixi run lint` and fix lint failures that are inside active implementation scope.
- [x] 4.3 Run `pixi run typecheck` and fix type-check failures in implementation code.
- [x] 4.4 Run `pixi run test` and fix unit-test failures.
- [x] 4.5 Run `pixi run validate-research-skills` and confirm diagnostics reflect only real active-surface issues or explicitly accepted remaining follow-up items.
- [x] 4.6 Run `openspec validate update-skillset-validation-specs --strict` before applying or archiving the change.
