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

The first release exposes synchronous-only Service Request dispatch. `project service-requests dispatch` creates the durable Service Request and Execution Adapter Command Request before executable work starts, then waits for terminal completion or a configured timeout or interruption. It always returns the stable Service Request ref and latest observed state. A timeout or client interruption does not invent terminal completion; `project service-requests status` reconciles the durable request later. The first release does not expose `--no-wait` or a separate asynchronous dispatch command.

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

UC-01 presents three agent-proposed directions by default, supports multi-selection and custom directions, and records the selected result as `kaoju:direction-set`. Each direction contains a stable direction id, scoped question, boundary, expected source classes, coverage date, expected depth, and deliverables. When empirical feasibility is relevant, the proposal may annotate current host hardware or environment capability, but it does not exclude or rank other directions solely because of the current host. The direction set remains distinct from `kaoju:survey-contract`.

UC-02 produces one scoped `kaoju:reading-list` per direction. Its default target is three priority and three secondary items. Inaccessible or unresolved candidates remain in provenance and blocker records but do not satisfy the reachable target. Discovery attempts bounded backfill; an unresolved deficit emits a non-blocking coverage warning. The human may approve a shorter list.

Clarification-first remains an interaction mode. Material ambiguity is resolved before mutation. Claim-shaping choices, publication-facing output, environment mutation outside accepted authorization, data export, and trial execution use the applicable Gate policy. UC-10 cannot execute until its `kaoju:method-trial-plan` has an explicit human Gate decision.

After the governing build or trial action is approved, the system may automatically retry an identical request after a transient failure and may apply bounded non-material repairs. Non-material paper repairs are limited to presentation or TeX syntax changes that preserve canonical MyST content and evidence meaning. A change to dependencies or lock state, source commit or patch, data, wrapper semantics or entry point, evaluator or metrics, resource limits, canonical paper content, or evidence interpretation is material and requires a revised plan plus the applicable human Gate. Every retry and repaired attempt remains a separate Run with its own logs, inputs, outputs, fidelity, and lineage.

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

`draft-paper` requires an accepted Audit Report and accepted Field Summary, Related-Work Catalog, and Claim Status Table. The write skill selects a typed MyST structure profile from the accepted direction, such as taxonomy, comparison, empirical survey, or general survey, records its rationale, and presents the structure for actor revision. It creates `kaoju:paper-structure-myst`, fills `kaoju:paper-draft-myst`, records `kaoju:citation-map` and `kaoju:paper-revision-log`, and optionally derives `kaoju:paper-draft-md`. The Markdown view is never an editable source for canonical paper state.

Figures and tables are separate file-backed Artifacts rather than content embedded in a structured paper record. The MyST structure and draft contain typed placeholders that reference those Artifacts. The citation map records their display role, evidence refs, caption or interpretation status, and insertion location so a display can be revised or reused without changing its evidence identity.

`init-tex` uses a MyST-aware parser to validate structure and initialize `kaoju:paper-template-tex` and `kaoju:paper-draft-tex`. The TeX template carries a compatibility fingerprint over venue or document class, toolchain policy, and required MyST construct set. It remains stable while that fingerprint is compatible and is revised or regenerated only after the fingerprint changes; the TeX draft is regenerated from each selected canonical MyST revision. Initialization emits explicit conversion diagnostics for unsupported directives, tables, citations, floats, and raw blocks. The write agent must inspect and edit the TeX files directly before build readiness. `build-pdf` dispatches the `document_build` extension point, records the exact toolchain and log, inspects the PDF result, and creates `kaoju:paper-pdf`, `kaoju:paper-compile-log`, and `kaoju:paper-pdf-revision-log`.

Continuing with LaTeX as canonical was rejected because it contradicts ADR-0006. Treating a general Markdown-to-PDF converter as the publication path was rejected because it loses the required explicit TeX repair and build stages.

### Use Versioned External Template Exchange

`export-template` writes the current `kaoju:paper-structure-myst` or `kaoju:paper-template-myst` to a user-selected path or a resolved Topic Workspace path. Every export receives an automatic export revision and manifest; the default managed target uses a versioned directory, while an actor-selected target requires an explicit update or overwrite choice before replacing existing content. The service writes `kaoju:paper-template-manifest` with source record id, source revision, base digest, source digest refs, paper line id, tied draft ref, export revision, export path, and export time, then registers `kaoju:paper-template-export`.

`apply-template` verifies the export manifest, base digest, active template revision, required sections, placeholders, citation references, and available source-digest refs. A stale base produces a conflict and leaves canonical state unchanged. Removing a required section is a validation error. Removing an optional section that still owns grounded content produces an orphaned-content report and requires explicit actor confirmation. A valid confirmed edit creates a revision of `kaoju:paper-template-myst`, regenerates `kaoju:paper-draft-myst`, and appends `kaoju:paper-revision-log`.

Directly editing the canonical record file was considered and rejected because it bypasses validation, provenance, conflict detection, and revision lineage.

### Implement Wiki Export as an Isomer-Owned Representation

`ext kaoju wiki export` queries accepted artifacts from the DB, renders human-readable Markdown pages, and creates one canonical JSON mapping manifest with a versioned schema. The manifest records topic identity, artifact ids, semantic ids, revisions, checksums, page paths, relationship edges, provenance refs, generation time, exporter version, schema version, and managed paths. Without an override, the CLI resolves a managed wiki target inside the Topic Workspace. Re-export stages an in-place update of recognized managed files, preserves unrecognized files, reports path changes in a changelog, and registers a new checksummed revision of `kaoju:llm-wiki-export` and `kaoju:llm-wiki-metadata` while leaving the target root stable.

`deploy` copies a package-owned compatible viewer to a Topic Workspace default or actor-selected directory, writes a JSON viewer manifest pointing to the wiki root, and registers `kaoju:llm-wiki-viewer` and `kaoju:llm-wiki-viewer-manifest`. A recognized deployment refreshes managed assets in place; an unrecognized non-empty target requires clarification. `start` binds to loopback by default, chooses or validates a port, launches through the command-execution adapter, records its Run and logs, and reports the local URL.

The implementation never loads or invokes the external `imsight-llm-wiki` skill. Existing external viewer material may be used only as a compatibility fixture. Code is bundled only after license and provenance validation; otherwise Isomer implements a compatible viewer against the export manifest.

Invoking the external skill was rejected by ADR-0007. Exporting rendered pages without machine-readable mapping metadata was rejected because it would lose artifact identity and provenance.

### Separate Source Acquisition, Environment Preparation, and Trial Execution

`project repos acquire` resolves a URL or a user-selected repository identity, obtains clarification for ambiguity, resolves a canonical external repository label, clones with depth one by default, records the immutable commit and source identity, and registers the repository only after acquisition succeeds. History is deepened only when identity resolution or an approved inspection requires historical evidence, and the acquisition record states the reason and resulting depth posture. Given a repository, the acquire skill automatically performs bounded associated-paper metadata discovery. A candidate relationship must be verified, and the paper must pass normal reading-list selection and approval before deep ingestion or evidentiary use. Source-code claims cite the immutable commit, local file, and line range.

Paper ingestion extracts figures and tables only when they support selected claims. Automated visual or tabular extraction is provisional until the finding is checked against the original source; evidence that cannot be checked reliably requires human review before acceptance.

UC-09 creates `kaoju:env-prep-plan`, then opens a Service Request scoped to the Research Task and Run. The Service Team inspects dependency hints and applies the accepted Pixi preference order: reuse a satisfying environment, add flexible compatible constraints to an existing environment while preferring `default`, or create a dedicated environment when necessary. The Service Request returns `kaoju:env-gate-revision`, `kaoju:pixi-env-ref`, `kaoju:smoke-run-script`, and `kaoju:smoke-run-result`. Flexible intent constraints are retained, while the derived environment ref records exact resolved versions and lockfile identity. The smoke script is a file-backed Artifact under a resolved `topic.records.*` surface, never canonical state beside external source or under a Local Tmp Surface; execution may use a disposable staged copy tied to the Run.

UC-10 verifies acquired source and an accepted environment result, creates `kaoju:method-trial-plan`, waits for a human Gate, creates a minimal durable wrapper, and dispatches execution. When an upstream command fits the approved task and environment, the wrapper invokes it and records its fidelity; otherwise the wrapper makes the smallest recorded adaptation needed for the task. It records logs, outputs, timing, environment, source commit, data identity, adaptations, and verdict in an immutable `kaoju:method-trial-run` and `kaoju:method-trial-result`. Random input also creates `kaoju:generated-dataset` and remains a capability probe unless a stronger reproduction contract is separately satisfied.

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

## Deferred Implementation Selections

- Select the compatible viewer implementation after license and provenance review. This does not change the required export or viewer-manifest contract, and an independently implemented viewer remains the fallback.
- Select the MyST parser package from Python 3.11-compatible candidates during implementation. Lock the dependency and verify that it satisfies the specified validation and initialization behavior.
