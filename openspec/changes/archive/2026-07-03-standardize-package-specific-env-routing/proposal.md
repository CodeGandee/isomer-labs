## Why

Environment gate derivation and package mutation can silently choose generic PyPI, Pixi, Conda, or verification rules even when a named package has known source, variant, accelerator, or runtime caveats. We need one consistent rule: package-specific knowledge is checked first for named packages, while operational env gate derivation remains owned by the environment setup services.

## What Changes

- Define `isomer-misc-pkg-specifics` as the package-specific caveat registry for named package source choices, variant checks, verification expectations, warnings, and blockers.
- Require any operational env gate derivation, package mutation, or package-specific runtime verification to consult `isomer-misc-pkg-specifics` before generic package-source, Pixi, PyPI, Conda, or verification rules.
- Keep high-level env intent in operator skills lightweight: operators can write source intent that names tools or libraries, but topic env target-spec derivation stays with `isomer-srv-topic-env-setup`, and agent cwd target-spec derivation stays with `isomer-srv-agent-env-setup`.
- Strengthen Topic Manager ad hoc package install, update, and remove guidance so package-specific rules are checked before generic package routes.
- Clarify that `isomer-srv-agent-env-setup` consumes topic dependency planning as predecessor evidence and only consults package-specific guidance for per-agent runtime verification caveats, or routes missing topic-level dependency planning back to `isomer-srv-topic-env-setup`.

## Capabilities

### New Capabilities

- `isomer-misc-pkg-specifics-skill`: Defines the package-specific caveat registry and its lookup contract for named packages.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Requires topic env gate derivation and topic env verification to consult package-specific guidance before generic dependency and verification rules.
- `topic-manager-skill`: Requires ad hoc package install, update, remove, and verification planning to consult package-specific guidance before generic package routes.
- `isomer-agent-env-setup-service-skill`: Clarifies that agent env derivation does not duplicate topic-level dependency planning, but it must use package-specific runtime verification caveats when per-agent cwd readiness depends on a named package.

## Impact

- Updates `skillset/misc/isomer-misc-pkg-specifics` guidance and validation coverage.
- Updates `skillset/service/isomer-srv-topic-env-setup` reference pages, especially `derive-env-gate.md`, `install-topic-deps.md`, and `verify-env-gate.md`.
- Updates `skillset/operator/isomer-admin-topic-mgr` environment mutation pages for install, update, remove, and verification.
- Updates `skillset/service/isomer-srv-agent-env-setup` derivation and verification guidance to preserve topic-level dependency ownership while honoring package-specific runtime checks.
- Adds or updates tests in skill validation to reject generic package routing that bypasses `isomer-misc-pkg-specifics` for named package decisions.
