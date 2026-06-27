## ADDED Requirements

### Requirement: Service Environment Setup Treats Tmp as Local Disposable
The service environment setup skill SHALL keep resolved `topic.tmp` in the baseline ignore policy and describe it as local disposable material rather than durable setup output.

#### Scenario: Topic Workspace environment setup ignores tmp
- **WHEN** Topic Workspace environment setup mutates the selected Topic Workspace
- **THEN** the owning Topic Workspace `.gitignore` ignores the resolved `topic.tmp` default path

#### Scenario: Setup output does not depend on tmp
- **WHEN** the service environment setup skill reports changed files, readiness evidence, dependency plans, verification logs, or blockers
- **THEN** it does not treat files under resolved `topic.tmp` as durable evidence unless they have been promoted to an approved durable path

#### Scenario: Temporary setup files stay local
- **WHEN** environment setup needs disposable intermediate files
- **THEN** the skill uses resolved `topic.tmp` or another explicitly temporary path and reports that the material is local and ignored
