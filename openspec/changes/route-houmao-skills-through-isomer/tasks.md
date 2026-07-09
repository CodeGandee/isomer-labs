## 1. Project Integration State

- [x] 1.1 Add typed parsing for `operator.integrations.houmao` Project Manifest state, including `enabled`, `disabled`, and missing/not-configured handling.
- [x] 1.2 Add Project Manifest write helpers for enabling, disabling, and preserving configured Houmao `skill_root` and `project_dir` values.
- [x] 1.3 Add diagnostics for invalid Houmao integration status values, unsafe paths, and configuration that points outside the Project Config Directory.

## 2. Houmao Skill Projection

- [x] 2.1 Add an Isomer-managed projection root helper for `<project-root>/.isomer-labs/houmao-skills`.
- [x] 2.2 Implement idempotent projection of selected Houmao-owned skill material into `.isomer-labs/houmao-skills/` with ownership metadata.
- [x] 2.3 Refuse unmanaged projection collisions and report deterministic diagnostics without overwriting user files.
- [x] 2.4 Write or update a small projection manifest that maps stable lifecycle-specific Isomer route names to projected Houmao skill directories.
- [x] 2.5 Add projection manifest entries for `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master`.

## 3. CLI Routing Surface

- [x] 3.1 Add `isomer-cli project integrations houmao status` with JSON output for integration status, configured paths, skip state, and diagnostics.
- [x] 3.2 Add `isomer-cli project integrations houmao enable` and `disable` commands that update Project Manifest policy idempotently.
- [x] 3.3 Add `isomer-cli project integrations houmao prepare-skills` to prepare the projection root for an enabled Project and skip cleanly when disabled.
- [x] 3.4 Add `isomer-cli project integrations houmao skill-context <skill-name>` that resolves absolute `houmao_skill_path`, `houmao_project_path`, `houmao_overlay_path`, and optional Topic Workspace context.
- [x] 3.5 Ensure `skill-context` rejects unknown skill routes and never fabricates paths from untrusted names.
- [x] 3.6 Ensure each Topic Service Master lifecycle subcommand requests the matching lifecycle-specific skill route.

## 4. Skill Guidance Updates

- [x] 4.1 Update `isomer-srv-houmao-interop` to request Houmao skill context through `isomer-cli` before routing to Houmao-owned procedures.
- [x] 4.2 Update `isomer-srv-topic-service-agent-support` to add explicit `prepare-topic-service-master`, `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master` lifecycle subcommands.
- [x] 4.3 Add one reference page per Topic Service Master lifecycle subcommand, with each page resolving Isomer context, checking Houmao integration policy, and requesting Houmao skill context through `isomer-cli`.
- [x] 4.4 Update `isomer-op-topic-creator` setup/finalize guidance to record skipped Houmao-backed Topic Service Master work when Project integration is disabled and to route enabled setup only to preparation.
- [x] 4.5 Keep `isomer-srv-houmao-interop` and `isomer-srv-topic-service-agent-support` in the core packaged system-skill group, and ensure they are inert when Project Houmao integration is disabled or not configured.
- [x] 4.6 Update relevant help and reference pages so user-facing text remains Isomer-first and describes Houmao as an internal integration provider.

## 5. Tests and Validation

- [x] 5.1 Add unit tests for Project Manifest parsing and writing of Houmao integration policy.
- [x] 5.2 Add unit tests for projection root safety, ownership metadata, update idempotence, and unmanaged collision refusal.
- [x] 5.3 Add CLI tests for `status`, `enable`, `disable`, `prepare-skills`, and `skill-context` JSON payloads.
- [x] 5.4 Add skill asset validation tests that check routing text includes returned skill paths and explicit `--project-dir` guidance.
- [x] 5.5 Add Topic Creator skill tests for disabled Houmao integration skip reporting.
- [x] 5.6 Run `pixi run lint`, `pixi run typecheck`, and `pixi run test`.
