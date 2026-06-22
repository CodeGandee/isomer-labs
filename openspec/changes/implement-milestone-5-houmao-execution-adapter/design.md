## Context

Milestone 4 gives Isomer a topic-scoped Workspace Runtime, readiness records, Agent Team Instance records, Agent Instance records, Agent Workspace records, path plans, validation, and deterministic CLI inspection. The next roadmap step is the first live adapter slice: start one manual-mode `deepsci-org` Agent Team Instance through the local Houmao checkout, inspect it, stop it, dispatch one handoff, observe a result through Houmao mail or gateway surfaces, and normalize the result back into Workspace Runtime.

The canonical language keeps Houmao as an Execution Adapter implementation detail. Core Isomer records should keep provider-neutral names such as Execution Adapter ref, Agent Team Instance, Agent Instance, Run, handoff, Signal Observation, Artifact, and Provenance Record. Houmao-specific ids, project-profile launch paths, mailbox ids, gateway urls, notifier refs, and managed-agent ids belong in opaque adapter payload refs or adapter-specific tables, not in generic Project Manifest, Research Topic Config, Topic Agent Team Profile, or core Agent Team Instance fields.

The local Houmao source checkout lives at `extern/orphan/houmao`. Work in Isomer may depend on that checkout for live adapter tests, but defects discovered in Houmao should be fixed in the Houmao repository and validated with Houmao's own commands before the Isomer adapter relies on the fix.

## Goals / Non-Goals

**Goals:**

- Add a Houmao Execution Adapter that can launch, inspect, stop, and recover one manual-mode `deepsci-org` Agent Team Instance from an existing Topic Agent Team Profile and Workspace Runtime.
- Materialize adapter launch material from `teams/deepsci-org/execplan/agents/`, generated skills, notifier prompts, topology, communication templates, and selected Agent Workspace path plans.
- Persist opaque adapter refs, launch material refs, launch status, inspection snapshots, Signal Observations, Run refs, handoff refs, and Provenance refs in Workspace Runtime.
- Add CLI/API commands that make live adapter mutation explicit and keep inspection commands read-only.
- Support one manual handoff from `deepsci-org-master` to a specialist, observe the candidate completion through Houmao mail or gateway surfaces, and require Operator Agent normalization before Workspace Runtime marks the handoff accepted.
- Add unit tests that run without Houmao and integration or manual-live tests that run only when the local Houmao build is available.

**Non-Goals:**

- Do not implement automatic-mode scheduling, multi-team concurrent launch, task-level fanout launch, GUI rendering, service-team launch, or full UC-01 research completion.
- Do not make Houmao terms first-class Isomer domain fields, schema names, or generic CLI labels.
- Do not copy or vendor Houmao source into Isomer, and do not commit `extern/orphan/houmao` state.
- Do not hide environment repair inside launch; failed preflight should direct setup work through Service Requests or explicit Houmao checkout fixes.

## Decisions

### Decision 1: Adapter module boundary

Implement adapter code in a dedicated module family such as `houmao_adapter.py`, `houmao_models.py`, and `houmao_launch_material.py`, while keeping generic runtime helpers in `runtime_store.py` and `runtime_validation.py`. The CLI should call provider-neutral command handlers that select the Houmao adapter by Execution Adapter ref or explicit `--adapter houmao`.

Alternative considered: put Houmao launch directly inside `cli.py` or Workspace Runtime store helpers. That would make the first launch faster to write but would tangle provider-specific behavior with generic runtime state and make future adapters harder.

### Decision 2: Opaque adapter refs and adapter records

Store Houmao-specific details in adapter-specific records or opaque payload refs linked from generic Workspace Runtime records. Generic records may say `execution_adapter_ref = "execution-adapter:houmao"` and point to adapter payload refs, but they must not add generic fields such as `houmao_managed_agent_id`, `mailbox_id`, or `gateway_url`.

Alternative considered: add Houmao fields directly to Agent Team Instance and Agent Instance records. That would simplify CLI output for this single backend, but it violates the domain-language boundary and would leak implementation language into later GUI and schema contracts.

### Decision 3: Launch material under recorded path plans

Materialize launch material under recorded Topic Workspace or Agent Workspace path plans, for example under an adapter-owned directory inside the selected Topic Workspace and per-agent launch material inside each Agent Workspace. The adapter should record path plans before writing generated project-profile launch files, notifier prompts, mailbox metadata, gateway metadata, and adapter logs.

Alternative considered: write generated material into `.isomer-labs/` or the Houmao checkout. `.isomer-labs/` is project configuration, not runtime state; the Houmao checkout is an implementation dependency, not a topic-owned runtime surface.

### Decision 4: Launch preflight before mutation

Launch requires a current-schema Workspace Runtime, a `ready` Topic Environment Readiness record, a validated Topic Agent Team Profile, Agent Team Instance records, Agent Workspace directories, a resolvable Houmao checkout, adapter launch material validation, and no unresolved launch Gate. Preflight diagnostics should be deterministic and should not partially launch agents.

Alternative considered: launch best-effort and repair missing pieces as failures occur. That would hide state changes, make rollback unclear, and make tests unreliable.

### Decision 5: Manual handoff normalization

The adapter may observe candidate completion through Houmao mail, gateway events, files, or inspection output, but only the Operator Agent normalization path can mark a handoff accepted and attach produced Artifact or Provenance refs. Signal Observations should remain durable evidence of possible completion, not completion authority.

Alternative considered: let the adapter mark a handoff complete when a Houmao reply arrives. That would make the first slice feel smoother, but it would bypass the accepted Isomer manual-mode control model.

### Decision 6: Live Houmao tests are capability-gated

Unit tests should mock the Houmao adapter boundary and prove generated records, command output, validation, side effects, and failure behavior. Live integration tests should be skipped or reported as unavailable unless `extern/orphan/houmao` exists and the required Houmao validation commands pass.

Alternative considered: make live Houmao launch required for the default unit test suite. That would make local development brittle and would blur the repository boundary when Houmao is absent or mid-change.

### Decision 7: Public Houmao project-profile launch boundary

The Houmao adapter should launch Milestone 5 Agent Instances through Houmao's public project-backed CLI surface: `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <generated-profile>`. The adapter may generate or select the Houmao project profile as launch material, parse the deterministic JSON result, and record Houmao profile, managed-agent, gateway, mailbox, and runtime refs as opaque adapter payload refs.

Alternative considered: treat explicit launch-dossier internals or the managed-agent gateway/passive-server API as the primary launch authority. Launch-dossier internals expose lower-level mechanics that are more likely to couple Isomer to Houmao implementation details, while gateway and passive-server surfaces are better treated as post-launch control, communication, observation, and discovery surfaces for this slice.

### Decision 8: Top-level handoffs CLI group

Milestone 5 should expose manual handoff dispatch, observation, and normalization under a top-level `handoffs` command group, for example `isomer-cli handoffs dispatch`, `isomer-cli handoffs observe`, and `isomer-cli handoffs normalize`. These commands should accept `--agent-team-instance` when they target a launched Agent Team Instance, while the handoff record itself remains a first-class Workspace Runtime record linked to Run, Signal Observation, Artifact, and Provenance refs.

Alternative considered: expose handoff behavior under `team-instances handoff ...` or hide it behind an adapter-specific test command. Nesting handoffs under team lifecycle would understate their durable Runtime role, while a hidden adapter command would postpone public behavior and make later CLI tests churn.

### Decision 9: Read-only Houmao capability gate

Before Isomer treats `extern/orphan/houmao` as available for Milestone 5 adapter behavior, preflight should run a lightweight read-only capability gate. The gate resolves the checkout path, confirms `tmux -V`, runs `pixi run houmao-mgr --version`, runs `pixi run houmao-mgr --print-json system-skills list`, runs `pixi run houmao-mgr --print-json project --project-dir <project> status`, and runs `pixi run houmao-mgr --print-json agents global list`.

Alternative considered: require Houmao `pixi run test-runtime` or a temporary live launch smoke as part of the default availability gate. Those checks provide stronger evidence, but they are slower, more credential-dependent, or mutation-prone, so they belong in live-gated integration or manual validation rather than ordinary launch preflight.

### Decision 10: No cache-like launch material retention

Milestone 5 should retain adapter launch material as durable file-backed Artifacts or adapter payload refs with Provenance Records. Generated project profiles, rendered launch files, notifier prompts, communication templates, mailbox metadata, gateway metadata, command JSON, checksums, and launch logs should not be marked cache-like after launch.

Alternative considered: keep only a minimal launch manifest as durable evidence and treat nonessential generated material as cache-like after the first successful launch. The no-cache policy uses more storage but preserves debugging, audit, and replay evidence without relying on rebuildable directories.

## Risks / Trade-offs

- [Risk] Houmao command surfaces or generated launch material expectations may drift. -> Mitigation: keep the adapter boundary thin, detect Houmao checkout capability during preflight, and document exact Houmao validation commands used by live tests.
- [Risk] Adapter records can become a second runtime database. -> Mitigation: store only adapter-specific refs and snapshots needed to map Houmao back to generic Workspace Runtime records; keep Agent Team Instance, Run, handoff, Artifact, and Provenance state authoritative in Workspace Runtime.
- [Risk] Durable launch material can increase Topic Workspace storage. -> Mitigation: keep the record file-backed and structured, avoid inline rich content in SQLite, and let runtime validation report missing durable files clearly.
- [Risk] A partially failed launch can leave Houmao-managed processes running. -> Mitigation: make launch transaction stages explicit, record launch attempts, add a best-effort stop/cleanup path, and report cleanup status without deleting failed records.
- [Risk] Mailbox or gateway observations can be mistaken for accepted research output. -> Mitigation: represent them as Signal Observations and require explicit normalization before changing handoff or Run terminal state.
- [Risk] Fixes needed in Houmao could be accidentally committed through Isomer. -> Mitigation: keep Houmao under `extern/orphan/`, document separate validation, and make Isomer tests report the Houmao checkout path and validation status rather than vendoring changes.

## Migration Plan

1. Add adapter models and store helpers for opaque adapter refs, launch material refs, inspection snapshots, Signal Observations, launch attempts, and adapter Provenance refs.
2. Add a Houmao adapter facade with preflight, materialize, launch, inspect, stop, dispatch handoff, observe, and normalize operations.
3. Wire CLI commands for launch, inspect, stop, and handoff operations with deterministic JSON output.
4. Add mocked unit tests for all command paths and validation failures.
5. Add a live-gated integration or manual test that launches one `deepsci-org` Agent Team Instance through the local Houmao checkout, dispatches one handoff, observes a result, normalizes it, and stops the team.
6. Update README and ROADMAP notes after validation passes.

Rollback is data-preserving: failed or stopped adapter records remain visible in Workspace Runtime, and stop/cleanup commands should mark adapter launch state stopped, failed, or stale rather than deleting records. If a migration changes schema shape, preflight must reject unsupported runtime schema versions before launching.

## Open Questions

None.
