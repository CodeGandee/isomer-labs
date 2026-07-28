## ADDED Requirements

### Requirement: Default Publication Preserves the Reproduction Graph
The publication layer SHALL select current intent, reproducible environment declarations, and every sanitizable typed durable research record needed to inspect evidence and reconstruct material decisions by default.

#### Scenario: Survey decision lineage exists
- **WHEN** the Source Topic Workspace contains current, superseded, rejected, failed, blocked, or accepted typed durable records linked by revision, evidence, decision, or provenance relationships
- **THEN** the publication plan selects their sanitizable structured content and relationships by default
- **AND** it does not reduce the publication to only the latest accepted outputs

#### Scenario: Reproducible environment declarations exist
- **WHEN** the Topic Workspace contains a manifest, Pixi declarations and lock, setup specifications, environment Gate records, or exact software and hardware observations
- **THEN** the plan selects the sanitizable declarations and reproducibility-relevant versions by default
- **AND** it excludes installed environments, caches, hardware serials, Workspace Runtime, and credentials

#### Scenario: Runtime database carries record state
- **WHEN** readers need a portable view of the published research lineage
- **THEN** the projection generates a sanitized research-record index with stable refs, semantic ids, revisions, states, fingerprints, and relationships
- **AND** it does not publish `state.sqlite`, runtime-only fields, absolute paths, or treat the index as canonical state

### Requirement: Raw Payload Bytes Require Explicit Selection
The publication layer SHALL distinguish default material and execution provenance from non-default raw payload bytes and SHALL include raw payload bytes only through explicit settings in the current approved Publication Plan.

#### Scenario: Downloaded material was used
- **WHEN** research records identify a downloaded paper, copied source tree, dataset, model, or related raw material
- **THEN** the default publication includes its sanitizable exact locator, version or digest, retrieval observation, access posture, license posture, and evidence relationships
- **AND** it excludes the downloaded bytes unless the plan explicitly selects raw material bytes

#### Scenario: Experiment produced raw outputs
- **WHEN** a trial or comparison produced profiler reports, raw logs, generated dataset bytes, dumps, checkpoints, or other raw execution outputs
- **THEN** the default publication includes sanitizable plans, commands, environment identity, normalized results, checksums, verdicts, and limitations
- **AND** it excludes the raw output bytes unless the plan explicitly selects raw experiment-output bytes

#### Scenario: Explicit raw-byte setting changes
- **WHEN** a raw material or raw experiment-output selection differs from the approved Publication Plan
- **THEN** the plan is stale
- **AND** synchronization requires renewed privacy, access, license, size, and remote-mutation review

### Requirement: Publication README Exposes the Latest Paper
The Topic Publication Copy SHALL always contain a generated root `README.md` with a stable latest-paper line and SHALL leave the Source Topic Workspace unchanged.

#### Scenario: Validated paper PDF exists
- **WHEN** one latest unambiguous checksummed paper PDF has accepted build and validation lineage and passes typed PDF privacy review
- **THEN** the projection publishes it at `paper/latest.pdf`
- **AND** `README.md` contains `Latest paper: [PDF](paper/latest.pdf)`

#### Scenario: Paper PDF is unavailable or ambiguous
- **WHEN** no eligible paper PDF exists or latest selection is ambiguous
- **THEN** `README.md` contains `Latest paper: not yet available.`
- **AND** the planner reports the absence or ambiguity without selecting by filename or modification time

#### Scenario: Prior paper revisions are safe
- **WHEN** prior checksummed paper PDF revisions are typed durable research outputs and pass size, license, and identity-metadata review
- **THEN** the plan may retain them with their lineage by default
- **AND** the README still points only to the latest eligible revision

### Requirement: Publication Protects Individual Identity Without Erasing Organization Provenance
The publication layer SHALL sanitize individual researcher, machine-local, network-local, and credential information while preserving credential-free organization, citation, and source provenance.

#### Scenario: Local individual identity appears
- **WHEN** content contains a local username, home path, local Git author or email, personal contact field, workstation hostname or IP address, identity-bearing actor or agent name, or hardware serial
- **THEN** the projection replaces it with an approved stable placeholder or blocks publication when safe transformation is unavailable
- **AND** source content remains unchanged

#### Scenario: GitHub repository identity appears
- **WHEN** content contains a normalized credential-free public or private GitHub repository locator, organization or owner segment, repository name, and immutable commit
- **THEN** publication preserves that repository identity as organization or source provenance
- **AND** it does not classify the owner segment as an individual-identity leak merely because it resembles a username

#### Scenario: Repository locator carries authentication
- **WHEN** a repository locator contains an embedded username, password, token, signed query, credential parameter, or fragment
- **THEN** publication blocks the locator until it is normalized to a credential-free form
- **AND** no credential-bearing value enters a plan, manifest, Git argument, generated file, or diagnostic

#### Scenario: Private repository limits access
- **WHEN** a preserved private GitHub reference is unavailable to part of the intended audience
- **THEN** the publication records an explicit access and reproduction limitation
- **AND** it does not copy private repository bytes by default or claim complete reproduction

## MODIFIED Requirements

### Requirement: Publication Selects All Available Components by Default
Each publication plan SHALL select every currently available Topic Main, registered Topic Actor Workspace, selected-team Agent Workspace, and registered GitHub reference repository resolved through read-only Isomer queries unless the user explicitly excludes that component or reference in the current plan.

#### Scenario: All current topic-owned components are available
- **WHEN** Topic Main, two registered Topic Actor Workspaces, and three selected-team Agent Workspaces resolve and exist
- **THEN** the publication plan selects all six topic-owned components by default
- **AND** each component remains subject to semantic classification, sanitization, privacy review, and current-plan approval

#### Scenario: Registered reference repositories are available
- **WHEN** canonical external repositories have registered credential-free GitHub locators and exact commits
- **THEN** the plan selects them as reference-repository submodules by default
- **AND** it records access, reachability, and license posture without copying their local checkout metadata

#### Scenario: Publication runs before components exist
- **WHEN** no topic-owned component workspace is available after Topic Workspace registration
- **THEN** the plan may produce a root-only publication with any independently registered reference repositories
- **AND** it reports unavailable expected topology without scanning directories or blocking solely because later lifecycle stages have not run

#### Scenario: Component or reference becomes available later
- **WHEN** a Topic Main, registered Topic Actor Workspace, selected-team Agent Workspace, or registered GitHub reference becomes available after an earlier plan or synchronization
- **THEN** the next plan selects it by default and treats the topology change as stale relative to the earlier plan
- **AND** publish sync requires renewed privacy and remote-mutation approval

#### Scenario: User excludes an available component or reference
- **WHEN** the user explicitly excludes an available component or reference in the current Publication Plan
- **THEN** the plan records that exclusion and omits it from the current projection
- **AND** the exclusion does not delete or mutate the Source Topic Workspace or canonical external repository

### Requirement: Publication Never Copies Source Git Metadata or History
The publication projection SHALL materialize fresh sanitized histories for topic-owned content, SHALL exclude Source Topic Workspace and topic-owned component Git control data, and SHALL represent registered GitHub references only through credential-free upstream submodules pinned to exact commits.

#### Scenario: Topic-owned Git control paths are encountered
- **WHEN** projection inventory encounters a `.git` directory, `.git` worktree file, Git config, objects, refs, reflogs, index, worktree administration data, credential helper data, or incidental source remote
- **THEN** it excludes that material from every topic-owned publication file copy and commit

#### Scenario: Topic-owned source commit contains a deleted secret
- **WHEN** topic-owned source history may contain content that is absent from the current working tree
- **THEN** publication does not reuse, import, fetch, bundle, or push that source history

#### Scenario: Sanitized topic-owned component history is fresh
- **WHEN** a topic-owned publication component is initialized
- **THEN** its commits contain only approved sanitized projection content and publication metadata

#### Scenario: Registered GitHub reference is selected
- **WHEN** a canonical external repository has an approved credential-free GitHub locator and exact commit
- **THEN** the superproject records an upstream submodule pinned to that commit
- **AND** it does not copy the local checkout or reinterpret upstream history as topic-owned publication history

### Requirement: Publication Plans Classify Every Source Path
The publish `plan` operation SHALL inventory every relevant Isomer-resolved semantic source surface, assign every considered path exactly one disposition of `track`, `template`, `exclude`, `component`, or `block`, and record the semantic publication class that caused the disposition.

#### Scenario: Publication plan records exact scope
- **WHEN** a plan is created
- **THEN** it records selected topic and workspace refs, safe Project-relative copy path, credential-safe remote, visibility acknowledgement, semantic content classes, raw-byte settings, source and output fingerprints, relative mappings, dispositions, selected components and references, transformations, reproduction limitations, conflicts, generated navigation fingerprints, expected commits, push order, blockers, and approval state
- **AND** it does not record secret values, sensitive excerpts, raw private diffs, source Git configuration, credential-bearing URLs, or publication-irrelevant absolute paths

#### Scenario: Required default surfaces exist
- **WHEN** planning encounters intent, environment declarations, typed durable research records, topic-owned components, or registered GitHub reference repositories
- **THEN** it selects their sanitizable publication forms by default
- **AND** it does not exclude them merely because they live under `records/`, use a supported typed binary format, or are canonical external repositories

#### Scenario: Private and non-default surfaces exist
- **WHEN** planning encounters Workspace Runtime, `state.sqlite`, installed environments, caches, temporary material, credentials, downloaded raw-material bytes, or raw experiment-output bytes
- **THEN** it excludes or blocks those paths unless an applicable raw-byte class has an explicit current-plan selection

#### Scenario: Risky material blocks publication
- **WHEN** planning encounters private keys, credential-like values, credential-bearing URLs, unsupported binaries, unsupported archives, excessive files, unresolved identity metadata, unresolved license or access posture, or content whose safe transformation cannot be established
- **THEN** it assigns `block`
- **AND** publish sync refuses the blocked scope

#### Scenario: Validated paper PDF is considered
- **WHEN** a checksummed paper PDF has accepted build and validation lineage and approved identity metadata
- **THEN** the planner treats it as a typed research output rather than an arbitrary unsupported binary
- **AND** size, signature, license, and privacy checks still apply

### Requirement: Nested Workspaces Become Sanitized Submodules
The Topic Publication Copy SHALL represent selected Topic Main, Topic Actor Workspace, and Agent Workspace projections as sanitized same-remote submodules and SHALL represent selected registered GitHub reference repositories as credential-free upstream submodules.

#### Scenario: Topic Main component is materialized
- **WHEN** Topic Main is selected for publication
- **THEN** its sanitized component repository uses publication branch `topic-owner/main`
- **AND** the superproject records its exact commit at the resolved Topic Main relative path

#### Scenario: Topic Actor component is materialized
- **WHEN** Topic Actor `<name>` is selected for publication
- **THEN** its sanitized component repository uses publication branch `per-topic-actor/<name>/main`
- **AND** the superproject records its exact commit at the actor's sanitized relative workspace path

#### Scenario: Agent component is materialized
- **WHEN** Agent `<name>` is selected for publication
- **THEN** its sanitized component repository uses publication branch `per-agent/<name>/main`
- **AND** the superproject records its exact commit at the agent's sanitized relative workspace path

#### Scenario: Topic-owned components use the publication remote
- **WHEN** `.gitmodules` is generated for selected Topic Main, Topic Actor, or Agent components
- **THEN** each topic-owned component uses the credential-safe user-provided publication remote, names its deterministic component branch, and is pinned by a gitlink commit

#### Scenario: Reference repository uses upstream
- **WHEN** `.gitmodules` is generated for a selected registered GitHub reference repository
- **THEN** the entry uses its normalized credential-free upstream locator and records its exact commit
- **AND** it does not name a publication component branch or copy local source Git metadata

#### Scenario: Recursive clone reports reproducibility
- **WHEN** a consumer clones `topic-workspace/main` with submodules
- **THEN** every published topic-owned component commit is reachable from its named branch in the publication remote
- **AND** every reference commit is either reachable from its recorded upstream for the intended audience or named in a recorded access limitation
