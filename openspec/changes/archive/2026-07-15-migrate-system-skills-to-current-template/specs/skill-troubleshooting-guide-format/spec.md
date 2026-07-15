## MODIFIED Requirements

### Requirement: Troubleshooting Guide section format
The system SHALL treat `## Troubleshooting Guide` as optional for an active packaged Isomer `SKILL.md` and SHALL include it only when the skill documents concrete recoverable execution problems. When present, the section SHALL use the current two-level problem-and-solution format.

#### Scenario: Skill has known recoverable failure modes
- **WHEN** an active packaged skill documents a likely execution problem with a corrective action
- **THEN** its `SKILL.md` may include a `## Troubleshooting Guide` entry using the required problem-and-solution structure

#### Scenario: Skill has no concrete troubleshooting content
- **WHEN** an active packaged skill has no likely recoverable execution problem to document
- **THEN** its `SKILL.md` omits `## Troubleshooting Guide` instead of adding an empty or generic placeholder

### Requirement: Troubleshooting Guide format applies to sub-pages
The system SHALL treat `## Troubleshooting Guide` as optional for active packaged Isomer command, procedure, scenario, binding, and reference pages and SHALL use it only for concrete recoverable problems specific to the page's actions.

#### Scenario: Subpage contains problem-and-recovery content
- **WHEN** an active subpage describes a likely recoverable execution problem and its corrective action
- **THEN** the guidance is organized under `## Troubleshooting Guide` with a first-level problem and a second-level solution in the form `If <problem>, then <action>.`

#### Scenario: Old bullet is a behavioral rule
- **WHEN** an old `## Common Mistakes` bullet prohibits or requires behavior rather than describing a recoverable problem
- **THEN** the bullet moves to `## Guardrails` instead of `## Troubleshooting Guide`
