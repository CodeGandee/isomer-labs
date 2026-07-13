## ADDED Requirements

### Requirement: Entrypoint Checks Effective Extension Availability
The operator entrypoint SHALL consult Project extension declarations and target-specific detection before automatically routing a request to an optional system-skill extension.

#### Scenario: Declared compatible extension routes normally
- **WHEN** the user's task maps to a Project-declared extension and detection reports that extension ready for the relevant operator target
- **THEN** the entrypoint selects the matching extension skill or pipeline
- **AND** it includes the target and compatibility basis in its routing rationale

#### Scenario: Detected compatible extension is undeclared
- **WHEN** the user's task maps to a compatible detected extension that the Project has not declared
- **THEN** the entrypoint explains that the extension is detected but undeclared
- **AND** it advises the declaration command without running it automatically
- **AND** it does not silently treat detection as Project policy

#### Scenario: Declared extension is unavailable or incompatible
- **WHEN** the user's task maps to a declared extension whose relevant target is missing, partial, unversioned, malformed, drifted, obsolete, or newer than the CLI
- **THEN** the entrypoint does not automatically invoke the extension
- **AND** it returns the detector's bounded repair or upgrade advice

#### Scenario: Explicit invocation still checks compatibility
- **WHEN** the user explicitly names an extension skill
- **THEN** the entrypoint preserves the explicit intent
- **AND** it reports and honors any compatibility blocker rather than claiming the skill is ready
