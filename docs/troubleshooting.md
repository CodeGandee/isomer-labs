# Troubleshooting

This page collects common diagnostics and recovery paths for Isomer Labs. Each section starts with read-only inspection and escalates to explicit mutation only when necessary.

## Missing Project

Symptom: `isomer-cli` reports that no Project Manifest was found.

Diagnosis:

- Confirm you are inside the Project tree or pass `--project <path>`.
- Confirm `.isomer-labs/manifest.toml` exists.

Recovery:

```bash
pixi run isomer-cli init
pixi run isomer-cli --print-json validate
```

`init` mutates the Project filesystem by creating `.houmao/`, `.isomer-labs/`, the first Research Topic Config, and the first Topic Workspace. If a Project already exists but the command cannot find it, use `--project` to point to the correct root.

## Houmao Project Bootstrap Failure

Symptom: `isomer-cli init` reports Houmao command resolution, invalid JSON, timeout, nonzero exit, or missing `.houmao/` diagnostics and does not write `.isomer-labs/manifest.toml`.

Diagnosis:

```bash
houmao-mgr --version
pixi run isomer-cli --print-json doctor
```

Recovery:

- Set `ISOMER_HOUMAO_COMMAND` to the supported Houmao manager command, add `houmao-mgr` to `PATH`, or expose the local checkout at `extern/orphan/houmao`.
- Rerun `pixi run isomer-cli init` after the Houmao command boundary works.
- Do not create `.isomer-labs/` by hand as a workaround; fresh init should create both `.houmao/` and `.isomer-labs/` together.

## Pixi or Readiness Failures

Symptom: `doctor` or `runtime prepare` reports missing Pixi, missing `pixi.lock`, or failed topic environment bindings.

Diagnosis:

```bash
pixi run isomer-cli --print-json doctor --topic default
pixi run isomer-cli --print-json runtime validate --topic default --require-ready-readiness
```

Recovery:

- Run `pixi install` to resolve the default environment.
- Add explicit `topic_pixi_environment_bindings` or `topic_standalone_pixi_bindings` entries to the Project Manifest.
- Treat environment setup or compatibility work as a Service Request rather than hiding it inside a read-only diagnostic.

## Invalid Topic Bindings

Symptom: `runtime prepare` records `blocked` for a Research Topic.

Diagnosis: inspect the Project Manifest for `topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings`. Isomer never infers a topic's environment from its id or name.

Recovery: add explicit bindings. For example:

```toml
[[topic_pixi_environment_bindings]]
research_topic_id = "default"
pixi_environment = "default"
purpose = "runtime"
```

## Workspace Runtime Schema Issues

Symptom: `runtime init` reports an unsupported schema version.

Diagnosis:

```bash
pixi run isomer-cli --print-json runtime inspect --topic default
```

Recovery:

- If the runtime is older, migration tooling may be required; in the current milestone, recreate the Topic Workspace after backing up research Artifacts.
- If the runtime is newer, upgrade `isomer-labs` to a version that understands the schema.

## Missing Agent Workspaces

Symptom: `runtime validate` reports missing Agent Workspace directories.

Diagnosis:

```bash
pixi run isomer-cli --print-json team-instances show <id> --topic default
pixi run isomer-cli --print-json paths preview --topic default
```

Recovery:

- If the Agent Team Instance exists but directories are missing, the Workspace Runtime record may be inconsistent. Re-create the Agent Team Instance or restore the directory from backup.
- If the Agent Team Instance was never created, run `team-instances create`.

## Invalid CLI JSON

Symptom: a command returns non-zero and JSON output is incomplete or redacted.

Diagnosis:

- Inspect the adapter command payload under `topic-workspaces/<topic>/runtime/adapters/houmao/<id>/command-payloads/`.
- Run the command with `--print-json` and capture stderr.

Recovery:

- Fix the underlying cause (missing topic binding, missing Agent Team Instance, bad Project Manifest).
- Direct JSON edits are an advanced recovery path; after editing, run `inspect-live --integrity` or `reconcile` to validate the manifest state.

## Manifest Drift

Symptom: `inspect-live --integrity` or `reconcile` reports material drift.

Diagnosis:

```bash
pixi run isomer-cli --print-json team-instances inspect-live <id> --topic default --adapter houmao --integrity
pixi run isomer-cli --print-json team-instances reconcile <id> --topic default
```

Recovery:

- If you edited launch material directly, restore the files to the recorded digests or regenerate material with `launch-material prepare`.
- If the drift is expected, run `reconcile` to record the new state and update `adapter-runtime-manifest.json`.

## Partial Launch

Symptom: `team-instances launch` returned a partial or failed status, but some Houmao agents may be running.

Diagnosis:

```bash
pixi run isomer-cli --print-json team-instances inspect-live <id> --topic default --adapter houmao
pixi run isomer-cli --print-json runtime validate --topic default
```

Recovery:

- Use `inspect-live` to discover known live refs.
- Run `stop` if cleanup is needed.
- Run `reconcile` to record the final state.

## Partial Stop

Symptom: `team-instances stop` returned partial or failed, and some agents remain live.

Diagnosis:

```bash
pixi run isomer-cli --print-json team-instances inspect-live <id> --topic default --adapter houmao
pixi run isomer-cli --print-json runtime validate --topic default
```

Recovery:

- Inspect live refs and remaining adapter state.
- Retry `stop` after resolving any underlying issue (missing `houmao-mgr`, changed agent names, stale manifests).
- Run `reconcile` to record the outcome.

## Handoff Dispatch Preflight

Symptom: `handoffs dispatch` returns `ISO070`, `ISO077`, or another adapter diagnostic and does not create a handoff.

Diagnosis:

```bash
pixi run isomer-cli --print-json runtime validate --topic default --require-ready-readiness
pixi run isomer-cli --print-json team-instances show <id> --topic default
pixi run isomer-cli --print-json team-instances inspect-live <id> --topic default --adapter houmao
```

Recovery:

- If Houmao is missing, set `ISOMER_HOUMAO_COMMAND`, add `houmao-mgr` to `PATH`, or expose `extern/orphan/houmao` as a symlink to the local checkout.
- If the Agent Team Instance has not been launched, linked, or adopted, run the launch, reconcile, or adopt workflow first.
- If source or target Agent Instance ids are wrong, use `team-instances show` and choose ids from that team only.
- If readiness is blocked, record repair as a Service Request before dispatching handoffs.

## Handoff Observation and Normalization

Symptom: `handoffs observe` records a candidate result, but the Run still appears `running`.

Explanation: this is expected. Signal Observations are non-authoritative adapter observations. They do not complete Runs, accept Artifacts, or promote returned claims into Evidence Items.

Recovery:

```bash
pixi run isomer-cli --print-json handoffs normalize <handoff-id> \
  --topic default \
  --status accepted \
  --signal-observation <signal-observation-id> \
  --output-artifact artifact:default:accepted-result
```

Use `--status rejected`, `--status blocked`, `--status superseded`, `--status repair_routed`, or `--status follow_up` when the candidate result is not acceptable. Add `--rationale` and `--corrective-ref` so the rejected or repair-routed state has durable context.

## UC-01 Headless Exploration

Symptom: the UC-01 manual harness reports the fixture is incomplete, skips live mode, or `runtime validate` reports diagnostics after a manual run.

Diagnosis:

```bash
pixi run isomer-cli --project tests/fixtures/projects/uc01-headless-gb10 --print-json validate
pixi run python tests/manual/uc01_headless_vertical_slice
```

Recovery:

- Missing fixture state: copy the fixture Project to a writable temporary directory, confirm the topic id is `flash-attention-gb10-peak-performance-optimization`, and rerun the manual harness.
- Failed adapter mode: use the default simulated mode for deterministic validation. Live mode requires `ISOMER_MANUAL_LIVE_HOUMAO=1`; without it, the harness must report `skipped: true` and `mutated: false`.
- Open follow-up Gate: inspect `gate-uc01-follow-up-inquiry` in the harness summary and rerun the harness only if the graph is incomplete. A completed rerun is restart-safe and returns `mutated: false`.
- Unsupported claim support: keep claim candidates as Finding records unless accepted Evidence Item links support a Research Claim under the recording contracts.
- Missing Artifact files: inspect `topic-workspaces/flash-attention-gb10-peak-performance-optimization/artifacts/uc01/`, restore the missing file, and rerun `runtime validate`.
- Incomplete Provenance refs: compare the harness `uc01_summary` output against `runtime validate` diagnostics and repair through a corrective run or explicit provenance record rather than editing lifecycle rows by hand.

## Stale Handoff

Symptom: `runtime validate` reports `ISO045` for a handoff.

Diagnosis:

```bash
pixi run isomer-cli --print-json team-instances show <id> --topic default
pixi run isomer-cli --print-json runtime validate --topic default
```

Recovery:

- Run `handoffs observe` again if a fresh Houmao mail, gateway, file, or inspection signal exists.
- Normalize the handoff as accepted, rejected, blocked, superseded, repair-routed, or follow-up after Operator review.
- If the adapter payload is missing or corrupt, inspect `handoff-payloads/`, `handoff-observations/`, and `command-payloads/` under the adapter root, then rerun validation.

## Direct Houmao Reconciliation

Symptom: you launched agents directly with `houmao-mgr` and Isomer does not know about them.

Diagnosis:

- Ensure `adapter-link.json` and `launch-material-manifest.json` exist under the Topic Workspace adapter directory.
- Run `inspect-live --integrity` to compare material digests.

Recovery:

```bash
pixi run isomer-cli --print-json team-instances reconcile <id> --topic default --adapter houmao
pixi run isomer-cli --print-json team-instances adopt <id> --topic default --adapter houmao --yes
```

`adopt` records an explicit decision to associate externally launched state with the Agent Team Instance. It requires `--yes`.

## Diagnostic Checklist

When a command fails unexpectedly:

1. Run `isomer-cli --print-json validate` to check the Project Manifest.
2. Run `isomer-cli --print-json doctor` to check host and Project Pixi state.
3. Run `isomer-cli --print-json context show --topic <topic>` to inspect Effective Topic Context.
4. Run `isomer-cli --print-json runtime validate --topic <topic>` to inspect Workspace Runtime.
5. For Houmao issues, verify `houmao-mgr` availability or set `ISOMER_HOUMAO_COMMAND`.
6. Inspect adapter payloads and manifests under `topic-workspaces/<topic>/runtime/adapters/houmao/<id>/`.
7. Escalate repair to explicit Service Requests rather than hiding it inside read-only diagnostics.
