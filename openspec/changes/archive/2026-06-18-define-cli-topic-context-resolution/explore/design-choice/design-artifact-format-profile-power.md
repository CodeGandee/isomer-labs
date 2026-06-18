# Artifact Format Profile Power

The accepted first-version design keeps Artifact Format Profiles declarative-only.

## Accepted Choice

Option A: Artifact Format Profiles may describe content expectations, validation hints, renderer hints, export hints, compatibility versions, and opaque future capability refs. They must not define executable validators, renderers, exporters, command requests, provider contracts, or adapter-specific runtime behavior.

## Rationale

The Artifact Core Record must stay generic and minimal, and unknown topic-specific formats must still degrade to generic Artifact handling. Executable format behavior would force command execution, provider, sandbox, trust, and Provenance decisions before the Execution Adapter command surface is designed.

## Consequences

- Research Topic Config can select topic-specific Artifact Format Profiles for expected outputs without making them runtime command contracts.
- `isomer-cli` and Research Recording Contracts can validate profile registration, compatibility metadata, core-field shadowing, and generic fallback behavior.
- Concrete validation, rendering, export, and provider behavior remains deferred to the future Execution Adapter command surface.

## Evidence

- `openspec/changes/define-cli-topic-context-resolution/design.md` keeps Execution Adapter command requests out of scope.
- `openspec/changes/define-cli-topic-context-resolution/specs/research-recording-contracts/spec.md` requires generic Artifact fallback when a profile is missing, unsupported, disabled, or unknown.
