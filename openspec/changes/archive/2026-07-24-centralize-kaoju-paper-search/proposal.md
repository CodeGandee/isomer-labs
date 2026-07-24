## Why

Kaoju currently describes paper lookup, seed expansion, and citation routes across `discover`, survey procedures, and shared provider contracts without one focused workflow owner or bundled retrieval approach. Centralizing these workflows will give agents one action-oriented paper-search capability while preserving provider-neutral Kaoju language and existing evidence boundaries.

## What Changes

- Add protected capability `isomer-kaoju-paper-search` as the single Kaoju owner for paper identity lookup, topic search, citing-paper search, cited-paper exploration, bounded citation-neighborhood traversal, and adjacent-paper search.
- Route paper-specific retrieval from `isomer-kaoju-discover` and applicable survey procedures through the new capability while leaving discovery strategy, candidate disposition, reading-list composition, and `KAOJU:DISCOVERY-LEDGER` persistence with `discover`.
- Define provider-neutral paper-search actions and normalized result, bound, completeness, provenance, and evidence-use contracts.
- Bundle Semantic Scholar (S2) as one paper-search approach, with API-specific endpoint, identifier, filtering, pagination, authentication, retry, redaction, and partial-result guidance kept below the action-oriented skill surface.
- Keep provider execution agent-driven through available provider-native or general-purpose CLI and HTTPS tools; do not add an S2 or literature-provider proxy to `isomer-cli`.
- Add provider-neutral `isomer-cli ext research literature` commands that validate and record normalized literature observations and query Isomer-owned local observation, paper, and citation data without provider I/O.
- Record one immutable provider-output Artifact per logical paper-search action, allow redacted raw responses only as optional file-backed attachments, and derive paper and citation-edge query rows from the normalized observation.
- Add separately versioned `isomer-literature-query-index.v1` projection tables inside Workspace Runtime while keeping the canonical `isomer-workspace-runtime.v1` contract unchanged.
- Permit future paper-search approaches to satisfy the same action and result contracts without changing Kaoju commands or domain language.
- Update the checked Kaoju process, packaged protected inventory, routing guidance, documentation, and validation tests for the new member.

## Capabilities

### New Capabilities

- `kaoju-paper-search`: Centralized action-oriented paper search, citation tracing, normalized provider observations, bounded execution, and pluggable provider approaches including S2.
- `literature-observation-data`: Provider-neutral normalized literature-observation recording, local literature queries, and separately versioned rebuildable paper and citation indexes without provider execution.

### Modified Capabilities

- `kaoju-research-extension`: Add the protected paper-search owner to the production Kaoju inventory and route paper retrieval through it.
- `kaoju-survey-intents`: Require reading-list and expansion workflows to delegate paper-specific lookup and citation traversal while retaining discovery ownership of selection and durable survey outputs.
- `packaged-system-skills`: Expand the checked Kaoju protected-member inventory and installation metadata to include the new self-contained bundle.
- `research-paradigm-skills`: Extend Kaoju validation and routing coverage to the paper-search member and its bundle-local provider resources.

## Impact

The change affects packaged Kaoju skill assets, the system-skill manifest, the checked survey-process resource, protected-member routing and dependency metadata, discovery and compatibility-procedure guidance, provider-neutral research-record format assets, the `ext research` CLI, research-record query projections, Workspace Runtime derived tables, skill validation, installer and contract inventory tests, and public documentation that reports the Kaoju protected inventory. It adds no new public top-level skill or required public survey command, does not change existing Kaoju Artifact producer ownership, does not make S2 part of core Isomer schema, does not route provider requests through `isomer-cli`, and does not require a Workspace Runtime v2 migration.
