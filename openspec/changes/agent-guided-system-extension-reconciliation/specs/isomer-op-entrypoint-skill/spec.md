## ADDED Requirements

### Requirement: Entrypoint Delegates System Skill Management
The operator entrypoint SHALL route extension detection, reconciliation, installation, status, and repair to `isomer-op-system-skill-mgr`.

#### Scenario: Extension management request selects owner
- **WHEN** the user asks to find, install, register, reconcile, inspect, or repair Isomer system-skill extensions
- **THEN** the entrypoint selects `isomer-op-system-skill-mgr`
- **AND** it proceeds through that owner rather than embedding provider-specific root discovery

#### Scenario: Extension research request uses owner evidence
- **WHEN** a concrete research request maps to an optional extension that is not already declared
- **THEN** the entrypoint delegates availability resolution and any authorized registration to the system-skill manager
- **AND** it resumes the selected research route after reconciliation succeeds

#### Scenario: Declared extension is trusted
- **WHEN** a concrete request maps to a Project-declared extension
- **THEN** the entrypoint trusts the Project declaration and attempts the selected extension route
- **AND** a later unavailable-skill failure is reported with system-skill-manager repair guidance

### Requirement: Entrypoint Does Not Encode Provider Discovery Paths
Entrypoint extension routing SHALL use Project declarations and the system-skill manager instead of hard-coded project or user-home skill roots.

#### Scenario: Entrypoint references remain provider-neutral
- **WHEN** entrypoint skill and routing references are inspected
- **THEN** they instruct the agent to use host-known roots and live inventory through the owner skill
- **AND** they do not require fixed Claude, Codex, Kimi, generic, plugin, or user-home paths as universal discovery rules
