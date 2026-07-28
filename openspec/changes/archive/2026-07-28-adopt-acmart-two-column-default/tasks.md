## 1. Package the ACM Default

- [x] 1.1 Replace packaged IEEE LaTeX `main` with the pinned ACM source tree, neutral marker entrypoint, authored metadata, resource version, and deterministic manifest digest.
- [x] 1.2 Update packaged-template loading and venue validation for the ACM required-member and `acm-sigconf` contracts.
- [x] 1.3 Extend typed template update so a venue transition validates and commits replacement authored metadata with the replacement tree.

## 2. Align Guidance and Specifications

- [x] 2.1 Update Kaoju write guidance and package documentation to describe the neutral ACM two-column fallback.
- [x] 2.2 Update the main `kaoju-paper-production` specification to match the accepted delta requirement.

## 3. Update and Run Product Tests

- [x] 3.1 Update packaged-default, installer, named-template, export, initialization, snapshot, and venue-validation tests for ACM.
- [x] 3.2 Run targeted template and paper tests and repair any regressions.
- [x] 3.3 Run repository lint, typecheck, unit tests, and OpenSpec validation.

## 4. Roll Out to pwinfer-analysis

- [x] 4.1 Re-read and atomically replace the topic-owned LaTeX `main`, then refresh and verify its clean exchange copy.
- [x] 4.2 Reinitialize and fill a new ACM TeX draft from the accepted canonical MyST and citation map without changing paper meaning.
- [x] 4.3 Build a new PDF, inspect every page, verify table and reference coverage, and retain publication as pending.
- [x] 4.4 Verify historical IEEE artifacts still resolve and record the new template and paper refs.
