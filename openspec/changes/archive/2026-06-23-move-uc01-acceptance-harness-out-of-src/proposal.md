## Why

The completed Milestone 6 implementation proved the UC-01 path, but it put case-specific orchestration and command shape into `src/isomer_labs`. That blurs the boundary between reusable Isomer platform behavior and acceptance-test material, and it risks turning every use case into a product command or source package.

## What Changes

- Move UC-01-specific runner code, constants, deterministic fixture outputs, simulated handoff payloads, and closeout assertions out of `src/isomer_labs` and into a dedicated manual acceptance harness under `tests/manual/uc01_headless_vertical_slice/`.
- Remove the product CLI surface `isomer-cli uc01 run` and `isomer-cli uc01 inspect`; the manual harness will drive existing generic commands and reusable Python APIs instead.
- Keep only reusable Isomer core behavior in `src/isomer_labs`, including Domain Agent Team Template discovery, generic Workspace Runtime persistence, generic lifecycle record support, generic validation, generic handoff/adapter APIs, and topic config parsing.
- Preserve the UC-01 fixture Project and manual validation value, but make it test material rather than a named workflow implementation inside the package.
- Update docs, roadmap wording, and tests so Milestone 6 is described as a manual acceptance harness over generic platform APIs, not as a permanent use-case command group.
- Ensure future UC-07 and UC-06 acceptance paths follow the same harness boundary unless a later accepted spec promotes a use-case workflow into core product language.

## Capabilities

### New Capabilities

- `manual-acceptance-harness-boundary`: Defines where use-case-specific acceptance harnesses live, what they may import, and what must remain reusable core platform code.

### Modified Capabilities

- `isomer-python-module-architecture`: Add a source layout requirement that `src/isomer_labs` must not contain named use-case orchestration packages or modules unless explicitly promoted by an accepted product spec.
- `isomer-cli-project-discovery`: Clarify that public `isomer-cli` command groups expose generic platform operations, while named use-case acceptance runners belong in manual tests or external harnesses.

## Impact

- Affected source: remove `src/isomer_labs/workflows/uc01*.py` and `src/isomer_labs/cli/commands/uc01.py`; keep or extract any generic helpers into `runtime`, `houmao`, `cli`, or other accepted core packages.
- Affected tests/manual: create `tests/manual/uc01_headless_vertical_slice/` with UC-01 constants, deterministic outputs, orchestration, assertions, and live-gated validation.
- Affected tests/unit: update CLI command-surface tests, source-architecture tests, and UC-01 validation tests to target the manual harness boundary.
- Affected docs: update workflow, CLI, Houmao adapter, troubleshooting, and roadmap text so UC-01 is run through a manual harness over generic commands.
- Compatibility: removing `uc01` from `isomer-cli` is acceptable because it has not been committed or archived as a durable product command; the generic runtime records and fixture remain.
