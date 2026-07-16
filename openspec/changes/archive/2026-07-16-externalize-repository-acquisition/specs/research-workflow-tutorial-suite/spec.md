## MODIFIED Requirements

### Requirement: Topic environment preparation tutorial
The tutorial suite SHALL teach users how to prepare a Topic Workspace environment after research intent is clear, including user-controlled or agent-controlled external repository acquisition followed by Isomer registration.

#### Scenario: Environment tutorial covers readiness checks
- **WHEN** a reader follows `docs/tutorial/prepare-topic-environment.md`
- **THEN** the tutorial explains how to prepare topic environment dependencies, capture host facts, handle proxy or dependency constraints, and verify readiness before research work begins
- **AND** for each required repository it shows how to query or choose a semantic target, run customizable repository commands outside `isomer-cli`, verify source identity, register the existing path, and preserve applicable evidence or blockers

#### Scenario: Environment tutorial preserves user command flexibility
- **WHEN** the tutorial demonstrates Git or provider-specific repository acquisition
- **THEN** it presents the commands as examples that the user may supply or the acting agent may adapt to branch, commit, sparse, partial, submodule, LFS, local-source, mirror, credential, and provider requirements
- **AND** it does not teach `project repos acquire`, a fixed depth-one policy, or Isomer-owned cleanup as the supported workflow
