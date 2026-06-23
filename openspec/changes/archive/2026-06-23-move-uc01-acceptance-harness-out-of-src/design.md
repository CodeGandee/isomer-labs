## Context

The current working tree contains the completed Milestone 6 UC-01 implementation, including `src/isomer_labs/workflows/uc01*.py` and a public `isomer-cli uc01` command group. That implementation proved the acceptance path, but it made a named use case part of the Isomer package surface.

The intended architecture is narrower. `src/isomer_labs` should hold reusable Isomer system behavior: Project discovery, topic context, runtime records, validation, Domain Agent Team Template handling, handoff state, and Houmao adapter boundaries. A pinned use case such as UC-01 should be executable as a manual or integration harness that drives those generic surfaces. The harness can contain UC-01 ids, deterministic fixture content, route decisions, and assertions because those are acceptance-test facts rather than core platform concepts.

The immediate implementation will revise the uncommitted Milestone 6 work before archive or commit. It should preserve the useful generic pieces and move the case-specific pieces into `tests/manual/uc01_headless_vertical_slice/`.

## Goals / Non-Goals

**Goals:**

- Keep `src/isomer_labs` free of named UC-01 orchestration modules and product command groups.
- Preserve the UC-01 fixture Project and repeatable validation value.
- Make the UC-01 manual harness drive reusable Isomer APIs and generic CLI commands.
- Keep reusable core additions from Milestone 6, including `deepsci-mini`, generic lifecycle record kinds, topic config refs parsing, runtime inspection summaries that are not UC-01-specific, and generic validation helpers.
- Update tests so future named use-case modules under `src/isomer_labs` fail unless an accepted spec explicitly promotes them into the product surface.
- Keep root-level `--print-json` behavior on generic commands and avoid adding command-local `--json` or `--format` flags.

**Non-Goals:**

- Do not remove the UC-01 fixture Project.
- Do not remove generic Workspace Runtime support needed to record Artifacts, Evidence Items, Findings, Gates, Decision Records, View Manifests, or Provenance Records.
- Do not implement a new general workflow engine in this change.
- Do not add a new external dependency or require live Houmao for deterministic validation.
- Do not archive or rewrite Milestone 6 history as part of the implementation; this change corrects the current working tree before finalization.

## Decisions

### Decision: Treat named use cases as acceptance harnesses by default

UC-01-specific code should live under `tests/manual/uc01_headless_vertical_slice/`. That directory may contain `constants.py`, `fixture_outputs.py`, `runner.py`, `assertions.py`, and `__main__.py` or an equivalent small script shape. The harness can import `isomer_labs` core modules, call generic CLI commands through subprocess, or use stable runtime APIs directly when doing so is cleaner.

Alternative considered: keep `src/isomer_labs/workflows/uc01.py` as a package-internal workflow module and hide only the CLI command. That still makes UC-01 a source-level platform behavior and invites UC-07, UC-06, and other use cases to grow as package modules. The boundary should be stronger.

### Decision: Keep reusable runtime primitives in core

Generic record kinds such as `finding` and `view_manifest`, generic lifecycle statuses needed by current contracts, topic config `refs` parsing, and Domain Agent Team Template support for `deepsci-mini` belong in `src/`. They are platform concepts and will be reused by UC-07, UC-04, and later inspection work.

Alternative considered: move every M6 runtime addition into the manual harness. That would make the harness write opaque records or duplicate runtime semantics, which would weaken the platform and lose the value of the M6 vertical slice.

### Decision: Remove `isomer-cli uc01` from the product command surface

The public CLI should expose generic operations such as `validate`, `runtime init`, `runtime prepare`, `team-instances create`, `handoffs dispatch`, `handoffs observe`, `handoffs normalize`, `runtime inspect`, and `runtime validate`. A named use-case runner may exist as a manual script or test entry point, not as a first-class `isomer-cli` group, unless a future accepted spec promotes that command.

Alternative considered: leave `uc01 inspect` because it is read-only. Even read-only named use-case commands encode acceptance-test vocabulary into product help output. The manual harness can print the same deterministic JSON summary.

### Decision: Split generic summaries from UC-01 assertions

Runtime inspection and validation should not have a hardcoded `uc01` section in core output. Core validation may report generic broken refs, unresolved Gates, unsupported claims, missing Artifact files, stale provenance, and cross-topic leakage. The UC-01 harness should read generic runtime output and assert that the expected UC-01 graph is complete.

Alternative considered: keep a generic "workflow summaries" registry in core and register UC-01 there. That is premature; the project does not yet have a general workflow abstraction, and this change exists to avoid inventing one from a single use case.

### Decision: Use architecture tests as the guardrail

Source architecture tests should allow accepted core package boundaries and reject named use-case packages or modules under `src/isomer_labs`. They should also check that manual harness directories can host case-specific code without creating package-import expectations for product code.

Alternative considered: rely on reviewer discipline. The previous implementation shows this boundary is easy to cross during a fast vertical slice, so a test guardrail is worthwhile.

## Risks / Trade-offs

- Manual harness becomes less ergonomic than `isomer-cli uc01 run` -> Provide a clear `pixi run python tests/manual/uc01_headless_vertical_slice` entry point and deterministic JSON output.
- Some useful UC-01 helper code has no obvious generic home -> Keep it in the harness until a second use case proves the abstraction.
- Removing `runtime.uc01` summaries may reduce convenient debugging -> Recreate the summary in the harness from generic runtime records and keep core runtime output provider-neutral.
- Tests may overfit the current directory names -> Guard against named use-case source modules, not against every future package; allow future product specs to update the allowed package list deliberately.
- Live Houmao validation may need cleanup reporting in harness code -> Keep live-gate skip and cleanup summaries in the manual harness output, with core Houmao cleanup APIs remaining generic.

## Migration Plan

1. Move UC-01 constants, deterministic output specs, handoff simulation, summary building, and assertions from `src/isomer_labs/workflows/` into `tests/manual/uc01_headless_vertical_slice/`.
2. Remove `src/isomer_labs/cli/commands/uc01.py` and unregister the command group from the CLI app.
3. Remove core runtime validation imports or output fields that mention UC-01 directly; replace tests with harness-level assertions over generic runtime output.
4. Keep generic core changes and adjust tests to prove they are not UC-01-specific.
5. Update docs and ROADMAP to run UC-01 through the manual harness.
6. Run OpenSpec validation, lint, typecheck, unit tests, research skill validation, and the UC-01 manual harness.

Rollback is straightforward because the prior source-level UC-01 command is uncommitted. If the harness loses coverage, restore behavior in `tests/manual/uc01_headless_vertical_slice/` rather than reintroducing named use-case modules under `src/`.

## Open Questions

- Should the manual harness call Python APIs directly, generic CLI commands only, or a hybrid? The preferred default is a hybrid: CLI for public behavior and Python APIs for concise test-only graph construction where no product command exists yet.
- Should we add a generic runtime query helper for lifecycle records by kind and metadata, or keep that logic inside the harness until UC-07 needs it too?
- Should docs name the harness directory as the stable acceptance entry point, or keep it framed as a developer/manual validation tool until after Milestone 6 is archived?
