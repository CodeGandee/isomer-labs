# Write Migration Provenance

This directory preserves the upstream DeepScientist `write` source and the analysis used to refactor it into `isomer-rsch-write`.

## Inventory

- `src/`: untouched copy of `extern/orphan/DeepScientist/src/skills/write/`, including the source entrypoint and all source support files.
- `analysis/analysis-of-write.md`: source-process analysis copied from `context/explore/deepscientist-skill-analysis/write.md`.

## Analysis Coverage

Analyzed workflow-bearing files:

- `src/SKILL.md`
- `src/references/experiments_analysis_patterns.md`
- `src/references/oral_package_patterns.md`
- `src/references/oral_writing_principles.md`
- `src/references/section_rewrite_checklist.md`

Copied but not treated as workflow-bearing instructions:

- `src/templates/DEEPSCIENTIST_NOTES.md`
- `src/templates/README.md`
- `src/templates/UPSTREAM_LICENSE.txt`
- `src/templates/aaai2026/README.md`
- `src/templates/aaai2026/aaai2026-unified-supp.tex`
- `src/templates/aaai2026/aaai2026-unified-template.tex`
- `src/templates/aaai2026/aaai2026.bib`
- `src/templates/aaai2026/aaai2026.bst`
- `src/templates/aaai2026/aaai2026.sty`
- `src/templates/acl/README.md`
- `src/templates/acl/acl.sty`
- `src/templates/acl/acl_latex.tex`
- `src/templates/acl/acl_lualatex.tex`
- `src/templates/acl/acl_natbib.bst`
- `src/templates/acl/anthology.bib.txt`
- `src/templates/acl/custom.bib`
- `src/templates/acl/formatting.md`
- `src/templates/asplos2027/main.tex`
- `src/templates/asplos2027/references.bib`
- `src/templates/colm2025/README.md`
- `src/templates/colm2025/colm2025_conference.bib`
- `src/templates/colm2025/colm2025_conference.bst`
- `src/templates/colm2025/colm2025_conference.sty`
- `src/templates/colm2025/colm2025_conference.tex`
- `src/templates/colm2025/fancyhdr.sty`
- `src/templates/colm2025/math_commands.tex`
- `src/templates/colm2025/natbib.sty`
- `src/templates/iclr2026/fancyhdr.sty`
- `src/templates/iclr2026/iclr2026_conference.bib`
- `src/templates/iclr2026/iclr2026_conference.bst`
- `src/templates/iclr2026/iclr2026_conference.sty`
- `src/templates/iclr2026/iclr2026_conference.tex`
- `src/templates/iclr2026/math_commands.tex`
- `src/templates/iclr2026/natbib.sty`
- `src/templates/icml2026/algorithm.sty`
- `src/templates/icml2026/algorithmic.sty`
- `src/templates/icml2026/example_paper.bib`
- `src/templates/icml2026/example_paper.tex`
- `src/templates/icml2026/fancyhdr.sty`
- `src/templates/icml2026/icml2026.bst`
- `src/templates/icml2026/icml2026.sty`
- `src/templates/neurips2025/Makefile`
- `src/templates/neurips2025/extra_pkgs.tex`
- `src/templates/neurips2025/main.tex`
- `src/templates/neurips2025/neurips.sty`
- `src/templates/nsdi2027/main.tex`
- `src/templates/nsdi2027/references.bib`
- `src/templates/nsdi2027/usenix-2020-09.sty`
- `src/templates/osdi2026/main.tex`
- `src/templates/osdi2026/references.bib`
- `src/templates/osdi2026/usenix-2020-09.sty`
- `src/templates/sosp2026/main.tex`
- `src/templates/sosp2026/references.bib`

These files are passive templates, assets, scripts, upstream license notices, eval fixtures, or agent metadata. They remain available for audit and later storage-binding work, but they do not define the migrated control workflow.

## Notes

The files under `src/` intentionally keep upstream DeepScientist language such as `quest`, `memory.*`, `artifact.*`, and `bash_exec(...)`. Runtime Isomer pages outside `org/` replace those assumptions according to `migrate/migration-plan.md` and `migrate/placeholders.md`.
