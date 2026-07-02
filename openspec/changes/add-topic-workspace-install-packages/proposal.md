## Why

Package installation requests are currently split across research skill guidance, service setup guidance, and ad hoc missing-dependency notes. A single operator-facing `install-packages` command on `isomer-admin-topic-workspace-mgr` gives agents and users one place to ask for Topic Workspace package mutation without requiring a formal schema-constrained request file.

## What Changes

- Add a public `install-packages` subcommand to `skillset/operator/isomer-admin-topic-workspace-mgr`.
- Allow `install-packages` to accept package requests from a plain user prompt, Markdown description file, YAML, JSON, requirements-style list, or copied blocker text.
- Make the subcommand infer requested packages, package kind, install route, verification checks, and blockers from flexible input.
- Install and verify packages through the selected Topic Workspace Pixi environment, using Pixi mutation and Pixi-scoped verification rather than local `venv`, ambient `pip`, `sudo`, system package managers, or unrecorded shell state.
- Route research-paradigm v2 missing package, missing runtime, and local virtualenv guidance to `$isomer-admin-topic-workspace-mgr install-packages`.
- Clarify that user-facing or cross-skill package-add requests route through the workspace manager, even when lower-level service setup policy remains relevant to Pixi command style and environment enclosure.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `topic-workspace-manager-skill`: Add flexible-intake `install-packages` as the operator-owned Topic Workspace package mutation surface.
- `research-paradigm-skills`: Require active v2 research skills to route package installation needs to `isomer-admin-topic-workspace-mgr install-packages` instead of giving direct install, `pip`, or local `venv` instructions.
- `isomer-service-env-setup-skill`: Clarify the boundary so package-add requests from users or other skills use the workspace manager surface rather than bypassing it.

## Impact

- Affects `skillset/operator/isomer-admin-topic-workspace-mgr/` by adding a subcommand reference page, updating the entrypoint, help, output contract, and guardrails.
- Affects active `skillset/research-paradigm/v2/*` guidance that currently mentions missing package installation or local virtual environments.
- May affect `skillset/service/isomer-srv-topic-env-setup/` guidance to align package mutation ownership with the workspace manager route.
- Does not require a new config file schema, a new package manager, or automatic routing to the manual `isomer-misc-tool-packs` catalog.
