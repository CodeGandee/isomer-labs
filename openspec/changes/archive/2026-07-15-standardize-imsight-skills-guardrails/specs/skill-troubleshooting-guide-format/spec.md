## ADDED Requirements

### Requirement: Troubleshooting Guide section format
Every Imsight skill SHALL include a `## Troubleshooting Guide` section in its `SKILL.md` file when the skill's workflow can encounter recoverable execution problems.

#### Scenario: Skill with known failure modes
- **WHEN** a skill has common execution problems that an agent can recover from
- **THEN** the skill's `SKILL.md` includes a `## Troubleshooting Guide` section

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
