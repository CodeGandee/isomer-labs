## MODIFIED Requirements

### Requirement: Topic Initialization Subcommand
The module skill SHALL provide an `init-topic` subcommand that starts the user-facing Topic Team Specialization flow by creating provisional topic definition material before team specialization when the Research Topic is new or unclear.

#### Scenario: Missing topic prompts clarification
- **WHEN** the user invokes `init-topic` without a Research Topic or with an unclear Research Topic
- **THEN** the subcommand asks the user for enough topic information before creating any directory or topic overview file

#### Scenario: Missing topic directory uses default base for clear topic
- **WHEN** the Research Topic is clear but no topic workspace directory is supplied
- **THEN** the subcommand derives a provisional topic seed directory under the effective Topic Workspace base, normally `isomer-content/topic-ws/<topic-slug>/`, before creating topic material

#### Scenario: Default base comes from manifest or built-in layout
- **WHEN** `init-topic` derives a provisional topic seed directory
- **THEN** it uses the Project Manifest `topic_workspace_base_dir` when present and otherwise uses the built-in `isomer-content/topic-ws/` base

#### Scenario: Ambiguous derived directory prompts user
- **WHEN** the derived provisional topic seed directory already exists or would collide with registered or unrelated Project material
- **THEN** the subcommand asks the user to confirm or provide a different topic workspace directory before creating or modifying topic material

#### Scenario: Explicit topic directory still wins
- **WHEN** the user supplies a topic workspace directory explicitly
- **THEN** the subcommand uses that directory after confirming it is clear and project-scoped according to this skill's guardrails

#### Scenario: Topic overview is created
- **WHEN** the user confirms a Research Topic and topic workspace directory or the subcommand derives a clear default directory
- **THEN** the subcommand creates the directory and writes `<topic-dir>/topic-def/topic-overview.md` from the agent's understanding of the Research Topic

#### Scenario: Topic overview has required sections
- **WHEN** `topic-overview.md` is written
- **THEN** it includes sections for the Research Topic, agent understanding, scope, initial objectives, assumptions, open questions, and source prompt or source material

#### Scenario: Provisional status is reported
- **WHEN** `init-topic` creates topic material that is not registered in the Project Manifest
- **THEN** the subcommand reports that the topic directory is a provisional topic workspace seed and is not yet an authoritative Isomer Research Topic or Topic Workspace registration

#### Scenario: Project config mutation remains bounded
- **WHEN** `init-topic` needs the new topic to become an authoritative Project Manifest-registered Research Topic
- **THEN** it stops at the registration boundary or routes through a supported Isomer CLI/API path instead of hand-editing `.isomer-labs/manifest.toml`

#### Scenario: Specialization waits for explicit topic readiness
- **WHEN** `fast-forward` or `step-by-step` cannot resolve a registered Research Topic but can create a provisional seed through `init-topic`
- **THEN** the workflow reports the provisional seed and any registration blockers before proceeding to template adaptation that requires authoritative topic refs
