## 1. Correct Packaged Guidance and Enforcement

- [x] 1.1 Replace all four stale system-skill manager `--json` examples with the global `isomer-cli --print-json` form.
- [x] 1.2 Extend packaged system-skill CLI validation to reject exact command-local `--json` tokens without rejecting valid JSON-bearing options.

## 2. Regression Coverage and Verification

- [x] 2.1 Add focused unit tests that reject command-local `--json` and accept global `--print-json` plus JSON-bearing options.
- [x] 2.2 Confirm `list` and `remember` option placement through CLI help, scan the packaged bundle for stale forms, and run focused and repository validation.
