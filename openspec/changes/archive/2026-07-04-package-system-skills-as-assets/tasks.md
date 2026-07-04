## 1. Asset Layout

- [x] 1.1 Move distributable `skillset/` entries except `dev/` into `src/isomer_labs/assets/system_skills/`.
- [x] 1.2 Recreate repo-root `skillset/` as an authoring view that preserves `dev/` locally and points distributable entries at package assets.
- [x] 1.3 Remove obsolete package asset placeholders that no longer describe the system-skill asset root.

## 2. Package Resource API

- [x] 2.1 Add a package-scoped `isomer_labs.skills` module family for system-skill asset helpers.
- [x] 2.2 Implement manifest loading, group listing, manifest-relative skill resolution, and traversal guards using `importlib.resources`.
- [x] 2.3 Implement non-destructive materialization of selected manifest groups while preserving manifest-relative paths.

## 3. Packaging and Architecture Guardrails

- [x] 3.1 Ensure packaged non-Python system-skill assets are included by the Python build backend.
- [x] 3.2 Update source architecture tests to allow package-owned `assets/system_skills` while still rejecting runtime repo-root `skillset/` dependencies.
- [x] 3.3 Add tests proving packaged system skills exclude `dev/`, resolve every manifest-listed skill, and materialize a selected group.

## 4. Validator and Documentation Alignment

- [x] 4.1 Keep existing skillset validators working through the repo-root authoring view.
- [x] 4.2 Update developer-facing documentation that describes where distributable skills live.
- [x] 4.3 Keep `skillset/manifest.toml` semantics unchanged for installable groups.

## 5. Verification

- [x] 5.1 Run `pixi run validate-skills`.
- [x] 5.2 Run `pixi run lint`.
- [x] 5.3 Run `pixi run typecheck`.
- [x] 5.4 Run `pixi run test`.
- [x] 5.5 Run `openspec status --change package-system-skills-as-assets`.
