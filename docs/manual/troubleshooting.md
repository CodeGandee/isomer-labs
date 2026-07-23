# Troubleshooting

This manual page collects common diagnostics and recovery paths for Isomer Labs. Each section starts with read-only inspection and escalates to explicit mutation only when necessary.

## Missing Project

Symptom: `isomer-cli` reports that no Project Manifest was found.

Diagnosis:

- Confirm you are inside the Project tree or pass `project --root <path>` before the Project subcommand.
- Confirm `.isomer-labs/manifest.toml` exists.

Recovery:

```bash
isomer-cli project init
isomer-cli --print-json project validate
```

`project init` mutates the Project filesystem by creating `.isomer-labs/`, the Isomer-managed Houmao overlay under `.isomer-labs/.houmao/`, and the selected generated content root (`isomer-content/` by default or `--content-dir <content-dir>` when supplied). It does not create a Research Topic Config or Topic Workspace; use `project topics create <topic-id> --statement "<research topic>"` for that. If a Project already exists but the command cannot find it, use `project --root <path>` to point to the correct root.

## Houmao Project Bootstrap Failure

Symptom: `isomer-cli project init` reports Houmao command resolution, invalid JSON, timeout, nonzero exit, or missing `.isomer-labs/.houmao/` diagnostics and does not write `.isomer-labs/manifest.toml`.

Diagnosis:

```bash
houmao-mgr --version
isomer-cli --print-json doctor
```

Recovery:

- Set `ISOMER_HOUMAO_COMMAND` to the supported Houmao manager command, add `houmao-mgr` to `PATH`, or expose the local checkout at `extern/orphan/houmao`.
- Rerun `isomer-cli project init` after the Houmao command boundary works.
- Do not create `.isomer-labs/` by hand as a workaround; fresh init should create `.isomer-labs/`, `.isomer-labs/.houmao/`, and the selected generated content root together.

## Pixi or Readiness Failures

Symptom: `doctor` or `project runtime prepare` reports missing Pixi, missing `pixi.lock`, or failed topic environment bindings.

Diagnosis:

```bash
isomer-cli --print-json doctor --with-topic my-topic
isomer-cli --print-json project runtime validate --topic my-topic --require-ready-readiness
```

Recovery:

- Run `pixi install` to resolve the default environment.
- If the registered Topic Workspace already has a Pixi manifest at its root, rerun diagnostics after Pixi is available on `PATH`; Isomer can use the Topic Workspace directory as the implicit default binding target.
- Add explicit `topic_pixi_environment_bindings` or `topic_standalone_pixi_bindings` entries only when the topic should use a Project-root environment or a non-default Topic Workspace Pixi target.
- Treat environment setup or compatibility work as a Service Request rather than hiding it inside a read-only diagnostic.

## Invalid Topic Bindings

Symptom: `project runtime prepare` records `blocked` for a Research Topic.

Diagnosis: inspect the Project Manifest for `topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings`, then run `doctor --with-topic <topic-id>` to see whether Pixi can resolve the registered Topic Workspace directory as the implicit default target. Isomer never infers a topic's environment from its id or name.

Recovery: keep the implicit default when the Topic Workspace root is the Pixi workspace, or add an explicit binding when the target is different. For example:

```toml
[[topic_pixi_environment_bindings]]
research_topic_id = "my-topic"
pixi_environment = "default"
purpose = "runtime"

[[topic_standalone_pixi_bindings]]
research_topic_id = "my-topic"
manifest_path_or_dir = "isomer-content/topic-ws/my-topic"
pixi_environment = "default"
```

## Workspace Runtime Schema Issues

Symptom: `project runtime init` reports an unsupported schema version.

Diagnosis:

```bash
isomer-cli --print-json project runtime inspect --topic my-topic
```

Recovery:

- If the runtime is older, migration tooling may be required; in the current milestone, recreate the Topic Workspace after backing up research Artifacts.
- If the runtime is newer, upgrade `isomer-labs` to a version that understands the schema.

## Missing Agent Workspaces

Symptom: `project runtime validate` reports missing Agent Workspace directories.

Diagnosis:

```bash
isomer-cli --print-json project team-instances show <id> --topic my-topic
isomer-cli --print-json project paths preview --topic my-topic
```

Recovery:

- If the Agent Team Instance exists but directories are missing, the Workspace Runtime record may be inconsistent. Re-create the Agent Team Instance or restore the directory from backup.
- If the Agent Team Instance was never created, run `project team-instances create`.

## Missing or Stale Isomer-managed Support

Symptom: `project runtime validate` reports a missing `isomer-managed/` support path, unsafe generated links, unpromoted dependencies on untracked share material, or a legacy `.isomer-agent/` support-path diagnostic.

Diagnosis:

```bash
isomer-cli --print-json project runtime validate --topic my-topic
isomer-cli --print-json project team-instances show <id> --topic my-topic
```

Recovery:

- Treat legacy `.isomer-agent/` and old top-level Topic Main Development Repository collaboration paths as breaking-layout diagnostics, not as instructions to delete files.
- Restore or prepare the current `isomer-managed/` layout through explicit operator workflow before launch-facing work depends on it.
- Promote files under `isomer-managed/agent-owned/` or `isomer-managed/topic-owned/` into tracked Isomer material, owner-preserved records, or Provenance Records before using them as durable evidence.
- Inspect generated `isomer-managed/links/` targets and remove or replace unsafe links only after the operator confirms the intended target.

## Invalid CLI JSON

Symptom: a command returns non-zero and JSON output is incomplete or redacted.

Diagnosis:

- Inspect the adapter command payload under `isomer-content/topic-ws/<topic>/runtime/adapters/houmao/<id>/command-payloads/` for fresh Projects, or under the registered Topic Workspace path for existing Projects.
- Run the command with `--print-json` and capture stderr.

Recovery:

- Fix the underlying cause (missing topic binding, missing Agent Team Instance, bad Project Manifest).
- Direct JSON edits are an advanced recovery path; after editing, run `inspect-live --integrity` or `reconcile` to validate the manifest state.

## Manifest Drift

Symptom: `inspect-live --integrity` or `reconcile` reports material drift.

Diagnosis:

```bash
isomer-cli --print-json project team-instances inspect-live <id> --topic my-topic --adapter houmao --integrity
isomer-cli --print-json project team-instances reconcile <id> --topic my-topic
```

Recovery:

- If you edited launch material directly, restore the files to the recorded digests or regenerate material with `launch-material prepare`.
- If the drift is expected, run `reconcile` to record the new state and update `adapter-runtime-manifest.json`.

## Partial Launch

Symptom: `project team-instances launch` returned a partial or failed status, but some Houmao agents may be running.

Diagnosis:

```bash
isomer-cli --print-json project team-instances inspect-live <id> --topic my-topic --adapter houmao
isomer-cli --print-json project runtime validate --topic my-topic
```

Recovery:

- Use `inspect-live` to discover known live refs.
- Run `stop` if cleanup is needed.
- Run `reconcile` to record the final state.

## Partial Stop

Symptom: `project team-instances stop` returned partial or failed, and some agents remain live.

Diagnosis:

```bash
isomer-cli --print-json project team-instances inspect-live <id> --topic my-topic --adapter houmao
isomer-cli --print-json project runtime validate --topic my-topic
```

Recovery:

- Inspect live refs and remaining adapter state.
- Retry `stop` after resolving any underlying issue (missing `houmao-mgr`, changed agent names, stale manifests).
- Run `reconcile` to record the outcome.

## Handoff Dispatch Preflight

Symptom: `project handoffs dispatch` returns `ISO070`, `ISO077`, or another adapter diagnostic and does not create a handoff.

Diagnosis:

```bash
isomer-cli --print-json project runtime validate --topic my-topic --require-ready-readiness
isomer-cli --print-json project team-instances show <id> --topic my-topic
isomer-cli --print-json project team-instances inspect-live <id> --topic my-topic --adapter houmao
```

Recovery:

- If Houmao is missing, set `ISOMER_HOUMAO_COMMAND`, add `houmao-mgr` to `PATH`, or expose `extern/orphan/houmao` as a symlink to the local checkout.
- If the Agent Team Instance has not been launched, linked, or adopted, run the launch, reconcile, or adopt workflow first.
- If source or target Agent Instance ids are wrong, use `project team-instances show` and choose ids from that team only.
- If readiness is blocked, record repair as a Service Request before dispatching handoffs.

## Handoff Observation and Normalization

Symptom: `project handoffs observe` records a candidate result, but the Run still appears `running`.

Explanation: this is expected. Signal Observations are non-authoritative adapter observations. They do not complete Runs, accept Artifacts, or promote returned claims into Evidence Items.

Recovery:

```bash
isomer-cli --print-json project handoffs normalize <handoff-id> \
  --topic my-topic \
  --status accepted \
  --signal-observation <signal-observation-id> \
  --output-artifact artifact:default:accepted-result
```

Use `--status rejected`, `--status blocked`, `--status superseded`, `--status repair_routed`, or `--status follow_up` when the candidate result is not acceptable. Add `--rationale` and `--corrective-ref` so the rejected or repair-routed state has durable context.

## UC-01 Headless Exploration

Symptom: the source-checkout UC-01 manual harness reports the fixture is incomplete, skips live mode, or `project runtime validate` reports diagnostics after a manual run.

Diagnosis:

```bash
isomer-cli --print-json project --root /path/to/project validate
pixi run python tests/manual/uc01_headless_vertical_slice
```

Recovery:

- Missing fixture state: copy the fixture Project to a writable temporary directory, confirm the topic id is `flash-attention-gb10-peak-performance-optimization`, and rerun the manual harness.
- Failed adapter mode: use the default simulated mode for deterministic validation. Live mode requires `ISOMER_MANUAL_LIVE_HOUMAO=1`; without it, the harness must report `skipped: true` and `mutated: false`.
- Open follow-up Gate: inspect `gate-uc01-follow-up-inquiry` in the harness summary and rerun the harness only if the graph is incomplete. A completed rerun is restart-safe and returns `mutated: false`.
- Unsupported claim support: keep claim candidates as Finding records unless accepted Evidence Item links support a Research Claim under the recording contracts.
- Missing Artifact files: inspect `topic-workspaces/flash-attention-gb10-peak-performance-optimization/records/artifacts/uc01/` for owner-preserved records or `repos/topic-main/isomer-managed/tracked/artifacts/uc01/` for worker-published material, restore the missing file, and rerun `project runtime validate`.
- Incomplete Provenance refs: compare the harness `uc01_summary` output against `project runtime validate` diagnostics and repair through a corrective run or explicit provenance record rather than editing lifecycle rows by hand.

## Stale Handoff

Symptom: `project runtime validate` reports `ISO045` for a handoff.

Diagnosis:

```bash
isomer-cli --print-json project team-instances show <id> --topic my-topic
isomer-cli --print-json project runtime validate --topic my-topic
```

Recovery:

- Run `project handoffs observe` again if a fresh Houmao mail, gateway, file, or inspection signal exists.
- Normalize the handoff as accepted, rejected, blocked, superseded, repair-routed, or follow-up after Operator review.
- If the adapter payload is missing or corrupt, inspect `handoff-payloads/`, `handoff-observations/`, and `command-payloads/` under the adapter root, then rerun validation.

## Direct Houmao Reconciliation

Symptom: you launched agents directly with `houmao-mgr` and Isomer does not know about them.

Diagnosis:

- Ensure `adapter-link.json` and `launch-material-manifest.json` exist under the Topic Workspace adapter directory.
- Run `inspect-live --integrity` to compare material digests.

Recovery:

```bash
isomer-cli --print-json project team-instances reconcile <id> --topic my-topic --adapter houmao
isomer-cli --print-json project team-instances adopt <id> --topic my-topic --adapter houmao --yes
```

`adopt` records an explicit decision to associate externally launched state with the Agent Team Instance. It requires `--yes`.

## Topic Git Local Init Is Blocked

Symptom: local init reports that an ancestor repository tracks or does not effectively ignore the Source Topic Workspace.

Diagnosis:

```bash
isomer-cli --print-json project self location
isomer-cli --print-json project self check --scope topic --topic <topic>
```

Inspect the exact ancestor repository and Source Topic Workspace-relative paths reported by Topic Git. An ancestor Project repository does not enable local tracking.

Recovery:

- Update the ancestor repository in a separate user-controlled Project operation so the Source Topic Workspace is absent from its index and effectively ignored.
- Re-run Topic Git local status and init planning.
- Do not edit the ancestor `.gitignore` or remove ancestor index entries through Topic Git.

## Topic Publication Is Stale, Missing, or Blocked

Symptom: publication status reports `stale`, `copy-missing`, or `blocked`.

Diagnosis:

```bash
isomer-cli --print-json project context show --topic <topic>
isomer-cli --print-json project runtime inspect --topic <topic>
```

Recovery:

- For `stale`, create a new publication plan after inspecting changed source content, expected outputs, current copy content, component topology, binding identity, and fetched refs.
- For `copy-missing`, reconstruct from the runtime binding or resupply the credential-safe remote. An unpushed pre-runtime copy has no durable plan and must be prepared again.
- For privacy or destination conflicts, resolve the exact blocked disposition or unsafe path without changing source files.
- For incompatible remote refs, review a fresh branch-specific destructive plan. Any remote ref change invalidates previous force approval.
- For partial push, resume from the recorded branch outcome. Components push before `topic-workspace/main`, so the previous superproject remains authoritative until the final push succeeds.

Topic Git never repairs these states by pulling, merging, rebasing, resetting, cleaning, deleting remote branches, broad staging, or changing Source Topic Workspace Git state during publication.

## Diagnostic Checklist

When a command fails unexpectedly:

1. Run `isomer-cli --print-json project validate` to check the Project Manifest.
2. Run `isomer-cli --print-json doctor` to check host and Project Pixi state.
3. Run `isomer-cli --print-json project context show --topic <topic>` to inspect Effective Topic Context.
4. Run `isomer-cli --print-json project runtime validate --topic <topic>` to inspect Workspace Runtime.
5. For Houmao issues, verify `houmao-mgr` availability or set `ISOMER_HOUMAO_COMMAND`.
6. Inspect adapter payloads and manifests under `isomer-content/topic-ws/<topic>/runtime/adapters/houmao/<id>/` for fresh Projects, or under the registered Topic Workspace path for existing Projects.
7. Escalate repair to explicit Service Requests rather than hiding it inside read-only diagnostics.
