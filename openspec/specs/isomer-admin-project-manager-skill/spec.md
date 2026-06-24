# isomer-admin-project-manager-skill Specification

## Purpose
Define the lean operator skill bundle for Isomer Project initialization, inspection, validation, runtime preparation guidance, and Project-level Houmao bootstrap.
## Requirements
### Requirement: Project Manager Skill Bundle
The repository SHALL provide a lean operator skill bundle named `isomer-admin-project-mgr` for Isomer Project initialization, inspection, validation, and runtime preparation guidance.

#### Scenario: Skill bundle exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-project-mgr/SKILL.md` and `skillset/operator/isomer-admin-project-mgr/agents/openai.yaml`

#### Scenario: Frontmatter is minimal
- **WHEN** `skillset/operator/isomer-admin-project-mgr/SKILL.md` is inspected
- **THEN** its YAML frontmatter contains `name: isomer-admin-project-mgr` and a trigger-oriented `description`, with no extra frontmatter fields

#### Scenario: UI metadata is present
- **WHEN** `skillset/operator/isomer-admin-project-mgr/agents/openai.yaml` is inspected
- **THEN** it contains `interface.display_name`, `interface.short_description`, and `interface.default_prompt`, and the default prompt names `$isomer-admin-project-mgr`

#### Scenario: Eval scaffolding is absent
- **WHEN** the `isomer-admin-project-mgr` skill folder is inspected
- **THEN** it does not contain an `evals/` directory or auxiliary docs that are not needed to execute the skill

### Requirement: Project Manager Skill Workflow
The project manager skill SHALL follow the Imsight skill-entrypoint structure and expose short local subcommands for Project lifecycle work.

#### Scenario: Workflow section is near the top
- **WHEN** `SKILL.md` is inspected
- **THEN** it contains a near-top `## Workflow` section before detailed helper, output, or guardrail sections

#### Scenario: Workflow steps are numbered
- **WHEN** the `## Workflow` section is inspected
- **THEN** it uses numbered steps that select default help mode for empty invocation, manual single-subcommand mode, ambiguity handling, execution of selected subcommands, and shared validation boundaries

#### Scenario: Freeform fallback exists
- **WHEN** the user's task does not map cleanly to the default workflow steps
- **THEN** the skill tells the agent to use its native planning tool to build and execute a step-by-step plan from the project context, subcommands, CLI boundaries, output contract, and guardrails

#### Scenario: Local subcommands exist
- **WHEN** the `isomer-admin-project-mgr` skill folder is inspected
- **THEN** it contains local subcommand pages named `help`, `init-project`, `check-project`, `list-topics`, `show-context`, `init-runtime`, `prep-runtime`, and `specialize-team` under `references/`

#### Scenario: Subcommand names are short
- **WHEN** local subcommand pages are inspected
- **THEN** each subcommand filename uses a short verb-object form such as `do-something.md`, except the intentional `help.md` command

#### Scenario: Subcommands have Imsight workflows
- **WHEN** each local subcommand page is inspected
- **THEN** it contains a near-top `## Workflow` section, numbered workflow steps, and a fallback for tasks that do not map cleanly to the default steps

### Requirement: Project Manager Help Behavior
The project manager skill SHALL explain its purpose and usage when invoked for help or without a prompt.

#### Scenario: Help subcommand prints usage
- **WHEN** the user invokes the local `help` subcommand
- **THEN** the skill prints what `isomer-admin-project-mgr` does, how to invoke it, available subcommands, expected outputs, and guardrails

#### Scenario: Empty invocation defaults to help
- **WHEN** the skill is invoked without a prompt
- **THEN** the entrypoint selects `help` and prints the same usage output

#### Scenario: Purpose is plain text
- **WHEN** operator documentation or skill text describes the workflow
- **THEN** it explains in plain text that the skill initializes and manages an Isomer Project by coordinating Project config, Research Topics, Topic Workspaces, Workspace Runtime preparation, and the Project-level Houmao overlay

### Requirement: Project Lifecycle Subcommands
The project manager skill SHALL guide Project lifecycle commands without bypassing Isomer CLI validation or Houmao CLI boundaries.

#### Scenario: Init project guides Isomer and Houmao bootstrap
- **WHEN** the user asks to initialize an Isomer Project
- **THEN** the skill routes to `init-project`, uses the supported `isomer-cli project init` command shape, and reports the resulting `.isomer-labs/` Project config and `.houmao/` Project-level Houmao overlay status

#### Scenario: Check project remains read-only
- **WHEN** the user asks to check, diagnose, or validate an existing Project
- **THEN** the skill routes to `check-project`, uses read-only `isomer-cli project validate`, `isomer-cli project doctor`, and related diagnostics commands, and includes Houmao project status checks without launching, stopping, or messaging managed agents

#### Scenario: Topic listing uses CLI surfaces
- **WHEN** the user asks what Research Topics or Topic Workspaces are available
- **THEN** the skill routes to `list-topics` and uses `isomer-cli project topics list` and `isomer-cli project workspaces list` rather than scanning unregistered directories as authority

#### Scenario: Context inspection uses Effective Topic Context
- **WHEN** the user asks which Project, Research Topic, Topic Workspace, template, profile, or runtime refs are selected
- **THEN** the skill routes to `show-context` and uses `isomer-cli project context show` or equivalent read-only context resolution surfaces

#### Scenario: Runtime init stays explicit
- **WHEN** the user asks to create or open Workspace Runtime state
- **THEN** the skill routes to `init-runtime` and preserves the explicit `isomer-cli project runtime init` boundary for creating `state.sqlite` and runtime directories

#### Scenario: Runtime preparation stays explicit
- **WHEN** the user asks to prepare launch-facing readiness
- **THEN** the skill routes to `prep-runtime` and preserves the explicit `isomer-cli project runtime prepare` and `project runtime validate --require-ready-readiness` boundaries

#### Scenario: Cleanup project stays explicit
- **WHEN** the user asks to remove Isomer-managed Project material or prepare a Project root for reinitialization
- **THEN** the skill routes to cleanup guidance that uses `isomer-cli project cleanup --dry-run` before any confirmed cleanup command

#### Scenario: Topic team specialization is handed off
- **WHEN** the user asks to adapt, instantiate, or specialize a Domain Agent Team Template for a Research Topic
- **THEN** the skill routes to `specialize-team`, resolves enough Project context with `isomer-cli project ...` command surfaces, and hands off to `isomer-admin-topic-team-specialize` instead of duplicating Topic Team Specialization logic

### Requirement: Project Manager Support References
The project manager skill SHALL keep required support knowledge inside its own skill directory.

#### Scenario: Required support references are local
- **WHEN** the `isomer-admin-project-mgr` skill folder is inspected
- **THEN** any required Isomer domain, runtime boundary, Houmao bootstrap, or CLI usage reference needed to execute the skill is stored under `skillset/operator/isomer-admin-project-mgr/references/`

#### Scenario: External support refs are absent
- **WHEN** the `isomer-admin-project-mgr` skill entrypoint and local references are inspected
- **THEN** they do not reference `.imsight-arts/`, `docs/`, `extern/`, or absolute local support paths for information needed to execute the skill

### Requirement: Project Manager Skill Validation
The implementation SHALL validate the project manager skill with skill-creator and repository validation surfaces.

#### Scenario: Skill creator validation runs
- **WHEN** the project manager skill bundle is ready for review
- **THEN** a developer or agent can run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-project-mgr` or the repo-local equivalent and receive a passing result

#### Scenario: Operator skillset validation runs
- **WHEN** `pixi run validate-operator-skills` runs
- **THEN** it accepts the project manager skill, detects missing required support-reference or subcommand terms, verifies local subcommand workflow structure and naming, rejects external support refs, and does not require `evals/`

#### Scenario: OpenSpec validation runs
- **WHEN** `openspec validate add-isomer-admin-project-manager-skill --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors

### Requirement: Project Manager Generated Content Layout Guidance
The project manager skill SHALL describe and report the default `isomer-content/` layout created by Project initialization.

#### Scenario: Init project reports content root
- **WHEN** the user asks to initialize an Isomer Project
- **THEN** the `init-project` subcommand reports `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, `isomer-content/`, `isomer-content/topic-ws/<topic-id>/`, `.houmao/`, diagnostics, and next operator action

#### Scenario: Project concepts use new default workspace path
- **WHEN** project-manager references explain the default Topic Workspace path created by `isomer-cli project init <topic-id>`
- **THEN** they name `isomer-content/topic-ws/<topic-id>/` instead of `topic-workspaces/<topic-id>/`

#### Scenario: Content root policy is explained
- **WHEN** project-manager help or initialization guidance describes `isomer-content/`
- **THEN** it explains that `README.md` and `.gitignore` are generated policy files and that generated content under the root is ignored by default unless the user intentionally tracks selected files

#### Scenario: Project config remains separate from content
- **WHEN** project-manager guidance describes Project Config and generated content
- **THEN** it keeps `.isomer-labs/` as the Project Config Directory and `isomer-content/` as the default generated-content root

### Requirement: Project Manager Custom Content Directory Guidance
The project manager skill SHALL describe and use the optional Project initialization content directory selector when the user wants generated Isomer content outside the default `isomer-content/` root.

#### Scenario: Init project accepts content directory request
- **WHEN** the user asks to initialize an Isomer Project with a custom generated content directory
- **THEN** the `init-project` subcommand includes `--content-dir <content-dir>` in the supported `isomer-cli project init` command shape instead of instructing the operator to hand-edit `.isomer-labs/manifest.toml`

#### Scenario: Init project reports custom content root
- **WHEN** Project initialization succeeds with a custom content directory
- **THEN** the `init-project` subcommand reports the selected generated content root, its generated `README.md` and `.gitignore` policy files, the derived `<content-dir>/topic-ws/<topic-id>/` Topic Workspace path, `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic-id>.toml`, `.houmao/`, diagnostics, and next operator action

#### Scenario: Help explains content directory option
- **WHEN** project-manager help or CLI boundary guidance describes fresh Project initialization
- **THEN** it explains that omitting `--content-dir` uses `isomer-content/`, while supplying `--content-dir <content-dir>` chooses a project-local generated content root and derives the default Topic Workspace base as `<content-dir>/topic-ws`

#### Scenario: Guardrails preserve project-local content
- **WHEN** project-manager guidance describes content directory choices
- **THEN** it says generated content roots must stay inside the Project root, must not live inside `.isomer-labs/`, and must not be used to initialize runtime or live Houmao state

### Requirement: Project Manager CLI Namespace Guidance
The project manager skill SHALL use `isomer-cli project ...` as the canonical command shape for Project-targeted CLI guidance.

#### Scenario: Help names project namespace
- **WHEN** project-manager help describes supported Isomer CLI command surfaces
- **THEN** it explains that Project-targeted commands live under `isomer-cli project`

#### Scenario: CLI boundary examples use project namespace
- **WHEN** the project-manager CLI boundary reference lists command examples
- **THEN** Project-scoped commands use shapes such as `isomer-cli project init`, `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project runtime init`, and `isomer-cli project cleanup --dry-run`

#### Scenario: Project selector examples use root option
- **WHEN** project-manager guidance selects a Project root explicitly
- **THEN** it uses `isomer-cli project --root <project-root> <subcmd>` as the canonical selector shape

#### Scenario: Ancestor discovery is explained
- **WHEN** project-manager guidance explains Project resolution
- **THEN** it says `isomer-cli project <subcmd>` starts at cwd and walks parent directories until it finds `.isomer-labs/manifest.toml` or fails

#### Scenario: Root-level project commands are not taught
- **WHEN** project-manager skill text or local references are inspected
- **THEN** they do not present root-level Project command shapes such as `isomer-cli init`, `isomer-cli validate`, or `isomer-cli runtime init` as canonical usage

### Requirement: Project Manager Cleanup Guidance
The project manager skill SHALL guide explicit Project cleanup through the supported `isomer-cli project cleanup` command surface without bypassing dry-run review or Isomer path-safety rules.

#### Scenario: Cleanup request routes to cleanup guidance
- **WHEN** the user asks to remove Isomer-managed Project material, reset Project bootstrap material, or prepare a Project root for reinitialization
- **THEN** the project-manager skill routes the request to cleanup guidance and uses `isomer-cli project cleanup` instead of instructing the operator to delete directories by hand

#### Scenario: Cleanup guidance starts with dry-run
- **WHEN** the project-manager skill prepares a cleanup command
- **THEN** it first runs or recommends `isomer-cli project cleanup --dry-run` with the selected parts before any command that can delete files

#### Scenario: Cleanup guidance explains confirmation
- **WHEN** the project-manager skill describes applying cleanup
- **THEN** it explains that actual deletion requires `--yes`, and that omitting `--yes` is non-mutating

#### Scenario: Cleanup guidance supports partial removal
- **WHEN** the user asks to remove only Project config, only the Project-level Houmao overlay, only content-root policy files, a selected Topic Workspace, runtime material, or the full content root
- **THEN** the skill selects the corresponding cleanup part and preserves unrelated Isomer-managed material

#### Scenario: Cleanup guidance preserves unknown content by default
- **WHEN** cleanup involves the selected generated content root
- **THEN** the skill explains that unknown files under the content root are preserved unless the user explicitly chooses content-root purge behavior

#### Scenario: Reinitialization guidance stays explicit
- **WHEN** the user wants to rerun `isomer-cli project init` after an existing manifest blocks initialization
- **THEN** the skill tells the user to review and apply cleanup first, then rerun `isomer-cli project init` only after the blocking Project Manifest has been removed

### Requirement: Project Manager Cleanup Subcommand
The project manager skill SHALL expose a short local cleanup subcommand for Project cleanup workflows.

#### Scenario: Cleanup project subcommand exists
- **WHEN** the `isomer-admin-project-mgr` skill folder is inspected
- **THEN** it contains a local subcommand page named `cleanup-project` under `references/`

#### Scenario: Help lists cleanup project
- **WHEN** project-manager help lists available subcommands
- **THEN** it includes `cleanup-project` with a concise purpose and expected cleanup outputs

#### Scenario: CLI boundary reference includes cleanup
- **WHEN** project-manager CLI boundary guidance is inspected
- **THEN** it includes `isomer-cli project cleanup --part <part> --dry-run` and the confirmed `isomer-cli project cleanup --part <part> --yes` command shape
