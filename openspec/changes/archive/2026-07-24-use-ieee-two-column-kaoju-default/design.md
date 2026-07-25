## Context

Kaoju loads immutable packaged writing-template defaults from the `isomer-kaoju-write` system-skill assets and identifies each default by role, name, resource version, and deterministic tree digest. The current `latex/main` contains one project-authored `article` entrypoint. Topic initialization copies that tree into topic-owned stock, while ordinary default selection uses it directly only when ready topic-owned `latex/main` is absent.

The Predictive Memory Survey later adopted a prepared IEEE Transactions template at `tmp/kaoju-ieee-real-template/`. Its source provenance points to `tmp/IEEE-Transactions-LaTeX2e-templates-and-instructions.zip` with SHA-256 `6c315c3b6729bd7b96a6a0e7d3bb6342023413a4cd4d113fb4a193019af1c603` and upstream entrypoint `bare_jrnl_new_sample4.tex`. The prepared tree contains `template.tex`, `IEEEtran.cls`, `bare_jrnl_new_sample4.tex`, `fig1.png`, and `metadata.json`; its marker-based entrypoint uses `\documentclass[lettersize,journal]{IEEEtran}` and `% ISOMER_BODY`. The current Predictive Memory Survey `latex/main` canonical state matches those five files and records the prepared tree as its update source.

The package must preserve the IEEE presentation without reading `tmp/` at runtime. It must also honor the existing immutable-template and paper-snapshot rules, including the fact that changing a packaged default does not authorize replacement of topic-owned stock or historical paper artifacts.

## Goals / Non-Goals

**Goals:**

- Make the prepared IEEE Transactions two-column tree the installed Kaoju `latex/main` default.
- Vendor the local IEEE class and all other files in the prepared source tree so export, topic initialization, and paper-local snapshotting preserve the complete presentation tree.
- Keep upstream-controlled files and notices intact, record stable provenance and LPPL 1.3 posture, and give the replacement tree a new packaged identity through its resource version and digest.
- Verify source-tree and built-package behavior, including the presence of `IEEEtran.cls`, the entrypoint contract, full-tree copying, and topic-stock precedence.
- Update Kaoju skill guidance and tests that currently describe the fallback as a neutral article.

**Non-Goals:**

- Do not change the generic MyST `content/main` scaffold.
- Do not replace, migrate, or compare existing topic-owned `latex/main` records merely because the packaged default changed.
- Do not rewrite existing paper template snapshots, TeX drafts, PDFs, or edited derived-intent exports.
- Do not turn IEEE into a new selectable template role or add a general venue-template catalog.
- Do not vendor unrelated TeX Live packages such as `algorithm`, `subfig`, or `cite`; they are compiler-distribution dependencies and are not files supplied by the prepared IEEE source tree. The IEEE-specific `IEEEtran.cls` is vendored locally.

## Decisions

### Use the Prepared Predictive Memory Survey Tree as the Vendoring Baseline

Implementation will source the replacement from `tmp/kaoju-ieee-real-template/`, cross-checked against the Predictive Memory Survey canonical `latex/main` artifact, rather than inventing a new skeleton or consuming either ZIP at runtime. This baseline is already known to satisfy Kaoju's marker composition and venue-structure validation.

The packaged `latex/main` tree will contain the five prepared members: `template.tex`, `IEEEtran.cls`, `bare_jrnl_new_sample4.tex`, `fig1.png`, and `metadata.json`. `template.tex` becomes the manifest entrypoint. `IEEEtran.cls`, the upstream sample, and its figure retain their source bytes; package-local metadata may replace disposable `tmp/` locators with stable archive provenance while retaining the upstream archive name, checksum, entrypoint, and license posture.

Using only `template.tex` plus a system-installed IEEE class was rejected because it would lose the requested style dependency and make output depend on host state. Vendoring the entire downloaded archive was also rejected because PDFs and how-to documents were not members of the prepared template tree used by the survey and are not required for composition.

### Treat the IEEE Class as Part of Every Managed Tree Copy

No loader or compiler special case will locate `IEEEtran.cls`. Existing arbitrary multi-file template behavior will copy and checksum it with the rest of `latex/main` during initialization, export, promotion, and paper-local snapshotting. TeX then resolves the local class beside the composed entrypoint.

This preserves the current storage model and makes missing or altered class bytes visible through the existing tree-digest checks. Adding an external class search path was rejected because it would bypass managed-tree integrity and installed-package portability.

### Change Packaged Identity Without Migrating Existing State

The packaged-template manifest will receive a new resource version aligned with the current project release (`0.6.0`) and a recomputed `latex/main` tree digest. Authored metadata will declare the `template.tex` entrypoint, `% ISOMER_BODY` marker composition, `tectonic` build profile, `ieee-transactions` venue, stable source provenance, and LPPL 1.3 posture.

Ready topic-owned stock continues to win. Existing topic stock created from the former article default remains unchanged because it is now independent canonical state. A topic with no stock observes the new packaged default immediately. Existing packaged-origin exports retain their recorded old identity and are reported through current stale or canonical-changed handling rather than silently refreshed. Existing paper snapshots retain the exact packaged identity and bytes they originally observed.

Keeping resource version `0.5.0` was rejected because the identity must distinguish the materially different immutable fallback. Automatically replacing old topic stock was rejected because source provenance does not grant mutation authority.

### Validate Both Source and Distribution Boundaries

Unit coverage will assert the IEEE document class and composition marker, required five-file inventory, deterministic digest, venue and license metadata, and local class presence. Initialization, export, and paper initialization coverage will assert that `IEEEtran.cls` and companion files survive complete-tree copies and that topic-owned selection precedence remains unchanged.

A built wheel or equivalent installed-resource check will confirm that non-Python assets, including the class and PNG, are shipped. A compiler-backed smoke test may run when Tectonic is available, but deterministic unit tests will not require network access or dynamically download a venue template.

## Risks / Trade-offs

- [The built-in fallback now expresses an IEEE Transactions venue choice rather than a neutral presentation] → State this explicitly in manifest and skill guidance, preserve explicit topic templates, and keep the content template venue-neutral.
- [The 2015 IEEEtran class is older than some host-installed releases] → Preserve the exact version proven by the survey and its provenance; future upgrades require a separate reviewed default-resource change.
- [LPPL conditions or upstream notices could be lost during copying] → Keep `IEEEtran.cls` byte-for-byte, retain its embedded notices, record LPPL 1.3 in authored metadata, and test provenance and license fields.
- [The entrypoint imports TeX packages not included in the IEEE archive] → Treat those as declared toolchain dependencies, keep the `tectonic` build profile, and distinguish them from the vendored IEEE-specific class.
- [Existing packaged-origin exports become stale relative to the new default] → Use existing identity and digest reconciliation; never overwrite editable exports automatically.
- [Binary or non-Python members could be omitted from a built distribution] → Add distribution-resource inspection for `IEEEtran.cls` and `fig1.png`.

## Migration Plan

1. Copy the five prepared template members into the packaged `latex/main` directory and remove the superseded neutral `main.tex`.
2. Normalize package-stable authored metadata, bump the packaged-template resource version to `0.6.0`, and recompute the complete tree digest.
3. Update skill guidance and deterministic tests for the new IEEE default and full-tree behavior.
4. Build and inspect the distribution, then run Kaoju template, initialization, paper-production, lint, type-check, and unit-test validation.
5. Roll back by restoring the prior packaged tree and manifest digest. Topic-owned templates and historical paper artifacts need no rollback because the deployment never mutates them.

## Open Questions

None. The selected source tree, entrypoint, style dependency, selection semantics, and migration posture are fixed by the request and current Kaoju contracts.
