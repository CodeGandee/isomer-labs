## ADDED Requirements

### Requirement: Design Subcommand Exists

The `imsight-agent-skill-handling` skill SHALL expose a `design` subcommand that generates a design overview document for a proposed skill from a user task.

#### Scenario: User invokes design subcommand

- **WHEN** a user explicitly invokes `$imsight-agent-skill-handling use design to design a skill for <task>`
- **THEN** the skill routes to the `design` subcommand workflow
- **AND** the skill does not create or modify any skill files

#### Scenario: Skill entrypoint lists design subcommand

- **WHEN** a user reads the `imsight-agent-skill-handling` `SKILL.md` Subcommands table
- **THEN** the table includes a `design` row naming its purpose and reference file

### Requirement: Design Captures Intent

The `design` subcommand SHALL capture the user's intent before proposing a skill design.

#### Scenario: Intent from prompt

- **WHEN** a user provides a task prompt directly in chat
- **THEN** the skill extracts what the proposed skill should enable the agent to do, when it should be invoked, and the expected output format

#### Scenario: Intent from conversation history

- **WHEN** a user asks the skill to design a skill for a workflow already discussed in the conversation
- **THEN** the skill extracts intent from the conversation history as well as the current prompt

### Requirement: Design Defaults to Multi-Subcommand Skill

The `design` subcommand SHALL default to proposing a multi-subcommand skill that includes a `help` subcommand.

#### Scenario: Task fits multi-subcommand shape

- **WHEN** a user task describes a workflow with distinct stages, routines, or modes
- **THEN** the design proposes a skill with multiple subcommands, including `help`
- **AND** the design justifies the multi-subcommand choice

#### Scenario: Task clearly fits single-command shape

- **WHEN** a user task clearly describes a single technique or pattern with no meaningful subcommands
- **THEN** the design may propose a single-command skill and document why the default was overridden

### Requirement: Design Follows Preferred Skill Format

The design overview SHALL include a draft of the proposed `SKILL.md` that follows the format rules in `references/create.md`.

#### Scenario: Draft SKILL.md content in design doc

- **WHEN** the skill generates a design overview document
- **THEN** the document includes a draft `SKILL.md` with valid YAML frontmatter containing `name` and `description`
- **AND** the draft includes `## Overview`, `## When to Use`, `## Workflow` or `## Core Pattern`, `## Common Mistakes`, and `## Subcommands` sections
- **AND** the description starts with "Use when..."

### Requirement: Design Output is Read-Only and Review-Focused

The `design` subcommand SHALL write only a design overview document and SHALL NOT create actual skill files.

#### Scenario: No skill files created

- **WHEN** the `design` subcommand runs
- **THEN** it writes only `design-overview.md`
- **AND** it does not write `SKILL.md`, `agents/openai.yaml`, `references/`, `commands/`, `scripts/`, or `assets/` in the proposed skill home

#### Scenario: Human review artifact

- **WHEN** the design document is complete
- **THEN** the chat summary explains that the output is for review and that implementation requires the `create` subcommand

### Requirement: Design Output Uses Imsight Output Contract

The `design` subcommand SHALL use the output directory contract defined in the Imsight skills README.

#### Scenario: User provides explicit output path

- **WHEN** a user provides an explicit file or directory path
- **THEN** the skill writes `design-overview.md` to the user-provided location

#### Scenario: IMSIGHT_SKILL_OUTPUT_DIR is set

- **WHEN** `IMSIGHT_SKILL_OUTPUT_DIR` is set and no explicit path is provided
- **THEN** the skill writes `design-overview.md` under the directory named by the environment variable

#### Scenario: Default output location

- **WHEN** no explicit path and no environment variable are provided
- **THEN** the skill writes `design-overview.md` under `<project-dir>/.imsight-arts/skill-designs/<slug-of-skill-name-no-more-than-6-words>/`

### Requirement: Design Document Includes Deep-Inspect-Style Process Model

The `design-overview.md` SHALL include the same structural sections used by `deep-inspect` output, adapted for a proposed skill.

#### Scenario: Required sections present

- **WHEN** the design document is generated
- **THEN** it includes Purpose, Proposed File Inventory, Concepts, High Level Process, Skill Call Graph, Formal Skill Process, Skill Process Explanation, Evidence Handoffs, and Open Questions

#### Scenario: Skill call graph shows proposed subcommands

- **WHEN** the design document includes a Skill Call Graph
- **THEN** the graph includes the proposed subcommands and any planned external skill calls
- **AND** route nodes explain why one subcommand calls another

### Requirement: Design Document Includes Open Questions

The design overview SHALL list assumptions and open questions for the designer to resolve before implementation.

#### Scenario: Open questions captured

- **WHEN** the skill makes assumptions because intent was incomplete
- **THEN** the design document records those assumptions and open questions explicitly
