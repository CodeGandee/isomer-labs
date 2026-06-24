## 1. CLI Project Bootstrap

- [x] 1.1 Add a Project-level Houmao bootstrap helper that uses the existing CLI-backed Houmao command runner and `HoumaoCommandCatalog.project_init(project_root)` without importing Houmao Python internals.
- [x] 1.2 Refactor `isomer-cli init` so it validates the topic id and existing Project Manifest guard before mutation, runs the Houmao bootstrap boundary, and writes `.isomer-labs/` only after Houmao bootstrap succeeds.
- [x] 1.3 Extend `isomer-cli init` text and JSON output with the resolved `.houmao/` Project overlay path and bounded Houmao bootstrap status.
- [x] 1.4 Preserve init side-effect boundaries so successful init does not create `state.sqlite`, Workspace Runtime directories, Agent Workspaces, adapter launch material, managed agents, mailboxes, gateways, sessions, or launch dossiers.
- [x] 1.5 Add unit tests for successful init with a fake Houmao command, explicit topic init, existing Project refusal, and Houmao bootstrap failure before `.isomer-labs/manifest.toml` is written.
- [x] 1.6 Add or update Houmao command catalog and runner tests for the Project bootstrap command shape and deterministic failure diagnostics.

## 2. Project Manager Skill Bundle

- [x] 2.1 Create `skillset/operator/isomer-admin-project-mgr/` with the skill-creator scaffold, `SKILL.md`, `agents/openai.yaml`, and `references/`.
- [x] 2.2 Write `SKILL.md` with minimal frontmatter, a plain-text purpose, near-top numbered `## Workflow`, default no-prompt help routing, manual subcommand routing, output contract, and guardrails.
- [x] 2.3 Add local subcommand pages `help.md`, `init-project.md`, `check-project.md`, `list-topics.md`, `show-context.md`, `init-runtime.md`, `prep-runtime.md`, and `specialize-team.md`, each with an Imsight-style numbered workflow and freeform fallback.
- [x] 2.4 Add any required self-contained support references under the skill directory for Isomer Project concepts, runtime boundaries, CLI command shapes, and Houmao Project bootstrap.
- [x] 2.5 Ensure the skill contains no `evals/`, no auxiliary docs, and no required support references to `.imsight-arts/`, `docs/`, `extern/`, `/data/`, or `/home/`.
- [x] 2.6 Regenerate or validate `agents/openai.yaml` so `display_name`, `short_description`, and `default_prompt` match `isomer-admin-project-mgr`.

## 3. Validators and Documentation

- [x] 3.1 Extend `scripts/validate_skillsets.py` with focused checks for `isomer-admin-project-mgr`, including required terms, subcommands, local support references, workflow structure, subcommand naming, no `evals/`, and no external required support refs.
- [x] 3.2 Add unit tests for the project-manager skill validator covering the accepted fixture, missing subcommands, external support refs, missing workflow fallbacks, and forbidden `evals/`.
- [x] 3.3 Update `skillset/operator/README.md` to list `isomer-admin-project-mgr`, describe when to use it, and show how it hands topic-team work to `isomer-admin-topic-team-specialize`.
- [x] 3.4 Update `docs/getting-started.md`, `docs/isomer-cli.md`, `docs/houmao-adapter.md`, and troubleshooting docs so Project init creates both `.isomer-labs/` and `.houmao/` while runtime and launch work remain explicit later commands.
- [x] 3.5 Update OpenSpec-facing wording if implementation details require narrower or clearer Project bootstrap terminology.

## 4. Verification

- [x] 4.1 Run skill-creator quick validation for `skillset/operator/isomer-admin-project-mgr`.
- [x] 4.2 Run `pixi run validate-operator-skills`.
- [x] 4.3 Run focused CLI and validator unit tests for init behavior and project-manager skill validation.
- [x] 4.4 Run `pixi run test`.
- [x] 4.5 Run `openspec validate add-isomer-admin-project-manager-skill --strict` and `openspec validate --all`.
- [x] 4.6 Run `pixi run lint` and `pixi run typecheck`.
