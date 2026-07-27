# Use a Minimal Publication Metadata Overlay

Publication will add root `README.md` and Git-required `.gitmodules`, while all other tracked publication-only metadata lives under reserved directory `.isomer-publication/`. The README links retained source paths and the latest eligible PDF at its path-preserved Artifact location; publication does not create a relocated `paper/latest.pdf` duplicate.

## Status

accepted

## Considered Options

- Keep root navigation minimal and place remaining generated metadata under `.isomer-publication/`.
- Put every generated file at the repository root.
- Put all generated files, including README, under the reserved overlay.
- Publish no generated navigation or verification metadata.

## Consequences

- Source-backed paths remain distinguishable from generated publication files.
- A Source Topic Workspace collision with `.isomer-publication/` blocks publication.
- A source-authored root README is sanitized in place and retains content outside a versioned generated navigation block.
- The portable index, projection manifest, and version manifest use stable paths below `.isomer-publication/`.
- Ordinary repository visitors receive immediate reproduction guidance from root `README.md`.
