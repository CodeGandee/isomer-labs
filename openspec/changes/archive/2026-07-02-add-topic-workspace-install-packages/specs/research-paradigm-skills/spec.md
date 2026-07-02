## ADDED Requirements

### Requirement: V2 Research Skills Route Package Installation to Workspace Manager
Active research-paradigm v2 skills SHALL route package installation needs to `isomer-admin-topic-workspace-mgr install-packages` instead of installing packages directly.

#### Scenario: Missing package blocker routes to workspace manager
- **WHEN** an active v2 research skill detects missing Python, R, CLI, native, LaTeX, or scientific runtime packages needed for its selected task
- **THEN** it records the missing package or runtime as a blocker or handoff
- **AND** it routes the package addition to `$isomer-admin-topic-workspace-mgr install-packages`

#### Scenario: Research skill may provide natural-language package request
- **WHEN** a v2 research skill routes missing packages to `install-packages`
- **THEN** it may provide package names, backend, task purpose, requester skill, and desired verification checks in plain prose or Markdown
- **AND** it does not require a schema-constrained request file

#### Scenario: Research skill does not issue direct install commands
- **WHEN** active v2 research skill guidance is inspected
- **THEN** it does not instruct agents to run direct package installation commands such as ambient `pip install`, `install.packages()`, `conda install`, `uv pip install`, or local package-manager mutation from the research skill
- **AND** it does not ask the user for permission to install dependencies directly from the research skill

#### Scenario: Research skill does not create local virtual environments
- **WHEN** active v2 research skill guidance is inspected
- **THEN** it does not instruct agents to create a local `venv`, `.venv`, or `virtualenv` to satisfy missing package needs
- **AND** it routes the package need to `isomer-admin-topic-workspace-mgr install-packages` instead

#### Scenario: Research execution resumes after workspace install
- **WHEN** `install-packages` reports installed or already-present packages with passing verification
- **THEN** the research skill may rerun its package or runtime check
- **AND** it still records a blocker when the workspace manager reports blocked, failed, or deferred package setup

### Requirement: Nature Companion Package Guidance Uses Workspace Manager
Nature-facing v2 companion skills SHALL keep backend and output discipline while routing package setup to the workspace manager.

#### Scenario: Nature figure R backend does not self-install
- **WHEN** `isomer-rsch-nature-figure-v2` selects the R backend and required R packages are missing
- **THEN** it stops before rendering and routes the missing R package request to `$isomer-admin-topic-workspace-mgr install-packages`
- **AND** it does not provide `install.packages()` commands as the installation route

#### Scenario: Nature figure Python backend does not self-install
- **WHEN** `isomer-rsch-nature-figure-v2` selects the Python backend and required Python plotting packages are missing
- **THEN** it stops before rendering and routes the missing Python package request to `$isomer-admin-topic-workspace-mgr install-packages`
- **AND** it does not create a local virtual environment or run ambient `pip`

#### Scenario: Nature paper2ppt does not create a local venv
- **WHEN** `isomer-rsch-nature-paper2ppt-v2` needs Python packages to build or verify an editable PPTX deck
- **THEN** it routes the package request to `$isomer-admin-topic-workspace-mgr install-packages`
- **AND** active reachable guidance does not tell the agent to create a local virtual environment for those packages

#### Scenario: Science package checks remain checks
- **WHEN** `isomer-rsch-science-v2` checks package, executable, module, container, license, or backend availability
- **THEN** it records availability evidence or blockers
- **AND** any desired package installation route is `$isomer-admin-topic-workspace-mgr install-packages`
