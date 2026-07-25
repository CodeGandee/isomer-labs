## 1. Vendor the IEEE Default Tree

- [x] 1.1 Cross-check `tmp/kaoju-ieee-real-template/` against the Predictive Memory Survey canonical `latex/main` state and record the five selected member checksums before copying.
- [x] 1.2 Replace packaged `latex/main/main.tex` with the prepared `template.tex`, `IEEEtran.cls`, `bare_jrnl_new_sample4.tex`, `fig1.png`, and `metadata.json`, preserving upstream-controlled class, sample, asset bytes, and notices.
- [x] 1.3 Normalize installed-package provenance and LPPL 1.3 metadata, set `template.tex` and `% ISOMER_BODY` as the composition contract, bump the packaged resource identity to `0.6.0`, and record the recomputed tree digest in `manifest.json`.

## 2. Align Kaoju Guidance and Verification

- [x] 2.1 Update packaged Kaoju skill guidance and references that describe `latex/main` as a neutral article so they identify the IEEE Transactions two-column fallback and retain topic-stock precedence.
- [x] 2.2 Extend packaged-template unit tests to verify the exact IEEE entrypoint contract, venue and license metadata, required five-file inventory, local `IEEEtran.cls`, resource version, and deterministic digest.
- [x] 2.3 Extend initialization, default export, and paper-local TeX tests to verify complete-tree copying, local IEEE class retention, packaged-fallback selection, topic-owned `main` precedence, and preservation of existing snapshots and exports.
- [x] 2.4 Build and inspect an installable package to prove `template.tex`, `IEEEtran.cls`, `bare_jrnl_new_sample4.tex`, `fig1.png`, and `metadata.json` ship as package resources.
- [x] 2.5 Run an offline composition-contract check and, when Tectonic is locally available, a compiler-backed smoke build that confirms the composed entrypoint uses the vendored IEEE class and produces the IEEE journal layout.

## 3. Validate the Change

- [x] 3.1 Run the targeted Kaoju packaged-template, named-template, initialization, and paper-production unit tests.
- [x] 3.2 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
- [x] 3.3 Run OpenSpec validation for `use-ieee-two-column-kaoju-default` and resolve every proposal, design, spec, or task diagnostic.
