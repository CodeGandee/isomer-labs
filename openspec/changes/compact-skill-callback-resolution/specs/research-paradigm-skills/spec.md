## ADDED Requirements

### Requirement: Participating Research Skills Consume Compact Callback Resolution
DeepSci and Kaoju system skills that declare User Skill Callback insertion points SHALL consume the compact execution projection during ordinary workflow execution.

#### Scenario: Skill applies compact callbacks in returned order
- **WHEN** a participating research skill resolves `begin` or `end` callbacks
- **THEN** its workflow guidance tells the agent to process callback entries in their returned order
- **AND** the agent reads each reported `instruction_path` as supplemental instruction material according to its `source_type`

#### Scenario: Skill-directory callback remains supplemental
- **WHEN** a compact callback entry has source type `skill_dir`
- **THEN** the agent reads the reported `SKILL.md` entrypoint and any directly required relative resources as supplemental callback material
- **AND** it does not treat the callback directory as an installed system skill or execute its scripts solely because resolution returned it

#### Scenario: Ordinary workflow avoids explanation metadata
- **WHEN** callback resolution succeeds during a normal participating skill workflow
- **THEN** the skill does not request `--explain` or parse registry, priority, scope, status, Toolbox registration, or gating metadata
- **AND** it uses `--explain`, `list`, `show`, or `validate` only when diagnosis or management is required

#### Scenario: Empty compact resolution continues normally
- **WHEN** ordinary callback resolution returns an empty callback list
- **THEN** the participating skill continues without treating the missing callback as a blocker

#### Scenario: Callback authority remains subordinate
- **WHEN** compact callback instruction material conflicts with higher-priority instructions, the current user request, the owning skill, shared research rules, evidence discipline, required Gates, validation, or recording obligations
- **THEN** the participating skill preserves the higher-priority constraint and reports a material callback conflict

#### Scenario: Skill validation enforces compact consumption
- **WHEN** the research-paradigm skill validation harness inspects callback-participating DeepSci and Kaoju skills
- **THEN** it requires guidance for ordered compact callback consumption and instruction-entrypoint reading
- **AND** it reports ordinary workflow guidance that requests detailed explanation or depends on management-only callback fields
