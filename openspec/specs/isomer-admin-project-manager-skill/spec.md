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
- **THEN** the skill routes to `check-project`, uses read-only Project validation and diagnostics commands, and includes Houmao project status checks without launching, stopping, or messaging managed agents

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
- **THEN** the skill routes to `prep-runtime` and preserves the explicit `isomer-cli project runtime prepare` and `isomer-cli project runtime validate --require-ready-readiness` boundaries

#### Scenario: Topic team specialization is handed off
- **WHEN** the user asks to adapt, instantiate, or specialize a Domain Agent Team Template for a Research Topic
- **THEN** the skill routes to `specialize-team`, resolves enough Project context, and hands off to `isomer-admin-topic-team-specialize` instead of duplicating Topic Team Specialization logic

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
