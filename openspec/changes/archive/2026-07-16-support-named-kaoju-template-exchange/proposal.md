## Why

Kaoju currently exports actor-editable MyST templates to versioned `exports/kaoju-paper/...` directories and scopes canonical templates by paper line, while the intended protocol uses a flat namespace of named templates in the topic database and stable editable copies under `intent/derived/writing-template/<template-name>/`. Treating every edit as a historical revision would introduce Git-like management and storage growth that the template workflow does not need.

## What Changes

- Make `KAOJU:PAPER-TEMPLATE-MYST` a mutable named, topic-scoped canonical object stored through the artifacts database, with `main` as the default template for ordinary paper use and export when no name is supplied.
- Add low-level isomer-cli CRUD for named templates: list, show, create, update content or metadata, copy one named template to another name, replace one named template from another, and archive or delete according to reference safety.
- Keep all named templates in one flat namespace. A user or agent can preserve a state by copying it to a conventionally chosen name, but the system defines no snapshot type, snapshot flag, snapshot registry, or special snapshot lifecycle.
- Make ordinary update replace the current content or metadata of the same stable named template without automatically creating a prior-content revision. Record lightweight actor, time, source, and before-and-after digest provenance without retaining old template bytes unless an explicit named copy exists.
- Permit deterministic replacement from another known named template. Complicated reconciliation remains agentic: the agent reads the source and target, constructs a new candidate tree, and uses low-level CLI update to store it.
- Resolve the default editable copy to `<topic-workspace>/intent/derived/writing-template/<template-name>/`, including `<topic-workspace>/intent/derived/writing-template/main/` for default export.
- Keep exports non-canonical and use reserved synchronization metadata containing template name, stable record ref, state token, tree digest, and path so the agent can discover post-export edits without assuming a standard template schema.
- Define source discovery for an update request with no template name, canonical ref, template path, or export path: prefer one unambiguously edited registered export; otherwise use `<topic-workspace>/intent/derived/writing-template/main/` when it exists in the current Topic Workspace; otherwise ask the user. Multiple or invalid edited-export candidates also require clarification.
- Keep high-level template construction, conversion, reconciliation, and merge logic in Kaoju skills. Isomer-cli validates and performs explicit low-level state changes but does not infer how an arbitrary user-edited tree should become the canonical template.
- **BREAKING**: Replace the versioned default `exports/kaoju-paper/<paper-line>/vNNNN/` layout and paper-line-scoped identity with stable named working directories and template-name-scoped mutable canonical records.
- **BREAKING**: Supersede the legacy LaTeX meaning of `intent/derived/writing-template/`; directories on this surface become non-canonical MyST-oriented working copies.
- **BREAKING**: Named template updates no longer create automatic Artifact revisions. Historical recoverability exists only when a user or agent explicitly creates another named template before or after an edit.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-paper-production`: Define mutable named canonical template trees, explicit named copies, direct replacement from a named source, stable editable exports, ordered source discovery, and agentic reconciliation.
- `kaoju-cli-services`: Provide low-level named-template CRUD, copy and replacement, export inspection, state-token concurrency, and provenance without high-level arbitrary-template conversion.
- `kaoju-artifact-bindings`: Add mutable named-state behavior for canonical template trees and keep explicit saved states as ordinary records under new names.
- `research-paradigm-skills`: Teach Kaoju skills ordered unnamed-update discovery, agentic template construction and merge, explicit named-copy conventions, and low-level CLI mutation.
- `workspace-path-resolution`: Add the topic-scoped writing-template exchange surface rooted at `intent/derived/writing-template` so services and skills do not hardcode or guess its location.

## Impact

The change affects the Kaoju paper service, CLI commands and metadata, Artifact revision-mode support, binding and semantic registries, Workspace Path Resolution, tree manifests and digests, export observations, system skills, migration, documentation, and tests. Existing paper-line-scoped records require migration into the flat name namespace; one unambiguous current template becomes `main`, while distinct templates require explicit names. Existing historical revisions remain readable but new ordinary updates use mutable named state.
