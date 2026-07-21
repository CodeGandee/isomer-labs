## Context

Kaoju uses MyST as canonical paper content. Its only mutable named template service is hard-coded to `KAOJU:PAPER-TEMPLATE-MYST`, while `KAOJU:PAPER-TEMPLATE-TEX` is a revisioned paper-line derivation. `init-tex` currently generates a fresh preamble from CLI flags, includes the MyST template digest in the TeX compatibility fingerprint, and never composes a user-stocked LaTeX tree. `build-pdf` validates a TeX-template ref but compiles only the draft tree through a hard-coded `main.tex` entrypoint. Current Topic Workspaces therefore accumulate derived TeX revisions without a durable presentation default.

The existing managed-directory, mutable-state, optimistic-concurrency, export-observation, Artifact lineage, Run, and execution-extension infrastructure is sufficient. The change needs a second template-kind contract and correct composition, not another storage subsystem.

The active `regroup-system-skills` change will relocate Kaoju skill resources. This design targets stable logical skill and semantic identities so implementation can coexist with that packaging change.

## Goals / Non-Goals

**Goals:**

- Use “content template” for MyST authoring structure and “LaTeX template” for presentation bundles everywhere users and agents make a choice.
- Provide independent named `content/main` and `latex/main` state in every Topic Workspace.
- Support arbitrary safe multi-file LaTeX trees, including document classes, styles, bibliography styles, assets, includes, and explicit composition metadata.
- Preserve a stable mutable stock for editing while capturing exact immutable or revisioned snapshots for reproducible paper builds.
- Make composition and compilation consume the selected LaTeX bytes and declared entrypoint.
- Preserve current MyST authority, evidence rules, build Runs, PDF validation, and publication Gates.
- Migrate existing Topic Workspace records and adopt unambiguous active TeX presentation state without deleting historical artifacts.

**Non-Goals:**

- Make LaTeX canonical paper content.
- Infer MyST content from legacy TeX.
- Implement arbitrary template merging or arbitrary shell build recipes inside `isomer-cli`.
- Automatically promote paper-specific TeX repairs into stocked LaTeX templates.
- Add a dedicated SQL table or Git-like history for mutable template stock.

## Decisions

### Keep two named template namespaces with independent `main` records

`KAOJU:PAPER-TEMPLATE-MYST` remains the durable content-template identity. A new `KAOJU:PAPER-TEMPLATE-LATEX` binding owns named mutable LaTeX stock. Both use path-safe names, stable refs, state tokens, tree digests, atomic managed-tree replacement, explicit named copies, mutation audits, and registered working-copy exports.

The stable refs are `artifact-paper-template-myst-<name>` for content and `artifact-paper-template-latex-<name>` for LaTeX. `main` is the default only within its namespace. This avoids a global default pointer and matches the user's omitted-name rule.

Repurposing `KAOJU:PAPER-TEMPLATE-TEX` as mutable stock was rejected because existing records use paper-line current-state lineage. It remains the exact derived snapshot selected for one paper composition.

### Parameterize the existing named-template service

Introduce a checked template-kind descriptor containing the semantic id, stable-ref prefix, user-facing label, exchange subdirectory, validation policy, and supported metadata. `KaojuTemplateService` and its state boundary receive one descriptor instead of importing MyST-only constants.

The CLI adds `--kind content|latex`, defaulting to `content` only for backward compatibility. New skill guidance always passes the kind explicitly. This keeps the existing command family and avoids duplicating every CRUD command under nested Click groups.

Export paths become `<template-exchange-root>/content/<name>/` and `<template-exchange-root>/latex/<name>/`. Existing `<template-exchange-root>/<name>/` content exports remain readable during migration but are not selected for new LaTeX operations. Export metadata records the kind, stable ref, state token, canonical digest, exported digest, path, actor, and authored metadata.

### Require a bounded LaTeX composition contract

LaTeX authored metadata requires an entrypoint and an `extensions.latex` object. The first contract version supports three deterministic composition modes:

- `preamble`: the selected file is a preamble fragment and the composer produces a complete `main.tex`.
- `marker`: the entrypoint is a complete document containing one declared marker that the composer replaces with generated paper content.
- `include`: the entrypoint is a complete document that already includes one declared generated body path, and the composer writes only that body file.

The contract also records a registered build profile, optional venue and document-class observations, source provenance, license posture, and use guidance. It never stores arbitrary command lines. Unsupported or ambiguous source trees remain agent-preparation work before low-level create or update.

`preamble` provides a lossless migration route for existing generated `template.tex` trees. `marker` and `include` support publisher packages without flattening their files.

### Compose exact content and presentation state

The TeX initializer becomes a composer. It resolves the exact canonical MyST draft, its observed content-template state, and either an explicit LaTeX template or `latex/main`. It creates or revises `KAOJU:PAPER-TEMPLATE-TEX` as a full snapshot of the selected stocked tree with its stable ref, name, state token, digest, authored metadata, and composition contract. It then creates a self-contained `KAOJU:PAPER-DRAFT-TEX` tree from that snapshot plus generated paper content.

The presentation compatibility fingerprint includes the LaTeX stock digest, composition contract, converter identity, required constructs, and build profile. The MyST draft checksum is recorded separately as draft lineage. A content-template edit never creates LaTeX-template drift by itself.

The composer requires agent inspection after mechanical conversion. Paper-local repairs revise only `KAOJU:PAPER-DRAFT-TEX`. Stock changes require the explicit named-template update workflow.

### Make builds entrypoint-aware and template-enforcing

`build-pdf` reads the draft manifest, verifies that its pinned template snapshot matches the supplied template ref when one is supplied, validates the snapshot digest, and compiles the self-contained composed tree. The declared entrypoint determines the compiler input and expected PDF name.

Build profiles remain registered, provider-neutral selections. The initial profiles retain Tectonic, latexmk, and pdfLaTeX support. Later engines or bibliography workflows can extend the checked profile registry without accepting shell commands from template metadata.

The redundant template-ref option remains during compatibility migration, but a mismatch becomes an error instead of being ignored.

### Represent drift explicitly

Template exchange reports working-copy drift using the existing digest comparison. Paper status and composition report stocked-template drift when a TeX draft's observed LaTeX token or digest differs from current named state. A derived TeX revision records paper-local repair drift separately.

No drift state triggers automatic mutation. Recomposition is explicit, and promoting a repair to stock requires the user to request a LaTeX-template update.

### Preserve records and migrate in place

The migration service annotates existing named MyST records as kind `content` without changing their stable refs. It preserves existing exports and can register or refresh their compatibility posture under the new metadata schema.

An actor-authorized LaTeX adoption copies one selected `KAOJU:PAPER-TEMPLATE-TEX` or legacy `KAOJU:WRITING-TEMPLATE` tree into `latex/<name>`, validates or supplies its composition metadata, and records the source ref. Historical source records remain unchanged.

Repository migration enumerates registered Topic Workspaces, upgrades content records, inspects current TeX candidates, adopts only an unambiguous or explicitly selected candidate as `latex/main`, and reports topics that lack a candidate instead of inventing one. For `predmem-survey`, the explicitly selected IEEE Transactions artifact is the adoption source.

## Risks / Trade-offs

- [Publisher templates may not expose a deterministic insertion point] → Require agent preparation and one checked composition mode before stocking them as ready.
- [Mutable stock does not retain prior bytes] → Preserve the existing explicit named-copy model and capture every used LaTeX state in derived TeX snapshots.
- [Two `main` records can confuse unqualified requests] → Require explicit terminology in skills and ask only when natural-language context cannot distinguish content from LaTeX.
- [Existing exports occupy the old root path] → Keep compatibility discovery for content exports and place all new exports in kind-specific subdirectories.
- [Current TeX records may have incomplete manifests] → Adoption validates the tree and requires explicit composition metadata rather than relabeling records in place.
- [Tests can pass with a fake compiler while ignoring template bytes] → Add integration tests that require a template-owned class or style file and fail when the selected tree is not composed.
- [The concurrent skill-regrouping change moves files] → Modify stable logical resources now and resolve path conflicts when either change is applied or rebased.

## Migration Plan

1. Add the new semantic and binding contracts without mutating current records.
2. Parameterize named-template state and expose format-explicit CLI operations.
3. Add LaTeX composition validation, exact snapshot creation, entrypoint-aware builds, and drift reporting.
4. Update skills, process resources, profiles, docs, and tests.
5. Run the Topic Workspace contract migration in preview mode and resolve every ambiguous presentation candidate explicitly.
6. Apply migration to all registered Topic Workspaces. Adopt the approved IEEE Transactions tree as `predmem-survey` LaTeX `main`.
7. Validate Project state, every Workspace Runtime, template manifests, query indexes, composed builds, and OpenSpec conformance.

Rollback disables new LaTeX mutations and restores legacy command routing while retaining the new records and managed trees as readable Artifacts. It does not delete exports, historical TeX records, drafts, builds, or PDFs.

## Open Questions

None. The user selected the terminology, default-name rule, implementation, and current-workspace migration scope.
