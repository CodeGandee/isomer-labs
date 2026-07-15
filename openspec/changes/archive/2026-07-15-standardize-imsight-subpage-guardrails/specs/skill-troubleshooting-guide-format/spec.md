## ADDED Requirements

### Requirement: Troubleshooting Guide format applies to sub-pages
Every subcommand and reference page that describes recoverable execution problems SHALL use the same two-level `## Troubleshooting Guide` format as the parent `SKILL.md`.

#### Scenario: Sub-page with problem-and-recovery content
- **WHEN** a subcommand or reference page contains problem-and-recovery guidance
- **THEN** the guidance is organized under `## Troubleshooting Guide` with first-level problems and second-level solutions

### Requirement: Sub-page troubleshooting is skill-specific
Every entry in a sub-page `## Troubleshooting Guide` SHALL be tightly related to the actions described by that page. Universal common-sense troubleshooting SHALL be omitted.

#### Scenario: Reviewing sub-page troubleshooting scope
- **WHEN** an editor reviews a sub-page troubleshooting entry
- **THEN** the entry is kept only if the problem is likely to occur while executing that page's workflow
