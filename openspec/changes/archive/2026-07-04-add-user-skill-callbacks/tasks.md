## 1. Registry Model and Config Refs

- [x] 1.1 Add a User Skill Callback registry model and parser with schema-version checks, callback id validation, supported stage validation, status validation, priority defaults, and exact system skill target fields.
- [x] 1.2 Add source validation for inline prompt material, prompt file paths, and external skill directories containing `SKILL.md`, including exactly-one-source enforcement.
- [x] 1.3 Add Project-root path policy for callback sources and registry refs, including explicit handling for allowed external callback sources.
- [x] 1.4 Extend Project Manifest parsing and validation to accept project-scoped User Skill Callback registry refs without treating them as runtime truth.
- [x] 1.5 Extend Research Topic Config parsing and validation to accept topic-scoped User Skill Callback registry refs and expose them through Effective Topic Context.
- [x] 1.6 Add redaction-sensitive validation for callback registry metadata and managed prompt content so secret-like values are rejected without printing the value.

## 2. CLI Commands

- [x] 2.1 Add the `isomer-cli project skill-callbacks` command group and help wiring under the existing Project CLI surface.
- [x] 2.2 Implement `register` for project-scoped and topic-scoped callbacks, including inline prompt materialization into managed callback content.
- [x] 2.3 Implement `resolve` as a read-only command that filters by exact system skill name and stage, merges project and topic callbacks, sorts deterministically, and returns JSON-friendly instruction refs and diagnostics.
- [x] 2.4 Implement `list` and `show` commands with stable text and `--print-json` output.
- [x] 2.5 Implement `disable` so callback records remain in the registry but are excluded from normal resolution.
- [x] 2.6 Implement `validate` so reachable callback registries, target system skill names, stages, duplicate active ids, source paths, external-source flags, priorities, statuses, and secret-like fields are checked.

## 3. Participating Skill Integration

- [x] 3.1 Define the concise shared User Skill Callback wording for participating system skills, including authority and conflict guidance.
- [x] 3.2 Update production `isomer-deepsci-*` `SKILL.md` files so top-level workflows resolve `begin` callbacks before workflow-specific work and `end` callbacks before final completion.
- [x] 3.3 Update DeepSci skill validation to require the callback reminder in each participating production DeepSci skill.
- [x] 3.4 Update packaged system skill manifest or validation fixtures only if needed to recognize callback-aware skill metadata without changing active skill names.

## 4. Tests and Documentation

- [x] 4.1 Add unit tests for callback registry parsing, schema-version rejection, stage rejection, status handling, priority ordering, disabled callback exclusion, and duplicate active id diagnostics.
- [x] 4.2 Add unit tests for callback source validation, including prompt materialization, prompt file bounds, skill directory `SKILL.md` checks, and explicit external-source handling.
- [x] 4.3 Add CLI tests for `register`, `resolve`, `list`, `show`, `disable`, `validate`, missing Project diagnostics, topic-scoped context resolution, and `--print-json` output shape.
- [x] 4.4 Add config tests showing Project Manifest and Research Topic Config callback registry refs are accepted as declarative refs and inline callback bodies or secret-like fields are rejected.
- [x] 4.5 Add DeepSci validation tests or fixtures proving each participating `isomer-deepsci-*` workflow contains the required `begin` and `end` callback resolution guidance.
- [x] 4.6 Update user-facing documentation with the User Skill Callback concept, CLI examples, source-type examples, authority rules, and the future convention that skill-family extensions use `isomer-<extension-name>-<purpose>` naming.

## 5. Verification

- [x] 5.1 Run `pixi run validate-skills` and fix any callback-related system skill validation issues.
- [x] 5.2 Run `pixi run validate-research-skills` and fix any callback-related DeepSci validation issues.
- [x] 5.3 Run `pixi run lint` and fix lint issues.
- [x] 5.4 Run `pixi run typecheck` and fix type errors.
- [x] 5.5 Run `pixi run test` and fix failing tests.
- [x] 5.6 Run `openspec status --change add-user-skill-callbacks` and confirm the implementation checklist is complete before archive.
