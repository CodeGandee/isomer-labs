## MODIFIED Requirements

### Requirement: Topic Workspace Pixi Layout
The service skill SHALL prepare the selected Topic Workspace Pixi layout and baseline VCS ignores needed for topic-scoped environment setup.

#### Scenario: Topic Workspace VCS ignores preserve topic tmp posture
- **WHEN** Topic Workspace environment setup mutates the selected Topic Workspace
- **THEN** the owning Topic Workspace `.gitignore` ignores the default `topic.tmp` path
- **AND** it still preserves unrelated existing ignore entries

### Requirement: Service Setup Resolves Semantic Topic Surfaces
The service environment setup skill SHALL resolve semantic Topic Workspace surfaces before setup and report their labels, sources, and blockers.

#### Scenario: Service setup reports topic tmp label when available
- **WHEN** `topic.tmp` is available through Workspace Path Resolution
- **THEN** the service output includes `topic.tmp` as local ignored disposable setup posture
- **AND** it does not treat files under `topic.tmp` as durable changed files, readiness evidence, dependency plan inputs, verification logs, or blockers unless the content has been promoted to an approved durable path

#### Scenario: Temporary setup files stay local
- **WHEN** environment setup needs disposable intermediate files
- **THEN** the skill uses resolved `topic.tmp` or another explicitly temporary path
- **AND** it reports that the material is local, ignored, disposable, not shared, and not durable evidence

### Requirement: Service Output Reports Semantic Evidence
The service environment setup skill SHALL report semantic path evidence in its output.

#### Scenario: Tmp is not durable service evidence
- **WHEN** the service reports changed files, setup commands, verification results, enclosure warnings, or next actions
- **THEN** files under resolved tmp labels are omitted from durable evidence unless they have been promoted to an approved durable path
