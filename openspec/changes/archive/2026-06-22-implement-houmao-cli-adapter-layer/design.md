## Context
Isomer Labs already has provider-neutral Project, Topic Workspace, Workspace Runtime, Topic Agent Team Profile, Agent Team Instance, Agent Profile, and Agent Instance records. The JSON manifest reconciliation change defines the bridge files Isomer needs to correlate those records with Houmao runtime state: `adapter-link.json`, `launch-material-manifest.json`, and `adapter-runtime-manifest.json`. The remaining missing part is the live adapter layer that can prepare Houmao material, invoke Houmao, and record the results.

The local Houmao checkout is CLI-first. Its stable integration surface is `houmao-mgr --print-json`, while the Python package does not currently expose a stable SDK for launching teams from Isomer. Isomer should therefore treat Houmao as an external execution backend and call its public CLI through a bounded subprocess runner. This preserves the repository boundary, avoids adding a runtime `houmao` import dependency to Isomer, and keeps Houmao-specific ids in adapter payloads rather than generic Isomer schemas.

Users need two launch paths. The quick path is an Isomer command that materializes launch material and starts the Houmao-managed Agent Instances. The direct path is a prepare-only Isomer command that writes the same launch material and manifests, after which the user can inspect, edit, or invoke `houmao-mgr` manually. Isomer later reconciles direct Houmao activity through manifests and read-only Houmao inspection.

## Goals / Non-Goals
**Goals:**
- Implement a Houmao Execution Adapter layer backed by `houmao-mgr --print-json` subprocess calls.
- Share one launch-material builder between quick launch and prepare-only/manual workflows.
- Record every adapter mutation and observation through Workspace Runtime records, path plans, adapter payload refs, and JSON manifests.
- Keep launch material, command payloads, logs, and inspection snapshots durable; do not treat them as cache.
- Support quick launch, prepare-only materialization, live inspection, stop, and reconciliation hooks for one Agent Team Instance.
- Preserve the existing Isomer domain language in CLI output and generic runtime records.

**Non-Goals:**
- Do not import Houmao internals or require `import houmao` from the Isomer runtime path.
- Do not implement handoff dispatch, observation ingestion, or Operator Agent normalization in this focused change.
- Do not make Houmao managed-agent ids, tmux sessions, mailboxes, gateways, or profile names generic Agent Team Instance fields.
- Do not write launch material into `.isomer-labs/` or the Houmao source checkout.
- Do not silently repair missing Houmao dependencies, invalid topic readiness, or partial launch state.

## Decisions
### Use the Houmao CLI JSON boundary
The adapter will invoke a configured Houmao command, defaulting to the local checkout through a Pixi-backed command runner when `extern/orphan/houmao` or `~/workspace/code/houmao` is available. Every live operation uses `houmao-mgr --print-json` and records argv, cwd, sanitized environment hints, exit status, parsed JSON summary, diagnostics, timestamps, and payload paths.

Alternative considered: import Houmao modules directly. That would expose Isomer to internal Click command wiring, project overlay behavior, tmux/session setup details, and Python packaging assumptions that Houmao has not presented as a stable SDK. The CLI boundary is slower than direct imports, but it matches Houmao’s supported operator surface and is easier to validate with black-box tests.

### Put a small facade in front of subprocess execution
Implementation should split the adapter into a command runner, command catalog, launch-material builder, runtime recorder, and high-level facade. CLI handlers call the facade; tests can mock the runner without starting Houmao.

Alternative considered: put subprocess calls directly in Click command handlers. That would make partial launch recovery, JSON manifest updates, and future GUI/API reuse harder to test.

### Materialize before mutation
Quick launch and prepare-only use the same materialization path. The adapter resolves path plans, creates durable adapter directories, writes Houmao project/profile/specialist material, records raw material digests in `launch-material-manifest.json`, writes `adapter-link.json`, and only then attempts any Houmao launch command.

Alternative considered: generate files inline during launch. That makes prepare-only inconsistent with quick launch and leaves no stable material for users to inspect before a mutation.

### Launch one Houmao managed agent per Agent Instance
Isomer keeps the Agent Team Instance as the user-facing runtime team. The adapter launches one Houmao managed-agent process per Isomer Agent Instance using generated or selected Houmao profiles. Runtime mappings are recorded per Agent Instance and stored as opaque Houmao adapter refs.

Alternative considered: ask Houmao to launch a whole team as one command. The currently inspected Houmao project command launches one managed-agent instance, so Isomer must orchestrate a team by iterating over Agent Instances.

### Treat command payloads and logs as durable adapter records
Command input payloads, sanitized stdout/stderr summaries, raw JSON outputs when safe, launch logs, inspection snapshots, and stop outcomes are stored under recorded Topic Workspace paths. They are not cache files and validation must report missing files rather than deleting refs.

Alternative considered: keep command output only in process memory or temporary directories. That blocks recovery after process restart and breaks reconciliation between direct Houmao and Isomer quick launch paths.

### Make partial launch recoverable
The launch facade records a launch attempt before starting agents, updates per-Agent Instance command attempts as each Houmao command finishes, and writes a failed or partial outcome if a later launch step fails. Inspect-live and stop operate on the known mappings even when the whole Agent Team Instance did not launch cleanly.

Alternative considered: fail the whole launch transaction and remove intermediate records. That would lose information about already-started Houmao agents and make cleanup unsafe.

### Keep handoff behavior out of this focused change
This change stops at launch materialization, quick launch, inspect-live, stop, and reconciliation hooks. Manual handoff dispatch, Signal Observation ingestion, and Operator Agent normalization stay in `implement-milestone-5-houmao-execution-adapter`.

Alternative considered: include the first manual handoff round now. That would provide a broader demo, but it would pull in Run-level dispatch, observation, and normalization work that the broader Milestone 5 change already owns.

## Risks / Trade-offs
- [Risk] Houmao CLI output or command shape changes. -> Mitigation: centralize the command catalog, require `--print-json`, add availability/capability probes, and keep exact argv tests against mocked runner fixtures.
- [Risk] Partial launch leaves live Houmao agents after Isomer reports failure. -> Mitigation: record each successful per-agent launch immediately, surface stop diagnostics, and never erase partial mappings.
- [Risk] Direct manual edits drift from generated material. -> Mitigation: preserve raw file digests, classify drift during reconciliation, and require explicit adopt or reconcile commands before Workspace Runtime treats external state as accepted.
- [Risk] CLI subprocess integration is slower than Python calls. -> Mitigation: launch/inspect/stop are coarse operations where stability and traceability matter more than call overhead.
- [Risk] Adapter payloads could leak secret-like output. -> Mitigation: reuse manifest redaction rules, reject secret-bearing payloads before durable recording, and store only sanitized summaries in normal JSON output.

## Migration Plan
1. Add adapter modules and runtime/path record helpers without wiring public launch commands to live Houmao.
2. Add prepare-only materialization and validate that existing manifest reconciliation commands can read the generated files.
3. Add quick launch behind explicit `team-instances launch` mutation behavior and mocked runner tests.
4. Add inspect-live and stop commands using the same command runner and runtime recorder.
5. Run repository validation with `pixi run lint`, `pixi run typecheck`, and `pixi run test`; keep live Houmao validation gated or manual because it starts external processes.
6. If rollback is needed, disable the public launch/stop commands while leaving generated manifests and Workspace Runtime adapter refs inspectable.

## Resolved Clarifications
- Command catalog seed: use top-level `houmao-mgr --print-json`, select project overlay with `project --project-dir <dir>`, create material with `project specialist create` and `project profile create`, launch one Agent Instance with `project agents launch --profile <profile> --name <agent>`, inspect with `project agents list` and `project agents get --name <agent>`, stop with `project agents stop --name <agent>`, and use `system-skills list` plus `agents global list --state all` for read-only probes.
- Scope boundary: this focused change excludes handoff dispatch, Signal Observation ingestion, and Operator Agent normalization. Those remain in `implement-milestone-5-houmao-execution-adapter`.

## Open Questions
- None for implementation planning after the 2026-06-22 exploration pass.
