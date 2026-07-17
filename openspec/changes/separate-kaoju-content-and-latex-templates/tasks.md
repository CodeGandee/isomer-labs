## 1. Contracts and Terminology

- [x] 1.1 Add `KAOJU:PAPER-TEMPLATE-LATEX` to the binding and semantic registries with mutable named directory behavior.
- [x] 1.2 Update template audit, export, TeX snapshot, TeX draft, paper contract, and publication lineage contracts for distinct content and LaTeX roles.
- [x] 1.3 Update structured record profiles and contract validation tests for template-kind and LaTeX composition metadata.

## 2. Named Template State

- [x] 2.1 Introduce checked content and LaTeX template-kind descriptors and parameterize stable identity, metadata, audits, dependency checks, and exchange paths.
- [x] 2.2 Generalize named-template list, show, create, copy, update, file, metadata, archive, and delete operations across both kinds.
- [x] 2.3 Generalize export, observation, drift inspection, and reserved metadata across kind-specific working-copy directories.
- [x] 2.4 Add LaTeX authored-metadata and composition-contract validation for preamble, marker, and include modes.

## 3. CLI and Migration

- [x] 3.1 Add `--kind content|latex` to every named-template CLI operation while preserving the unqualified content compatibility default.
- [x] 3.2 Add deterministic template-contract migration preview and apply behavior, including explicit TeX or legacy-template adoption.
- [x] 3.3 Update CLI help, JSON results, diagnostics, examples, and manual reference to use content-template and LaTeX-template terminology.

## 4. TeX Composition and Build

- [x] 4.1 Refactor `init-tex` to resolve explicit or default named LaTeX stock and snapshot its exact multi-file tree.
- [x] 4.2 Implement preamble, marker, and include composition into a self-contained `KAOJU:PAPER-DRAFT-TEX` tree with separate content and presentation lineage.
- [x] 4.3 Make presentation fingerprints independent of content-template digests and record canonical MyST draft checksums separately.
- [x] 4.4 Make `build-pdf` verify the pinned template snapshot, use the manifest entrypoint, and reject mismatched refs before execution.
- [x] 4.5 Add stocked-template and paper-repair drift reporting without silent propagation.

## 5. Kaoju Skills and Process Resources

- [x] 5.1 Update the public template-management procedure to resolve content versus LaTeX role before source discovery or mutation.
- [x] 5.2 Update content-template creation, paper drafting, TeX composition, PDF building, write guidance, and shared semantics for both template roles.
- [x] 5.3 Update the checked survey-process resource, artifact bindings, README, and skill-validation assertions.

## 6. Test Coverage

- [x] 6.1 Extend named-template unit tests for independent content and LaTeX `main` records, kind-safe exports, concurrency, metadata, and reference safety.
- [x] 6.2 Extend paper integration tests to prove multi-file LaTeX stock is composed and required template-owned files reach the build tree.
- [x] 6.3 Add tests for missing defaults, explicit names, non-main entrypoints, template mismatches, drift, and historical-record preservation.
- [x] 6.4 Add migration tests for existing content records, explicit TeX adoption, ambiguous candidates, and compatibility export paths.

## 7. Current Topic Workspace Migration

- [x] 7.1 Enumerate all registered Topic Workspaces and preview their template-contract migration state.
- [x] 7.2 Apply content-template contract upgrades to every current Topic Workspace without changing stable refs or tree bytes.
- [x] 7.3 Adopt the approved IEEE Transactions tree as `predmem-survey` LaTeX `main` and adopt or report every other workspace presentation state.
- [x] 7.4 Validate migrated Workspace Runtime records, managed trees, exports, query indexes, and current paper template lineage.

## 8. Verification

- [x] 8.1 Run focused contract, named-template, paper-build, skill-asset, path-resolution, and migration tests.
- [x] 8.2 Run Ruff, MyPy, the full unit suite, Project validation, and strict OpenSpec validation.
- [x] 8.3 Audit every proposal and delta-spec requirement against current code, records, commands, and test evidence.
