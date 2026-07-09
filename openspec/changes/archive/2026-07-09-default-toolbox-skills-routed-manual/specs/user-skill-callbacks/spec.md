## ADDED Requirements

### Requirement: Toolbox Skill Routing Does Not Imply Automatic Invocation
User Skill Callback guidance SHALL keep Toolbox skill routing separate from automatic skill invocation.

#### Scenario: Prompt callback routes explicitly
- **WHEN** a callback prompt tells the active agent to invoke a Toolbox skill and subcommand
- **THEN** that instruction is treated as explicit supplemental routing under the active owning skill workflow
- **AND** the owning skill's callback application step, current user request, and higher-priority constraints remain authoritative

#### Scenario: Toolbox skill metadata can disable implicit invocation
- **WHEN** a Toolbox skill includes agent metadata with `policy.allow_implicit_invocation = false`
- **THEN** agent-host discovery should treat the skill as manually invoked or explicitly routed by instructions rather than as a normal implicit auto-selection candidate
- **AND** callback resolution still does not execute the skill automatically
