## Context

The packaged Kaoju extension declares fourteen independent skill directories in `assets/system_skills/manifest.toml`, but its canonical survey-process and binding JSON files currently live in an undeclared sibling `kaoju/contracts/` directory. Repository projections use symlinks, so parent-relative references resolve during local development even though normal materialization copies only manifest-listed skill directories.

The research extensions also expose one concept through incompatible artifact identity conventions. Kaoju registries, skills, Python services, and CLI operations use lowercase extension-qualified identifiers such as `kaoju:survey-contract`. Active DeepSci skills use angle-wrapped upper-snake placeholders such as `<MAIN_RUN_RECORD>`, two double-bracket placeholder grammars, a hard-coded `deepsci:` derivation in the query index, and four pipeline control ids that are not qualified at all. The current validator has separate regular expressions and parsing branches for these forms.

The domain language treats Artifacts as durable file or file-backed outputs and treats system-owned schemas as built-in artifacts queried and validated through `isomer-cli`. This design gives every extension artifact one manifest-owned semantic identity, applies the skill/shared-resource boundary to shared extension contracts, and retains `isomer-kaoju-shared` as the owner of common human and agent procedure.

## Goals / Non-Goals

**Goals:**

- Use exact uppercase `EXTENSION-NAME:WHAT` identifiers for extension artifacts in active skill prose, registries, binding pages, generated summaries, CLI arguments and responses, schemas, tests, source constants, and record operations.
- Refactor all active DeepSci and Kaoju artifact references, including older DeepSci skill registries and pipeline control artifacts, rather than adding a wrapper, display form, normalization rule, or translation convention.
- Remove parsing, derivation, aliasing, indexing, querying, and write behavior for angle-wrapped, double-bracket, bare, lowercase, or mixed-case artifact identities.
- Make every materialized Kaoju and DeepSci skill valid as an ordinary standalone directory.
- Give agents stable, versioned, context-free CLI queries for shared Kaoju process, semantic, and binding data.
- Preserve one canonical Kaoju loader for CLI discovery and topic-scoped Artifact operations.
- Keep one-skill procedures and projections bundle-local, and keep cross-skill procedures in the matching `<prefix>-shared` skill.
- Make validation fail on identity and layout assumptions that currently pass only because of family-specific parsing or repository symlinks.

**Non-Goals:**

- Migrate, normalize, or preserve records authored with superseded artifact identity forms; those forms are outside the supported contract after this change.
- Preserve angle-wrapped, double-bracket, bare, lowercase, or mixed-case artifact identifiers on any active identity surface.
- Redesign Artifact core fields, Kaoju binding fields, content profiles, or the Artifact storage model.
- Remove or rename `project artifacts describe`, `put`, `revise`, `latest`, `list`, or `show`.
- Move deterministic paper or wiki behavior into skills.
- Treat the physical Python package data path as a public API.

## Decisions

### Use One Canonical Extension Artifact Identifier

Every active extension artifact identifier will use this durable semantic-id shape:

```text
EXTENSION-NAME:WHAT
```

Both segments use ASCII uppercase letters, digits, and single hyphens between non-empty components. The extension segment must equal the uppercase projection of the `extension_id` from the owning packaged system-skill group; the manifest value and CLI extension command remain lowercase. The object segment names the artifact's durable research meaning rather than its storage profile, path, record kind, or producing skill. Examples include `DEEPSCI:MAIN-RUN-RECORD`, `DEEPSCI:EXPERIMENT-CONTRACT`, and `KAOJU:SURVEY-CONTRACT`.

The exact grammar is `^[A-Z0-9]+(?:-[A-Z0-9]+)*:[A-Z0-9]+(?:-[A-Z0-9]+)*$`. Underscores, repeated or edge hyphens, whitespace, wrappers, and any lowercase character are invalid.

The same exact string will appear in skill prose, local binding projections, machine registries, source constants and schemas, CLI requests and responses, record metadata, validators, and tests. Markdown guidance uses inline code for readability, but the backticks are presentation markup and are not part of the identifier. Shell examples pass the identifier directly without angle brackets.

Uppercase makes identifiers visually distinct from ordinary prose while retaining a shell-safe and JSON-safe string. An alternative was to keep lowercase source values and render a separate uppercase or angle-wrapped agent form. That would retain two representations, require case-changing round trips, and make skill prose disagree with stored values. One exact uppercase identifier avoids those costs.

### Apply a Clean Break to Artifact Identity

Only exact uppercase `EXTENSION-NAME:WHAT` values participate in artifact registration, binding lookup, source validation, record writes, record identity indexing, semantic-id filters, or extension queries. The parser does not case-fold input, unwrap angle tokens, expand bare names, recognize double-bracket values, or consult an alias table.

Create, update, revision, list, show, and query guidance uses values such as `--semantic-id DEEPSCI:MAIN-RUN-RECORD`. The `--placeholder` artifact-identity option, placeholder-to-semantic-id derivation, derived identity source, semantic alias resolution, and old-form query logic are removed. Invalid input receives the normal exact-syntax or ownership diagnostic; the system does not derive or suggest a converted identity from the rejected value.

The extension-neutral parser validates uppercase syntax, maps the namespace to the lowercase extension catalog only for ownership checking, and serializes the original canonical value unchanged. `artifact_family`, manifest extension ids, CLI command names, skill names, paths, and profile URIs retain their existing lowercase conventions because they are not artifact identifiers.

No old-form record conversion or read adapter is part of this change. Existing data that lacks an exact uppercase artifact identifier does not gain one through indexing or query behavior.

### Refactor the Complete Active DeepSci Skill Surface

The refactor will replace all registered DeepSci artifact identities in both the source skill tree and packaged system-skill assets. Each old upper-snake token is replaced by a `DEEPSCI:` identifier by removing its wrapper, converting underscores to hyphens, and retaining uppercase letters. The implementation inventory proves that every active semantic object receives exactly one new identity and that no old form remains; it is not a runtime conversion table.

The refactor includes active workflow prose, migration registries, binding pages, shared semantic guidance, pipeline control-object guidance, generated summaries, CLI examples, source constants, schemas, tests, and validator fixtures. The four bare pipeline ids become `DEEPSCI:PIPELINE-RECIPE-CONTEXT`, `DEEPSCI:PIPELINE-TERMINAL-REPORT`, `DEEPSCI:PIPELINE-RUN-RECORD`, and `DEEPSCI:PIPELINE-RESUME-PACKET`. Active binding commands use `--semantic-id`; no active DeepSci instruction or source path accepts another artifact form.

Migration-oriented filenames may remain as bundle organization, but they do not grant runtime or validation status to the values they previously contained. Every active row and consumer uses the uppercase canonical identifier.

### Classify Resources by Consumer and Purpose

The canonical owner follows the resource's consumers and semantics, not its current directory.

| Resource Class | Canonical Owner | Agent Access |
| --- | --- | --- |
| Resource or procedure used by one skill | Owning skill directory | Descendant-relative local reference |
| Machine-readable data used by several skills or package services | Extension implementation package | `isomer-cli --print-json ext <prefix> ...` |
| Procedure used by several skills in one family | `<prefix>-shared` skill | Skill invocation or routing by name |
| Per-skill summary generated from shared data | Owning skill directory | Local projection followed by a CLI query for authority |

This classification keeps pipeline command pages local because only the pipeline dispatches them. It keeps evidence, lineage, Gate, owner-routing, and terminal procedure in the family shared skill. It treats survey-process, artifact-semantic, and binding registries as shared machine data when skills, validators, and Python services all consume them.

An alternative was to copy every shared JSON file into every consuming skill. That would make each directory self-contained but create several authorities and drift-prone update work. Another alternative was to materialize each research family root as one monolithic bundle. That would contradict the manifest's independent skill units and prevent standalone skill installation.

### Store Canonical Kaoju Data with the Extension Implementation

Canonical Kaoju data will move to `src/isomer_labs/kaoju/resources/`:

- `survey-process.v2.json`
- `artifact-semantics.v1.json`
- `artifact-semantics.v1.schema.json`
- `bindings.v2.json`
- `bindings.v2.schema.json`

`contracts.py` will continue using `importlib.resources`, but its constants will point to `kaoju/resources/`. The semantic registry will hold storage-neutral meaning, minimum content, producer, consumer, and update intent. The binding registry will retain physical declarative fields. Both registries use exact registered `KAOJU:WHAT` identifiers.

The survey-process document will replace `binding_registry_resource` and any other filesystem locator with logical query metadata for `ext kaoju bindings list` and `describe`. Internal schemas remain package resources used by the loader; agents receive validated projections rather than schema paths.

An alternative was to leave the data below `assets/system_skills` and hide it behind CLI commands. That would prevent direct agent access but retain the wrong ownership and invite future skill-relative coupling. Package resources under `isomer_labs.kaoju` make the extension service the explicit owner.

### Add Three Context-Free Kaoju CLI Queries

The Kaoju command tree will add:

- `isomer-cli --print-json ext kaoju process show`
- `isomer-cli --print-json ext kaoju bindings list`
- `isomer-cli --print-json ext kaoju bindings describe KAOJU:SURVEY-CONTRACT`

These commands will not call Effective Topic Context resolution. They will emit the normal CLI envelope with `ok`, `mutated: false`, an operation id, version metadata, and deterministic data. `process show` returns the normalized process contract. `bindings list` returns an artifact-identifier-sorted compact inventory. `bindings describe` joins one semantic entry with its complete declarative binding. Only an exact registered uppercase identifier resolves; an unknown or noncanonical identifier returns a structured error.

The existing `project artifacts describe` remains available for topic-scoped Artifact work. Both command families use `load_contract()`, `load_semantic_registry()`, and `load_binding_registry()` without an artifact-identity alias resolver. The extension queries discover shared data; project Artifact commands perform or prepare topic-scoped operations.

### Keep Local Projections Non-Authoritative

Each producer may retain a bundle-local binding page because the page selects the small set of artifact identifiers relevant to that skill. The page will remove the parent-relative registry path, identify itself as a convenience projection, and direct current resolution to `ext kaoju bindings describe` or the applicable extension query. Shared readable projections identify the extension query rather than a source file as authority.

The Kaoju pipeline will replace its direct contract read with `ext kaoju process show`. Shared workflow guidance will query `ext kaoju bindings describe` before invoking topic-scoped `project artifacts` commands. No skill will link into another skill's directory.

### Validate Identity, Logical Boundaries, and Flat Projections

The validation code will use the shared artifact-identity parser for active DeepSci and Kaoju guidance. It will reject angle-wrapped, double-bracket, unqualified, lowercase, mixed-case, wrong-family, unknown, duplicated, or non-round-tripping identifiers without old-form fixture exemptions. It will compare active skill references, per-skill registries, binding projections, package registries, profile declarations, source constants, and generated summaries.

Resource validation will determine the owning skill root, parse active local references, normalize path components without following links, and reject parent traversal or sibling and family-root targets. Kaoju-specific checks will reject active mentions of the old shared JSON filenames as agent-readable authorities and require the applicable `ext kaoju` query.

Tests will materialize each selected skill into a temporary ordinary directory with no family-root contracts and no source-link preservation. Separate tests will run extension queries from outside the repository layout and compare their results with shared loaders and topic-scoped Artifact operations. Wheel or installed-package tests will confirm that all extension resources are included and active skill guidance uses canonical identifiers.

## Risks / Trade-offs

- [Risk] The DeepSci refactor touches hundreds of registry and binding rows, workflow references, and mirrored files. → Generate a deterministic replacement inventory, fail on collisions or uncovered references, and compare source and packaged mirrors before deleting old active forms.
- [Risk] Old callers and records no longer participate in artifact-identity operations. → Document the release as breaking, remove old options and derivation code together, and test that every noncanonical form fails instead of entering a mixed mode.
- [Risk] A lowercase manifest extension id and an uppercase registry namespace can drift. → Derive the expected namespace mechanically from the packaged manifest and validate every registered and active artifact identifier against it.
- [Risk] Agents cannot query shared data if a skill bundle is installed without the required `isomer-cli` version. → Skill metadata and installer preflight state the minimum version; no repository fallback is allowed.
- [Risk] Bundle-local summaries drift from canonical registries. → Validation compares their identifiers and producer ownership with the package registry while the pages state that CLI results are authoritative.
- [Risk] Joining semantic and binding data changes `describe` output as registries evolve. → Each response includes schema versions, and contract tests pin required fields while allowing additive fields.
- [Trade-off] `project artifacts describe` and `ext kaoju bindings describe` overlap in returned data. → They intentionally share one loader but serve different context boundaries.

## Implementation Plan

1. Introduce the extension-neutral uppercase artifact-identity parser and validator and derive namespace ownership from the packaged manifest without case-normalizing accepted values.
2. Build and validate a complete DeepSci replacement inventory, then update source and packaged skill registries, binding pages, active prose, pipeline control artifacts, generated summaries, source constants, schemas, CLI examples, and fixtures to exact `DEEPSCI:WHAT` values.
3. Make `semantic_id` the only extension artifact identity in research-record operations and remove `--placeholder`, placeholder derivation, derived identity indexing, lowercase acceptance, and semantic artifact aliases.
4. Add the Kaoju extension-owned resource directory, create the semantic registry and schema, move the survey-process and binding documents, update logical links, and point the shared loader to the new package resources.
5. Add context-free Kaoju process and binding CLI groups with deterministic JSON and text output, exact uppercase identifier handling, and structured resource-load failures.
6. Update the Kaoju pipeline, shared skill, semantic projection, and every producer binding page to use the new query surfaces and remove parent-relative or absolute contract paths.
7. Replace family-specific identifier and path-literal validator rules with canonical identity, ownership, and query-routing checks; add flat projection and installed-package fixtures for both research families.
8. Remove the old Kaoju family-root contracts after no active code, skill, test, or manifest refers to them and run the full package, research-skill, lint, type, and test suites.

Rollback is limited to reverting the complete code-and-asset change before release. The design does not define a mixed-mode runtime, dual-write period, identity translation, or data rollback between old and uppercase identifiers.

## Open Questions

None. The uppercase artifact syntax, clean-break boundary, resource classes, canonical owners, command names, and implementation order are fixed by this change.
