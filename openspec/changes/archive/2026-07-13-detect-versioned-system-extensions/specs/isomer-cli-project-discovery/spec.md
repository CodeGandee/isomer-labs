## ADDED Requirements

### Requirement: Project Initialization Reports Extension Installation Advice
Project initialization SHALL inspect deterministic Project-local system-skill installation artifacts and report target-specific extension observations without recording operator system-extension declarations.

#### Scenario: Initialization finds a compatible Project-local extension
- **WHEN** `isomer-cli project init` finds a valid target-root receipt and complete compatible extension under a Project-local agent skill root
- **THEN** initialization reports the target, extension id, detected version state, declaration advice, and supporting receipt path
- **AND** the generated Project Manifest does not automatically add the extension to `[operator.system_extensions]`

#### Scenario: Different Project-local targets have different extensions
- **WHEN** initialization observes different extension sets or versions under Claude Code, Kimi Code, and generic roots
- **THEN** it reports each target independently
- **AND** it does not select an operator target or derive one Project-wide installed state

#### Scenario: Initialization finds no installation artifacts
- **WHEN** no deterministic Project-local target contains an Isomer installation receipt or recognizable packaged extension projection
- **THEN** initialization completes normally with an empty extension observation list
- **AND** core Project initialization behavior is unchanged

#### Scenario: Initialization finds obsolete or partial installation
- **WHEN** a Project-local target contains an obsolete, unversioned, malformed, drifted, or partial extension installation
- **THEN** initialization completes unless another Project initialization requirement fails
- **AND** it reports repair advice without modifying the target root
