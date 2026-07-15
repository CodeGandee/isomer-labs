## 1. Establish Canonical Extension Artifact Identity

- [x] 1.1 Add one extension-neutral parser and validator for exact uppercase `EXTENSION-NAME:WHAT` identifiers, derive the expected uppercase namespace from the packaged manifest or installed extension catalog, and preserve the parsed uppercase value exactly.
- [x] 1.2 Replace family-specific identity parsing, constants, schema patterns, validation branches, and semantic artifact alias resolution with the canonical uppercase parser; do not case-fold, unwrap, qualify, map, or promote any rejected form.
- [x] 1.3 Make `semantic_id` the sole identity field for extension artifact create, update, revision, list, show, and query operations, remove `--placeholder` identity behavior, and return structured diagnostics for non-uppercase, bare, wrapped, wrong-family, unknown, aliased, or missing required identifiers without deriving replacements.
- [x] 1.4 Remove DeepSci placeholder derivation, lowercase semantic-id acceptance, derived identity indexing, placeholder-backed semantic filters, compatibility readers, and all code that assigns canonical identity from old metadata.
- [x] 1.5 Add unit tests for uppercase syntax, manifest ownership projection, exact round trips, invalid case, invalid wrappers, invalid aliases, invalid prefixes, strict writes, strict reads and queries, and the absence of normalization or inferred identity.

## 2. Refactor the Complete DeepSci Skill Family

- [x] 2.1 Build a checked implementation inventory of every registered DeepSci semantic object in the source and packaged skill trees, assign each exactly one `DEEPSCI:WHAT` identifier, fail on collisions or unmatched bindings, and do not ship the inventory as a runtime conversion table.
- [x] 2.2 Update all active source-tree DeepSci workflow prose, migration registries, binding pages, shared semantic guidance, generated summaries, source declarations, and command examples to exact uppercase `DEEPSCI:WHAT` identifiers without angle-wrapped, double-bracket, bare, lowercase, or mixed-case forms.
- [x] 2.3 Apply the same replacement to packaged DeepSci system-skill assets and add mirror checks that compare canonical identifier sets and relevant active guidance with the source skill tree.
- [x] 2.4 Qualify the pipeline control objects as `DEEPSCI:PIPELINE-RECIPE-CONTEXT`, `DEEPSCI:PIPELINE-TERMINAL-REPORT`, `DEEPSCI:PIPELINE-RUN-RECORD`, and `DEEPSCI:PIPELINE-RESUME-PACKET`, and update their profiles, bindings, source constants, commands, and tests to agree.
- [x] 2.5 Change every active DeepSci binding command and record-operation instruction from `--placeholder` to `--semantic-id`, delete old-form command examples and identity fixtures, and remove any instruction that converts between representations.
- [x] 2.6 Update DeepSci workspace-manager aggregation, paper-line bindings, producer and consumer references, and source-contract guidance so every durable handoff uses the same uppercase canonical identifier as its binding row.
- [x] 2.7 Add focused tests that prove all replaced registry rows have exact binding coverage, no active DeepSci skill or source declaration emits a superseded form, no fixture receives an old-form exemption, and existing method, evidence, lineage, display, and structured-payload behavior remains intact.

## 3. Establish Extension-Owned Kaoju Contract Resources

- [x] 3.1 Create `kaoju/resources/artifact-semantics.v1.json` and its schema from the current storage-neutral semantic page, including canonical uppercase `KAOJU:WHAT` identity, meaning, minimum content, producer, consumers, and update intent for every registered id.
- [x] 3.2 Copy the survey-process contract, binding registry, and binding schema into `src/isomer_labs/kaoju/resources/`, replace filesystem-valued cross-resource fields with logical `ext kaoju` query metadata, replace every artifact id with its uppercase canonical value, and preserve their schema versions and declared behavior unrelated to identity.
- [x] 3.3 Extend `src/isomer_labs/kaoju/contracts.py` with cached semantic-registry loading, exact uppercase identifier validation, schema validation, deterministic coverage diagnostics, joined semantic-binding descriptions, no semantic artifact alias resolver, and resource constants that point only to `kaoju/resources/`.
- [x] 3.4 Add unit tests that reject malformed, duplicate, missing, extra, aliased, lowercase, mixed-case, cross-registry, wrong-family, and noncanonical identifiers and prove all extension-owned resources load through `importlib.resources` outside the repository layout.

## 4. Expose Shared Resources Through `ext kaoju`

- [x] 4.1 Register context-free `process` and `bindings` groups under `isomer-cli ext kaoju` without calling Effective Topic Context resolution.
- [x] 4.2 Implement `process show` with deterministic text and JSON output, `mutated: false`, versioned process data, and logical binding-query metadata.
- [x] 4.3 Implement canonical-identifier-sorted `bindings list` summaries and joined `bindings describe KAOJU:WHAT` output with exact uppercase identity preservation and structured unknown-id, noncanonical-id, or resource-load errors without alias fallback or derived recovery.
- [x] 4.4 Route the new commands and existing `project artifacts describe`, put, and revise preflight through the same contract loaders and add parity assertions for uppercase identifiers, versions, binding fields, producer policy, scope policy, and validation expectations.
- [x] 4.5 Add CLI tests for help, text output, `--print-json`, deterministic ordering, context-free invocation, exact uppercase canonical identifiers, rejection of lowercase and aliased ids, unknown ids, and execution from outside a Project or Topic Workspace.

## 5. Refactor Kaoju Skill Guidance

- [x] 5.1 Replace the pipeline's `../contracts/survey-process.v2.json` instruction with `isomer-cli --print-json ext kaoju process show` while preserving its internal planning requirement and bundle-local `commands/` routing.
- [x] 5.2 Update `isomer-kaoju-shared` workflow and its artifact-semantic projection to query `ext kaoju bindings describe`, retain shared evidence and recording procedure locally, use exact uppercase artifact identifiers, and remove every family-root registry path.
- [x] 5.3 Update every producer-local `artifact-bindings.md` page to remain a concise bundle-local `KAOJU:WHAT` projection, identify the CLI query as authority, and remove parent-relative registry references and full command-shape duplication.
- [x] 5.4 Scan every active Kaoju skill, command page, projection, source declaration, and example to confirm exact uppercase canonical identifiers are preserved without angle wrappers, bare object names, lowercase or mixed case, or semantic artifact aliases.
- [x] 5.5 Document the skill/shared-resource classification in the packaged research-paradigm guidance, including private resources, extension-owned shared data, `<prefix>-shared` procedures, and non-authoritative local projections.
- [x] 5.6 Confirm that local links stay below the owning skill, shared data uses `ext kaoju`, common processes route to `isomer-kaoju-shared`, and no source checkout or package data path is an agent-facing dependency.

## 6. Enforce Identity and Resource Boundaries

- [x] 6.1 Extend the research-paradigm validator with the shared uppercase artifact-identity parser, manifest namespace projection, registry-to-binding coverage, source-to-package mirror comparison, and exact-file diagnostics.
- [x] 6.2 Reject angle-wrapped, double-bracket, bare, lowercase, mixed-case, wrong-family, unknown, duplicate, aliased, lossy, or `--placeholder` artifact guidance in every active source, package, command, record, and fixture context while distinguishing generic CLI metavariables, Kaoju MyST document placeholders, and passive source-provenance material.
- [x] 6.3 Add a reusable active-reference check that determines the owning skill root, rejects lexical parent traversal and sibling or family-root targets before link resolution, and reports skill, file, line, and offending reference.
- [x] 6.4 Replace the Kaoju validator's required `contracts/bindings.v2.json` literal with uppercase canonical identifier projection and `ext kaoju bindings describe` checks, and reject active instructions that name old shared JSON files as agent-readable authorities.
- [x] 6.5 Add family-specific validation that requires common Kaoju evidence, lineage, Gate, owner-routing, recording, and terminal procedure to route through `isomer-kaoju-shared` without sibling-file traversal or known full-process duplication.
- [x] 6.6 Add invalid fixtures for every superseded artifact form, wrong extension ownership, identifier collisions, semantic aliases, parent traversal, sibling links, direct contract filenames, missing extension-query routing, oversized binding authority copies, and shared-procedure bypass.
- [x] 6.7 Add valid fixtures that copy each DeepSci and Kaoju skill into an ordinary isolated directory with no symlinks or family-root contracts, use uppercase artifact identifiers only, and validate extension queries separately from bundle-local references.

## 7. Complete Package Refactor

- [x] 7.1 Update system-skill materialization tests to assert that only manifest-listed ordinary skill directories are copied, private resources remain available, uppercase canonical artifact namespaces match the owning extension, and undeclared family-root data is not treated as an implicit dependency.
- [x] 7.2 Add wheel or installed-package tests that verify all five `kaoju/resources/` files, the three new CLI queries, uppercase DeepSci and Kaoju guidance, strict rejection of every old artifact form, and flat materialized skills work without `.kimi-code` or a repository checkout.
- [x] 7.3 Remove `assets/system_skills/research-paradigm/kaoju/contracts/` after code, skill, validator, manifest, documentation, and test searches show no active dependency on it.
- [x] 7.4 Update CLI help, examples, and relevant package documentation for exact uppercase extension artifact identifiers and `ext kaoju` discovery; remove old identity options, conversion messages, alias documentation, and physical resource paths.

## 8. Validate the Completed Change

- [x] 8.1 Run targeted uppercase semantic-id, strict old-form rejection, DeepSci binding, Kaoju contract, CLI, artifact-service, system-skill materialization, and research-paradigm validator unit tests and resolve every regression.
- [x] 8.2 Run `pixi run validate-research-skills` and confirm the production Kaoju and DeepSci families pass uppercase canonical identity and resource ownership checks from flat projections.
- [x] 8.3 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`, then record any unrelated pre-existing failures separately from change failures.
- [x] 8.4 Build and inspect the distributable package to confirm uppercase canonical identifiers appear consistently, extension resources are included once, old family-root contracts and artifact identity forms are absent, and no installed command or skill depends on repository layout.
