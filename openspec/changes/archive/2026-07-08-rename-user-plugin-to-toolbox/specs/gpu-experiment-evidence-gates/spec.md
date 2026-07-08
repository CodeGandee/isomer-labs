## MODIFIED Requirements

### Requirement: Experiment Gate Guidance Remains Generic and Project-Local
The strengthened guidance SHALL remain generic to GPU kernel analytical modeling and project-local to the Toolbox directory.

#### Scenario: No packaged skill changes
- **WHEN** the change is implemented
- **THEN** packaged system skills remain unchanged
- **AND** GPU analytical modeling guidance lives under `skillset/toolboxes/gpu-analytical-modeling/`

#### Scenario: No topic-specific hard-coding
- **WHEN** the strengthened guidance uses examples
- **THEN** examples may name generic GPU evidence roles and hardware components but must not require a specific kernel, GPU SKU, topic workspace, host setup, command wrapper, profiler command, paper venue, paper artifact, or artifact path as general Toolbox context
