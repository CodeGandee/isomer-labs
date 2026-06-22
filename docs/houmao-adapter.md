# Houmao Adapter

The Houmao Execution Adapter lets Isomer Labs launch and reconcile an Agent Team Instance through Houmao without importing Houmao Python internals. Isomer calls the public `houmao-mgr --print-json` CLI, stores command payloads under the selected Topic Workspace, and records adapter refs in Workspace Runtime.

Houmao-specific concepts such as specialist, project profile, native role, recipe, launch dossier, and managed-agent id belong to this adapter. They are not promoted to generic Isomer domain language unless an accepted spec explicitly does so.

## Launch Paths

### Quick launch

Use the quick path when Isomer should prepare material and launch the Houmao managed agents in one command:

```bash
isomer-cli --print-json team-instances launch <agent-team-instance-id> --adapter houmao --topic <research-topic-id>
```

Quick launch runs preflight, writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, launches one Houmao managed agent per Isomer Agent Instance, writes `adapter-runtime-manifest.json`, and records command runs, payload refs, a launch attempt, and reconciliation state in Workspace Runtime.

### Prepare-only / manual operation

Use the manual path when the operator wants to inspect or edit Houmao material before invoking Houmao directly:

```bash
isomer-cli --print-json team-instances launch-material prepare <agent-team-instance-id> --adapter houmao --topic <research-topic-id>
```

Prepare-only writes the same material and manifests but does not launch, stop, message, or inspect Houmao managed agents. The JSON output includes bounded manual guidance for equivalent `houmao-mgr` commands. After direct Houmao work, use `inspect-live`, `reconcile`, or `adopt` so Isomer can compare manifests, file digests, and read-only Houmao observations.

## Runtime Files

Generated files live under `runtime/adapters/houmao/<agent-team-instance-id>/` inside the selected Topic Workspace.

- `adapter-link.json` — durable link manifest that binds the Agent Team Instance to Houmao launch context.
- `launch-material-manifest.json` — manifest of generated launch material files, their digests, editable policy, and agent instance mapping.
- `adapter-runtime-manifest.json` — runtime reconciliation state, agent bindings, live observation summary, and diagnostics.
- `command-payloads/` — JSON payloads for Houmao CLI invocations, redacted when they contain secret-like fields.
- `logs/` — adapter command logs.
- `inspection-snapshots/` — bounded read-only inspection snapshots.
- `stop-outcomes/` — records of stop command results.
- `handoff-payloads/` — durable Isomer-authored dispatch payloads handed to Houmao.
- `handoff-observations/` — non-authoritative Signal Observation payloads collected from mail, gateway, file, or inspection sources.
- `handoff-normalizations/` — Operator Agent normalization payloads that accept, reject, block, supersede, repair-route, or follow up on a candidate result.
- `houmao-project-overlay/` — generated Houmao project overlay directory.

The adapter records path plans for the adapter root, launch material, per-Agent Instance material, command payloads, logs, inspection snapshots, stop outcomes, handoff payloads, handoff observations, handoff normalizations, and the generated Houmao project overlay. These files are durable runtime records, not cache.

## Manual Handoff Round

Handoff commands are a generic Isomer CLI surface backed here by Houmao. Use `--print-json` at the root when scripts need deterministic JSON; without it, the commands print structured human-readable status lines. The handoff commands do not expose command-local `--json` or `--format json` flags.

```bash
isomer-cli --print-json handoffs dispatch \
  --topic <research-topic-id> \
  --agent-team-instance <agent-team-instance-id> \
  --source-agent-instance <source-agent-instance-id> \
  --target-agent-instance <target-agent-instance-id> \
  --run <run-id> \
  --message "Please produce the requested handoff result." \
  --expected-output artifact:<topic>:handoff-result
```

`handoffs dispatch` requires a ready Workspace Runtime and a launched, adopted, or linked Houmao adapter context. It creates or reuses the selected Run, writes a durable dispatch payload, invokes the Houmao mail dispatch command, records an `HandoffRecord`, and links adapter command and payload refs. Houmao message ids, gateway event ids, mailbox details, managed-agent ids, and command payload internals stay inside adapter payload JSON or adapter-specific records.

```bash
isomer-cli --print-json handoffs observe <handoff-id> --topic <research-topic-id> --source mail
isomer-cli --print-json handoffs observe <handoff-id> --topic <research-topic-id> --source gateway
isomer-cli --print-json handoffs observe <handoff-id> --topic <research-topic-id> --source file --payload-json handoff-observation.json
isomer-cli --print-json handoffs observe <handoff-id> --topic <research-topic-id> --source inspection
```

`handoffs observe` records a Signal Observation. A Signal Observation is not completion authority: it can move a handoff into candidate state, but it does not complete the Run, promote a returned claim into an Evidence Item, or accept an Artifact. The Operator Agent must normalize the result.

```bash
isomer-cli --print-json handoffs normalize <handoff-id> \
  --topic <research-topic-id> \
  --status accepted \
  --signal-observation <signal-observation-id> \
  --output-artifact artifact:<topic>:handoff-result \
  --rationale "Operator accepted the candidate result."
```

`handoffs normalize` records the Operator Agent decision. `accepted` marks the handoff accepted and completes the linked Run. `rejected`, `blocked`, `superseded`, `repair_routed`, and `follow_up` preserve the observations and rationale; `repair_routed` maps the handoff to repair state and should include a corrective Service Request or follow-up ref when available.

## Backend Resolution

By default, Isomer resolves `houmao-mgr` from `PATH`. You can override it with `ISOMER_HOUMAO_COMMAND`:

```bash
ISOMER_HOUMAO_COMMAND="/path/to/houmao-mgr" isomer-cli team-instances launch <id> --adapter houmao
```

If `houmao-mgr` is not on `PATH`, Isomer looks for a Pixi-backed checkout at `extern/orphan/houmao`, `ISOMER_HOUMAO_CHECKOUT`, or `~/workspace/code/houmao`.

Before live mutation, use read-only checks:

```bash
isomer-cli --print-json doctor --topic <research-topic-id>
isomer-cli --print-json runtime validate --topic <research-topic-id> --require-ready-readiness
houmao-mgr --version
```

The expected local checkout is `extern/orphan/houmao`, usually a symlink to `~/workspace/code/houmao`. Isomer tests and manual checks must not write into or commit that checkout. If a Houmao defect blocks launch, mail, gateway, inspection, or stop behavior, fix it in the Houmao repository and validate it there before depending on it from Isomer.

## Manifests and Reconciliation

### `adapter-link.json`

Created by `team-instances adapter-link export` or by launch/prepare commands. It stores project refs, the Agent Team Instance id, the Topic Agent Team Profile id, the Domain Agent Team Template id, agent bindings, and the Houmao project overlay directory.

### `launch-material-manifest.json`

Created by launch or prepare commands. It stores a digest-backed inventory of generated launch material files. `inspect-live --integrity` and `reconcile` compare current file digests against this manifest to detect drift.

### `adapter-runtime-manifest.json`

Created by launch, reconcile, or adopt commands. It stores the reconciliation state, mapping confidence, manifest digest summary, live observation summary, agent bindings, material drift, and diagnostics.

### Reconciliation states

The adapter can report these reconciliation states:

- `linked` — the adapter link manifest exists and no launch material or live state contradicts it.
- `launched_by_isomer` — the runtime manifest indicates Isomer performed the quick launch.
- `external_detected` — live Houmao state matches the agent bindings but the source mode is not `isomer_quick_launch`.
- `adopted` — the operator explicitly adopted externally launched state.
- `drifted` — file digests differ from `launch-material-manifest.json`.
- `conflicted` — agent instance to Houmao managed-agent mapping is inconsistent.
- `stale` — observations are out of date.
- `rejected` — the adapter link manifest is missing or reconciliation cannot proceed.

## Inspect and Stop

`inspect-live --adapter houmao` runs read-only Houmao CLI inspection and records a bounded adapter inspection snapshot. It does not launch or stop agents.

```bash
isomer-cli --print-json team-instances inspect-live <agent-team-instance-id> --adapter houmao --topic <research-topic-id>
```

`stop --adapter houmao` is an explicit live mutation. It targets known mapped Houmao agent names from manifests or launch attempts and records a stopped, partial, failed, or stale outcome.

```bash
isomer-cli --print-json team-instances stop <agent-team-instance-id> --adapter houmao --topic <research-topic-id>
```

## Troubleshooting

- Missing Houmao checkout or command: set `ISOMER_HOUMAO_COMMAND`, add `houmao-mgr` to `PATH`, or expose the local checkout at `extern/orphan/houmao`.
- Failed preflight: run `isomer-cli runtime validate --require-ready-readiness --topic <topic>` and verify the selected Agent Team Instance exists.
- Failed handoff dispatch: verify the Agent Team Instance has a launched, adopted, or linked Houmao adapter context and that source and target Agent Instance ids belong to that team.
- Stale handoff: run `handoffs observe` again if a fresh adapter signal exists, or record `handoffs normalize --status rejected`, `--status blocked`, or `--status repair_routed` with rationale.
- Rejected or repair-routed result: keep the Signal Observation ids attached to the normalization and include corrective Service Request or follow-up refs with `--corrective-ref`.
- Invalid CLI JSON: inspect the adapter command payload under `runtime/adapters/houmao/<id>/command-payloads/`; the normal CLI output is redacted and bounded.
- Direct edit drift: run `isomer-cli team-instances inspect-live <id> --integrity --topic <topic>` or `reconcile` to compare current file digests with `launch-material-manifest.json`.
- Partial launch: run `inspect-live --adapter houmao` to discover known live refs, then run `stop --adapter houmao` if cleanup is needed.
- Partial stop: use `inspect-live --adapter houmao` again and review `runtime validate` warnings before retrying stop.

## Manual Validation

The live-gated handoff manual test is:

```bash
pixi run python tests/manual/houmao_handoff_round.py --live-houmao
```

Set `ISOMER_MANUAL_LIVE_HOUMAO=1` before running it against a real Houmao checkout. Without `--live-houmao`, the script uses a local fake Houmao command and validates the Isomer-side handoff records only.

See [Troubleshooting](troubleshooting.md) for the full diagnostics guide.
