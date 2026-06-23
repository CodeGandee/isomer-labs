# isomer-cli Reference

`isomer-cli` is the command-line interface for Isomer Labs. It supports Project discovery, Project Manifest validation, Effective Topic Context resolution, Workspace Path Resolution previews, Workspace Runtime management, Domain Agent Team Template and Topic Agent Team Profile work, Agent Team Instance records, and Houmao-backed launch paths.

## Global Options

The following options are available on most commands:

- `--project TEXT` — explicit Project root selector.
- `--manifest TEXT` — explicit Project Manifest selector.
- `--print-json` — emit deterministic JSON for the selected command.
- `-h, --help` — show help for the command.

When `--project` is omitted, `isomer-cli` walks up from the current working directory until it finds a `.isomer-labs/` Project Config Directory.

Many topic-scoped commands also accept lifecycle selectors such as `--topic`, `--topic-workspace`, `--research-inquiry`, `--task`, `--run`, `--agent-team-instance`, and `--agent-instance`. These selectors refine the Effective Topic Context. They do not by themselves mutate state.

## Output Posture

JSON output uses the `isomer-cli-output.v1` wrapper and includes a `mutated` flag when the command mutates Project files, Workspace Runtime records, adapter manifests, or live Houmao state. Use root-level `--print-json` for every command that needs deterministic JSON. Without `--print-json`, commands print structured human-readable text. Command-local `--json`, `--format json`, and `--format=json` are not public command shapes.

## Command Groups

### `init`

Initialize the smallest valid Project configuration.

**Side effects:** writes `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/<topic>.toml`, and `topic-workspaces/<topic>/`. Does not create `state.sqlite`, Workspace Runtime subdirectories, Agent Workspaces, or adapter launch material.

**Prerequisites:** the target directory must not already be an Isomer-managed Project unless you intend to reinitialize.

```bash
pixi run isomer-cli init
pixi run isomer-cli init my-topic --topic-statement "Why is kernel A faster than kernel B?"
```

### `doctor`

Run read-only dependency, Project, and topic diagnostics.

**Side effects:** none. Checks host Pixi availability, Project-level Pixi configuration, optional `requires-pixi`, `pixi.lock` presence, and selected Research Topic environment bindings. Does not install Pixi environments, create lockfiles, create Topic Workspace runtime state, create Agent Workspaces, or edit Project config.

```bash
pixi run isomer-cli --print-json doctor
pixi run isomer-cli --print-json doctor --topic default
```

### `validate`

Validate the Project Manifest and registered configs.

**Side effects:** none.

```bash
pixi run isomer-cli --print-json validate
pixi run isomer-cli --print-json --project tests/fixtures/projects/deepsci-profile-use-cases validate
```

### `topics list`

List registered Research Topics.

**Side effects:** none.

```bash
pixi run isomer-cli topics list
pixi run isomer-cli --print-json topics list
```

### `workspaces list`

List registered Topic Workspaces.

**Side effects:** none.

```bash
pixi run isomer-cli workspaces list
pixi run isomer-cli --print-json workspaces list
```

### `context show`

Show resolved Effective Topic Context.

**Side effects:** none. The resolved context is process-local and is not stored as Workspace Runtime state.

```bash
pixi run isomer-cli --print-json context show --topic default
```

### `paths preview`

Preview workspace paths without creating them.

**Side effects:** none.

```bash
pixi run isomer-cli paths preview --topic default
pixi run isomer-cli --print-json paths preview --topic default
```

### `schemas list`

List Isomer built-in schemas and contracts.

**Side effects:** none.

```bash
pixi run isomer-cli schemas list
pixi run isomer-cli --print-json schemas list
```

### `runtime init`

Initialize or reopen the selected Workspace Runtime.

**Side effects:** creates or reopens `<topic-workspace>/state.sqlite`, stores schema metadata, records owner Research Topic and Topic Workspace refs, persists path plans for `state.sqlite`, `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`, and creates those default runtime directories. Reopening a current-schema runtime is idempotent. Unsupported older or newer schemas produce diagnostics and do not create directories or rewrite owner refs.

```bash
pixi run isomer-cli --print-json runtime init --topic default
```

### `runtime prepare`

Record selected topic environment readiness.

**Side effects:** writes or updates a `TopicEnvironmentReadinessRecord` in Workspace Runtime. Checks only explicit Project Manifest `topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings`. Does not install Pixi environments or perform hidden repair.

```bash
pixi run isomer-cli --print-json runtime prepare --topic default
pixi run isomer-cli --print-json runtime prepare --topic default --actor operator
```

### `runtime inspect`

Inspect Workspace Runtime metadata without mutation.

**Side effects:** none.

```bash
pixi run isomer-cli runtime inspect --topic default
pixi run isomer-cli --print-json runtime inspect --topic default
```

### `runtime validate`

Validate Workspace Runtime records without mutation.

**Side effects:** none. Reports metadata, record counts, readiness summaries, path-plan mismatches, broken refs, missing Agent Workspace directories, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, schema mismatches, and cross-topic leakage.

```bash
pixi run isomer-cli runtime validate --topic default
pixi run isomer-cli --print-json runtime validate --topic default --require-ready-readiness
```

### `team-instances create`

Create an Agent Team Instance record.

**Side effects:** writes Agent Team Instance record, Agent Instance records, Agent Workspace records, Agent Workspace path plans, initial Workflow Stage Cursor records, and provenance refs, and materializes Agent Workspace directories under `<topic-workspace>/agents/<agent-instance-id>/`. Does not launch Houmao agents, create mailboxes, write launch dossiers, or store adapter-specific launch refs.

**Prerequisites:** Workspace Runtime must be initialized, the Research Topic's single Topic Agent Team Profile Bundle must be materialized, and readiness should be `ready` for launch-facing work.

```bash
pixi run isomer-cli --print-json team-instances create \
  --topic default \
  --id ati-default-deepsci
```

### `team-instances list`

List Agent Team Instance records.

**Side effects:** none.

```bash
pixi run isomer-cli team-instances list --topic default
pixi run isomer-cli --print-json team-instances list --topic default
```

### `team-instances show`

Show one Agent Team Instance record.

**Side effects:** none.

```bash
pixi run isomer-cli --print-json team-instances show ati-default-deepsci --topic default
```

### `team-instances adapter-link export`

Write or print a Houmao adapter link JSON manifest.

**Side effects:** writes `adapter-link.json` under the Topic Workspace adapter directory unless `--print` is used. Does not launch agents.

```bash
pixi run isomer-cli --print-json team-instances adapter-link export ati-default-deepsci --topic default
pixi run isomer-cli --print-json team-instances adapter-link export ati-default-deepsci --topic default --print
```

### `team-instances launch-material prepare`

Prepare Houmao launch material without launching agents.

**Side effects:** writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, and records materialization state in Workspace Runtime. Does not launch, stop, message, or inspect Houmao managed agents.

```bash
pixi run isomer-cli --print-json team-instances launch-material prepare ati-default-deepsci \
  --topic default --adapter houmao
```

### `team-instances launch`

Quick-launch a Houmao-backed Agent Team Instance.

**Side effects:** runs preflight, writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, launches one Houmao managed agent per Isomer Agent Instance, writes `adapter-runtime-manifest.json`, and records command runs, payload refs, a launch attempt, and reconciliation state in Workspace Runtime. This is a live mutation of external Houmao state.

```bash
pixi run isomer-cli --print-json team-instances launch ati-default-deepsci \
  --topic default --adapter houmao
```

### `team-instances inspect-live`

Inspect Houmao adapter manifest integrity without mutation.

**Side effects:** none. Runs read-only Houmao CLI inspection and records a bounded adapter inspection snapshot in Workspace Runtime. The snapshot is a durable record of the observation; the underlying Houmao state is not modified.

```bash
pixi run isomer-cli --print-json team-instances inspect-live ati-default-deepsci \
  --topic default --adapter houmao --integrity
```

### `team-instances stop`

Stop a Houmao-backed Agent Team Instance.

**Side effects:** an explicit live mutation. Targets known mapped Houmao agent names from manifests or launch attempts and records a stopped, partial, failed, or stale outcome in Workspace Runtime.

```bash
pixi run isomer-cli --print-json team-instances stop ati-default-deepsci \
  --topic default --adapter houmao
```

### `team-instances reconcile`

Record Houmao adapter manifest reconciliation state.

**Side effects:** writes or updates `adapter-runtime-manifest.json` and records an `AdapterReconciliationRecord` in Workspace Runtime. Does not start, stop, or message Houmao-managed agents.

```bash
pixi run isomer-cli --print-json team-instances reconcile ati-default-deepsci \
  --topic default
```

### `team-instances adopt`

Adopt externally launched Houmao runtime state.

**Side effects:** records an explicit decision to associate externally launched Houmao runtime state with the selected Agent Team Instance. Requires `--yes` to confirm.

```bash
pixi run isomer-cli --print-json team-instances adopt ati-default-deepsci \
  --topic default --yes
```

### `handoffs dispatch`

Dispatch a manual handoff through the selected Execution Adapter.

**Side effects:** writes or reuses a Run lifecycle record, writes a Handoff record, links the handoff and Run to the Agent Team Instance, writes durable handoff payload files, invokes Houmao mail dispatch for the Houmao adapter, and records adapter command and payload refs. Requires ready Workspace Runtime and a launched, adopted, or linked adapter context.

```bash
pixi run isomer-cli --print-json handoffs dispatch \
  --topic default \
  --agent-team-instance ati-default-deepsci \
  --source-agent-instance ati-default-deepsci-deepsci-org-master \
  --target-agent-instance ati-default-deepsci-deepsci-org-experimenter \
  --run run-default-first-handoff \
  --message "Draft the first experiment execution plan." \
  --expected-output artifact:default:first-handoff
```

### `handoffs observe`

Record a non-authoritative Signal Observation for a handoff.

**Side effects:** writes a Signal Observation record, durable observation payload files, and any adapter command/payload refs needed to read mail or gateway output. Observation alone does not complete a Run, accept a handoff, promote returned claims into Evidence Items, or accept an Artifact.

```bash
pixi run isomer-cli --print-json handoffs observe <handoff-id> --topic default --source mail
pixi run isomer-cli --print-json handoffs observe <handoff-id> --topic default --source gateway
pixi run isomer-cli --print-json handoffs observe <handoff-id> --topic default --source file --payload-json handoff-observation.json
pixi run isomer-cli --print-json handoffs observe <handoff-id> --topic default --source inspection
```

### `handoffs normalize`

Record the Operator Agent decision for a handoff result.

**Side effects:** writes a handoff normalization record and payload ref, updates the Handoff record, records output Artifact lifecycle refs when supplied, and completes the linked Run only for `accepted`. Supported statuses are `accepted`, `rejected`, `blocked`, `superseded`, `repair_routed`, and `follow_up`.

```bash
pixi run isomer-cli --print-json handoffs normalize <handoff-id> \
  --topic default \
  --status accepted \
  --signal-observation <signal-observation-id> \
  --output-artifact artifact:default:first-handoff \
  --rationale "Accepted after Operator review."
```

### UC-01 Manual Harness

UC-01 is intentionally not a product CLI command. Run the pinned acceptance path from the manual harness so case-specific ids, fixture output specs, simulated handoff payloads, summaries, and closeout assertions stay outside `src/isomer_labs`.

```bash
pixi run python tests/manual/uc01_headless_vertical_slice
ISOMER_MANUAL_LIVE_HOUMAO=1 pixi run python tests/manual/uc01_headless_vertical_slice --live-houmao
```

### `team-templates list`

List registered Domain Agent Team Templates.

**Side effects:** none.

```bash
pixi run isomer-cli team-templates list
pixi run isomer-cli --print-json team-templates list
```

### `team-templates inspect`

Inspect a registered Domain Agent Team Template.

**Side effects:** none.

```bash
pixi run isomer-cli --print-json team-templates inspect deepsci-org
```

### `team-templates validate`

Validate a registered Domain Agent Team Template.

**Side effects:** none.

```bash
pixi run isomer-cli team-templates validate deepsci-org
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases team-templates validate fixture-method-team
```

### `team-profiles specialize`

Derive a candidate Topic Agent Team Profile for the selected Research Topic.

**Side effects:** by default, prints a design-time preview without writing files. Legacy preview-write behavior may write a single profile file, but authoritative topic-team materialization writes the Research Topic's one Topic Agent Team Profile Bundle under `team-profile/` in the owning Topic Workspace and keeps only the Project Manifest ref in Project Config. Does not launch Houmao agents, create an Agent Team Instance, or write Workspace Runtime state.

```bash
pixi run isomer-cli --print-json team-profiles specialize \
  --topic default --use-case UC-01
pixi run isomer-cli --print-json team-profiles specialize \
  --topic default --use-case UC-01 --write
```

### `team-profiles validate`

Validate a Topic Agent Team Profile file or a `profile.toml` file inside a Topic Agent Team Profile Bundle.

**Side effects:** none.

```bash
pixi run isomer-cli team-profiles validate topic-workspaces/default/team-profile/profile.toml
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases team-profiles validate topic-workspaces/novel-biomarker/team-profile/profile.toml
```

## Side-effect Summary

| Command | Mutates Project files | Mutates Workspace Runtime | Mutates adapter files | Mutates live Houmao state |
|---|---|---|---|---|
| `init` | yes | no | no | no |
| `doctor` | no | no | no | no |
| `validate` | no | no | no | no |
| `topics list` | no | no | no | no |
| `workspaces list` | no | no | no | no |
| `context show` | no | no | no | no |
| `paths preview` | no | no | no | no |
| `schemas list` | no | no | no | no |
| `runtime init` | yes (dirs, sqlite) | yes | no | no |
| `runtime prepare` | no | yes | no | no |
| `runtime inspect` | no | no | no | no |
| `runtime validate` | no | no | no | no |
| `team-instances create` | yes (dirs) | yes | no | no |
| `team-instances list` | no | no | no | no |
| `team-instances show` | no | no | no | no |
| `team-instances adapter-link export` | yes (manifest) | yes (ref) | yes | no |
| `team-instances launch-material prepare` | yes (material) | yes | yes | no |
| `team-instances launch` | yes (material, manifests) | yes | yes | yes |
| `team-instances inspect-live` | no | yes (snapshot) | no | no |
| `team-instances stop` | no | yes (outcome) | no | yes |
| `team-instances reconcile` | no | yes | yes (runtime manifest) | no |
| `team-instances adopt` | no | yes | no | no |
| `handoffs dispatch` | no | yes | yes (handoff payloads) | yes |
| `handoffs observe` | no | yes | yes (observation payloads) | mail/gateway only |
| `handoffs normalize` | no | yes | yes (normalization payloads) | no |
| `team-templates list` | no | no | no | no |
| `team-templates inspect` | no | no | no | no |
| `team-templates validate` | no | no | no | no |
| `team-profiles specialize` | only with `--write` | no | no | no |
| `team-profiles validate` | no | no | no | no |

## Environment Variables

- `ISOMER_HOUMAO_COMMAND` — override the `houmao-mgr` executable path used by the Houmao adapter.
- `ISOMER_HOUMAO_CHECKOUT` — override the local Houmao checkout path used when `houmao-mgr` is not on `PATH`.

If `houmao-mgr` is not on `PATH`, the adapter falls back to `extern/orphan/houmao`, then `ISOMER_HOUMAO_CHECKOUT`, then `~/workspace/code/houmao`.
