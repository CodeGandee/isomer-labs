# Tasks: fix-kaoju-paper-tex-composition

## 1. Template Adoption Validation

- [x] 1.1 In `src/isomer_labs/kaoju/template_validation.py`, add a venue-construct check: when adopted LaTeX template metadata declares a venue, verify the stored entrypoint contains that venue's document class and title/author/abstract/keywords constructs.
- [x] 1.2 Add shim rejection: detect a short hand-written entrypoint whose only venue linkage is a comment or checksum reference to an external official template, and reject adoption with an explanatory diagnostic.
- [x] 1.3 Confirm verbatim directory packing (whole tree, per-file checksums) remains the adoption behavior; add or adjust tests in the template service test module covering real-tree adoption, shim rejection, and missing-construct rejection.

## 2. init-tex Scaffold and Fill Contract

- [x] 2.1 In `src/isomer_labs/kaoju/paper.py` (`init_tex`), materialize the adopted venue template tree as the scaffold base and emit a fill manifest listing composition obligations with MyST locators and TeX targets: frontmatter-to-title/author mapping, abstract and keywords environments, section mapping, bibliography materialization from `--citation-ref` entries, tables, floats, venue constructs.
- [x] 2.2 Extract MyST frontmatter (title, authors, date) and abstract into the fill manifest instead of passing them through as body text; strip `# Title`/`# Abstract` style body headings from conversion input.
- [x] 2.3 Remove the hardcoded `\title{Survey Paper}`/`\author{}` injection in `src/isomer_labs/kaoju/paper_support.py` (composition branch) and delete the dead `_tex_template`/`_tex_document` twins in `paper.py`.
- [x] 2.4 Parse the referenced `kaoju:citation-map` entries into the fill manifest (key, source ref, bibliographic metadata) and report entries lacking usable metadata as a prerequisite pause.

## 3. Unfilled-Obligation Diagnostics

- [x] 3.1 Add validation checks for mechanical pass-through signatures: raw `---` frontmatter in TeX body, placeholder title/author, `\section{Title}`/`\section{Abstract}`, `\cite` keys with no bibliography present, remaining `% ISOMER_REPAIR_TABLE` markers.
- [x] 3.2 Wire these checks into the inspected/build-ready gate so `build_pdf` refuses trees with open obligations, extending the existing `--inspected` requirement.

## 4. Skill Docs and Content Template

- [x] 4.1 Update `isomer-kaoju-write` SKILL.md and `references/latex-build.md` to describe the agent fill procedure (scaffold, fill manifest, recorded decisions) instead of "parse MyST structurally" mechanical language.
- [x] 4.2 Correct the MyST content template so title/authors live in frontmatter and abstract is a mappable block, removing `# Title`/`# Abstract` body headings.

## 5. Tests and Verification

- [x] 5.1 Extend `tests/integration/test_kaoju_paper_wiki.py` with composed-TeX content assertions: no raw frontmatter, real title from MyST, abstract environment present, every `\cite` key resolvable, no unrepaired table markers after a recorded fill.
- [x] 5.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 5.3 Re-adopt the real IEEE template tree in the predmem-survey workspace (operations step, not code) and rebuild the paper PDF through the new fill procedure as the end-to-end validation.
