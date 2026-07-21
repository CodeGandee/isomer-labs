# Design: fix-kaoju-paper-tex-composition

## Context

The predmem-survey paper PDF exposed two defects. First, the stored LaTeX template (`artifact-paper-template-latex-main`) was a 16-line hand-written stub whose manifest recorded only checksums of the official `bare_jrnl_new_sample4.tex`; template adoption (`KaojuTemplateService` in `src/isomer_labs/kaoju/templates.py`) copies whatever directory it is given and `template_validation.py:75-113` validates only authored metadata, so the stub passed. Second, `init_tex` (`src/isomer_labs/kaoju/paper.py:252-437`) converts MyST with `_myst_to_tex` (`paper.py:674-704`), a line-by-line regex pass with no frontmatter handling, a hardcoded `\title{Survey Paper}` in `paper_support.py:46-55`, no bibliography path, and tables dropped to `% ISOMER_REPAIR_TABLE` markers. The integration test never asserts composed TeX content.

The user decision that frames this design: the copy behavior of template adoption is correct (the actor hands over a directory, the system packs it); what failed was the content that was adopted. And MyST-to-TeX is not meant to be mechanical — the agent should read the filled MyST and fill the LaTeX template by content judgment, with MyST as the complete content source and TeX as presentation.

## Goals / Non-Goals

**Goals:**
- Template adoption validation detects placeholder/reference-only shims and requires the real venue tree with venue constructs present.
- `init-tex` becomes a scaffold-plus-fill-contract step: real template tree, fill manifest of obligations, no pretense of faithful auto-conversion.
- Silent pass-through (frontmatter dump, placeholder title, unresolved citations, literal Title/Abstract sections) becomes named diagnostics that block inspected/build-ready status.
- Bibliography materialization from the citation map is a first-class fill obligation.
- Skill docs (`isomer-kaoju-write`, `latex-build.md`) describe the agent fill procedure accurately; tests assert composed-TeX content.

**Non-Goals:**
- No migration of existing topic-workspace template records (for example the predmem stub); this change defines the corrected procedure. Re-adopting the real IEEE tree there is follow-up operations work.
- No full pandoc-class structural converter; the agent is the converter, the CLI only scaffolds and validates.
- No change to the MyST canonical model, the publication Gate, or the build toolchains.

## Decisions

**D1: Keep verbatim directory adoption; add content checks at validation.**
Alternatives: (a) keep metadata-only validation — rejected, that is how the stub got in; (b) force a fixed template schema — rejected, the spec already allows arbitrary tree shape for named templates. Chosen: after copy, validation inspects the entrypoint for venue constructs (document class, `\title`/author block, abstract and keywords environments) when the metadata declares a venue, and rejects shim-shaped candidates (short entrypoint whose only venue linkage is a comment or checksum reference). Detection is heuristic and conservative: it flags "claims a venue but lacks its constructs", it does not police TeX style.

**D2: Replace the silent regex converter with scaffold + fill manifest, not with a smarter converter.**
Alternatives: (a) build real frontmatter/abstract/bibliography conversion into `_myst_to_tex` — rejected by the user's contract statement that composition is agent judgment; a mechanical converter would keep pretending completeness it cannot deliver; (b) leave the converter as-is and fix docs only — rejected, silent failures stay silent. Chosen: `init_tex` materializes the adopted template tree, performs only mechanical staging (frontmatter extraction into the fill manifest, `\cite` key collection, table/directive location marking), and emits a fill manifest listing each obligation with MyST locators and TeX targets. The agent then fills. The hardcoded `\title{Survey Paper}` block is removed from composition; title and author come from the fill.

**D3: Unfilled obligations are hard diagnostics.**
`validate`/inspection gains checks for the known pass-through signatures: raw `---` frontmatter in body, placeholder title, `\section{Title}`/`\section{Abstract}` in venue templates, `\cite` keys with no bibliography file or environment, remaining `ISOMER_REPAIR_TABLE` markers. Any open obligation blocks the `inspected` flag that `build_pdf` requires, extending the existing gate (`paper.py:536-537`) rather than adding a new one.

**D4: Bibliography comes from the citation map, filled by the agent.**
`init-tex` already accepts `--citation-ref`; today it only echoes refs into the manifest. The fill manifest will include the parsed citation-map entries (key, source ref, available bibliographic metadata) so the agent can write a `.bib` or `thebibliography`. Entries lacking metadata become a reported prerequisite, matching the existing pause-for-prerequisite posture.

**D5: MyST content template gains no Title/Abstract body headings.**
The current MyST template emits `# Title` and `# Abstract` as body headings, which guarantees wrong sections under any heading mapper. The content template should carry frontmatter title/authors and an abstract block the composition contract can map to venue environments. This is a template-content correction delivered with the skill doc updates, keeping canonical MyST complete (frontmatter + abstract are content, so MyST still holds everything TeX shows).

## Risks / Trade-offs

- [Heuristic shim detection misfires on a legitimate minimal template] → Detection only triggers when metadata declares a venue whose constructs are absent; the actor can adopt the same tree under a neutral venue declaration, and the rejection message explains what was missing.
- [Agent fill quality varies, PDFs could still look wrong] → The unfilled-obligation diagnostics and the existing inspected/build gates make the known failure signatures unbuildable; remaining quality risk is reviewable in the composition report and at the publication Gate.
- [Older drafts reference the stub template's compatibility fingerprint] → No record migration; new compositions require a template that passes the new validation, and the fingerprint mechanism already forces a template revision when constructs change.
- [Fill manifest adds a new artifact shape to maintain] → It reuses the existing manifest JSON pattern and diagnostics channels; no new Artifact binding is required in this change.

## Migration Plan

1. Update specs (this change), then implement validation + scaffold changes in `src/isomer_labs/kaoju/`.
2. Update `isomer-kaoju-write` skill docs and the MyST content template to match the fill contract.
3. Extend integration tests with composed-TeX content assertions and shim-rejection cases.
4. Rollback: revert the validation additions; the prior copy behavior is untouched and old template records remain readable.

## Open Questions

- Should the fill manifest be registered as its own typed Artifact (for example `kaoju:paper-composition-report`) so the publication Gate can cite it directly, or is a file inside the TeX tree manifest sufficient for now?
- For venues without a declared template in metadata, which minimal construct set (if any) should validation require?
