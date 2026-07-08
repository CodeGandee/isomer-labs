## MODIFIED Requirements

### Requirement: Strengthening Remains Project-Local and Generic
The strengthened guidance SHALL remain generic to GPU kernel analytical modeling and project-local to the Toolbox directory.

#### Scenario: No packaged skill changes
- **WHEN** the change is implemented
- **THEN** packaged system skills remain unchanged
- **AND** GPU analytical modeling guidance lives under `skillset/toolboxes/gpu-analytical-modeling/`

#### Scenario: No topic-specific hard-coding
- **WHEN** the strengthened guidance uses examples
- **THEN** examples may name common GPU components but must not require a specific kernel, GPU SKU, private topic path, cross-host setup, paper artifact, host, environment setup, or topic-specific artifact as general Toolbox context
