# DeepScientist Template Notes

These templates are vendored from `Orchestra-Research/AI-Research-SKILLs/20-ml-paper-writing` so the `write` skill can use them offline inside local quest workspaces.

Selection defaults:

- general ML / AI paper with no stronger venue constraint: start from `iclr2026/`
- targeting ICLR / ICML / NeurIPS / COLM / AAAI: use the matching venue directory directly
- ACL-style NLP / CL paper: use `acl/`
- systems paper: use `asplos2027/`, `nsdi2027/`, `osdi2026/`, or `sosp2026/` as appropriate

Usage rule:

1. Activate the dedicated `paper/*` branch/worktree.
2. Copy the chosen template directory into the active paper workspace's `paper/latex/`.
3. Keep the template's main `.tex` file as the build root unless there is a concrete reason to rename it.
4. Draft the paper inside that `paper/latex/` tree and keep `paper/` for supporting notes, plans, figures, and bundle metadata.
5. Compile with Tectonic first, for example `tectonic -X compile main.tex`, and record the engine, command, PDF path, and warnings in the compile report.
6. Use TeX Live, `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, or Biber only when Tectonic is unavailable, fails for a template-specific reason, or the venue requires that exact workflow; record the fallback reason.

License:

The upstream source is MIT-licensed. See `UPSTREAM_LICENSE.txt`.
