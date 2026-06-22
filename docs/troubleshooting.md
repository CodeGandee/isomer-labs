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
pixi run isomer-cli validate --json
```

`init` mutates the Project filesystem. If a Project already exists but the command cannot find it, use `--project` to point to the correct root.

## Pixi or Readiness Failures

Symptom: `doctor` or `runtime prepare` reports missing Pixi, missing `pixi.lock`, or failed topic environment bindings.

Diagnosis:

```bash
pixi run isomer-cli doctor --topic default --json
pixi run isomer-cli runtime validate --topic default --require-ready-readiness --json
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
pixi run isomer-cli runtime inspect --topic default --json
```

Recovery:

- If the runtime is older, migration tooling may be required; in the current milestone, recreate the Topic Workspace after backing up research Artifacts.
- If the runtime is newer, upgrade `isomer-labs` to a version that understands the schema.

## Missing Agent Workspaces

Symptom: `runtime validate` reports missing Agent Workspace directories.

Diagnosis:

```bash
pixi run isomer-cli team-instances show <id> --topic default --json
pixi run isomer-cli paths preview --topic default --json
```

Recovery:

- If the Agent Team Instance exists but directories are missing, the Workspace Runtime record may be inconsistent. Re-create the Agent Team Instance or restore the directory from backup.
- If the Agent Team Instance was never created, run `team-instances create`.

## Invalid CLI JSON

Symptom: a command returns non-zero and JSON output is incomplete or redacted.

Diagnosis:

- Inspect the adapter command payload under `topic-workspaces/<topic>/runtime/adapters/houmao/<id>/command-payloads/`.
- Run the command with `--json` and capture stderr.

Recovery:

- Fix the underlying cause (missing topic binding, missing Agent Team Instance, bad Project Manifest).
- Direct JSON edits are an advanced recovery path; after editing, run `inspect-live --integrity` or `reconcile` to validate the manifest state.

## Manifest Drift

Symptom: `inspect-live --integrity` or `reconcile` reports material drift.

Diagnosis:

```bash
pixi run isomer-cli team-instances inspect-live <id> --topic default --adapter houmao --integrity --json
pixi run isomer-cli team-instances reconcile <id> --topic default --json
```

Recovery:

- If you edited launch material directly, restore the files to the recorded digests or regenerate material with `launch-material prepare`.
- If the drift is expected, run `reconcile` to record the new state and update `adapter-runtime-manifest.json`.

## Partial Launch

Symptom: `team-instances launch` returned a partial or failed status, but some Houmao agents may be running.

Diagnosis:

```bash
pixi run isomer-cli team-instances inspect-live <id> --topic default --adapter houmao --json
pixi run isomer-cli runtime validate --topic default --json
```

Recovery:

- Use `inspect-live` to discover known live refs.
- Run `stop` if cleanup is needed.
- Run `reconcile` to record the final state.

## Partial Stop

Symptom: `team-instances stop` returned partial or failed, and some agents remain live.

Diagnosis:

```bash
pixi run isomer-cli team-instances inspect-live <id> --topic default --adapter houmao --json
pixi run isomer-cli runtime validate --topic default --json
```

Recovery:

- Inspect live refs and remaining adapter state.
- Retry `stop` after resolving any underlying issue (missing `houmao-mgr`, changed agent names, stale manifests).
- Run `reconcile` to record the outcome.

## Direct Houmao Reconciliation

Symptom: you launched agents directly with `houmao-mgr` and Isomer does not know about them.

Diagnosis:

- Ensure `adapter-link.json` and `launch-material-manifest.json` exist under the Topic Workspace adapter directory.
- Run `inspect-live --integrity` to compare material digests.

Recovery:

```bash
pixi run isomer-cli team-instances reconcile <id> --topic default --adapter houmao --json
pixi run isomer-cli team-instances adopt <id> --topic default --adapter houmao --yes --json
```

`adopt` records an explicit decision to associate externally launched state with the Agent Team Instance. It requires `--yes`.

## Diagnostic Checklist

When a command fails unexpectedly:

1. Run `isomer-cli validate --json` to check the Project Manifest.
2. Run `isomer-cli doctor --json` to check host and Project Pixi state.
3. Run `isomer-cli context show --topic <topic> --json` to inspect Effective Topic Context.
4. Run `isomer-cli runtime validate --topic <topic> --json` to inspect Workspace Runtime.
5. For Houmao issues, verify `houmao-mgr` availability or set `ISOMER_HOUMAO_COMMAND`.
6. Inspect adapter payloads and manifests under `topic-workspaces/<topic>/runtime/adapters/houmao/<id>/`.
7. Escalate repair to explicit Service Requests rather than hiding it inside read-only diagnostics.
