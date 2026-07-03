## ADDED Requirements

### Requirement: Topic Manager Package Mutation Uses Package Specifics First
The Topic Manager environment mutation commands SHALL consult `isomer-misc-pkg-specifics` for every named package before applying generic install, update, remove, source-selection, or verification rules.

#### Scenario: Package install checks package-specific guidance first
- **WHEN** `env-install-packages` receives a named package request
- **THEN** it checks `isomer-misc-pkg-specifics` before choosing a generic PyPI, Pixi, Conda, R, CLI, runtime-wiring, or verification route
- **AND** it records selected package-specific evidence or `no package-specific rule` in the install plan

#### Scenario: Package update checks package-specific guidance first
- **WHEN** `env-update-packages` receives a named package update, downgrade, or constraint request
- **THEN** it checks `isomer-misc-pkg-specifics` before choosing a generic update route
- **AND** it preserves package-specific variant, accelerator, runtime, compatibility, and verification expectations in the update plan

#### Scenario: Package removal checks package-specific risk first
- **WHEN** `env-remove-packages` receives a named package removal request
- **THEN** it checks `isomer-misc-pkg-specifics` for known runtime, accelerator, or companion-package caveats before planning removal
- **AND** it reports package-specific breakage risks, verification checks, or blockers before mutation

#### Scenario: Package-specific verification outranks generic import checks
- **WHEN** an environment mutation command verifies a package with package-specific runtime guidance
- **THEN** it uses the package-specific verification expectation
- **AND** it does not report ready from solver success, package metadata, or generic import success alone when the package-specific rule requires stronger evidence

### Requirement: Topic Manager Package Mutation Keeps Topic Workspace Pixi Ownership
The Topic Manager package mutation commands SHALL continue to mutate only the selected Topic Workspace Pixi environment and SHALL NOT route ad hoc package mutation to full topic env setup unless the user asks for full gate-driven setup.

#### Scenario: Ad hoc package request stays in topic manager
- **WHEN** a user asks only to install, update, remove, repair, or verify named packages for an initialized Topic Workspace
- **THEN** Topic Manager handles the request through the matching `env-*` command
- **AND** it uses package-specific guidance as a preflight before generic package planning

#### Scenario: Full gate setup still routes to topic env service
- **WHEN** a package request requires deriving or repairing `topic.env.topic_setup_target_spec` from `topic.intent.topic_env_requirements`
- **THEN** Topic Manager routes full gate-driven setup or repair to `isomer-srv-topic-env-setup`
- **AND** it does not derive the operational topic env target spec itself
