# isomer-cli Reference

`isomer-cli` is the command-line interface for Isomer Labs. It supports Project discovery, Project Manifest validation, Effective Topic Context resolution, Workspace Path Resolution previews, Workspace Runtime management, Domain Agent Team Template and Topic Agent Team Profile work, Agent Team Instance records, and Houmao-backed launch paths.

## Global Options

The following options are available on most commands:

- `--project TEXT` — explicit Project root selector.
- `--manifest TEXT` — explicit Project Manifest selector.
- `--format [text|json]` — output format.
- `--json` — emit JSON; shorthand for `--format json`.
- `-h, --help` — show help for the command.

When `--project` is omitted, `isomer-cli` walks up from the current working directory until it finds a `.isomer-labs/` Project Config Directory.

Many topic-scoped commands also accept lifecycle selectors such as `--topic`, `--topic-workspace`, `--research-inquiry`, `--task`, `--run`, `--agent-team-instance`, `--agent-instance`, and `--topic-agent-team-profile`. These selectors refine the Effective Topic Context. They do not by themselves mutate state.

## Output Posture

JSON output uses the `isomer-cli-output.v1` wrapper and includes a `mutated` flag when the command mutates Project files, Workspace Runtime records, adapter manifests, or live Houmao state. Read-only commands report `mutated: false`. Text output is intended for human inspection and may omit nested details that JSON includes.

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
pixi run isomer-cli doctor --json
pixi run isomer-cli doctor --topic default --json
```

### `validate`

Validate the Project Manifest and registered configs.

**Side effects:** none.

```bash
pixi run isomer-cli validate --json
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases validate --json
```

### `topics list`

List registered Research Topics.

**Side effects:** none.

```bash
pixi run isomer-cli topics list
pixi run isomer-cli topics list --json
```

### `workspaces list`

List registered Topic Workspaces.

**Side effects:** none.

```bash
pixi run isomer-cli workspaces list
pixi run isomer-cli workspaces list --json
```

### `context show`

Show resolved Effective Topic Context.

**Side effects:** none. The resolved context is process-local and is not stored as Workspace Runtime state.

```bash
pixi run isomer-cli context show --topic default --json
```

### `paths preview`

Preview workspace paths without creating them.

**Side effects:** none.

```bash
pixi run isomer-cli paths preview --topic default
pixi run isomer-cli paths preview --topic default --json
```

### `schemas list`

List Isomer built-in schemas and contracts.

**Side effects:** none.

```bash
pixi run isomer-cli schemas list
pixi run isomer-cli schemas list --json
```

### `runtime init`

Initialize or reopen the selected Workspace Runtime.

**Side effects:** creates or reopens `<topic-workspace>/state.sqlite`, stores schema metadata, records owner Research Topic and Topic Workspace refs, persists path plans for `state.sqlite`, `artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, and `logs/`, and creates those default runtime directories. Reopening a current-schema runtime is idempotent. Unsupported older or newer schemas produce diagnostics and do not create directories or rewrite owner refs.

```bash
pixi run isomer-cli runtime init --topic default --json
```

### `runtime prepare`

Record selected topic environment readiness.

**Side effects:** writes or updates a `TopicEnvironmentReadinessRecord` in Workspace Runtime. Checks only explicit Project Manifest `topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings`. Does not install Pixi environments or perform hidden repair.

```bash
pixi run isomer-cli runtime prepare --topic default --json
pixi run isomer-cli runtime prepare --topic default --actor operator --json
```

### `runtime inspect`

Inspect Workspace Runtime metadata without mutation.

**Side effects:** none.

```bash
pixi run isomer-cli runtime inspect --topic default
pixi run isomer-cli runtime inspect --topic default --json
```

### `runtime validate`

Validate Workspace Runtime records without mutation.

**Side effects:** none. Reports metadata, record counts, readiness summaries, path-plan mismatches, broken refs, missing Agent Workspace directories, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, schema mismatches, and cross-topic leakage.

```bash
pixi run isomer-cli runtime validate --topic default
pixi run isomer-cli runtime validate --topic default --require-ready-readiness --json
```

### `team-instances create`

Create an Agent Team Instance record.

**Side effects:** writes Agent Team Instance record, Agent Instance records, Agent Workspace records, Agent Workspace path plans, initial Workflow Stage Cursor records, and provenance refs, and materializes Agent Workspace directories under `<topic-workspace>/agents/<agent-instance-id>/`. Does not launch Houmao agents, create mailboxes, write launch dossiers, or store adapter-specific launch refs.

**Prerequisites:** Workspace Runtime must be initialized and readiness should be `ready` for launch-facing work.

```bash
pixi run isomer-cli team-instances create \
  --topic default \
  --topic-agent-team-profile default-deepsci \
  --id ati-default-deepsci \
  --json
```

### `team-instances list`

List Agent Team Instance records.

**Side effects:** none.

```bash
pixi run isomer-cli team-instances list --topic default
pixi run isomer-cli team-instances list --topic default --json
```

### `team-instances show`

Show one Agent Team Instance record.

**Side effects:** none.

```bash
pixi run isomer-cli team-instances show ati-default-deepsci --topic default --json
```

### `team-instances adapter-link export`

Write or print a Houmao adapter link JSON manifest.

**Side effects:** writes `adapter-link.json` under the Topic Workspace adapter directory unless `--print` is used. Does not launch agents.

```bash
pixi run isomer-cli team-instances adapter-link export ati-default-deepsci --topic default --json
pixi run isomer-cli team-instances adapter-link export ati-default-deepsci --topic default --print --json
```

### `team-instances launch-material prepare`

Prepare Houmao launch material without launching agents.

**Side effects:** writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, and records materialization state in Workspace Runtime. Does not launch, stop, message, or inspect Houmao managed agents.

```bash
pixi run isomer-cli team-instances launch-material prepare ati-default-deepsci \
  --topic default --adapter houmao --json
```

### `team-instances launch`

Quick-launch a Houmao-backed Agent Team Instance.

**Side effects:** runs preflight, writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, launches one Houmao managed agent per Isomer Agent Instance, writes `adapter-runtime-manifest.json`, and records command runs, payload refs, a launch attempt, and reconciliation state in Workspace Runtime. This is a live mutation of external Houmao state.

```bash
pixi run isomer-cli team-instances launch ati-default-deepsci \
  --topic default --adapter houmao --json
```

### `team-instances inspect-live`

Inspect Houmao adapter manifest integrity without mutation.

**Side effects:** none. Runs read-only Houmao CLI inspection and records a bounded adapter inspection snapshot in Workspace Runtime. The snapshot is a durable record of the observation; the underlying Houmao state is not modified.

```bash
pixi run isomer-cli team-instances inspect-live ati-default-deepsci \
  --topic default --adapter houmao --integrity --json
```

### `team-instances stop`

Stop a Houmao-backed Agent Team Instance.

**Side effects:** an explicit live mutation. Targets known mapped Houmao agent names from manifests or launch attempts and records a stopped, partial, failed, or stale outcome in Workspace Runtime.

```bash
pixi run isomer-cli team-instances stop ati-default-deepsci \
  --topic default --adapter houmao --json
```

### `team-instances reconcile`

Record Houmao adapter manifest reconciliation state.

**Side effects:** writes or updates `adapter-runtime-manifest.json` and records an `AdapterReconciliationRecord` in Workspace Runtime. Does not start, stop, or message Houmao-managed agents.

```bash
pixi run isomer-cli team-instances reconcile ati-default-deepsci \
  --topic default --json
```

### `team-instances adopt`

Adopt externally launched Houmao runtime state.

**Side effects:** records an explicit decision to associate externally launched Houmao runtime state with the selected Agent Team Instance. Requires `--yes` to confirm.

```bash
pixi run isomer-cli team-instances adopt ati-default-deepsci \
  --topic default --yes --json
```

### `team-templates list`

List registered Domain Agent Team Templates.

**Side effects:** none.

```bash
pixi run isomer-cli team-templates list
pixi run isomer-cli team-templates list --json
```

### `team-templates inspect`

Inspect a registered Domain Agent Team Template.

**Side effects:** none.

```bash
pixi run isomer-cli team-templates inspect deepsci-org --json
```

### `team-templates validate`

Validate a registered Domain Agent Team Template.

**Side effects:** none.

```bash
pixi run isomer-cli team-templates validate deepsci-org
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases team-templates validate fixture-method-team
```

### `team-profiles specialize`

Derive a candidate Topic Agent Team Profile.

**Side effects:** by default, prints a design-time preview without writing files. When `--write` is requested, writes only the profile TOML file to the Project Config Directory and reports a deterministic `registration_suggestion` object for adding the profile to the Project Manifest. Does not launch Houmao agents, create an Agent Team Instance, or write Workspace Runtime state.

```bash
pixi run isomer-cli team-profiles specialize \
  --topic default --profile-id default-deepsci --use-case UC-01 --json
pixi run isomer-cli team-profiles specialize \
  --topic default --profile-id default-deepsci --use-case UC-01 --write --json
```

### `team-profiles validate`

Validate a Topic Agent Team Profile file.

**Side effects:** none.

```bash
pixi run isomer-cli team-profiles validate .isomer-labs/team-profiles/default-deepsci.toml
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases team-profiles validate .isomer-labs/team-profiles/uc-01-novel-biomarker.toml
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
| `team-templates list` | no | no | no | no |
| `team-templates inspect` | no | no | no | no |
| `team-templates validate` | no | no | no | no |
| `team-profiles specialize` | only with `--write` | no | no | no |
| `team-profiles validate` | no | no | no | no |

## Environment Variables

- `ISOMER_HOUMAO_COMMAND` — override the `houmao-mgr` executable path used by the Houmao adapter.
- `ISOMER_HOUMAO_CHECKOUT` — override the local Houmao checkout path used when `houmao-mgr` is not on `PATH`.

If `houmao-mgr` is not on `PATH`, the adapter falls back to `extern/orphan/houmao`, then `ISOMER_HOUMAO_CHECKOUT`, then `~/workspace/code/houmao`.
