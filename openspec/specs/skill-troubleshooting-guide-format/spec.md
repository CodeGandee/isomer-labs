## Purpose

Define when active packaged Isomer skill pages may include troubleshooting guidance and the required problem-and-solution structure when they do.

## Requirements

### Requirement: Troubleshooting Guide section format
The system SHALL treat `## Troubleshooting Guide` as optional for an active packaged Isomer `SKILL.md` and SHALL include it only when the skill documents concrete recoverable execution problems. When present, the section SHALL use the current two-level problem-and-solution format.

#### Scenario: Skill has known recoverable failure modes
- **WHEN** an active packaged skill documents a likely execution problem with a corrective action
- **THEN** its `SKILL.md` may include a `## Troubleshooting Guide` entry using the required problem-and-solution structure

#### Scenario: Skill has no concrete troubleshooting content
- **WHEN** an active packaged skill has no likely recoverable execution problem to document
- **THEN** its `SKILL.md` omits `## Troubleshooting Guide` instead of adding an empty or generic placeholder

### Requirement: Troubleshooting entries use a two-level nested list
Each entry in the `## Troubleshooting Guide` section SHALL use exactly two bullet levels. The first-level bullet SHALL name the problem. The second-level bullet SHALL state the solution or corrective action.

#### Scenario: Problem-and-solution structure
- **WHEN** an agent reads a troubleshooting entry
- **THEN** the first-level bullet describes the problem and the second-level bullet states the solution in the form "If <problem>, then <action>."

### Requirement: Troubleshooting entries are sparse and essential
The `## Troubleshooting Guide` section SHALL include only problems an agent is likely to encounter while executing the skill. Redundant, obvious, or rarely occurring entries SHALL be omitted.

#### Scenario: Reviewing troubleshooting list length
- **WHEN** an editor reviews a skill's `## Troubleshooting Guide` section
- **THEN** every entry addresses a concrete, skill-specific execution problem and the list contains no filler items

#### Scenario: Distinguishing skill-specific from universal problems
- **WHEN** an editor reviews a candidate troubleshooting entry
- **THEN** the entry is kept only if the problem is likely to occur while executing this skill's workflow and the solution is not common knowledge that applies to any skill

#### Scenario: Distinguishing guardrails from troubleshooting
- **WHEN** an editor classifies a bullet from an old `## Common Mistakes` section
- **THEN** prohibited or required behaviors move to `## Guardrails` and problem-and-recovery items move to `## Troubleshooting Guide`

### Requirement: Troubleshooting Guide format applies to sub-pages
The system SHALL treat `## Troubleshooting Guide` as optional for active packaged Isomer command, procedure, scenario, binding, and reference pages and SHALL use it only for concrete recoverable problems specific to the page's actions.

#### Scenario: Subpage contains problem-and-recovery content
- **WHEN** an active subpage describes a likely recoverable execution problem and its corrective action
- **THEN** the guidance is organized under `## Troubleshooting Guide` with a first-level problem and a second-level solution in the form `If <problem>, then <action>.`

#### Scenario: Old bullet is a behavioral rule
- **WHEN** an old `## Common Mistakes` bullet prohibits or requires behavior rather than describing a recoverable problem
- **THEN** the bullet moves to `## Guardrails` instead of `## Troubleshooting Guide`

### Requirement: Sub-page troubleshooting is skill-specific
Every entry in a sub-page `## Troubleshooting Guide` SHALL be tightly related to the actions described by that page. Universal common-sense troubleshooting SHALL be omitted.

#### Scenario: Reviewing sub-page troubleshooting scope
- **WHEN** an editor reviews a sub-page troubleshooting entry
- **THEN** the entry is kept only if the problem is likely to occur while executing that page's workflow
