## 1. Version and Compatibility Metadata

- [x] 1.1 Add a direct PEP 440 version dependency and extend packaged system-skill catalog models with group compatibility floors and per-skill overrides.
- [x] 1.2 Add the current Isomer release version to every packaged skill `agents/openai.yaml` and extend skill validators to require valid release-aligned metadata.

## 2. Installer Receipts and Status

- [x] 2.1 Add per-skill versions to installation receipt records, write the new receipt schema, and preserve read support for legacy unversioned receipts.
- [x] 2.2 Classify projected skill version state and compatibility in system-skill status output, including receipt drift, obsolete, compatible-older, current, and newer-than-CLI states.

## 3. Project Extension Detection

- [x] 3.1 Implement read-only per-target extension detection with complete-family aggregation, Project declaration context, and bounded advice.
- [x] 3.2 Add `project system-extensions detect` CLI options, JSON output, and text rendering without mutation.
- [x] 3.3 Add Project-local extension observations to successful Project initialization output without writing declarations.

## 4. Operator Routing and Documentation

- [x] 4.1 Update `isomer-op-entrypoint` to check declared and target-specific compatibility state before automatic optional-extension routing.
- [x] 4.2 Document skill version metadata, compatibility floors, advisory detection, Project initialization behavior, and repair commands.

## 5. Verification

- [x] 5.1 Add focused tests for candidate versions, validator failures, receipt migration and drift, compatibility states, per-target detection, non-mutation, and Project initialization advice.
- [x] 5.2 Run OpenSpec validation, skill validation, lint, type checking, and unit tests; repair regressions within scope.
