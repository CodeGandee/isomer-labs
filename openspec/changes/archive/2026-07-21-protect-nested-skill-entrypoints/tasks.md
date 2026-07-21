## 1. Imsight Authoring Contract

- [x] 1.1 Update `imsight-agent-skill-handling` target resolution, creation, formatting, inspection, testing, migration, layout, and grammar guidance for public `SKILL.md`, protected `SKILL-MAIN.md`, legacy nested input, and `SKILL-SOURCE.md` provenance.
- [x] 1.2 Audit every `imsight-*` bundle, rename nested provenance entrypoints and local references, and verify that only each suite member's root uses `SKILL.md`.

## 2. Role-Aware Isomer Asset APIs

- [x] 2.1 Add shared public/protected entrypoint filename constants and role-aware packaged entrypoint resolution, then migrate asset, installer, inspection, and version or identity callers away from hard-coded protected `SKILL.md` paths.
- [x] 2.2 Promote `SKILL-MAIN.md` to `SKILL.md` only while materializing flattened protected private projections and keep complete public-pack materialization unchanged.

## 3. Packaged Skill Migration

- [x] 3.1 Rename all 53 manifest-declared protected entrypoints to `SKILL-MAIN.md`, rename nested source snapshots to `SKILL-SOURCE.md`, and update direct local references without changing public root or callback filenames.
- [x] 3.2 Update the standard invocation-notation notice across packaged system skills and make each public execution entrypoint explicitly load only the selected protected member's `SKILL-MAIN.md`.
- [x] 3.3 Update active developer documentation and path-sensitive package guidance for the role-aware filenames and private-projection promotion rule.

## 4. Validation and Regression Coverage

- [x] 4.1 Make general and research-paradigm skillset validation select entrypoints by manifest role and reject nested undeclared or provenance `SKILL.md` files.
- [x] 4.2 Update focused unit fixtures and assertions for protected source entrypoints, complete-pack non-discovery, flattened private-projection discovery, installation, inspection, and routing behavior.
- [x] 4.3 Add or update repository-wide assertions that every public package root has `SKILL.md`, every protected member has only `SKILL-MAIN.md`, and every nested provenance entrypoint uses a non-discovery filename.

## 5. Verification

- [x] 5.1 Validate the OpenSpec change and run the focused system-skill asset, catalog, installer, inspection, validation, research-paradigm, and Houmao adapter unit tests.
- [x] 5.2 Run `pixi run validate-skills`, `pixi run lint`, `pixi run typecheck`, `pixi run test`, and the package import smoke test; resolve failures caused by this migration.
