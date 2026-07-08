## 1. Packaged System-Skill Catalog

- [x] 1.1 Extend `src/isomer_labs/assets/system_skills/manifest.toml` with group classification, stable extension ids, callback stage definitions, and per-skill callback insertion point declarations.
- [x] 1.2 Update `src/isomer_labs/skills/system_assets.py` data models and loaders to parse core groups, extension groups, stage definitions, and callback insertion points from the manifest.
- [x] 1.3 Add helper APIs for listing known system extensions, listing callback insertion points by core and extension filters, and validating a `(target_skill, stage)` insertion point pair.
- [x] 1.4 Update packaged system-skill asset tests for group classification, extension ids, insertion point parsing, manifest ordering, invalid metadata, and materialization behavior.

## 2. Project Operator System Extension Declarations

- [x] 2.1 Extend Project Manifest parsing and serialization to preserve user-declared operator system extension ids.
- [x] 2.2 Add command-layer operations for listing known system extensions, remembering a known optional extension, and forgetting a Project declaration without touching operator skill files.
- [x] 2.3 Wire `isomer-cli project system-extensions list`, `remember`, and `forget` with deterministic text and JSON output.
- [x] 2.4 Add Project Manifest and CLI tests for empty declarations, idempotent remember, forget, unknown extension rejection, missing Project behavior, and JSON verification-boundary fields.

## 3. Callback Insertion-Point Discovery

- [x] 3.1 Add command-layer support for `project skill-callbacks insertion-points` using core catalog points plus Project-declared operator extension points by default.
- [x] 3.2 Implement `--extension`, `--all-catalog-extensions`, `--core-only`, target skill, and stage filters with deterministic ordering and diagnostics for invalid filter combinations or unknown extension ids.
- [x] 3.3 Include availability provenance in JSON output, distinguishing `core_always_available`, `project_manifest_user_declared`, and explicitly requested catalog-only extension points.
- [x] 3.4 Wire the CLI command and update help text for `project skill-callbacks`.
- [x] 3.5 Add CLI tests for default listing, Project-declared extension listing, explicit extension listing, all-catalog listing, core-only listing, target skill and stage filters, and missing Project behavior.

## 4. Callback Target Validation

- [x] 4.1 Replace hardcoded callback target validation in User Skill Callback registry parsing, registration, resolution, and validation with manifest-declared insertion point validation.
- [x] 4.2 Replace Toolbox callback manifest target validation with manifest-declared insertion point validation.
- [x] 4.3 Ensure diagnostics for undeclared insertion points name the target skill and stage and suggest querying callback insertion points.
- [x] 4.4 Add tests for accepted declared insertion points, rejected undeclared packaged skill targets, known optional extension targets, and Toolbox callback validation behavior.

## 5. Documentation and Verification

- [x] 5.1 Update `docs/isomer-cli.md` with `project system-extensions` and `project skill-callbacks insertion-points` examples and the user-declared extension verification boundary.
- [x] 5.2 Update relevant OpenSpec-facing or packaged-skill documentation if callback-aware skill guidance references insertion-point discovery.
- [x] 5.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 5.4 Run `openspec validate catalog-callback-insertion-points --strict` and fix any artifact or spec issues before applying the change.
