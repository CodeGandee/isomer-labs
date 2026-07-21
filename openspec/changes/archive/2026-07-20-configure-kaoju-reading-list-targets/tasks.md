## 1. Reading List Contract

- [x] 1.1 Extend Reading List validation to resolve and validate default, user-total, and user-category targets while preserving legacy 3+3 payloads.
- [x] 1.2 Validate persisted achieved counts and calculate non-blocking shortage diagnostics against the effective category targets.

## 2. Kaoju Skill and Design Guidance

- [x] 2.1 Update the Kaoju discover skill and `build-reading-list` command with target derivation, clarification, persistence, and reporting rules.
- [x] 2.2 Update Reading List semantics, the accepted ADR, and the survey use case to describe configurable targets and backward compatibility.

## 3. Verification

- [x] 3.1 Add unit coverage for default compatibility, odd and even totals, category overrides, zero-category targets, invalid metadata, achieved-count mismatches, and target-relative shortages.
- [x] 3.2 Update integration fixtures and assertions to cover persisted configurable targets without weakening direction scope, version-family, blocker, or approval checks.
- [x] 3.3 Run OpenSpec validation, targeted Kaoju tests, lint, type checking, and the repository unit test suite; resolve change-related failures.
