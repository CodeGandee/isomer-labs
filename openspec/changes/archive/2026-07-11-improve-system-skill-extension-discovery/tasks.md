## 1. Package Discovery Metadata

- [x] 1.1 Add entry-skill and ordered command metadata for the DeepSci and Kaoju extension groups.
- [x] 1.2 Extend manifest parsing and extension models with validation for extension-only discovery metadata.
- [x] 1.3 Add package-asset tests for valid discovery metadata and deterministic invalid metadata diagnostics.

## 2. CLI Discovery Surface

- [x] 2.1 Add `system-skills extensions list` with deterministic human and JSON summaries.
- [x] 2.2 Add `system-skills extensions show <extension-id>` with entry, command, skill, install, status, and invocation guidance.
- [x] 2.3 Make shared `--extension` options advertise catalog extension ids and clarify the `ext` namespace help.
- [x] 2.4 Add CLI tests for discovery output, selector help, unknown extension handling, and the absence of a Kaoju runtime group.

## 3. Documentation and Validation

- [x] 3.1 Update packaged-system-skill and CLI documentation with extension discovery examples and namespace guidance.
- [x] 3.2 Run targeted tests, OpenSpec validation, lint, type checking, and the unit test suite; repair regressions within scope.
