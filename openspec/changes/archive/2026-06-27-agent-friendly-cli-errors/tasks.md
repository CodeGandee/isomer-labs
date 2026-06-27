## 1. Diagnostic and Output Model

- [x] 1.1 Extend `Diagnostic` with optional structured remediation fields for `hint`, `usage`, and `examples` while preserving existing constructor behavior.
- [x] 1.2 Update JSON rendering so diagnostics include remediation fields only when present.
- [x] 1.3 Update text diagnostic rendering so hint, usage, and examples render after the primary diagnostic line in stable order.
- [x] 1.4 Add a shared CLI failure rendering helper that can emit `ok: false`, diagnostics, mutation information, and optional debug details through the existing text or JSON output paths.

## 2. Entrypoint Failure Normalization

- [x] 2.1 Add raw-argv detection for root-level `--print-json`, root-level debug mode, and `ISOMER_CLI_DEBUG=1` before Click dispatch completes.
- [x] 2.2 Convert Click usage and parse exceptions from `isomer_labs.cli.main` into invocation diagnostics with non-zero exit status and `mutated: false`.
- [x] 2.3 Convert non-usage `click.ClickException` failures into Isomer diagnostics without calling `exc.show()` directly.
- [x] 2.4 Catch `KeyboardInterrupt` at the installed entrypoint and return an interruption diagnostic without a traceback.
- [x] 2.5 Catch unexpected Python exceptions at the installed entrypoint and return an internal-error diagnostic with `mutation_state: "unknown"` when mutation certainty cannot be proven.
- [x] 2.6 Include traceback details only when explicit debug mode is enabled, with JSON debug details isolated from the primary diagnostic message.

## 3. Invocation Examples

- [x] 3.1 Add a command example registry keyed by public command path, seeded from the canonical examples in `docs/isomer-cli.md`.
- [x] 3.2 Implement nearest-command selection for malformed invocations using Click context when available and raw argv fallback when context is incomplete.
- [x] 3.3 Limit wrong-format diagnostics to one to three examples and prefer command-specific examples over group-level fallbacks.
- [x] 3.4 Add registry coverage for high-value public commands, including `project paths get`, `project paths register`, `project paths materialize-default`, `project topics create`, `project validate`, and `project doctor`.

## 4. Tests

- [x] 4.1 Add `cli.main(...)` tests for missing argument, unknown subcommand, invalid option, and text-mode invocation diagnostics.
- [x] 4.2 Add `cli.main(...)` tests proving malformed invocations with `--print-json` emit valid `isomer-cli-output.v1` JSON.
- [x] 4.3 Add tests that wrong-format diagnostics include expected usage and one to three relevant examples.
- [x] 4.4 Add tests for unexpected exception normalization without traceback by default.
- [x] 4.5 Add tests for debug-mode traceback visibility in text and JSON modes.
- [x] 4.6 Add tests proving existing domain diagnostics without remediation fields remain text and JSON compatible.
- [x] 4.7 Add tests for mutation reporting: pre-dispatch failures report `mutated: false`, and unexpected post-dispatch failures report unknown mutation state when needed.

## 5. Documentation and Validation

- [x] 5.1 Update `docs/isomer-cli.md` to describe normalized failure output, remediation examples, traceback suppression, debug mode, and mutation certainty.
- [x] 5.2 Document that root-level `--print-json` is the deterministic JSON path for both success and failure output.
- [x] 5.3 Add or update validation that keeps high-value registered CLI examples aligned with documented public examples.

## 6. Verification

- [x] 6.1 Run `openspec validate agent-friendly-cli-errors --strict` and fix proposal or spec issues.
- [x] 6.2 Run `pixi run docs-validate` and fix documentation validation issues.
- [x] 6.3 Run `pixi run lint` and fix style issues.
- [x] 6.4 Run `pixi run typecheck` and fix type errors.
- [x] 6.5 Run `pixi run test` and fix regressions.
- [x] 6.6 Confirm `openspec status --change agent-friendly-cli-errors --json` reports the change apply-ready.
