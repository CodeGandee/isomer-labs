# kaoju-paper-search Specification

## Purpose
TBD - created by archiving change centralize-kaoju-paper-search. Update Purpose after archive.
## Requirements
### Requirement: Kaoju Centralizes Paper-Search Actions
The Kaoju extension SHALL provide protected capability `isomer-kaoju-paper-search` as the single workflow owner for paper identity lookup, topic search, citing-paper search, cited-paper exploration, bounded citation-neighborhood traversal, and adjacent-paper search.

#### Scenario: Paper-search capability is routed
- **WHEN** the public Kaoju entrypoint receives a direct paper-search task or a Kaoju procedure needs paper retrieval
- **THEN** it routes the bounded retrieval action to `isomer-ext-kaoju-entrypoint->paper-search`
- **AND** it does not promote the protected member as a public top-level skill

#### Scenario: Action inventory is inspected
- **WHEN** `isomer-kaoju-paper-search` guidance is inspected
- **THEN** it exposes action-oriented routes for `resolve-paper`, `search-papers`, `find-citing-papers`, `explore-cited-papers`, `trace-citation-neighborhood`, and `find-related-papers`
- **AND** its top-level workflow does not present a provider API or endpoint list as the user-facing action model

#### Scenario: Discover requests paper retrieval
- **WHEN** `isomer-kaoju-discover` needs a paper query, target-paper resolution, citation traversal, or adjacent-paper search
- **THEN** `discover` delegates that retrieval to `isomer-kaoju-paper-search`
- **AND** `discover` retains search strategy, cross-source-class coverage, candidate disposition, reading-list composition, and durable Discovery Ledger ownership

### Requirement: Paper-Search Actions Remain Provider Neutral
Paper-search actions SHALL declare research purpose, query or seed inputs, scope bounds, expected normalized fields, evidence-use intent, and Literature Provider Binding without exposing provider-specific request bodies as generic Kaoju behavior.

#### Scenario: Bound provider approach is selected
- **WHEN** a paper-search action has a valid Literature Provider Binding
- **THEN** the capability selects a compatible bundled or externally bound approach that implements the requested action
- **AND** the action and normalized result contracts remain unchanged across provider approaches

#### Scenario: User explicitly requests an approach
- **WHEN** the user explicitly requests S2 or another available provider approach
- **THEN** the capability uses that approach only when the resolved binding, credentials, Gate policy, and operation availability permit it
- **AND** it reports a blocked or scope-limited result instead of silently substituting a different provider

#### Scenario: Provider binding is missing
- **WHEN** no valid Literature Provider Binding can perform the requested external search
- **THEN** the capability reports the missing binding and may continue only with user-provided sources, accepted local Artifacts, or an explicit reduced scope
- **AND** it does not invent provider availability

### Requirement: Paper Identity and Citation Direction Are Explicit
The paper-search capability SHALL resolve target identity before graph traversal and SHALL distinguish papers that cite the target from papers cited by the target.

#### Scenario: Stable target identifier is supplied
- **WHEN** the request supplies a supported stable paper identifier or supported publication URL
- **THEN** the selected approach resolves it to normalized target metadata and records the requested and resolved identifiers
- **AND** traversal uses the resolved immutable provider identity while preserving external identifiers

#### Scenario: Title resolution is ambiguous
- **WHEN** title or metadata matching yields several plausible target papers
- **THEN** the capability presents the candidates or returns an ambiguity blocker before citation traversal
- **AND** it does not select a target solely by provider rank

#### Scenario: Forward citation trace is requested
- **WHEN** the user asks for papers that cite the target
- **THEN** the result labels the route as forward and records each provider-reported edge from a citing paper to the target

#### Scenario: Backward citation trace is requested
- **WHEN** the user asks for papers cited by the target
- **THEN** the result labels the route as backward and records each provider-reported edge from the target to a cited paper

### Requirement: Paper Searches Are Bounded and Reproducible
Every paper-search action SHALL resolve concrete bounds, pagination posture, stop conditions, and completeness reporting before claiming completion.

#### Scenario: Recent years are requested
- **WHEN** the actor requests citing papers from the most recent `N` years
- **THEN** the capability resolves `N` against the observation date into an explicit inclusive date or year range
- **AND** it records that resolved range and whether filtering occurred at the provider or after retrieval

#### Scenario: Citation neighborhood is traversed
- **WHEN** the actor requests multi-hop citation tracing
- **THEN** the capability requires or applies declared direction, depth, node, per-node result, and page bounds with one hop as the default depth
- **AND** it prevents cycles and reports the reached frontier

#### Scenario: Search reaches a bound before exhaustion
- **WHEN** a provider reports more results after a page, result, node, or resource bound is reached
- **THEN** the capability returns a truncated result with the reached bound and continuation posture
- **AND** it does not describe the result as exhaustive

### Requirement: Paper-Search Results Use One Normalized Contract
Every provider approach SHALL return normalized target, candidate, relationship, filtering, pagination, completeness, provenance, and limitation fields required by downstream Kaoju workflows.

#### Scenario: Provider returns paper candidates
- **WHEN** a paper query or traversal succeeds
- **THEN** each candidate includes provider identity, available stable external identifiers, title, authors, publication date or year, venue or source, locator, parent seed or query, route, and observation time
- **AND** the result records requested bounds, applied bounds, provider, access method, pages inspected, records inspected, retained count, searched-through date, and complete or truncated status

#### Scenario: Provider fields are missing
- **WHEN** a provider omits a requested field or returns a null paper or edge record
- **THEN** the normalized result preserves the missing-field or unresolved-record posture without inventing metadata
- **AND** downstream identity and selection logic can distinguish incomplete metadata from a negative finding

#### Scenario: Provider partially fails
- **WHEN** some pages or seed expansions succeed before throttling, network failure, or an invalid provider record prevents continuation
- **THEN** the capability returns the accepted partial observations with the exact failed operation, limitations, retry posture, and incomplete status
- **AND** it does not discard successful bounded work or report full completion

#### Scenario: Logical action is recorded
- **WHEN** a paper-search action completes with complete or partial normalized observations
- **THEN** the capability submits one `isomer-literature-provider-observation.v1` payload for the logical action through `isomer-cli ext research literature record`
- **AND** provider pages, paper candidates, and citation edges do not become independent canonical research records

#### Scenario: Raw provider response is retained
- **WHEN** the capability retains a provider response for diagnosis or reproducibility
- **THEN** it records the redacted response only as an optional file-backed attachment with checksum and Provenance refs
- **AND** normalized result validation and indexing do not require or parse the raw attachment

### Requirement: Semantic Scholar Is a Bundled Paper-Search Approach
The paper-search bundle SHALL include a self-contained Semantic Scholar approach for the supported paper actions without making S2 terminology part of generic Isomer domain schema.

#### Scenario: S2 approach resources are inspected
- **WHEN** the `isomer-kaoju-paper-search` bundle is materialized
- **THEN** its local references document the S2 paper detail, title or topic search, batch metadata, citation, reference, and recommendation operations needed by the declared actions
- **AND** the bundle does not require the external `imsight-paper-search` skill or another repository checkout

#### Scenario: S2 date filtering differs by operation
- **WHEN** a requested S2 operation supports the requested publication-date restriction
- **THEN** the approach applies the restriction in the provider request and records provider-side filtering
- **AND** when the selected S2 operation lacks that filter, it applies a bounded local filter and records local filtering

#### Scenario: S2 pagination is executed
- **WHEN** an S2 response indicates another offset or token
- **THEN** the approach follows pagination until the requested result bound, page bound, provider exhaustion, or terminal failure
- **AND** it records the final continuation and completeness posture

#### Scenario: S2 credentials are resolved
- **WHEN** authenticated S2 access is available
- **THEN** the approach obtains the key through the approved credential binding or non-empty `S2_API_KEY` process environment
- **AND** it does not place the key in skill files, query URLs, chat, logs, normalized results, Artifacts, or Provenance Records

#### Scenario: Agent executes the S2 approach
- **WHEN** the selected paper-search action requires an S2 provider request
- **THEN** the agent uses an available external provider-native or general-purpose CLI or bounded direct HTTPS tool according to the bundle-local approach
- **AND** it does not invoke an `isomer-cli` provider search, resolution, recommendation, citation-fetch, or reference-fetch command

#### Scenario: S2 output is normalized
- **WHEN** an external S2 tool returns provider-shaped output
- **THEN** the S2 approach maps it to the provider-neutral normalized observation before asking Isomer to record it
- **AND** `isomer-cli` does not interpret S2 response wrappers or perform the provider-specific normalization

### Requirement: Paper Search Preserves Kaoju Evidence and Owner Boundaries
Paper-search output SHALL remain provider observation until accepted by the applicable Kaoju owner and SHALL not take over discovery, acquisition, examination, or Artifact producer responsibilities.

#### Scenario: Search output feeds discovery
- **WHEN** a paper-search result participates in reading-list or direction-expansion discovery
- **THEN** `discover` applies relevance, version-family, inclusion, exclusion, duplicate, blocker, and priority judgments
- **AND** only `discover` creates or revises `KAOJU:DISCOVERY-LEDGER`, `KAOJU:READING-LIST`, or its existing catalog delta outputs

#### Scenario: Candidate needs claim-bearing use
- **WHEN** a selected search result must support or challenge a Research Claim
- **THEN** the workflow routes material access to `acquire` and source inspection to `examine`
- **AND** provider metadata alone does not receive full-text inspection or claim-bearing authority

#### Scenario: Direct search stops at provider output
- **WHEN** a user asks only for a bounded paper search without durable survey integration
- **THEN** the capability returns normalized observations, provider provenance, completeness, and limitations through the provider-output recording required by the declared evidence-use intent
- **AND** it does not create a Reading List, Discovery Ledger, Source Digest, Finding, or Evidence Item implicitly

### Requirement: Paper-Search Resources and Validation Are Self-Contained
The protected paper-search bundle SHALL contain its active action, normalized-result, provider-approach, execution, and troubleshooting guidance locally while using declared shared dependencies for family-wide contracts.

#### Scenario: Bundle is projected independently
- **WHEN** the paper-search capability is materialized through a complete pack or bounded private projection
- **THEN** its `SKILL-MAIN.md`, metadata, action pages, and directly required provider references resolve inside the projected bundle
- **AND** no active instruction traverses to a sibling path or external source checkout

#### Scenario: Top-level action boundary is validated
- **WHEN** skill validation inspects `isomer-kaoju-paper-search`
- **THEN** it requires the complete action inventory and rejects a top-level API overview, endpoint catalog, base-URL catalog, credential value, or hard-coded external checkout path
- **AND** it requires provider-specific operational details in bundle-local approach references
