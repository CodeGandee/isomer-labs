## 1. Skill Structure

- [x] 1.1 Create `skillset/operator/isomer-admin-welcome/` with `SKILL.md`, `agents/openai.yaml`, and `references/`.
- [x] 1.2 Define `SKILL.md` frontmatter, workflow, usage-path subcommand table, routing/support subcommand table, required inputs, output contract, and guardrails for `isomer-admin-welcome`.
- [x] 1.3 Add reference pages for `help`, `show-options`, `choose-path`, `show-skill-map`, `next-step`, `start-research-manually`, and `start-research-by-agent-team`.
- [x] 1.4 Ensure the default invocation selects `show-options` and prints visible typical usage paths rather than a tutorial-first system introduction.

## 2. Routing and Guardrails

- [x] 2.1 Write option guidance that routes Project setup or checks to `isomer-admin-project-mgr`.
- [x] 2.2 Write option guidance that routes blank or partial Research Topic creation and manual-research-ready topic preparation to `isomer-admin-topic-creator`.
- [x] 2.3 Write option guidance that routes initialized-topic storage, Topic Actors, package mutation, environment verification, reset checkpoints, and diagnostics to `isomer-admin-topic-mgr`.
- [x] 2.4 Write option guidance that routes Topic Team Specialization to `isomer-admin-topic-team-specialize`.
- [x] 2.5 Write option guidance that routes Houmao loop, runtime, launch profile, mailbox, gateway, and template-mapping questions to `isomer-admin-houmao-interop`.
- [x] 2.6 Preserve read-only default posture and restrict `next-step` to read-only Project inspection commands before recommending an owner workflow.
- [x] 2.7 Exclude active routing to `isomer-admin-topic-workspace-mgr`, `isomer-admin-topic-prepare`, and `isomer-admin-manual-research-session`.
- [x] 2.8 Avoid automatic routing to `isomer-misc-tool-packs`; mention tool packs only as a manual skill when explicitly relevant.

## 3. Inventory and Documentation

- [x] 3.1 Add `operator/isomer-admin-welcome` to `skillset/manifest.toml`.
- [x] 3.2 Remove retired `operator/isomer-admin-topic-prepare` and `operator/isomer-admin-manual-research-session` entries from `skillset/manifest.toml`.
- [x] 3.3 Update `skillset/operator/README.md` to list `isomer-admin-welcome` as the action-oriented menu and path chooser.
- [x] 3.4 Ensure active operator documentation uses only current owner skills for welcome-routing examples.

## 4. Validation and Tests

- [x] 4.1 Extend `scripts/validate_skillsets.py` so operator validation covers `isomer-admin-welcome` frontmatter, UI metadata, local references, workflow, subcommands, output contract, and guardrails.
- [x] 4.2 Add validation checks that welcome guidance contains active owner-skill routes and direct invocation language.
- [x] 4.3 Add validation checks that welcome guidance does not present retired operator skills as active routes.
- [x] 4.4 Add or update unit tests in `tests/unit/test_validate_skillsets.py` for accepted welcome fixtures and representative welcome validation failures.
- [x] 4.5 Add or update operator skill tests to confirm the manifest includes welcome and excludes retired compatibility skill entries.

## 5. Verification

- [x] 5.1 Run `python scripts/validate_skillsets.py`.
- [x] 5.2 Run `pixi run test`.
- [x] 5.3 Run `openspec status --change add-isomer-admin-welcome-skill` and confirm the change is apply-ready.
