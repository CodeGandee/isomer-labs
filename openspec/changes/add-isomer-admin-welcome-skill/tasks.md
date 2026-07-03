## 1. Skill Structure

- [ ] 1.1 Create `skillset/operator/isomer-admin-welcome/` with `SKILL.md`, `agents/openai.yaml`, and `references/`.
- [ ] 1.2 Define `SKILL.md` frontmatter, workflow, subcommand table, required inputs, output contract, and guardrails for `isomer-admin-welcome`.
- [ ] 1.3 Add reference pages for `help`, `show-options`, `choose-path`, `show-skill-map`, and `next-step`.
- [ ] 1.4 Ensure the default invocation selects `show-options` and prints an action-oriented menu rather than a tutorial-first system introduction.

## 2. Routing and Guardrails

- [ ] 2.1 Write option guidance that routes Project setup or checks to `isomer-admin-project-mgr`.
- [ ] 2.2 Write option guidance that routes blank or partial Research Topic creation and manual-research-ready topic preparation to `isomer-admin-topic-creator`.
- [ ] 2.3 Write option guidance that routes initialized-topic storage, Topic Actors, package mutation, environment verification, reset checkpoints, and diagnostics to `isomer-admin-topic-mgr`.
- [ ] 2.4 Write option guidance that routes Topic Team Specialization to `isomer-admin-topic-team-specialize`.
- [ ] 2.5 Write option guidance that routes Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping questions to `isomer-admin-houmao-interop`.
- [ ] 2.6 Preserve read-only default posture and restrict `next-step` to read-only Project inspection commands before recommending an owner workflow.
- [ ] 2.7 Exclude active routing to `isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-prepare`, and `isomer-admin-manual-research-session`.
- [ ] 2.8 Avoid automatic routing to `isomer-misc-tool-packs`; mention tool packs only as a manual skill when explicitly relevant.

## 3. Inventory and Documentation

- [ ] 3.1 Add `operator/isomer-admin-welcome` to `skillset/manifest.toml`.
- [ ] 3.2 Remove retired `operator/isomer-admin-topic-prepare` and `operator/isomer-admin-manual-research-session` entries from `skillset/manifest.toml`.
- [ ] 3.3 Update `skillset/operator/README.md` to list `isomer-admin-welcome` as the action-oriented menu and path chooser.
- [ ] 3.4 Ensure active operator documentation uses only current owner skills for welcome-routing examples.

## 4. Validation and Tests

- [ ] 4.1 Extend `scripts/validate_skillsets.py` so operator validation covers `isomer-admin-welcome` frontmatter, UI metadata, local references, workflow, subcommands, output contract, and guardrails.
- [ ] 4.2 Add validation checks that welcome guidance contains active owner-skill routes and direct invocation language.
- [ ] 4.3 Add validation checks that welcome guidance does not present retired operator skills as active routes.
- [ ] 4.4 Add or update unit tests in `tests/unit/test_validate_skillsets.py` for accepted welcome fixtures and representative welcome validation failures.
- [ ] 4.5 Add or update operator skill tests to confirm the manifest includes welcome and excludes retired compatibility skill entries.

## 5. Verification

- [ ] 5.1 Run `python scripts/validate_skillsets.py`.
- [ ] 5.2 Run `pixi run test`.
- [ ] 5.3 Run `openspec status --change add-isomer-admin-welcome-skill` and confirm the change is apply-ready.
