# Proposal: fix-kaoju-paper-tex-composition

## Why

The Kaoju paper pipeline produces PDFs that do not look like venue papers. A built predmem-survey PDF showed raw MyST frontmatter as page-one body text, the hardcoded placeholder title "Survey Paper", `Title` and `Abstract` rendered as numbered sections, every citation as `[?]`, and all tables dropped. Investigation traced this to two contract failures: the stored LaTeX template artifact was a 16-line hand-written stub that only referenced the official IEEE template by checksum, and the `init-tex` converter was built as a mechanical regex transformer even though the design intent is agent-mediated composition, where the agent reads the filled MyST and fills the LaTeX template by content judgment.

## What Changes

- **Template adoption packs real content.** The template CRUD procedure already copies an actor-prepared directory verbatim into managed storage; the failure was that a stub directory was adopted as the "IEEE Transactions" template. Clarify and enforce that template adoption packs the whole directory content (files and byte streams) into the artifact store, and that adopting a venue template means ingesting the actual template tree (entrypoint `.tex`, class files, assets), not a hand-written shim that names the official file in a comment.
- **MyST-to-TeX is agent composition, not mechanical conversion.** Restate the contract: MyST is canonical and must contain all content of the TeX version (or more); TeX is a presentational projection; drift between them is permitted only for formatting requirements. Replace the pretense of automatic conversion with an explicit agent-fill procedure: `init-tex` scaffolds the template tree and a structured fill contract (frontmatter to `\title`/`\author`, abstract/keywords to IEEEtran environments, citation-map to a real bibliography, tables to real LaTeX tables), and the agent performs and records the fill before build.
- **Silent failures become loud.** Frontmatter passthrough, placeholder title/author, and missing bibliography currently produce no diagnostic. The fill contract and validation must detect and report them the way dropped tables already are.
- **Docs and tests align with the agent-composition contract.** `latex-build.md` claims "Parse MyST structurally"; the integration test never asserts composed TeX content. Both must reflect the real contract.

## Capabilities

### New Capabilities

- `kaoju-tex-agent-composition`: the agent-mediated MyST-to-TeX fill contract, covering content completeness (MyST holds all TeX content), presentation-only drift, the structured fill obligations (frontmatter, abstract/keywords, bibliography, tables), and the diagnostics that make unfilled or mechanically-passed-through content visible.

### Modified Capabilities

- `kaoju-paper-production`: requirements for LaTeX template adoption change from "copy an actor-prepared directory with metadata validation" to "pack the full template tree content as the venue template, rejecting placeholder or reference-only shims"; init-tex and build requirements change from mechanical-conversion-plus-unstructured-repair to the agent-composition fill contract with named diagnostics.

## Impact

- Specs: `openspec/specs/kaoju-paper-production/spec.md` (delta), new `openspec/specs/kaoju-tex-agent-composition/spec.md`.
- Code: `src/isomer_labs/kaoju/paper.py` (`init_tex`, `_myst_to_tex`, diagnostics), `src/isomer_labs/kaoju/paper_support.py` (composition, placeholder title), `src/isomer_labs/kaoju/templates.py` and `template_validation.py` (template adoption checks).
- Skills: `isomer-kaoju-write` SKILL.md and `references/latex-build.md` (agent fill procedure), possibly `commands/build-paper-pdf.md`.
- Records: existing stub LaTeX template artifacts in topic workspaces (for example the predmem-survey `artifact-paper-template-latex-main`) need re-adoption from the real template tree; this change defines the corrected procedure, not a migration of live records.
- Tests: `tests/integration/test_kaoju_paper_wiki.py` gains composed-TeX content assertions.
