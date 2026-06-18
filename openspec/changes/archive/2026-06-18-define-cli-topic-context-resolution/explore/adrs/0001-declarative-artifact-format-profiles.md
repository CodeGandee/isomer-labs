# Declarative Artifact Format Profiles

Artifact Format Profiles are declarative-only in the first version of CLI topic context resolution. They may carry schema refs, template refs, validation hints, renderer hints, export hints, compatibility metadata, and opaque future capability refs, but they do not define executable validators, renderers, exporters, command requests, provider contracts, or adapter-specific runtime behavior.

## Status

accepted

## Considered Options

- Declarative profiles with opaque future capability refs.
- Executable validators, renderers, or exporters inside profiles.
- Removing artifact format customization from this change.

## Consequences

This keeps the Artifact Core Record generic and makes unknown profiles non-fatal. It also defers concrete validation, rendering, export, provider, sandbox, and Provenance behavior to the future Execution Adapter command surface.
