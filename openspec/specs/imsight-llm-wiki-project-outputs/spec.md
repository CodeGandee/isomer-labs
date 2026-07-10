# Purpose

Define the project-output capability of `imsight-llm-wiki`, which groups related outputs into a deliverable folder.

## Requirements

### Requirement: Project subcommand groups outputs
The `imsight-llm-wiki` skill SHALL provide a `project` subcommand that creates a grouped output folder for related deliverables.

#### Scenario: User creates a project
- **WHEN** the user invokes `$imsight-llm-wiki use project to create "<slug>" "<goal>"`
- **THEN** the skill SHALL create `outputs/projects/<slug>/WHY.md` containing the goal and rationale

### Requirement: Project adds deliverables
The project workflow SHALL support adding query answers, compiled articles, or generated artifacts into a project folder.

#### Scenario: User adds a deliverable
- **WHEN** the user invokes `$imsight-llm-wiki use project to add <slug> <file-or-query>`
- **THEN** the skill SHALL copy or generate the artifact into `outputs/projects/<slug>/`

### Requirement: Project lists contents
The project workflow SHALL list all projects and their deliverables.

#### Scenario: User lists projects
- **WHEN** the user invokes `$imsight-llm-wiki use project to list`
- **THEN** the skill SHALL enumerate `outputs/projects/*/` folders and their `WHY.md` titles

### Requirement: Project archives completed work
The project workflow SHALL support archiving a completed project.

#### Scenario: User archives a project
- **WHEN** the user invokes `$imsight-llm-wiki use project to archive <slug>`
- **THEN** the skill SHALL move `outputs/projects/<slug>/` to `outputs/projects/.archive/<slug>/`

### Requirement: Project logs changes
The project workflow SHALL append log entries for create, add, and archive operations.

#### Scenario: Project created
- **WHEN** a project is created
- **THEN** it SHALL append `## [HH:MM] project | created <slug>`
