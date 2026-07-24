## Context

The generic Topic Creator owns Project registration, Topic Workspace creation, Workspace Runtime readiness, and `topic.intent.overview`. The public Kaoju `create-topic` command delegates those prerequisites and then invokes `isomer-kaoju-topic-creator`, which currently creates only three topic-owned Mindset Sources. Kaoju paper templates use a different model: mutable named `content` and `latex` stock is canonical in Workspace Runtime, while `topic.paper.template_exchange_root` contains non-canonical editable exports under the singular built-in path `intent/derived/writing-template`.

This change must preserve the core and extension ownership boundary, the distinction between canonical named stock and exchange copies, user edits, optimistic concurrency, and explicit topic selection. It must also support generic topics that have not run Kaoju initialization and partially initialized or upgraded topics without making paper production depend on local template files.

## Goals / Non-Goals

**Goals:**

- Make one explicit Kaoju `create-topic` operation establish the overview prerequisite, three Mindset Sources, canonical content and LaTeX `main` stock, and editable plural-path exports.
- End topic initialization with a concrete derived-material inventory and adjustment guidance before later setup or research begins.
- Provide immutable packaged content and LaTeX defaults that can seed topic stock and support non-mutating fallback.
- Preserve valid existing state and make partial initialization safely resumable.
- Change the built-in exchange root to `intent/derived/writing-templates` without changing its semantic label or compatibility id.
- Keep missing topic-local writing templates non-blocking for default paper consumption and export, with exact provenance for packaged fallback.
- Keep missing Mindset Sources optional without using their packaged seeds at Run time.
- Give legacy singular exchange roots a visible, conflict-safe migration path.
- Let one later natural-language apply request validate and route recognized changed derived material so accepted edits govern future operations without rewriting historical snapshots.

**Non-Goals:**

- Adding Kaoju-specific behavior to the generic Topic Creator or `project topics create`.
- Making exchange directories canonical or replacing named template records with direct filesystem authority.
- Falling back from an explicitly requested non-`main` template name.
- Silently repairing invalid topic records, invalid exports, or conflicting singular and plural directories.
- Creating Mindset Sources or topic template stock during installation, welcome, help, read-only inspection, or ordinary research preflight.
- Selecting a publication venue or specializing the packaged LaTeX default for a venue during topic initialization.
- Treating every file beneath `intent/derived` as directly user-applicable or adding a generic derived-file import mechanism.
- Revising past Runs, Mindset Records, paper drafts, TeX snapshots, PDFs, or other Artifacts as part of the default apply request.
- Adding a synthetic aggregate derived-intent Artifact when existing Source digests, template mutation audits, export observations, and the per-material result provide the required evidence.

## Decisions

### Keep Kaoju Initialization Behind the Public Kaoju Command

Public `create-topic` remains a composed workflow. It delegates generic prerequisites to `isomer-op-entrypoint->topic-create`, then invokes the protected Kaoju topic owner. The protected owner sequences Mindset Source creation and a deterministic template-default ensure operation after a concrete overview and Workspace Runtime exist.

This makes initialization appear as one user operation while preventing core Isomer from importing extension schemas, resources, or policy. A generic topic remains valid without Kaoju derived intent.

### End Initialization With an Adjustment-Oriented Handoff

After creating or preserving Kaoju derived intent, the agent resolves and inspects the actual recognized `intent/derived` surfaces for the selected topic. It reports each material by semantic owner rather than presenting the directory as one undifferentiated configuration tree:

- Mindset Sources are directly editable current topic intent. The handoff names each deterministic key, purpose, schema constraints, and future Run applicability.
- `writing-templates/content/<name>/` and `writing-templates/latex/<name>/` are non-canonical working copies. The handoff explains which paper behavior each role controls and that edits require state-checked promotion.
- Environment target specifications and other service-generated derived files, when present later, are not direct override inputs. The handoff names the source intent and regeneration owner instead.

The agent stops after this report unless the user's original request explicitly includes a later initialization or research target. The user may edit immediately or return after later Topic Workspace use. The same explanation remains valid because it is based on semantic ownership rather than initialization age.

### Store Packaged Template Defaults With the Kaoju Write Owner

The `isomer-kaoju-write` bundle will contain immutable `content/main` and `latex/main` trees plus checked metadata. The content tree will be a generic MyST-oriented survey-paper scaffold. The LaTeX tree will be a neutral article-style presentation with an explicit entrypoint, composition contract, and build profile, not a venue-specific template.

Package validation will calculate each tree digest and verify the same path-safety, reserved-file, content, and LaTeX-contract rules used for topic stock. A packaged identity will include the template kind, `main` name, packaged resource version, and digest. Invalid packaged resources block initialization and fallback with a stable diagnostic.

Keeping these assets with the write owner preserves resource ownership. The topic creator coordinates initialization but does not become the authority for template semantics.

### Add an Idempotent Typed Ensure-Defaults Operation

The typed Kaoju template service will expose one topic-selected ensure-defaults operation used by `create-topic`. For each `content/main` and `latex/main` namespace independently, it will:

1. Preserve a valid ready named record.
2. Create a missing named record from the checked packaged tree using the existing atomic managed-tree and audit boundary.
3. Export a newly created or already ready record to `<topic.paper.template_exchange_root>/<kind>/main/` when the target is absent.
4. Preserve a recognized edited export or an export whose canonical state has drifted and report its posture.
5. Block that kind without overwrite when a canonical record is invalid, the target contains unrecognized content, or identity metadata conflicts.

The result will report `created`, `preserved`, `exported`, `fallback_available`, `invalid`, and `conflict` posture by kind. A failure after one kind completes leaves valid resumable state; retry revalidates and preserves it.

The alternative was to write template trees directly from the topic-creator skill. That would bypass state tokens, mutation audit, query-index maintenance, and managed-tree validation, so the typed service remains the mutation owner.

### Use Ordered Default Template Resolution

Default-consuming operations will use one shared resolver:

1. An explicit name or ref must resolve exactly. Missing, archived, ambiguous, or invalid explicit state blocks without fallback.
2. An omitted selector means role-local `main`.
3. A ready topic-owned `main` record wins.
4. If no topic-owned `main` exists, the corresponding checked packaged default is selected.

An invalid or ambiguous existing topic `main` is not absence and blocks fallback. Missing exchange directories never block paper consumption because they are non-canonical.

Packaged fallback is immutable and does not create a named topic record or topic-derived file. The consumer snapshots the exact packaged tree into the normal paper-local Artifact and records the packaged identity, resource version, digest, selected role, and `selection_source = "packaged-default"`. Topic stock continues to record `selection_source = "topic-stock"` and its stable ref and state token.

Default export may also select the packaged default. Its metadata identifies a packaged source and has no mutable topic state token. Promoting that edited export uses named-template create, not update. Listing and showing named stock remain topic-state queries and do not pretend that packaged defaults are topic records.

This keeps generic and partially initialized topics usable without silently manufacturing current topic intent. The alternative, lazy creation of canonical `main` records during first paper use, would make fallback mutate topic state and blur the explicit initialization boundary.

### Apply Edited Derived Material by Owner

The public Kaoju entrypoint treats “I have modified the derived materials, now apply them” and equivalent wording as a composite agent workflow, not a new generic filesystem import command. It pins one Research Topic and Topic Workspace, inventories only semantically known or registered material, and completes a read-only preflight before any named-record mutation.

The workflow routes changes as follows:

1. Validate changed Mindset Sources by deterministic filename, key, closed schema, and digest. Valid files are already current topic intent and need no Artifact update. The result reports their accepted current digest.
2. Assess changed content and LaTeX exports against their export metadata and current named stock. Promote accepted changes through typed named-template create or optimistic-concurrency update, which emits new state tokens, digests, and mutation audits.
3. Reject direct application of generated environment target specifications or unknown derived files. Identify their source intent or owning service instead of inventing an import route.

The complete preflight prevents avoidable partial named-record mutation, but the workflow reports independent per-material outcomes because direct topic files and database-backed template records cannot form one transaction. A stale export, invalid Source, or unsupported generated file remains unchanged and receives an exact recovery route.

Accepted state affects later Runs and newly created or explicitly reinitialized paper artifacts. An active Run retains its Mindset Source snapshot, and existing paper lines retain their content and LaTeX template snapshots. Retrospective compatibility is a separate user-authorized workflow that requires exact historical targets and produces new revisions or derived Artifacts with provenance rather than rewriting old records.

### Preserve the Existing Mindset Missing-State Contract

Mindset packages and writing-template packages have different runtime roles. A missing Mindset Source records `skipped_source_missing` and proceeds without reflection. It never loads the packaged mindset seed. A missing default writing template selects the immutable packaged template because drafting and composition require concrete structural input.

The archived scenarios that still describe implicit create-missing during a normal research action will be removed from the topic-creation requirement. Only explicit `create-topic` and explicit repair create topic-derived resources.

### Rename Only the Built-In Path, Not the Semantic API

`topic.paper.template_exchange_root` and `topic_paper_template_exchange_root` remain stable. The `isomer-default.v1` path changes to `intent/derived/writing-templates`. Role and name remain children, producing:

```text
intent/derived/writing-templates/content/main/
intent/derived/writing-templates/latex/main/
```

Environment overrides and explicit Topic Workspace Manifest bindings retain precedence. An explicit binding to the singular path therefore remains valid and receives a legacy-path advisory rather than being rewritten.

### Make Legacy Migration Explicit and Conflict-Safe

When no higher-precedence binding exists, compatibility inspection checks only the exact legacy sibling `intent/derived/writing-template`. The effective default still resolves to the plural path. If legacy content exists, diagnostics identify whether the plural path is absent, empty, equivalent, or conflicting.

The existing template migration surface will gain preview and apply support for the exchange-root rename. Apply requires explicit authorization and succeeds only when every recognized kind/name tree can move without overwriting plural content. It stages the plural tree, verifies file digests and export metadata, atomically publishes it, records new export observations where applicable, and removes the singular tree only after verification. If both roots contain non-equivalent content, migration blocks and leaves both unchanged.

Historical export observations keep their original observed paths. New observations and all new default exports use the effective plural root. Rollback can restore the staged singular tree or retain an explicit singular manifest binding; no database template content needs rewriting.

## Risks / Trade-offs

- [Packaged defaults could be mistaken for topic intent] → Machine and chat output always identify `packaged-default`, and fallback creates no topic record or derived file.
- [Initialization can complete mindsets but fail templates, or one template kind can precede a failure in the other] → Return per-resource status and make every step idempotent so explicit retry resumes safely.
- [An invalid topic `main` could be hidden by fallback] → Treat invalid, ambiguous, or archived current state as a blocker; fallback applies only to verified absence.
- [Changing the built-in path can strand unbound legacy exports] → Detect only the known singular sibling, preserve registered historical observations, and provide preview-before-apply migration with conflict checks.
- [A generic internal LaTeX default may produce plain output] → Keep it deliberately neutral and record its identity; venue adoption remains an explicit later operation.
- [Packaged export metadata lacks a mutable state token] → Use a distinct packaged-source metadata variant and require named-template create when promoting edited content.
- [More fallback branches increase template-selection complexity] → Centralize selection in one typed resolver consumed by draft, export, and TeX composition paths.
- [Users may assume every derived file is editable or that “apply” is one atomic import] → Report ownership and activation behavior at initialization, inventory only recognized surfaces, preflight all changes, and return per-material status.
- [A later apply request could silently change active or historical work] → Make the default boundary future-only, preserve pinned snapshots, and require exact targets plus separate authorization for retrospective reconciliation.

## Migration Plan

1. Add and validate packaged content and LaTeX defaults without changing selection behavior.
2. Add the shared selection descriptor, packaged fallback handling, ensure-defaults service, and structured diagnostics.
3. Change the built-in semantic-surface path to plural and add legacy preview/apply migration.
4. Update the Kaoju topic-creator and write skill workflows to call the typed operations, report the adjustment-oriented handoff, and route later natural-language apply requests by material ownership.
5. Add future-only application tests covering Mindset validation, template promotion, stale edits, generated-file rejection, and historical snapshot preservation.
6. Update tests and documentation, then run lint, type checking, unit tests, targeted integration tests, skill validation, and package-resource validation.
7. Existing explicit singular bindings remain usable. Operators can preview and apply migration per selected topic. Rollback restores the prior package and keeps or restores the singular binding or directory.

## Open Questions

None. The packaged defaults are neutral, role-local `main` resources; explicit topic initialization creates canonical stock and exports, while verified absence during later default consumption uses immutable packaged fallback.
