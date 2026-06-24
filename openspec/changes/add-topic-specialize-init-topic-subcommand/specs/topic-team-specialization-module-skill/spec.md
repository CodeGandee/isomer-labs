## MODIFIED Requirements

### Requirement: Skill Creator Bundle Layout
The repository SHALL provide a lean operator skill bundle named `isomer-admin-topic-team-specialize` for Topic Team Specialization.

#### Scenario: Skill bundle exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` and `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml`

#### Scenario: Frontmatter is minimal
- **WHEN** `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` is inspected
- **THEN** its YAML frontmatter contains `name: isomer-admin-topic-team-specialize` and a trigger-oriented `description`, with no extra frontmatter fields

#### Scenario: UI metadata is present
- **WHEN** `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml` is inspected
- **THEN** it contains `interface.display_name`, `interface.short_description`, and `interface.default_prompt`, and the default prompt names `$isomer-admin-topic-team-specialize`

#### Scenario: Eval scaffolding is absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it does not contain an `evals/` directory or auxiliary docs that are not needed to execute the skill

#### Scenario: Local subcommands exist
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it contains local subcommand pages named `help`, `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, `draft-profile`, `approve-profile`, `materialize-profile`, `launch-team`, `fast-forward`, and `step-by-step` under `references/`

#### Scenario: Subcommands are grouped by contract
- **WHEN** help text, workflow text, or operator documentation lists local subcommands
- **THEN** it groups `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, `materialize-profile`, and `launch-team` as procedural subcommands, `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile` as helper subcommands, and `help`, `fast-forward`, and `step-by-step` as misc subcommands

#### Scenario: Helper subcommands remain lower-level
- **WHEN** helper subcommands are described in help text, workflow text, or operator documentation
- **THEN** the documentation frames the five helper subcommands as finer-grained commands called by procedural subcommands while still allowing direct manual invocation

#### Scenario: Subcommand names are short
- **WHEN** local subcommand pages are inspected
- **THEN** each subcommand filename uses a short verb-object form such as `do-something.md`, except the intentional `help.md` and `step-by-step.md` commands

#### Scenario: Help subcommand prints usage
- **WHEN** the user invokes the local `help` subcommand
- **THEN** the skill prints what `isomer-admin-topic-team-specialize` does, how to invoke it, available modes, subcommands, outputs, and guardrails

#### Scenario: Empty invocation defaults to help
- **WHEN** the skill is invoked without a prompt
- **THEN** the entrypoint selects `help` and prints the same usage output

#### Scenario: Step-by-step performs guided specialization
- **WHEN** the user asks to specialize step by step, proceed interactively, or confirm each stage
- **THEN** the module skill executes `step-by-step`, follows the same required specialization path as `fast-forward`, explains the current step, and waits for user confirmation before continuing to the next step

#### Scenario: Service routing subcommand is absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it does not contain `references/route-service.md`

#### Scenario: Required support references are local
- **WHEN** the `isomer-admin-topic-team-specialize` skill folder is inspected
- **THEN** it contains local support references for Isomer domain language and runtime/file boundaries under `references/`

#### Scenario: External support refs are absent
- **WHEN** the `isomer-admin-topic-team-specialize` skill entrypoint and local references are inspected
- **THEN** they do not reference `.imsight-arts/`, `docs/`, `extern/`, or absolute local support paths for information needed to execute the skill

#### Scenario: Incorporated standalone skills are absent
- **WHEN** the operator skillset is inspected
- **THEN** it does not contain standalone `isomer-admin-project-aware`, `isomer-admin-template-inspect`, `isomer-admin-topic-context-resolve`, `isomer-admin-service-request-route`, `isomer-admin-placeholder-reconcile`, `isomer-admin-topic-profile-draft`, `isomer-admin-profile-review-approval`, `isomer-admin-profile-materialize`, or `isomer-admin-team-launch-orchestrate` skill folders

### Requirement: Skill Validation
The implementation SHALL validate the module skill with skill-creator and repository validation surfaces.

#### Scenario: Skill creator validation runs
- **WHEN** the module skill bundle is ready for review
- **THEN** a developer or agent can run `pixi run python /home/huangzhe/.codex/skills/.system/skill-creator/scripts/quick_validate.py skillset/operator/isomer-admin-topic-team-specialize` or the repo-local equivalent and receive a passing result

#### Scenario: Operator skillset validation runs
- **WHEN** `pixi run validate-operator-skills` runs
- **THEN** it accepts the module skill, detects missing required guide, plan, support-reference, subcommand-group, predecessor-artifact, or subcommand terms including `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, and `finalize-topic-team`, verifies local subcommand workflow structure and naming, rejects external support refs, and does not require `evals/`

#### Scenario: OpenSpec validation runs
- **WHEN** `openspec validate add-topic-specialize-init-topic-subcommand --strict` runs
- **THEN** the change artifacts validate without schema or scenario-format errors

## ADDED Requirements

### Requirement: Topic Initialization Subcommand
The module skill SHALL provide an `init-topic` subcommand that starts the user-facing Topic Team Specialization flow by creating provisional topic definition material before team specialization when the Research Topic is new or unclear.

#### Scenario: Missing topic prompts clarification
- **WHEN** the user invokes `init-topic` without a Research Topic or with an unclear Research Topic
- **THEN** the subcommand asks the user for enough topic information before creating any directory or topic overview file

#### Scenario: Missing topic directory prompts user
- **WHEN** the Research Topic is clear but no topic workspace directory is supplied
- **THEN** the subcommand asks the user for the topic workspace directory before creating topic material

#### Scenario: Topic overview is created
- **WHEN** the user confirms a Research Topic and topic workspace directory
- **THEN** the subcommand creates the directory and writes `<topic-dir>/topic-def/topic-overview.md` from the agent's understanding of the Research Topic

#### Scenario: Topic overview has required sections
- **WHEN** `topic-overview.md` is written
- **THEN** it includes sections for the Research Topic, agent understanding, scope, initial objectives, assumptions, open questions, and source prompt or source material

#### Scenario: Provisional status is reported
- **WHEN** `init-topic` creates topic material that is not registered in the Project Manifest
- **THEN** the subcommand reports that the topic directory is a provisional topic workspace seed and is not yet an authoritative Isomer Research Topic or Topic Workspace registration

#### Scenario: Project config mutation remains bounded
- **WHEN** `init-topic` needs the new topic to become an authoritative Project Manifest-registered Research Topic
- **THEN** it stops at the registration boundary or routes through a supported Isomer CLI/API path instead of hand-editing `.isomer-labs/manifest.toml`

#### Scenario: Specialization waits for explicit topic readiness
- **WHEN** `fast-forward` or `step-by-step` cannot resolve a registered Research Topic but can create a provisional seed through `init-topic`
- **THEN** the workflow reports the provisional seed and any registration blockers before proceeding to template adaptation that requires authoritative topic refs

### Requirement: User-Facing Topic Team Flow
The module skill SHALL present the primary user-facing flow as procedural subcommands for topic initialization, optional topic clarification, team specialization, optional team clarification, topic environment setup, per-agent workspace setup, readiness validation, final summary, and explicit approval or materialization boundaries.

#### Scenario: Flow order is documented
- **WHEN** help text, workflow text, or operator documentation describes the normal user-facing path
- **THEN** it presents the order as `init-topic`, optional `clarify-topic`, `specialize-team`, optional `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, then explicit `approve-profile`, `materialize-profile`, or `launch-team` when requested

#### Scenario: Procedural subcommands refuse missing predecessor artifacts
- **WHEN** a procedural subcommand after `init-topic` is selected and the artifacts expected from its predecessor steps are missing
- **THEN** the subcommand refuses to run, explains which predecessor artifacts are missing, and tells the user which previous subcommand should create them

#### Scenario: Init topic has no predecessor artifact requirement
- **WHEN** `init-topic` is selected
- **THEN** it states that no predecessor artifacts are required because it is the first procedural step

#### Scenario: Clarify topic revises topic overview
- **WHEN** the user asks to refine, answer open questions, or clarify the Research Topic after `init-topic`
- **THEN** the skill routes to `clarify-topic` and updates or reports revisions to `<topic-dir>/topic-def/topic-overview.md` without specializing the team yet

#### Scenario: Specialize team selects domain team
- **WHEN** the user asks to specialize a team after the topic is clear
- **THEN** the skill routes to `specialize-team`, asks the user to select or confirm one Domain Agent Team Template, and runs the internal specialization path against the topic material

#### Scenario: Specialize team creates topic team material
- **WHEN** `specialize-team` completes its specialization work
- **THEN** it reports the created or updated Topic Agent Team Profile Bundle inputs, copied template material, placeholder resolutions, deferrals, validation refs, and next operator action

#### Scenario: Clarify topic team revises specialization
- **WHEN** the user asks to revise the specialized team, adjust roles, change assumptions, or answer open questions about the proposed topic team
- **THEN** the skill routes to `clarify-topic-team` and updates or reports revisions to the specialization outputs without claiming approval, materialization, or launch

#### Scenario: Topic environment setup is explicit
- **WHEN** the specialized topic team needs a development environment before work can start
- **THEN** the skill routes to `setup-topic-env`, runs or reports explicit environment setup steps, and records environment setup status, commands, blockers, and validation refs

#### Scenario: Agent workspace setup is explicit
- **WHEN** the specialized topic team has expected agent roles or Agent Instances that need workspaces
- **THEN** the skill routes to `setup-agent-workspace`, creates or reports per-agent workspace directories and boundary notes, and records workspace paths, ownership, blockers, and validation refs

#### Scenario: Topic team readiness is validated
- **WHEN** topic definition, specialization, environment setup, and agent workspace setup are complete or intentionally deferred
- **THEN** the skill routes to `validate-topic-team` and checks whether the topic team has the topic overview, specialized team material, environment posture, per-agent workspaces, deferrals, and blockers needed for the team to start

#### Scenario: Final topic summary is written
- **WHEN** the topic team has been validated or blockers have been explicitly recorded
- **THEN** the skill routes to `finalize-topic-team` and creates `isomer-topic-summary.md` with the topic team, goal, working logic, environment setup, agent workspace layout, validation status, blockers, and next actions

#### Scenario: Fast-forward remains execution mode
- **WHEN** the user asks for `fast-forward`
- **THEN** the skill treats it as an execution mode that runs the same required path as `init-topic` when needed, optional clarification only when required to unblock, `specialize-team`, setup, validation, and final topic-team summary output

#### Scenario: Step-by-step remains guided execution mode
- **WHEN** the user asks for `step-by-step`
- **THEN** the skill treats it as the guided form of the same user-facing path and waits for confirmation between topic initialization, clarification, team specialization, team clarification, setup, validation, and finalization steps
