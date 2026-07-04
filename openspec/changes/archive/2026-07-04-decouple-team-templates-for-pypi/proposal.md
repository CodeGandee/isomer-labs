## Why

Isomer core currently discovers `deepsci-org` and `deepsci-mini` by deriving a repository root from `src/isomer_labs` and reading `teams/*/execplan`. That makes the PyPI package depend on repository-local content and blurs the boundary between the platform package and reusable Agent Team templates.

We want Isomer core to publish cleanly as a Python package while treating Agent Team definitions as external plugins or Team Repository content that users can list, select, register, and specialize through `isomer-cli`.

## What Changes

- **BREAKING**: Remove implicit built-in Domain Agent Team Templates from `src/isomer_labs`; `deepsci-org`, `deepsci-mini`, and future teams are no longer always available from Isomer core.
- Add a Team Repository concept with a manifest that lists available Domain Agent Team Templates and their source paths.
- Add CLI discovery/inspection/registration behavior so users can list Team Repositories, list templates from a Team Repository, select a template, and register it into a Project before specialization.
- Keep Domain Agent Team Template validation and Topic Team Specialization in Isomer core, but require template sources to come from Project registrations or configured Team Repositories.
- Add source architecture checks so `src/` does not derive repository roots, reference repo-only directories such as `teams/`, `skillset/`, `tests/`, or `openspec/`, or require local repository files at runtime.
- Clean PyPI-facing package metadata by separating runtime dependencies from development/documentation/test dependencies and using release-compatible version metadata.

## Capabilities

### New Capabilities

- `domain-agent-team-repository`: Defines external Team Repository manifests, discovery, CLI listing, template selection, and Project registration for Domain Agent Team Templates.

### Modified Capabilities

- `domain-agent-team-template-registration`: Changes template discovery from implicit core built-ins to Project registrations plus configured Team Repository templates.
- `isomer-python-module-architecture`: Tightens the source boundary so PyPI package code cannot reference repository-local directories or keep built-in Agent Team templates in core registries.

## Impact

- Affected code includes `src/isomer_labs/teams/templates.py`, CLI team-template commands, Project Manifest registration parsing, package metadata, and source architecture tests.
- Tests that expect `deepsci-org` or `deepsci-mini` to be globally built in must create or configure a fixture Team Repository instead.
- Existing Project-local template registration remains supported.
- The current repository-local `teams/` content can remain in the repository as source material for a future or fixture Team Repository, but it must not be required by `src/` at package runtime.
