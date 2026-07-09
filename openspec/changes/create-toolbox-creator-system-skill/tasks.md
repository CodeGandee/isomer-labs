## 1. Skill Asset Structure

- [x] 1.1 Create `src/isomer_labs/assets/system_skills/operator/isomer-op-toolbox-mgr/SKILL.md` with frontmatter, workflow, subcommand selection, output contract, and guardrails.
- [x] 1.2 Create concise reference pages for procedural subcommands: `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`.
- [x] 1.3 Create concise reference pages for grouped helper subcommands: `author-toolbox-source`, `edit-callback-declarations`, `edit-runtime-params`, and `inspect-effective-state`.
- [x] 1.4 Add a help or orientation reference page for empty invocations.

## 2. Toolbox Guidance Content

- [x] 2.1 Encode canonical Toolbox concepts, scope rules, project-local source layout, and path-safety rules in the main skill or shared reference page.
- [x] 2.2 Document CLI-backed workflows for Toolbox install, callback refresh, runtime-param definition and mutation, validation, listing, showing, explaining, enabling, disabling, source update, and uninstall.
- [x] 2.3 Add authoring guidance for Toolbox manifests, callback local keys, installed callback ids, runtime-param local keys, default bundles, README notes, and validation diagnostics.
- [x] 2.4 Add safety guidance for project-wide effects, destructive operations, secret-like material, external paths, rollback hints, and blocked status.

## 3. Packaging Integration

- [x] 3.1 Add `operator/isomer-op-toolbox-mgr` to `groups.core.skills` in `src/isomer_labs/assets/system_skills/manifest.toml`.
- [x] 3.2 Update any packaged operator README or catalog text that needs to mention Toolbox Manager.
- [x] 3.3 Ensure directly linked reference pages are packaged with the skill during core materialization.

## 4. Validation

- [x] 4.1 Add or update package asset tests that assert the manifest entry resolves, the skill has `SKILL.md`, and directly linked references exist.
- [x] 4.2 Add or update tests or validators that assert the new operator skill follows the `isomer-op-*` namespace and frontmatter identity convention.
- [x] 4.3 Run the relevant package asset tests, then run `pixi run lint`, `pixi run typecheck`, and `pixi run test` if the change touches Python or validation code.
  - Note: focused package asset tests, `pixi run lint`, and `pixi run typecheck` passed. `pixi run test` ran and failed on unrelated dirty `web/read_model.py:933` file-size architecture check.
- [x] 4.4 Run OpenSpec validation for `create-toolbox-creator-system-skill` before implementation is considered ready.
