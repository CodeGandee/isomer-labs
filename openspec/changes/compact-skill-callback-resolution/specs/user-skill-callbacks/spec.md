## ADDED Requirements

### Requirement: Compact User Skill Callback Execution Projection
The system SHALL make ordinary User Skill Callback resolution a compact agent-execution projection while preserving explicit detailed explanation for management and diagnosis.

#### Scenario: Ordinary resolution returns only actionable callback fields
- **WHEN** a caller runs `isomer-cli --print-json project skill-callbacks resolve --skill <skill-name> --stage <stage>` and one or more callbacks are active and effectively enabled
- **THEN** each callback entry contains its stable callback id, source type, and absolute instruction entrypoint path
- **AND** the response does not include callback target echoes, scope, status, priority, registry path, source aliases, source summary, Toolbox identity, Toolbox status, Toolbox registration, or gated callback ids

#### Scenario: Prompt source resolves to its readable file
- **WHEN** an active callback source type is `prompt` or `prompt_file`
- **THEN** its `instruction_path` is the absolute resolved prompt file that the agent must read

#### Scenario: Skill-directory source resolves to SKILL.md
- **WHEN** an active callback source type is `skill_dir`
- **THEN** its `instruction_path` is the absolute `<skill-dir>/SKILL.md` entrypoint
- **AND** resolution does not inline the skill body or automatically execute or install the callback skill directory

#### Scenario: External source is marked only when applicable
- **WHEN** a resolved callback uses an explicitly authorized source outside the Project root
- **THEN** its compact callback entry reports `external: true`
- **AND** internal callback entries do not carry redundant false-valued external-source metadata

#### Scenario: Compact array preserves application order
- **WHEN** multiple active callbacks match the requested skill and stage
- **THEN** the compact callback entries appear in the existing deterministic scope, priority, and stable-id application order
- **AND** the agent does not need scope or priority fields to reconstruct that order

#### Scenario: Empty resolution remains compact success
- **WHEN** no active and effectively enabled callback matches the requested skill and stage
- **THEN** ordinary resolution succeeds with an empty callback list and no management metadata

#### Scenario: Explain mode returns detailed evidence
- **WHEN** a caller runs the same resolution with `--explain`
- **THEN** the response includes full callback metadata, registry refs, source metadata, effective Toolbox status, and gated callback ids needed to diagnose resolution
- **AND** explained resolution remains read-only

### Requirement: Callback Resolution Diagnostics Are Purpose Bounded
The system SHALL keep ordinary and explained callback-resolution diagnostics limited to state that can affect the requested callback resolution.

#### Scenario: Resolution keeps relevant diagnostics
- **WHEN** Project or topic selection, a visible callback registry, the requested insertion point, a callback source, duplicate callback identity, or applicable Toolbox gating is invalid
- **THEN** callback resolution reports deterministic diagnostics for that condition
- **AND** an error that prevents trustworthy instruction selection makes the resolution unsuccessful

#### Scenario: Unrelated Project diagnostic is excluded
- **WHEN** an environment, template, profile, research-record, or other Project capability has a validation problem that cannot affect the requested callback resolution
- **THEN** ordinary and explained callback resolution omit that diagnostic
- **AND** the unrelated problem does not change the callback command exit status

#### Scenario: Dedicated validation retains broad callback inspection
- **WHEN** a user needs registry-wide callback health rather than one execution resolution
- **THEN** `project skill-callbacks validate` remains the detailed callback validation surface
- **AND** general Project health remains available through `project validate`

#### Scenario: Compact payload growth is guarded
- **WHEN** repository tests serialize empty and representative active compact resolutions
- **THEN** they enforce an exact compact-field allowlist and stable response-size ceilings

## MODIFIED Requirements

### Requirement: Toolbox Status Gates Toolbox-Installed Callbacks
The system SHALL honor effective Toolbox status when resolving callbacks installed from Toolbox manifests.

#### Scenario: Active Toolbox callback resolves normally
- **WHEN** an active callback record has `toolbox_id` metadata and the effective Toolbox status for the selected Project, Research Topic, Topic Actor, or Topic Agent context is `active`
- **THEN** callback resolution may include that callback when its target skill and stage match the request

#### Scenario: Disabled Toolbox callback is skipped
- **WHEN** an active callback record has `toolbox_id` metadata and the effective Toolbox status for the selected context is disabled
- **THEN** callback resolution excludes that callback without deleting or mutating the callback registry record

#### Scenario: Missing Toolbox registration blocks installed callback
- **WHEN** an active callback record has `toolbox_id` metadata but no applicable Toolbox registration exists
- **THEN** callback resolution excludes that callback with a deterministic diagnostic

#### Scenario: Disablement is context-specific
- **WHEN** a Toolbox is disabled for one Topic Actor or Topic Agent but remains enabled at the broader Research Topic or Project scope
- **THEN** callback resolution skips the Toolbox callbacks only for the disabled effective context and continues resolving them for other contexts where the Toolbox remains enabled

#### Scenario: Management and explained resolution expose Toolbox gating
- **WHEN** a callback list, show, validate, or `resolve --explain` command reports Toolbox-installed callbacks
- **THEN** the output includes enough Toolbox status metadata to explain whether each callback is effective or gated off for the selected context
- **AND** ordinary compact resolution returns only admitted callbacks plus any resolution-blocking Toolbox diagnostic
