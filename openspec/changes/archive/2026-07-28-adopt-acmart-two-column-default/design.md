## Context

Kaoju has two independent LaTeX default layers. The immutable packaged `latex/main` serves new-topic initialization and fallback selection, while a valid topic-owned `latex/main` takes precedence. Both currently contain the same IEEE Transactions tree. The accepted PowerInfer paper has canonical MyST content and historical IEEE TeX and PDF artifacts, and an off-record trial compiled the same content with the supplied ACM archive as a ten-page, two-column PDF.

The supplied `tmp/acmart-primary.zip` identifies archive commit `062edc8119be9067a346ce874281eab48b2c29a4`, has SHA-256 `027fe22f3c15fcd178f9d84d32a7e0a96f68357df1fa6712c808cc078ee6fdd7`, and contains `acmart` 2.19. Its README labels the GitHub package experimental, but the actor explicitly selected this archive after a successful local trial. Generated class and sample headers require their `.dtx` sources to accompany distribution.

## Goals / Non-Goals

**Goals:**

- Make a pinned, self-contained ACM `sigconf,nonacm` two-column tree the checked packaged LaTeX `main`.
- Keep the default neutral by omitting invented ACM rights, DOI, conference, ISBN, CCS, affiliation, and researcher-identity metadata.
- Validate the ACM document class and title, author, abstract, and keyword constructs before accepting packaged or topic-owned stock that declares the ACM venue.
- Replace `pwinfer-analysis` topic-owned LaTeX `main` through the typed optimistic-concurrency boundary and refresh its clean exchange copy.
- Recompose and rebuild the accepted PowerInfer survey without changing its canonical MyST meaning.
- Preserve all earlier named-template snapshots, TeX drafts, build runs, and PDFs as historical artifacts.

**Non-Goals:**

- Do not create an ACM submission-ready rights or conference configuration.
- Do not migrate every existing Topic Workspace or rewrite historical snapshots.
- Do not change the content-template role, canonical MyST, accepted evidence, or publication Gate.
- Do not publish or synchronize the rebuilt topic workspace to a remote repository.
- Do not bundle generated ACM documentation PDFs, sample PDFs, Git configuration, or Git metadata.

## Decisions

### Use neutral `sigconf,nonacm` as packaged `main`

The entrypoint will use `\documentclass[sigconf,nonacm]{acmart}`. This produces the requested two-column ACM layout while suppressing fake publication metadata. Standard `sigconf` was rejected as the generic default because it expects venue-specific rights and conference fields. A later submission target can be stored as another named LaTeX template.

### Package source-complete runtime material without generated PDFs

The packaged tree will retain the upstream class, class source and installer, bibliography styles, source samples and their `.dtx` inputs, license, README, and source assets. It will exclude generated documentation and sample PDFs plus `.gitconfig`, `.gitignore`, and unrelated repository metadata. The Isomer-authored `template.tex` will be a renamed marker-based derivative of `sigconf.tex`, satisfying the upstream requirement that modified generated samples use another filename.

The loader will validate an ACM required-member subset instead of encoding an exact flat five-file IEEE inventory. The deterministic tree digest still binds every packaged byte, including additional upstream source files.

### Declare and validate an ACM venue contract

Authored metadata will declare venue `acm-sigconf`, marker composition, Tectonic, the exact archive and commit, upstream entrypoint `samples/sigconf.tex`, and LPPL posture. Venue validation will require document class `acmart` and the constructs `\title{`, `\author{`, `\begin{abstract}`, and `\keywords{`. The packaged metadata file and manifest copy must remain identical.

### Change packaged identity explicitly

The packaged resource version will advance from `0.6.0` to the current project version `0.6.1`, and the manifest tree digest will be regenerated. This prevents the ACM bytes from masquerading as the old packaged identity.

### Update topic stock through the existing typed service

The implementation will prepare the exact ACM tree and authored metadata outside managed storage, re-read the current `pwinfer-analysis` state token, then call `template update --kind latex --name main --from ... --metadata-file ... --expected-state ...`. The typed update surface will validate and commit a replacement tree and replacement authored metadata atomically so a document-class or venue transition cannot deadlock on the old metadata contract. It will not edit the state database or managed artifact directory directly. Because the registered exchange is currently unchanged, a subsequent default export can refresh `intent/derived/writing-templates/latex/main` safely.

### Rebuild from canonical MyST as a new derived lineage

The existing `paper-draft-myst-pwinfer-e2e-offloading-20260728` remains canonical. `init-tex` will observe the new topic `main`, produce a new incompatible template snapshot and TeX draft, and retain the same citation map and accepted audit inputs. Agent filling may apply presentation-only ACM repairs, but content or evidence changes require a separate paper revision. Each compile attempt produces a distinct build run and log. The final PDF must pass text extraction, citation and table counts, and direct inspection of every page. Publication remains pending.

## Risks / Trade-offs

- **Pinned archive is an upstream development snapshot** → Record its archive digest, commit, class version, and README posture; keep replacement explicit rather than silently following upstream.
- **Source-complete ACM material increases package size** → Exclude generated PDFs and Git metadata while retaining required source and license material.
- **ACM requires richer author metadata for actual submission** → Keep `main` neutral and omit fabricated affiliations; use a named submission template when a real venue supplies those fields.
- **Dense full-width tables may be small in `sigconf`** → Inspect every page and keep any sizing or line-breaking adjustment paper-local unless a generic repair clearly belongs in stock.
- **Changing packaged fallback could surprise new builds** → Change the packaged identity and update specifications, skill guidance, and tests. Existing topic stock and historical artifacts remain untouched unless explicitly selected.
- **Topic update could race another template edit** → Re-read and supply the exact current state token immediately before the typed update.

## Migration Plan

1. Replace and validate packaged ACM resources, metadata, manifest version, and digest.
2. Update code, specifications, skills, documentation, and tests; run lint, typecheck, unit tests, and targeted integration tests.
3. Re-read `pwinfer-analysis` LaTeX `main` and export status.
4. Atomically replace stable topic `main`, then refresh the unchanged exchange directory.
5. Initialize and fill a new ACM TeX line from the accepted MyST and citation map.
6. Build and inspect the new PDF, preserving publication as a separate pending Gate.
7. Verify that old IEEE snapshots and PDFs still resolve.

Rollback of the packaged source uses the prior Git revision. Topic rollback is not implicit because named-template update does not retain restorable bytes; if required, an actor can explicitly replace `main` from the historical IEEE template snapshot through the adoption route. Historical paper artifacts need no rollback.

## Open Questions

None. The actor selected the supplied archive, neutral two-column ACM presentation, explicit topic replacement, and local PDF recreation.
