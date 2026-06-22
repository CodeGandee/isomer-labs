# Houmao Execution Adapter Design Choices

Date: 2026-06-22

## Context

Recent Houmao adapter work already added the modular CLI-backed launch, launch material, inspect-live, stop, manifest reconciliation, and adoption foundation for one manual-mode `deepsci-org` Agent Team Instance. The revised Milestone 5 change adds the remaining handoff/control slice on top of that foundation. The adapter must keep Houmao gateway, mailbox, notifier, managed-agent, message, and session details behind opaque adapter refs while Workspace Runtime remains authoritative for Isomer Agent Team Instance, Agent Instance, Run, handoff, Artifact, Signal Observation, and Provenance Record state.

## Resolved Choices

### Houmao Launch Entrypoint

Use the existing thin Isomer wrapper over Houmao's public project-backed CLI launch path: `houmao-mgr --print-json project --project-dir <dir> agents launch --profile <generated-profile>`.

The adapter foundation may generate or select Houmao project-profile launch material, run the public launch command, parse deterministic JSON output, and record Houmao profile, managed-agent, gateway, mailbox, and runtime refs as opaque adapter payload refs. The revised Milestone 5 handoff work should reuse those existing refs and should not relaunch or re-materialize launch material just to dispatch a handoff.

Rejected alternatives were direct launch-dossier or native-agent internals as the primary Isomer launch path, and managed-agent gateway or passive-server APIs as the initial launch authority. The public project-profile CLI path aligns with Houmao's documented maintained launch surface while avoiding unnecessary coupling to lower-level launch-dossier mechanics.

### Handoff CLI Shape

Use a top-level `handoffs` command group for Milestone 5 manual handoff dispatch, observation, and normalization commands.

The CLI should expose paths such as `isomer-cli handoffs dispatch`, `isomer-cli handoffs observe`, and `isomer-cli handoffs normalize`, with `--agent-team-instance` used when a command targets a launched Agent Team Instance. This keeps handoffs aligned with first-class Workspace Runtime records while preserving links to Agent Team Instance, Run, Signal Observation, Artifact, and Provenance Record state.

Handoff commands should use structured human-readable output by default and deterministic JSON through root-level `isomer-cli --print-json ...`; they should not add command-local JSON flags.

Rejected alternatives were `team-instances handoff ...`, which would hide handoffs under team lifecycle, and an adapter-specific hidden command, which would defer public command behavior and create later test churn.

### Houmao Availability Validation

Use a lightweight read-only capability gate before treating `extern/orphan/houmao` as adapter-available.

The gate should resolve the checkout path, confirm `tmux -V`, run `pixi run houmao-mgr --version`, run `pixi run houmao-mgr --print-json system-skills list`, run `pixi run houmao-mgr --print-json project --project-dir <project> status`, and run `pixi run houmao-mgr --print-json agents global list`. These checks confirm the local source checkout, primary CLI, packaged skill catalog, selected project overlay, and read-only managed-agent registry surfaces without starting agents or mutating Houmao state.

Broader Houmao validation such as `pixi run test-runtime` and live launch smoke checks should stay in live-gated integration or manual validation. They are useful evidence but too slow, credential-dependent, or mutation-prone for default adapter availability.

### Launch Material Retention

Do not use cache-like retention for adapter launch material or handoff payload evidence.

The existing adapter foundation retains generated project profiles, rendered launch files, notifier prompts, communication templates, mailbox metadata, gateway metadata, command JSON, checksums, and launch logs as durable file-backed Artifacts or adapter payload refs with Provenance Records. The revised handoff work should apply the same policy to handoff dispatch payloads, mailbox or gateway observations, normalization artifacts, repair payloads, and adapter logs. Missing material should be reported as missing durable evidence by runtime validation rather than silently regenerated or ignored as disposable cache.

Rejected alternatives were a hybrid policy that retained only a minimal manifest durably while treating nonessential generated material as cache-like, and a lean policy that cached most launch material after successful launch.

## Remaining Questions

None.
