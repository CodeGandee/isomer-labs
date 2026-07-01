## ADDED Requirements

### Requirement: Topic Actor Research Recording
Research recording APIs SHALL accept records produced by Topic Actors, Project Operator Sessions, Operator Agents, or formal Agent Instances without requiring Agent Team Instance identity for human-orchestrated work.

#### Scenario: Topic Actor creates accepted artifact
- **WHEN** a Topic Actor creates or updates an accepted research artifact through `isomer-cli ext research records`
- **THEN** the recorded lifecycle row and body location include the Research Topic or Topic Workspace context, record kind, placeholder token when applicable, semantic label, profile metadata, producer metadata, `topic_actor_name`, actor kind or runtime kind when known, controller metadata when known, and optional adapter refs
- **AND** Agent Team Instance, Agent Instance, and formal Agent Workspace refs remain absent unless the record was actually produced inside a launched team context

#### Scenario: Topic Actor records remain queryable with team records
- **WHEN** a later skill queries research records for the selected Topic Workspace
- **THEN** records created by Topic Actors are returned alongside records created by Operator Agents, Execution Adapters, Agent Instances, or Service Agent Instances when they match the same topic, placeholder, record kind, profile, semantic label, producer, or topic actor filters

#### Scenario: Formal adoption is out of scope
- **WHEN** a caller asks to adopt Topic Actor-produced work into a formal Agent Instance or Agent Team Instance identity
- **THEN** the system reports that formal adoption is unsupported by this change
- **AND** it preserves the original Topic Actor production metadata instead of rewriting, copying, or linking it as formal team output
