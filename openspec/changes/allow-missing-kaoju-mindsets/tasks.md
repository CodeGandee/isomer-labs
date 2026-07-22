## 1. Run Mindset Resolution

- [x] 1.1 Add typed `recorded` and `skipped_source_missing` Run mindset resolution validation, verified Source absence, verified Run-scoped Record identity, immutable idempotent persistence, and recorded-mode input-ref updates to `KaojuRunService`.
- [x] 1.2 Add `project runs resolve-mindset` with mutually exclusive `--record-ref` and `--source-missing` modes and ensure Run status, checkpoints, and completion preserve and report the stored posture.
- [x] 1.3 Replace the checked process `ensure_mode` with resolution mode `record-or-skip-missing-per-run` and update contract validation without adding Source bodies or packaged runtime fallback.

## 2. Kaoju Workflow Guidance

- [x] 2.1 Update the public Kaoju entrypoint, README, and shared mindset contract to stop concrete-action lazy creation, persist either recorded or skipped Run resolution, propagate that resolution, and report explicit `create-topic` recovery.
- [x] 2.2 Update reading-item, source-code, and examine guidance so verified missing Source posture skips Record creation, question answering, collector checks, revision, and terminal Record output while preserving normal reading Artifacts.
- [x] 2.3 Keep invalid, unreadable, mismatched, ambiguous, or unsafe existing Sources blocking and keep explicit Kaoju topic creation and requested create-missing generation available.

## 3. Verification

- [x] 3.1 Add focused service and CLI tests for recorded resolution, missing resolution, actual-path verification, invalid mode combinations, immutable idempotency, input refs, and checkpoint or terminal preservation.
- [x] 3.2 Update contract and packaged-skill asset tests for optional missing-Source routing and conditional closeout guidance.
- [x] 3.3 Run focused Kaoju tests, package asset validation, `pixi run lint`, `pixi run typecheck`, `pixi run test`, and strict OpenSpec validation.
