## Context

The July 14 Kaoju survey-process feature defines ten user-facing use cases and ten ADRs. The accepted decisions require one selected direction set, direction-owned reading lists, state-DB discovery for every durable output, MyST as the canonical paper format, manual template exchange, derived TeX and PDF publication artifacts, a self-contained LLM Wiki export and viewer, repository ingestion, Service Request-backed environment preparation, and a separately approved source-code trial.

The current Kaoju implementation already has useful pieces: an entry pipeline, focused stage skills, an exact semantic-id vocabulary, structured record profiles, Workspace Runtime persistence, lineage, render and export support, semantic path resolution, execution extension points, and service skills for environment preparation. The ownership boundaries are inverted in several places. Skills repeat physical record commands in prose, current binding data is duplicated across semantic and per-skill files, the paper path treats LaTeX as canonical, the template CLI hardcodes a derived directory and invokes compilers directly, and environment setup is described as direct skill work rather than a recorded Service Request.

The platform language constrains the design. An Artifact Core Record remains a minimal DB index, file content remains authoritative, Artifact Format Profiles stay declarative, Project Operator Sessions and Operator Agents own user interaction, Service Team work starts from a Service Request, and executable work uses a Research Operation Extension Point and Execution Adapter Command Request. Houmao may implement an adapter or dispatch form, but no Houmao term becomes part of the Kaoju schema or public user language.

The existing `add-kaoju-paper-writing` change is partially implemented. Its audit, citation, validation, build provenance, and publication quality work remains useful. Its LaTeX-first canonical manuscript, `kaoju:writing-template`, direct template CLI, and Markdown rejection requirements conflict with ADR-0006 and are superseded by this change.

## Goals / Non-Goals

**Goals:**

- Provide one discoverable pipeline entry for all ten survey-process use cases without removing existing public procedure ids.
- Keep research selection, interpretation, claim formation, source appraisal, TeX repair, and approval decisions in agent skills.
- Put deterministic storage, path resolution, validation, conversion initialization, repository acquisition, Service Request dispatch, builds, and viewer operations behind typed CLI and service APIs.
- Register every durable output as a file-backed Artifact Core Record in the Topic Workspace state DB and make DB queries the only accepted durable-record discovery mechanism.
- Preserve revision lineage, immutable Run history, provenance, source identity, exact locators, human Gates, clarification-first behavior, and resumable stage state.
- Make MyST the only canonical paper source while providing derived Markdown, TeX, PDF, and external editing views.
- Preserve useful existing Kaoju procedures and legacy records through explicit compatibility routes and migrations.
- Keep all functionality package-owned and usable without a repository checkout or invocation of an external wiki skill.

**Non-Goals:**

- Replacing agent research judgment with a deterministic workflow engine.
- Making the CLI search literature, select survey directions, author claims, audit evidence, repair TeX semantics, or approve a governed action.
- Treating a reading-list target as proof of comprehensive coverage.
- Treating generated-data trials as paper reproduction or benchmark evidence.
- Copying external local datasets into managed storage or deleting their source directories.
- Promoting Houmao, a literature provider, a compiler, or a package manager into canonical Isomer domain language.
- Building a general-purpose wiki platform or rich browser IDE as part of this change.
- Automatically converting historical LaTeX manuscripts into authoritative MyST content.

## Decisions

### Keep the Pipeline as the Single Intent Router

`isomer-kaoju-pipeline` remains the extension entry skill and becomes a thin router. It adds ten public intent procedures while preserving the existing procedures and grouped managers.

| Use Case | Public Procedure | Capability Owners |
| --- | --- | --- |
| UC-01 | `choose-directions` | `isomer-kaoju-frame` |
| UC-02 | `build-reading-list` | `isomer-kaoju-discover` |
| UC-03 | `ingest-reading-item` | `isomer-kaoju-acquire`, then `isomer-kaoju-examine` |
| UC-04 | `draft-paper` | `isomer-kaoju-audit`, `isomer-kaoju-synthesize`, then `isomer-kaoju-write` |
| UC-05 | `manage-paper-template` | `isomer-kaoju-write` |
| UC-06 | `build-paper-pdf` | `isomer-kaoju-write` |
| UC-07 | `export-survey-wiki` | new `isomer-kaoju-export` |
| UC-08 | `ingest-source-code` | `isomer-kaoju-acquire`, then `isomer-kaoju-examine` |
| UC-09 | `prepare-code-run` | pipeline orchestration and a Service Request handled by the Service Team |
| UC-10 | `run-code-trial` | new `isomer-kaoju-trial` |

`isomer-kaoju-reproduce` narrows to genuine reproduction work. `method-trial-pass` remains a compatibility procedure that routes capability-probe and bounded-trial requests to `isomer-kaoju-trial`; a request that actually claims reproduction must satisfy the stronger reproduction contract. `paper-pass` becomes a compatibility composite over `draft-paper` and optional `build-paper-pdf`. `create-paper-template` remains callable but creates the canonical MyST template; a requested legacy TeX template is recorded only as a derived `kaoju:paper-template-tex`.

This keeps one user entry surface and focused capability owners. A second survey facade was considered and rejected because it would duplicate routing, manifest metadata, clarification behavior, and public documentation.

### Use a Single Machine-Readable Binding Authority

A new versioned Kaoju binding registry becomes the physical binding authority. The shared semantic registry continues to define storage-neutral meanings. Each binding entry declares:

- Exact semantic id and artifact type.
- Compatible core record kind and Artifact Format Profile ref.
- Default Semantic Workspace Surface Label.
- Content mode: structured file, ordinary file, directory manifest, external path, or canonical repository reference.
- Producer skill, allowed consumers, and required relationship roles.
- Revision mode: current state, append-only event, immutable Run, or derived view.
- Scope key policy and latest-selection policy.
- Acceptance, validation, audit, and Gate requirements.

Per-skill `artifact-bindings.md` files become generated summaries or concise links to `isomer-cli project artifacts describe`. They no longer repeat executable command shapes. Artifact Format Profiles remain declarative and do not contain validators, converters, providers, or command payloads.

Keeping the current duplicated binding pages was considered and rejected because agents must currently reproduce record kind, label, profile, producer, and consumer arguments from prompt text. Folding physical bindings into the semantic registry was also rejected because it would break the existing storage-neutral semantic boundary.

### Add Canonical Core CLI Services and Kaoju Extension Commands

The CLI gains these canonical groups:

```text
isomer-cli project artifacts describe|put|revise|latest|list|show|archive
isomer-cli project runs begin|checkpoint|status|complete
isomer-cli project repos acquire
isomer-cli project service-requests create|dispatch|status
isomer-cli ext kaoju paper export-template|apply-template|derive-markdown|init-tex|build-pdf
isomer-cli ext kaoju wiki export|deploy|start
```

`project artifacts put` and `revise` accept an exact semantic id plus a content file or directory. They resolve the binding, validate the producer and content, persist or register the file, create the Artifact Core Record and links, and return stable JSON refs. `describe` exposes the resolved declarative contract to skills and diagnostics.

The current `ext research records` commands remain compatibility aliases over the same record service. The current `ext research templates` group remains available for listing, inspecting, compiling, or archiving historical `kaoju:writing-template` records during migration, but it does not create canonical paper state after the new path is enabled. New paper work uses `ext kaoju paper`.

A Kaoju-only monolithic command that executes complete use cases was considered and rejected. It would place research decisions inside the CLI and duplicate pipeline orchestration.

### Keep File Content Authoritative and the DB Discoverable

Every durable output has an Artifact Core Record with stable id, Topic Workspace id, artifact kind, status, locator kind, locator, timestamps, and media type when known. Format, producer, Run, provenance, evidence, lineage, validation, and Kaoju binding data attach through existing metadata and link records rather than widening the core record.

Structured records use a validated JSON file as authoritative content. MyST, Markdown, TeX, PDF, scripts, logs, and ordinary downloaded material use their actual file as authoritative content. A directory artifact uses a versioned manifest file as its content locator; the manifest lists member paths, media types, byte sizes, checksums, and external or managed locator posture. Canonical external repositories use the registered repository locator plus immutable commit identity rather than copying the tree into a structured payload.

Creation uses a staged write, content validation, atomic rename when the filesystem supports it, then DB registration. A failed DB commit removes the staged managed content or leaves a recovery-journal entry that bootstrap can diagnose. An external user-selected target is not modified by recovery without authorization; its incomplete manifest remains unregistered and is reported as a blocker.

Directory scanning was considered as a fallback for missing records and rejected. ADR-0003 makes the DB authoritative for artifact metadata, existence, and discovery.

### Add Scoped Current-Record Resolution

The record query index gains an optional `scope_key` extension field and index. The active candidate key becomes `(topic_workspace_id, semantic_id, scope_key)`. Examples include:

- `direction:<direction-id>` for one active reading list per direction.
- `source:<source-identity>` for source digests, blockers, or associated-code state.
- `paper:<paper-line-id>` for current structure, template, and draft state.
- `target:<normalized-target-digest>` for export or deployment state when a current target record is useful.

Current-state revisions preserve history and advance the scoped latest pointer. Runs, compile attempts, smoke results, export events, and trial results remain append-only. Ambiguous competing accepted candidates produce a conflict instead of timestamp-only selection.

Using topic-wide `latest_for_semantic_id` was considered and rejected because two survey directions or sources would overwrite each other's current-state lookup.

### Persist Use-Case Progress Through Research Tasks and Runs

Each bounded intent invocation creates or resumes a Research Task and a Run. Run transition metadata records the procedure id, stage id, normalized input refs, produced output refs, pending Gate or Service Request refs, terminal status, and resume hint. `project runs checkpoint` records these transitions through Workspace Runtime after each durable stage.

Resume is context, not a public macro procedure. The pipeline queries the Run and scoped latest artifacts, verifies that referenced files and inputs still match their checksums or source identities, and starts at the first incomplete stage. Completed durable stages are not rerun unless the user requests refresh or their inputs are stale.

A separate custom workflow database was considered and rejected because Research Tasks, Runs, Workspace Runtime, Gates, and artifact lineage already provide the accepted lifecycle vocabulary.

### Make Human Decisions Explicit

UC-01 presents agent-proposed directions, supports multi-selection and custom directions, and records the selected result as `kaoju:direction-set`. Each direction contains a stable direction id, scoped question, boundary, expected source classes, coverage date, expected depth, and deliverables. It remains distinct from `kaoju:survey-contract`.

UC-02 produces one scoped `kaoju:reading-list` per direction. Its default target is three priority and three secondary items. Inaccessible or unresolved candidates remain in provenance and blocker records but do not satisfy the reachable target. Discovery attempts bounded backfill; an unresolved deficit emits a non-blocking coverage warning. The human may approve a shorter list.

Clarification-first remains an interaction mode. Material ambiguity is resolved before mutation. Claim-shaping choices, publication-facing output, environment mutation outside accepted authorization, data export, and trial execution use the applicable Gate policy. UC-10 cannot execute until its `kaoju:method-trial-plan` has an explicit human Gate decision.

Automatically accepting agent-proposed directions or interpreting a target count as coverage completeness was considered and rejected.

### Make MyST the Canonical Paper Graph

The canonical paper graph is:

```text
accepted audit and synthesis
            |
   paper-structure-myst
            |
      paper-draft-myst ----------------> paper-draft-md
            |                               derived view
            |
     TeX initialization
       /             \
paper-template-tex  paper-draft-tex
                          |
                 agent inspection and repair
                          |
                      paper-pdf
```

`draft-paper` requires an accepted Audit Report and accepted Field Summary, Related-Work Catalog, and Claim Status Table. It creates `kaoju:paper-structure-myst`, fills `kaoju:paper-draft-myst`, records `kaoju:citation-map` and `kaoju:paper-revision-log`, and optionally derives `kaoju:paper-draft-md`. The Markdown view is never an editable source for canonical paper state.

`init-tex` uses a MyST-aware parser to validate structure and initialize `kaoju:paper-template-tex` and `kaoju:paper-draft-tex`. It emits explicit conversion diagnostics for unsupported directives, tables, citations, floats, and raw blocks. The write agent must inspect and edit the TeX files directly before build readiness. `build-pdf` dispatches the `document_build` extension point, records the exact toolchain and log, inspects the PDF result, and creates `kaoju:paper-pdf`, `kaoju:paper-compile-log`, and `kaoju:paper-pdf-revision-log`.

Continuing with LaTeX as canonical was rejected because it contradicts ADR-0006. Treating a general Markdown-to-PDF converter as the publication path was rejected because it loses the required explicit TeX repair and build stages.

### Use Versioned External Template Exchange

`export-template` writes the current `kaoju:paper-structure-myst` or `kaoju:paper-template-myst` to a user-selected path or a resolved Topic Workspace path. It writes `kaoju:paper-template-manifest` with source record id, source revision, base digest, source digest refs, paper line id, tied draft ref, export path, and export time, then registers `kaoju:paper-template-export`.

`apply-template` verifies the export manifest, base digest, active template revision, required sections, placeholders, citation references, and available source-digest refs. A stale base produces a conflict and leaves canonical state unchanged. A valid edit creates a revision of `kaoju:paper-template-myst`, regenerates `kaoju:paper-draft-myst`, and appends `kaoju:paper-revision-log`.

Directly editing the canonical record file was considered and rejected because it bypasses validation, provenance, conflict detection, and revision lineage.

### Implement Wiki Export as an Isomer-Owned Representation

`ext kaoju wiki export` queries accepted artifacts from the DB, renders human-readable Markdown pages, and creates a versioned JSON or YAML mapping manifest. The manifest records topic identity, artifact ids, semantic ids, revisions, checksums, page paths, relationship edges, provenance refs, generation time, exporter version, and schema version. It registers `kaoju:llm-wiki-export` and `kaoju:llm-wiki-metadata`.

`deploy` copies a package-owned compatible viewer to a user-selected directory, writes a viewer manifest pointing to the wiki root, and registers `kaoju:llm-wiki-viewer` and `kaoju:llm-wiki-viewer-manifest`. `start` binds to loopback by default, chooses or validates a port, launches through the command-execution adapter, records its Run and logs, and reports the local URL.

The implementation never loads or invokes the external `imsight-llm-wiki` skill. Existing external viewer material may be used only as a compatibility fixture. Code is bundled only after license and provenance validation; otherwise Isomer implements a compatible viewer against the export manifest.

Invoking the external skill was rejected by ADR-0007. Exporting rendered pages without machine-readable mapping metadata was rejected because it would lose artifact identity and provenance.

### Separate Source Acquisition, Environment Preparation, and Trial Execution

`project repos acquire` resolves a URL or a user-selected repository identity, obtains clarification for ambiguity, resolves a canonical external repository label, clones with depth one by default, records the immutable commit and source identity, and registers the repository only after acquisition succeeds. History is deepened only when an approved inspection requires it. Source-code claims cite the immutable commit, local file, and line range.

UC-09 creates `kaoju:env-prep-plan`, then opens a Service Request scoped to the Research Task and Run. The Service Team inspects dependency hints and applies the accepted Pixi preference order: reuse a satisfying environment, add flexible compatible constraints to an existing environment while preferring `default`, or create a dedicated environment when necessary. The Service Request returns `kaoju:env-gate-revision`, `kaoju:pixi-env-ref`, `kaoju:smoke-run-script`, and `kaoju:smoke-run-result`. Flexible intent constraints are retained, while the derived environment ref records exact resolved versions and lockfile identity.

UC-10 verifies acquired source and an accepted environment result, creates `kaoju:method-trial-plan`, waits for a human Gate, creates a minimal durable wrapper, and dispatches execution. It records logs, outputs, timing, environment, source commit, data identity, adaptations, and verdict in an immutable `kaoju:method-trial-run` and `kaoju:method-trial-result`. Random input also creates `kaoju:generated-dataset` and remains a capability probe unless a stronger reproduction contract is separately satisfied.

Letting Kaoju mutate Pixi state directly was rejected because environment support belongs to the Service Team. Combining preparation and execution was rejected because ADR-0009 and ADR-0010 require separate resumable use cases.

## Risks / Trade-offs

- [The change touches skills, CLI, storage, execution, and packaged assets] → Deliver it in vertical slices with one integration fixture per use case and keep compatibility aliases until all slices pass.
- [A single binding registry can become an overpowered plugin contract] → Keep it declarative, keep executable implementations in code, and validate that profiles and bindings contain no command bodies or provider payloads.
- [Filesystem and DB updates cannot form one native transaction] → Use staged managed writes, atomic rename where supported, DB registration after validation, recovery diagnostics, and idempotent retry keys.
- [Scoped latest lookup changes query behavior] → Add the field as optional extension metadata, backfill known current records, preserve topic-wide queries when no scope is supplied, and report ambiguous legacy candidates.
- [MyST conversion may lose advanced document constructs] → Treat conversion as initialization, emit diagnostics, require agent inspection of TeX, retain canonical MyST, and preserve every derived edge through checksummed lineage.
- [Template exports can be edited or moved outside the Topic Workspace] → Require an explicit path, register locator posture and base digest, refuse stale or mismatched apply, and never infer canonical state from an unregistered directory.
- [Viewer source may have unclear licensing] → Make license review a blocking task before vendoring and retain the option to implement a small compatible viewer from the documented manifest.
- [Service Request infrastructure may be incomplete] → Implement the generic Project CLI and record contract first, then adapt the existing topic environment service skill behind it without exposing provider details.
- [Legacy commands may surprise users after semantic changes] → Emit deprecation and canonical-format notices, provide explicit legacy inspection paths, and never silently promote legacy TeX into MyST.
- [The 3 plus 3 reading-list target may be mistaken for completeness] → Store target, achieved counts, search boundary, saturation evidence, deficits, and explicit non-completeness language.

## Migration Plan

1. Add the v2 Kaoju binding registry and validators without changing current producers. Register all new semantic ids and content modes, add `scope_key`, and expose `project artifacts describe`.
2. Add canonical project artifact, Run, repository acquisition, and Service Request services. Make current research record commands delegate to the same implementation.
3. Refactor shared, workspace, pipeline, frame, discover, acquire, and examine guidance for UC-01 through UC-03 and UC-08. Add state checkpoints and DB-only discovery.
4. Add `isomer-kaoju-trial`, narrow reproduction semantics, and implement Service Request-backed UC-09 and approved UC-10.
5. Refactor `isomer-kaoju-write` around MyST, add paper CLI commands, then migrate `paper-pass` and `create-paper-template` compatibility routes.
6. Add `isomer-kaoju-export`, the wiki exporter, mapping schema, viewer asset, deployment, and launch path.
7. Update the package manifest, extension command metadata, callbacks, generated assets, documentation, and exact inventory tests.
8. Run focused unit and integration tests, then `pixi run lint`, `pixi run typecheck`, `pixi run test`, and strict OpenSpec validation.

Legacy `kaoju:writing-template`, `kaoju:survey-manuscript`, `kaoju:paper-build-run`, `kaoju:paper-validation-report`, and `kaoju:publication-bundle` records remain readable and historical. New MyST records may cite them as prior work, but the migration does not infer MyST content from TeX. A user-authorized import may register an existing TeX tree as `kaoju:paper-template-tex` or `kaoju:paper-draft-tex` with explicit legacy provenance.

Rollback disables the new intent commands and restores legacy command routing while preserving all newly written Artifact Core Records and files. It does not delete user exports, repositories, environments, Runs, or accepted records. The optional scoped index can remain because it is backward-compatible when absent.

## Open Questions

- Which compatible viewer implementation can be bundled after license review? This does not change the required export or viewer-manifest contract.
- Which MyST parser package best fits the existing Pixi environment and Python 3.11 support? The selected dependency must be locked and remain an implementation of the specified validation and initialization behavior.
- Should the first release expose `project service-requests dispatch` synchronously only, or also support an asynchronous adapter handle? Both forms must use the same Service Request and Run records.
