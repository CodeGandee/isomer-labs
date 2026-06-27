## ADDED Requirements

### Requirement: Semantic Project-local Artifact Locators
Research Recording Contracts SHALL preserve semantic surface evidence for project-local file-backed Artifacts and Provenance-linked files.

#### Scenario: Artifact locator stores semantic surface evidence
- **WHEN** an Artifact is recorded for a project-local file under a resolved semantic surface
- **THEN** the durable record stores or links the semantic label, scope ref, Path Plan id when available, and relative path beneath the resolved surface instead of relying only on an absolute path

#### Scenario: Provenance file ref stores semantic surface evidence
- **WHEN** a Provenance Record or linked support record references a project-local file produced by a command, service, adapter, or Agent Instance
- **THEN** the durable reference stores or links semantic path evidence before the file becomes part of durable research state

#### Scenario: External locator remains explicit
- **WHEN** an Artifact points outside accepted Project or Topic Workspace semantic surfaces
- **THEN** the recording API stores it as an external or adopted locator with explicit provenance rather than pretending it is covered by Workspace Path Resolution

#### Scenario: Tmp path cannot become durable locator directly
- **WHEN** a caller tries to record a file under `topic.tmp`, `topic.repos.main.tmp`, `agent.tmp`, or another disposable semantic surface as a durable Artifact or Provenance file
- **THEN** validation rejects the dependency until the file is promoted or copied to an accepted durable semantic surface
