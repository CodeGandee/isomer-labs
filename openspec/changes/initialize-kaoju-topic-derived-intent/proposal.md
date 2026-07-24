## Why

Kaoju topic creation currently stops after the generic Topic Creator writes `topic-overview.md` and the extension derives Mindset Sources, leaving paper-template stock to a later manual workflow and exposing the singular `intent/derived/writing-template` path. A new Kaoju topic should acquire its complete initial derived intent in one resumable operation, while missing topic-local writing templates should remain non-blocking through validated packaged defaults.

## What Changes

- Extend public Kaoju `create-topic` so that, after the generic Topic Creator establishes the Topic Workspace, Workspace Runtime, and concrete `topic.intent.overview`, the protected Kaoju topic-creation owner initializes both the three topic-owned Mindset Sources and default content and LaTeX writing-template stock.
- Make `create-topic` stop with an adjustment-oriented inventory of the actual recognized `intent/derived` materials, explaining each material's purpose, supported edits, application route, and whether it can be adjusted immediately or after later Topic Workspace use.
- Rename the built-in writing-template exchange directory from `intent/derived/writing-template` to `intent/derived/writing-templates`, while retaining the semantic label `topic.paper.template_exchange_root` and compatibility id.
- Package validated internal `content/main` and `latex/main` defaults for use as immutable seeds and runtime fallbacks.
- Make omitted/default `main` template selection non-blocking when topic-local writing-template state is absent: prefer ready topic stock, otherwise use the corresponding packaged default without silently creating topic intent.
- Preserve existing valid Mindset Sources, named template records, and writing-template exports during repeated or resumed initialization; report invalid or conflicting existing state without overwriting it.
- Preserve the existing missing-mindset behavior: missing Mindset Sources permit a Run to proceed without mindset reflection and do not cause packaged seed fallback.
- Add compatibility diagnostics and an explicit migration path for legacy singular writing-template roots. New default materialization and exports use only the plural directory.
- Route a later natural-language request to apply modified derived materials by material ownership: validate directly editable Mindset Sources, promote assessed writing-template exports through named template create or update, and redirect edits to service-generated derived files back to their source intent.
- Make derived-intent application future-facing by default. Later Runs and newly initialized paper work observe accepted changes, while active and completed Runs, Mindset Records, paper drafts, TeX snapshots, PDFs, and other historical Artifacts remain pinned unless the user explicitly scopes a separate retrospective reconciliation.
- Reconcile stale Kaoju requirements that still describe implicit mindset creation during ordinary research actions; only explicit Kaoju topic initialization or explicit repair creates missing topic-derived resources.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-mindsets`: Expand the Kaoju topic-creation owner into the complete extension-local derived-intent initializer while preserving optional missing-mindset Run behavior.
- `kaoju-paper-production`: Define packaged content and LaTeX defaults, initialization of topic template stock, ordered default selection, fallback provenance, and preservation rules.
- `kaoju-cli-services`: Add deterministic packaged-template resolution and fallback diagnostics to the typed template and paper services.
- `research-paradigm-skills`: Update public `create-topic`, protected owner, and write/build guidance to initialize and consume the complete Kaoju topic state.
- `workspace-path-resolution`: Change the built-in template exchange path to plural and define safe legacy singular-path compatibility and migration behavior.

## Impact

The change affects the semantic surface catalog, Kaoju topic-creator and writer skill assets, conversational initialization and apply routing, named-template and paper-composition services, packaged resource validation, template-selection payloads and provenance, migration diagnostics, CLI and integration tests, and user/developer documentation. Existing explicit semantic-path bindings remain authoritative. Existing unbound workspaces that contain only the legacy singular directory require compatibility detection and an explicit conflict-safe migration rather than silent data movement or merging.
