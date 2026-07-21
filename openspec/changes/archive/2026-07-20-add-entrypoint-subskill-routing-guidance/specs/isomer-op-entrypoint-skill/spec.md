## ADDED Requirements

### Requirement: Core Entrypoint Explains Every Protected Route
The `isomer-op-entrypoint` skill SHALL provide one context-aware `When to Route Here` sentence for every protected operator, service, and shared subskill in its protected-subskill table. The sentences SHALL convert the existing category labels into actionable selection conditions while preserving owner and delegation boundaries.

#### Scenario: Core protected inventory is inspected
- **WHEN** `isomer-op-entrypoint/SKILL.md` is inspected
- **THEN** all 20 protected-member rows contain one routing sentence
- **AND** the existing member names, logical ids, areas, and internal designators remain unchanged

#### Scenario: Project and Topic lifecycle routes overlap
- **WHEN** a request could relate to Project lifecycle, blank-state Research Topic setup, initialized Research Topic management, or formal Topic Agent Team specialization
- **THEN** the applicable routing sentences distinguish `project`, `topic-create`, `topic-manage`, and `topic-team` by lifecycle state and requested outcome

#### Scenario: Service or shared support is considered
- **WHEN** a task may require environment, package repository, Houmao, Topic Service Agent, bounded-run, NVIDIA, package-specific, Tool Pack, research-idea, or Operation Set support
- **THEN** the routing sentences identify the bounded support condition without replacing the normal operator-owner route

#### Scenario: Public command and protected member share a name
- **WHEN** the table explains a protected member such as `gui`
- **THEN** the sentence does not change the distinction between the bare protected designator and the parenthesized public subcommand designator
