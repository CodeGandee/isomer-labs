## 1. Add Workspace Manager Install Surface

- [x] 1.1 Update `skillset/operator/isomer-admin-topic-workspace-mgr/SKILL.md` description, workflow, subcommand table, output contract, and guardrails to include `install-packages`.
- [x] 1.2 Add `skillset/operator/isomer-admin-topic-workspace-mgr/references/install-packages.md` as an executable subcommand page with required inputs, workflow, package inference, install planning, verification, blockers, and output guidance.
- [x] 1.3 Update `skillset/operator/isomer-admin-topic-workspace-mgr/references/help.md` and any summary/top-level support pages so the new subcommand is discoverable.
- [x] 1.4 Ensure the subcommand accepts plain prompts, Markdown files, YAML, JSON, requirements-style lists, and copied blocker text without requiring a fixed schema file.

## 2. Define Pixi Install and Verification Policy

- [x] 2.1 Teach `install-packages` to resolve the selected Project, Research Topic, Topic Workspace, Topic Workspace Pixi manifest, and Pixi environment before mutation.
- [x] 2.2 Specify package-kind inference for Python libraries, R packages, native/Conda tools, CLI tools, LaTeX or document tools, scientific packages, and external runtime blockers.
- [x] 2.3 Specify Pixi-scoped install routes and verification commands for imports, library loads, CLI version checks, minimal file generation, and task-specific smoke checks.
- [x] 2.4 Add guardrails rejecting local `venv`, ambient `pip`, unrecorded user R libraries, `sudo`, system package managers, global shell profile edits, daemons, kernel driver changes, and other machine-global mutation.
- [x] 2.5 Add bounded-run/resource-risk handling for heavy package installation or verification paths.

## 3. Route Research v2 Package Needs

- [x] 3.1 Update `isomer-rsch-nature-figure-v2` active guidance so missing Python or R backend packages route to `$isomer-admin-topic-workspace-mgr install-packages`.
- [x] 3.2 Remove active `install.packages()` guidance from `isomer-rsch-nature-figure-v2` and replace it with a workspace-manager package request handoff.
- [x] 3.3 Update `isomer-rsch-nature-paper2ppt-v2` reachable active guidance so missing Python packages route to `install-packages` instead of creating a local virtual environment.
- [x] 3.4 Verify `isomer-rsch-science-v2` keeps package checks as availability evidence and routes desired package installation through `install-packages`.
- [x] 3.5 Search active v2 research guidance, excluding bounded migration/source-copy material, to ensure no direct install, ambient `pip`, `install.packages()`, or local `venv` instruction remains.

## 4. Align Service Setup Boundary

- [x] 4.1 Update `skillset/service/isomer-srv-topic-env-setup` guidance so user-facing or cross-skill package-add requests route to `$isomer-admin-topic-workspace-mgr install-packages`.
- [x] 4.2 Preserve full gate-driven service setup behavior while avoiding a competing direct package-add entrypoint.
- [x] 4.3 Ensure service guidance keeps Pixi-scoped Topic Workspace mutation and no-sudo/no-ambient-venv guardrails.

## 5. Validate

- [x] 5.1 Run `pixi run validate-operator-skills`.
- [x] 5.2 Run `pixi run validate-service-skills`.
- [x] 5.3 Run `pixi run validate-research-skills`.
- [x] 5.4 Run targeted searches for direct install guidance in active research v2 skill text and service/operator routing text.
- [x] 5.5 Run `openspec validate add-topic-workspace-install-packages --strict`.
