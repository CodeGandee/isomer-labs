## 1. Scope and Classification

- [x] 1.1 Audit the current Milestone 6 working tree and classify each UC-01-related change as reusable core, fixture material, manual harness material, documentation, or obsolete product command surface.
- [x] 1.2 Confirm reusable core changes that remain in `src/`: `deepsci-mini` template support, generic lifecycle record kind/status additions, topic config `refs` parsing, generic runtime validation, and provider-neutral adapter/runtime helpers.
- [x] 1.3 Confirm case-specific material that must move out of `src/`: UC-01 ids, route constants, deterministic output specs, simulated UC-01 handoff payloads, UC-01 graph summaries, and UC-01 closeout assertions.

## 2. Manual Harness Restructure

- [x] 2.1 Create `tests/manual/uc01_headless_vertical_slice/` as the UC-01 acceptance harness package or script directory.
- [x] 2.2 Move UC-01 constants, deterministic fixture output definitions, simulated handoff result construction, summary building, and assertion logic from `src/isomer_labs/workflows/uc01*.py` into the manual harness.
- [x] 2.3 Preserve a simple manual entry point, such as `pixi run python tests/manual/uc01_headless_vertical_slice`, that copies the UC-01 fixture Project to a temporary directory and prints deterministic JSON.
- [x] 2.4 Ensure the harness drives generic Isomer CLI commands or reusable Python APIs for Project validation, runtime init/prepare, Agent Team Instance creation, handoff dispatch or simulated equivalent, normalization, runtime validation, and inspection.
- [x] 2.5 Keep live Houmao validation gated by `ISOMER_MANUAL_LIVE_HOUMAO=1` and report skipped status without creating runtime or live state when the gate is absent.

## 3. Core Source Cleanup

- [x] 3.1 Remove `src/isomer_labs/cli/commands/uc01.py` and unregister `uc01` from the CLI app.
- [x] 3.2 Remove `src/isomer_labs/workflows/uc01.py`, `uc01_constants.py`, `uc01_handoffs.py`, and `uc01_records.py`, or replace them only with generic helpers whose names and payloads contain no pinned use-case ids.
- [x] 3.3 Remove UC-01-specific imports and output fields from runtime inspection and validation modules.
- [x] 3.4 Keep or extract generic runtime summary/query helpers only if they are provider-neutral and have no UC-01 vocabulary.
- [x] 3.5 Ensure no `src/isomer_labs` module imports from `tests.manual`, fixture Projects, or harness code.

## 4. CLI and Architecture Guardrails

- [x] 4.1 Update command-surface tests so `isomer-cli --help` does not list `uc01`, `uc01 run`, or `uc01 inspect`.
- [x] 4.2 Update source architecture tests to reject named use-case orchestration modules under `src/isomer_labs`.
- [x] 4.3 Keep architecture tests permissive for manual harness modules under `tests/manual/<harness>/`.
- [x] 4.4 Ensure root-level `--print-json` tests continue to pass for generic commands and no command-local `--json`, `--format json`, or `--format=json` options are introduced.

## 5. UC-01 Fixture and Validation Tests

- [x] 5.1 Keep the UC-01 fixture Project under `tests/fixtures/projects/uc01-headless-gb10` and verify it validates before runtime creation.
- [x] 5.2 Update unit tests to prove fixture validation, no runtime-truth leakage, explicit topic readiness binding, and exact `deepsci-mini` role refs without depending on `isomer-cli uc01`.
- [x] 5.3 Add or update tests for the manual harness simulated run, restart-safe runtime inspection through generic outputs, and no UC-07 measurement records.
- [x] 5.4 Add or update live-gated manual validation coverage that records skipped status when `ISOMER_MANUAL_LIVE_HOUMAO` is absent.

## 6. Documentation and Roadmap

- [x] 6.1 Update workflow docs to run UC-01 through `tests/manual/uc01_headless_vertical_slice` rather than `isomer-cli uc01`.
- [x] 6.2 Update CLI docs and side-effect tables to remove `uc01 run` and `uc01 inspect`.
- [x] 6.3 Update Houmao adapter and troubleshooting docs so UC-01 is described as a manual harness over generic adapter/runtime surfaces.
- [x] 6.4 Update ROADMAP Milestone 6 wording to say the acceptance path is a manual harness, not a product CLI command.
- [x] 6.5 Update the M6 OpenSpec artifacts if needed so they do not imply named use-case implementation belongs in `src/`.

## 7. Verification

- [x] 7.1 Run `openspec validate move-uc01-acceptance-harness-out-of-src --strict`.
- [x] 7.2 Run `openspec validate --all`.
- [x] 7.3 Run `pixi run lint`.
- [x] 7.4 Run `pixi run typecheck`.
- [x] 7.5 Run `pixi run test`.
- [x] 7.6 Run `pixi run validate-research-skills`.
- [x] 7.7 Run the UC-01 manual harness in simulated mode and record route classification, Artifact count, Evidence Item count, View Manifest count, diagnostics, and live-gate skipped status.
- [x] 7.8 Run `git diff --check` and confirm no generated `__pycache__`, temporary runtime files, or disposable fixture runtime outputs are tracked.
