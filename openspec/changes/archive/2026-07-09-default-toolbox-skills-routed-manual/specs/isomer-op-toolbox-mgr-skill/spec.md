## ADDED Requirements

### Requirement: Toolbox Manager Defaults Toolbox Skills to Routed or Manual Invocation
The Toolbox Manager skill SHALL author and describe Toolbox skills as routed or manually invoked surfaces by default, not as implicitly auto-invoked skills.

#### Scenario: Source scaffolding includes non-implicit metadata
- **WHEN** `isomer-op-toolbox-mgr` authors a Toolbox skill directory with `SKILL.md`
- **THEN** it also authors or recommends `agents/openai.yaml`
- **AND** that metadata sets `policy.allow_implicit_invocation` to `false`

#### Scenario: Default prompt names routed and manual use
- **WHEN** Toolbox Manager scaffolds or documents `agents/openai.yaml` for a Toolbox skill
- **THEN** the default prompt says to use the skill when routed by a Toolbox callback prompt or manually invoked for its named purpose
- **AND** it does not describe ordinary implicit auto-invocation as the default behavior

#### Scenario: Prompt-file router is preferred
- **WHEN** Toolbox Manager authors a callback that should apply a Toolbox skill subcommand
- **THEN** it prefers a short prompt-file callback that names the installed Toolbox skill, subcommand, and purpose
- **AND** it keeps reusable behavior in the Toolbox skill subcommand rather than duplicating it in the callback prompt

#### Scenario: Skill-directory callback is explicit exception
- **WHEN** Toolbox Manager uses a `skill_dir` callback source
- **THEN** it labels that source as supplemental instruction material
- **AND** it does not claim that registering the source automatically executes or implicitly invokes that skill

### Requirement: Toolbox Manager Conversion Preserves Invocation Boundary
The Toolbox Manager skill SHALL preserve the routed/manual invocation boundary when converting existing skill material into Toolbox material.

#### Scenario: Converted skill is not treated as automatic
- **WHEN** `convert-skill` converts an existing skill into Toolbox source
- **THEN** the converted Toolbox skill metadata disables implicit invocation by default
- **AND** callback declarations route to it through explicit prompt text unless the user chooses direct supplemental skill-directory material

#### Scenario: Converted callback reports invocation posture
- **WHEN** `convert-skill`, `author-toolbox`, or `insert-callback` reports created callback material
- **THEN** Essential Output includes whether the Toolbox skill is routed by prompt, manually invokable, or used as direct supplemental instruction material
