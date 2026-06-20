## Context

`isomer-cli` is Click-backed and already exposes Project discovery, validation, Effective Topic Context, Workspace Path Resolution preview, and design-time template/profile commands. Recent Milestone 4 exploration accepted Pixi as a required Project dependency, kept the Project-level Pixi manifest as the Pixi environment authority, moved explicit Research Topic to Pixi environment bindings into Project Manifest, allowed one Research Topic to use multiple Project-root Pixi environments, represented standalone Pixi isolation with a separate manifest binding table, and kept `doctor` read-only. The new command must therefore inspect host, Project, and topic readiness without becoming the mutating environment-preparation surface.

## Goals / Non-Goals

**Goals:**

- Add a top-level `doctor` command that uses the existing common Click options and can run with `--json`.
- Report host-level Pixi availability even when no Isomer Project is discoverable.
- Report Project-level Pixi readiness when a Project is discoverable or selected.
- Report topic-level Project Manifest environment bindings and Pixi environment readiness when a topic is selected or defaults can select one.
- Keep all checks read-only and deterministic enough for unit tests and CI.
- Reuse Isomer diagnostics, output schema versioning, Project discovery, Research Topic Config loading, and Effective Topic Context where those surfaces already exist.

**Non-Goals:**

- Do not install, repair, or remove Pixi environments.
- Do not create Workspace Runtime state, `state.sqlite`, Topic Workspace subdirectories, Agent Workspaces, Run directories, or readiness records.
- Do not launch Houmao, inspect live Houmao agents, create mailboxes, create gateways, or write adapter launch material.
- Do not add a Service Request flow or the future mutating preparation command.
- Do not make Topic Workspaces into Pixi workspaces by default.

## Decisions

### `doctor` Runs in Three Read-only Phases

`doctor` should build a check report from host, Project, and optional topic phases. The host phase always runs and checks the `pixi` executable and version. The Project phase runs when Project discovery succeeds or selectors are provided and checks Project Manifest validity, Pixi manifest presence, optional `requires-pixi`, and `pixi.lock` presence. The topic phase runs when Effective Topic Context can be resolved and checks the selected Research Topic's explicit Project Manifest environment binding against the Project-level Pixi environments.

Alternatives considered: make `doctor` strictly Project-scoped, or make it topic-scoped only. Dependency-only host checks are useful when setup is broken before Project discovery, while topic checks are needed before runtime preparation. A phased report keeps both without inventing hidden state.

### Project Manifest Gets Explicit Topic Environment Bindings

Project Manifest should record which Project-root Pixi environment or environments each Research Topic uses through repeated `[[topic_pixi_environment_bindings]]` tables. Each Project-root binding should include `research_topic_id`, `pixi_environment`, optional `purpose`, and optional `status`; multiple active rows for one Research Topic are allowed when the topic uses multiple Pixi environments. Standalone Pixi isolation should use a separate repeated `[[topic_standalone_pixi_bindings]]` table with `research_topic_id`, Project-root-relative `manifest_path`, optional `pixi_environment`, optional `purpose`, and optional `status`. `doctor` must validate those explicit bindings against the Project-level Pixi manifest or standalone manifest file and must not infer topic-to-environment relationships from Research Topic ids or environment names. Specialized names such as `<topic-slug>-<env-purpose>` are allowed as human convention, but the Project Manifest binding is the source of truth.

Alternatives considered: store the mapping in Research Topic Config, infer names from Research Topic ids, add a separate environments file, or store it only in Workspace Runtime. Project Manifest is already the discovery authority for Research Topics and their Project-level refs, while Workspace Runtime does not exist before preparation.

### Pixi Inspection Uses CLI Probes Plus Local TOML Reads

Implementation should use `shutil.which("pixi")` and a bounded subprocess call such as `pixi --version` for host availability. Project-level details can be obtained from local TOML parsing for `pyproject.toml` or `pixi.toml`; optional richer checks can call `pixi info --json --manifest-path <manifest-or-project-root>` when Pixi exists. `requires-pixi` compatibility should be checked with `pixi workspace requires-pixi verify --manifest-path <manifest-or-project-root>` when the manifest declares a requirement, and reported as skipped when Pixi is missing.

Alternatives considered: depend on Pixi internals as a Python library, or parse every Pixi lockfile detail ourselves. CLI probes match Pixi's public contract and avoid a new Python dependency.

### Deterministic Report Shape

The JSON payload should include `mode`, `ok`, `mutated`, `checks`, optional `pixi`, optional `project`, optional `topic`, and diagnostics under the existing `isomer-cli-output.v1` wrapper. Each check should have a stable id, scope, status (`pass`, `warn`, `fail`, or `skip`), concept, summary, and optional source path/detail. `ok` is false when any error-severity diagnostic or `fail` check exists. Text output should group checks by scope and use the same summaries without printing secrets.

Alternatives considered: return only diagnostics, or return raw `pixi info` JSON. A stable Isomer check shape is easier to test and safer for future Operator Agent consumption.

### Read-only Behavior is Testable

`doctor` should avoid all filesystem writes and should not call commands that install or update environments. Unit tests should assert that `state.sqlite`, `artifacts/`, `.pixi/` inside fixture Topic Workspaces, Agent Workspace directories, Run directories, and Project Manifest/Research Topic Config files remain unchanged after `doctor`.

Alternatives considered: add `doctor --fix`. ADR 0024 rejected this because diagnostics and mutation need separate provenance.

## Risks / Trade-offs

- Pixi CLI JSON or command behavior may vary by Pixi version → Keep the first implementation tolerant: use `pixi --version`, local TOML parsing, and narrow optional probes before relying on rich `pixi info` fields.
- Dependency-only mode could hide Project errors if users run from the wrong directory → Text and JSON output should name the mode and report skipped Project checks clearly.
- Environment names can look topic-specific without being authoritative → `doctor` should report only explicit Project Manifest bindings and should not infer topic relationships from names.
- Standalone topic Pixi isolation can blur Isomer Topic Workspace and Pixi workspace language → User-facing labels should say "standalone Pixi isolation" or "standalone Pixi manifest", not "Topic Workspace is a Pixi workspace" unless the opt-in is explicit in `topic_standalone_pixi_bindings`.
- `doctor` may become too broad over time → Keep this change limited to read-only preflight; runtime preparation, Service Requests, Houmao launch, and live inspection should remain separate commands or later changes.

## Migration Plan

1. Add the `doctor` command without changing existing command behavior.
2. Add optional parsing and validation for Project Manifest topic environment bindings.
3. Add unit tests for dependency-only, Project-scoped, topic-scoped, missing Pixi, missing environment binding, missing bound Pixi environment, JSON shape, and side-effect-free behavior.
4. Update docs to show `pixi run isomer-cli doctor --json`.
5. Rollback is removal of the new command and optional config parsing; no durable runtime migration is needed because this change is read-only.

## Open Questions

- Whether the future mutating command should be named `workspaces prepare`, `runtime prepare`, or `topics prepare`.
- Whether `doctor` should eventually expose a `--check <id>` filter after the first implementation stabilizes.
