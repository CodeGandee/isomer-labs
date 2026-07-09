## Context

The current doctor command is registered as `isomer-cli project doctor`, but its behavior is broader than a Project subcommand. It checks host Pixi, can run without a discovered Project by suppressing the normal missing-Project diagnostic, and then adds Project and Research Topic checks only when those contexts exist. The CLI also has docs, examples, self-query guidance, and system skill assets that teach `project doctor` as the diagnostic entrypoint.

The user wants a breaking cleanup: `doctor` becomes a top-level command, and `project doctor` is removed rather than retained as a compatibility alias. The same change should always check required system dependencies, optionally check Houmao availability, always attempt Project discovery, and scan Topic Workspaces by default when a Project exists.

## Goals / Non-Goals

**Goals:**

- Make `isomer-cli doctor` the only doctor command.
- Remove `doctor` registration from the `project` command group.
- Keep doctor read-only and preserve existing Project diagnostics when a Project exists.
- Always run system-level dependency checks for required Pixi and optional `houmao-mgr`.
- Always perform Project discovery and report its result.
- Scan all manifest-registered active Research Topics by default when a Project exists.
- Add repeatable `--with-topic <research-topic-id>` filters that narrow topic checks to the requested Research Topics.
- Replace user-facing guidance, docs, examples, self-query usage strings, and tests that reference `isomer-cli project doctor`.

**Non-Goals:**

- Do not add a compatibility alias for `isomer-cli project doctor`.
- Do not add a mutating repair or prepare mode.
- Do not change Project discovery semantics for other Project-scoped commands.
- Do not make the doctor command bootstrap Houmao or Pixi state.

## Decisions

### Register Doctor on the Root Click Group

Register `register_doctor_commands(app)` instead of `register_doctor_commands(project_group)`. The command should keep root-level Project selector options and add repeatable `--with-topic <research-topic-id>` filters. The handler should always run host diagnostics first, then attempt Project discovery, then run Project and Topic Workspace checks only when a Project is available.

Alternative considered: keep both root and Project registrations temporarily. This conflicts with the requested breaking cleanup and would keep stale command guidance alive.

### Reuse Existing Doctor Handler and Output Shape

Keep the JSON wrapper and core doctor payload fields stable: `ok`, `mode`, `mutated`, `checks`, and `diagnostics` remain the contract. Replace the singular `topic` payload with `topics`, always an array, because the command now checks zero, one, or many Research Topics. Existing tests and agents must migrate by changing both the command path and any singular `topic` parser logic.

Alternative considered: create a separate root-level handler. That would duplicate Project/topic diagnostic branching and increase the chance of inconsistent output.

Alternative considered: keep `topic` for one checked topic and use `topics` only for multiple checked topics. That conditional shape makes machine parsing harder and conflicts with the all-topic default.

### Treat Houmao as an Optional Host Check

Add Houmao checks beside Pixi under the host scope: `host.houmao.executable` and, when executable resolution succeeds, `host.houmao.version`. Pixi remains required. Houmao is optional at this layer, so missing `houmao-mgr` should produce a warning or skipped optional check rather than making system-level dependency readiness fail. The check should use the same subprocess discipline as Pixi checks: bounded execution, stable diagnostics, no shell expansion, and no mutation.

Alternative considered: require Houmao whenever `doctor` runs. That is too strict for read-only Project inspection and environments where Houmao-backed launch is not being exercised yet.

The doctor report's `ok` value should be false only when a required check fails or an error diagnostic is present. Missing optional `houmao-mgr` should remain visible as a warning but should not make `ok` false.

### Always Report Project Discovery

After host checks, `doctor` should always attempt Project discovery. If a Project is found, it reports normal Project checks. If no Project is found and no explicit Project selector was supplied, it reports a deterministic no-Project check and continues without topic checks. If an explicit Project selector is invalid, it reports a failing Project discovery diagnostic.

Alternative considered: keep the current dependency-only mode that suppresses missing Project discovery. That hides useful context from a top-level command whose job is to tell the user what the local environment can see.

### Default Topic Scan Covers All Detected Topics

When a Project exists and the user does not provide `--with-topic`, `doctor` should detect manifest-registered active Research Topics and run topic readiness checks for each topic's registered or default Topic Workspace. It should not scan unregistered filesystem directories under the Topic Workspace base directory as managed topics. The output should group or identify topic checks by Research Topic so users can see the whole Project health surface without knowing a default topic first.

When the user provides one or more `--with-topic <research-topic-id>` values, `doctor` should check only those Research Topics. Multiple filters are inclusive. Once at least one filter is present, the command must not also scan all topics. The filter matches only the canonical Research Topic id, not Topic Workspace id or future display title fields. Unknown or duplicate filters should produce deterministic diagnostics and must not crash.

JSON output should include `topics: []` for topic results in every mode. Per-topic payload entries should identify the Research Topic id and Topic Workspace id when known. The top-level `checks` list can remain flat, but topic checks must include the Research Topic id in `details` so callers can group checks without parsing summary text.

Alternative considered: keep the current selected/default topic behavior. That is less useful for doctor because it checks a narrow active context while the command is meant to scan health broadly.

Alternative considered: scan filesystem directories under the Topic Workspace base directory in addition to manifest registrations. That can catch stale workspaces, but it muddies Project Manifest ownership and should be handled later by an explicit audit mode if needed.

### Remove Stale Guidance in One Pass

Implementation should search all user-facing and agent-facing text for `project doctor` and replace it with `doctor` where it refers to the Isomer CLI command. This includes docs, examples, system skills, self-query usage strings, specs, and tests. References in archived OpenSpec changes do not affect runtime behavior, but current docs and packaged assets must be updated.

Alternative considered: update only runtime code and tests. That would leave agents and users calling a removed command.

## Risks / Trade-offs

- Breaking scripts that call `isomer-cli project doctor` -> The command will now fail clearly as an unknown Project subcommand, and docs/tests will point users to `isomer-cli doctor`.
- Active CLI help changes overlap this command surface -> Keep this change scoped to the canonical root `doctor` command and update the same top-level help expectations when implementation runs.
- Houmao version behavior may vary by installed Houmao build -> Treat an executable that exists but cannot report a version as a deterministic warning diagnostic, not as an uncaught exception.
- Root-level Project selectors may be less obvious than `project --root ... doctor` -> The root doctor command should expose the same read-only common Project selector options that the current doctor command accepts.
- Large Projects may have many Topic Workspaces -> Provide `--with-topic` filters and keep per-topic diagnostics bounded, deterministic, and grouped by topic.
- Optional Houmao warnings may be missed by automation that checks only `ok` -> Keep the warning in `checks` and diagnostics text, and reserve `ok=false` for required-readiness failures.

## Migration Plan

1. Move doctor registration to the root command group and remove it from `project`.
2. Add required Pixi and optional Houmao host inspection to doctor diagnostics.
3. Add always-on Project discovery reporting.
4. Change topic diagnostics from selected/default-topic behavior to all manifest-registered active Research Topics by default, with repeatable `--with-topic <research-topic-id>` filters for inclusive narrowing.
5. Replace singular doctor JSON `topic` output with stable `topics: []` output.
6. Update tests from `["project", "doctor", ...]` to `["doctor", ...]`, and add an assertion that `["project", "doctor"]` exits as an invocation error.
7. Update docs, CLI examples, self-query usage strings, system skill assets, and validation fixtures to use `isomer-cli doctor`.
8. Validate with OpenSpec, unit tests covering CLI behavior, lint, and typecheck.

Rollback is a code revert. There is no data migration because this change only moves a read-only command surface and adds diagnostics.

## Open Questions

None. The user explicitly chose the breaking design with no compatibility layer.
