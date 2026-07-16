## Context

The current MyST-first Kaoju service treats canonical templates as paper-line-scoped current-state Artifacts whose edits create superseding records. Its manual-edit exchange creates versioned `exports/kaoju-paper/<paper-line>/vNNNN/` directories. The intended model is smaller: a Topic Workspace has a flat namespace of mutable named templates, stable editable working directories, and optional saved states created only when a user or agent copies a template to another name.

A paper template is an agent-interpreted MyST-oriented file tree without a required filename, section schema, or merge grammar. Isomer-cli can safely mutate named canonical state, including file and JSON metadata edits, but it cannot decide how an arbitrary user-edited tree maps into the target template. The Kaoju agent owns that high-level construction and reconciliation.

## Goals / Non-Goals

**Goals:**

- Keep one stable mutable canonical record per template name.
- Let ordinary edits replace that named state without accumulating automatic content revisions.
- Let users and agents preserve a state explicitly by copying it to another ordinary template name.
- Provide low-level CLI CRUD, exact named-template copy and replacement, optimistic concurrency, path safety, and lightweight provenance.
- Keep arbitrary-directory interpretation and complicated merging agentic.
- Preserve the accepted edited-export, current-topic `main/`, user-clarification discovery order for underspecified updates.

**Non-Goals:**

- Defining a snapshot entity, type, flag, API family, or retention system.
- Providing Git-like commits, branches, automatic version history, three-way merge, or revision garbage collection.
- Defining a universal paper-template tree schema or requiring a conventional entrypoint.
- Retaining old template content after every update unless an explicit named copy preserves it.
- Allowing agents to update SQL rows or managed Artifact files directly.

## Decisions

### 1. One Flat Namespace Contains All Templates and Saved Copies

`KAOJU:PAPER-TEMPLATE-MYST` is scoped by path-safe `template_name`. Each active name maps to one stable database record and one current managed directory tree. `main`, `neurips-2026`, and `main-before-methodology-change` have identical semantics to isomer-cli.

The system defines no snapshot distinction. To preserve current `main`, a user or agent creates another named template from it, for example `main-before-methodology-change`. The name communicates intent by convention only. That copied template remains independently readable, mutable, usable for a paper, copyable, replaceable, archivable, or deletable like any other template.

`main` is the default name for ordinary paper use and export. Explicit selection can use any other name. The unnamed database-update workflow follows source discovery instead of immediately selecting database `main`.

### 2. Named Templates Use Mutable Canonical State

The Kaoju binding gains mutable named-state behavior. `create` allocates the stable record for a new name. `update` atomically replaces its current content tree or allowed metadata in the same logical record. It does not create `revision_of`, `supersedes`, or a historical template-content record.

Every mutation writes a lightweight audit event containing stable record ref, name, actor, timestamp, operation, source refs, prior state token and digest, and resulting state token and digest. The event does not retain prior template bytes. Storage may deduplicate or later collect unreferenced internal blobs, but those blobs are not user-visible revision history and cannot be relied on for restore.

A paper draft records the selected template name, stable ref, and observed content digest. Updating that template does not rewrite the draft. Reproducing old content requires an explicitly preserved named copy; this is an accepted consequence of the simpler model.

Alternative considered: automatically create an immutable revision on each update. That recreates the version-management and accumulation problem the design intends to avoid.

### 3. Canonical Content Is a Flexible Managed Tree

The stable named record points to a managed directory manifest containing safe relative paths, checksums, sizes, and media types. It can hold MyST, configuration, includes, assets, or guidance without a fixed entrypoint. Agent-observed entrypoint and use guidance can live in mutable JSON metadata, but isomer-cli does not infer or require it.

CLI integrity checks reject traversal, unsafe symlinks, reserved exchange files, broken manifests, and inconsistent digests. They do not claim semantic validity or compatibility with a paper workflow.

### 4. Isomer-CLI Exposes Low-Level CRUD

The canonical interface is conceptually:

```text
isomer-cli ext kaoju paper template list
isomer-cli ext kaoju paper template show --name NAME
isomer-cli ext kaoju paper template create --name NAME --from PATH
isomer-cli ext kaoju paper template create --name NEW --from-template EXISTING
isomer-cli ext kaoju paper template update --name NAME --from PATH --expected-state TOKEN
isomer-cli ext kaoju paper template update --name TARGET --from-template SOURCE --expected-state TOKEN
isomer-cli ext kaoju paper template file put --name NAME --path RELPATH --from FILE --expected-state TOKEN
isomer-cli ext kaoju paper template file remove --name NAME --path RELPATH --expected-state TOKEN
isomer-cli ext kaoju paper template metadata patch --name NAME --patch-file FILE --expected-state TOKEN
isomer-cli ext kaoju paper template archive --name NAME --expected-state TOKEN
```

`create --from-template` makes an explicit saved copy without introducing a special type. `update --from-template` exactly replaces the target content and applicable metadata from a known named source; it performs no merge. `update --from PATH`, `file put`, `file remove`, and `metadata patch` are low-level writes. Kaoju skills invoke them only after preparing and assessing the intended state.

Immutable identity, template name, binding, record kind, content digest, state token, and audit fields remain service-controlled. Metadata patch accepts only allowed authored fields or an explicit extension namespace. Archive or delete follows reference-safety policy and never silently removes a template still selected by durable paper state.

Alternative considered: prohibit a template update command and allow only a prepared-revision wrapper. Low-level mutable CRUD is simpler, fits the intended API, and still prevents direct SQL or managed-file mutation.

### 5. High-Level Construction and Merge Remain Agentic

When a source is an arbitrary user-edited directory, the Kaoju agent inspects the source tree, current target tree, export metadata, and paper context. It determines intentional changes, identifies entrypoints, resolves structural differences, prepares a clean candidate, and calls low-level `template update` with the expected state token.

If the user requests a merge with another named template, export, or directory, the agent reads both inputs and constructs a third candidate. It then updates the target from that candidate. Isomer-cli never interprets a directory as a patch and never performs a semantic or generic text merge.

When the user explicitly requests replacement from another named template, no interpretation is required: `update --from-template` copies the known canonical tree and allowed metadata exactly into the target after concurrency checks.

### 6. Underspecified Updates Use Ordered Source Discovery

The discovery protocol applies only when the user asks to update the current artifacts-database template without supplying a template name, canonical ref, template path, or export path.

1. Query registered exports and recompute their tree digests. If exactly one eligible export differs from its recorded export digest, use that directory and its recorded target name.
2. If none qualifies, resolve `topic.paper.template_exchange_root` and use `<resolved-root>/main/` when it exists. Valid export metadata can confirm identity; otherwise target name is `main` by directory convention.
3. If neither source exists, ask the user which template or directory to use.

Multiple edited exports or inconsistent identity are ambiguous and require clarification. Explicit input bypasses discovery. Canonical database `main` is not the second source; the current Topic Workspace directory is.

### 7. Stable Working Directories Remain Non-Canonical

Workspace Path Resolution exposes `topic.paper.template_exchange_root`, defaulting to `<topic-workspace>/intent/derived/writing-template`. Default export appends the selected name, so unnamed export uses `main/`.

The arbitrary exported tree contains reserved `.isomer-template-export.json` metadata with template name, stable canonical ref, state token, canonical digest, exported digest, observed path, and time. Registered export status can report unchanged, edited, missing, identity-invalid, and canonical-changed posture.

Deterministic export writes a new directory or refreshes one that has not been edited. It refuses to overwrite an edited tree. Export reconciliation is agentic and remains non-canonical until an explicit template update succeeds.

### 8. Skills Explain Explicit Copies and Destructive Updates

Skills use low-level CRUD but own the high-level decision. Before replacing mutable named state, they report the selected target, current state token and digest, source, and whether an explicit named copy exists or is being created. They create a saved copy only when the user requests it or the agent explicitly chooses it within authorized scope; ordinary updates never create one silently.

Natural-language requests such as “save the current template before changing it” map to `create --from-template` with an agent- or user-chosen name. “Restore main from <name>” maps to exact `update --from-template`. “Merge main with <name>” maps to agent construction followed by `update --from`.

## Risks / Trade-offs

- [An ordinary update cannot restore prior bytes] → expose explicit named copy before destructive edits and clearly report when none exists.
- [Named copies can still accumulate] → they appear in the ordinary template list and can be explicitly archived or deleted; the system creates none automatically.
- [Mutable names weaken historical reproducibility] → drafts record observed digests, while exact recovery requires a deliberately preserved named copy.
- [Low-level update can be misused with an uninterpreted directory] → skills require agent inspection and assessment; CLI still enforces state token, integrity, and provenance but does not claim semantic correctness.
- [Concurrent agents can overwrite one another] → every mutation requires the current opaque state token and fails atomically when it is stale.
- [Several edited exports can match an unnamed request] → ask the user with concrete candidate names and paths rather than choosing by time.

## Migration Plan

1. Add the exchange-root surface, flexible directory content, and mutable named-state binding behavior.
2. Inspect old paper-line-scoped current records. Move one unambiguous current template into stable name `main`; require explicit names for distinct templates. Preserve old historical records as legacy reads without generating new revisions.
3. Add list, show, create, update, named copy, exact named replacement, file editing, metadata patch, archive or safe delete, export, and export-status operations.
4. Switch Kaoju skills to ordered discovery, agentic construction and merge, and explicit named-copy conventions.
5. Disable legacy `ext research templates` mutation, stop versioned default exports, and preserve existing directories non-destructively.
6. Test ordinary in-place logical update, explicit named copy, exact replacement, stale-state rejection, arbitrary tree editing, ordered source discovery, agentic merge, reference-safe removal, and migration.

Rollback restores prior binding and command routing. Mutable updates made after migration do not have automatic rollback content; rollback can recover only states that were explicitly copied to another name or remain in pre-migration legacy records.

## Open Questions

None. Templates use one flat namespace, ordinary updates mutate current named state, saved states are ordinary named copies, and high-level construction and merging remain agent-owned.
