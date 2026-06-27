# isomer-cli Reference

`isomer-cli` is the command-line interface for Isomer Labs. It supports Project discovery, Project Manifest validation, Effective Topic Context resolution, Workspace Path Resolution previews, Workspace Runtime management, Domain Agent Team Template and Topic Agent Team Profile work, Agent Team Instance records, and Houmao-backed launch paths.

## Root and Project Options

The root command exposes:

- `--print-json` — emit deterministic JSON for the selected command.
- `-h, --help` — show help for the command.

The `project` command group exposes:

- `--root TEXT` — explicit Project root selector.
- `--manifest TEXT` — explicit Project Manifest selector.

When `project --root` is omitted, `isomer-cli` walks up from the current working directory until it finds a `.isomer-labs/` Project Config Directory.

Many topic-scoped commands also accept lifecycle selectors such as `--topic`, `--topic-workspace`, `--research-inquiry`, `--task`, `--run`, `--agent-team-instance`, and `--agent-instance`. These selectors refine the Effective Topic Context. They do not by themselves mutate state.

## Output Posture

JSON output uses the `isomer-cli-output.v1` wrapper and includes a `mutated` flag when the command mutates Project files, Workspace Runtime records, adapter manifests, or live Houmao state. Use root-level `--print-json` for every command that needs deterministic JSON. Without `--print-json`, commands print structured human-readable text. Command-local `--json`, `--format json`, and `--format=json` are not public command shapes.

## Command Groups

### `project init`

Initialize the smallest valid Project configuration and Project-level Houmao overlay.

**Side effects:** runs the supported Houmao Project bootstrap boundary for the selected Project root and writes `.isomer-labs/manifest.toml`, the Isomer-managed Houmao overlay under `.isomer-labs/.houmao/`, and the selected content root's `README.md` and `.gitignore`. The fresh manifest contains path defaults but no Research Topic defaults, Research Topic registrations, or Topic Workspace registrations. The generated `.gitignore` ignores generated content by default while keeping `README.md` and `.gitignore` trackable. Does not create a Research Topic Config, Topic Workspace directory, `state.sqlite`, Workspace Runtime subdirectories, Agent Workspaces, adapter launch material, mailboxes, gateways, managed agents, sessions, or launch dossiers.

**Prerequisites:** the target directory must not already be an Isomer-managed Project unless you intend to reinitialize. Houmao command resolution must succeed through `houmao-mgr`, `ISOMER_HOUMAO_COMMAND`, or a supported local checkout.

**Options:** pass `--content-dir <content-dir>` to select a project-local generated content root during fresh initialization.

```bash
pixi run isomer-cli project init
pixi run isomer-cli project init --content-dir custom-content
```

`--content-dir <content-dir>` must resolve inside the Project root and must not live inside `.isomer-labs/` or collide with root `.houmao/`. When omitted, init uses `isomer-content/`. Create Research Topics with `project topics create`, not `project init`.

### `project content-root move`

Plan or apply relocation of the Project generated content root.

**Side effects:** without `--yes`, none. `--dry-run` always builds the relocation plan without moving files or rewriting the Project Manifest, and omitting both `--dry-run` and `--yes` defaults to dry-run mode. With `--yes`, moves only Isomer-managed content-root policy files and registered Topic Workspace directories that are safe to move, updates Project Manifest path defaults and Topic Workspace paths, preserves unmanaged leftovers, and reports skipped or blocked entries. It does not rewrite runtime-internal paths inside moved Topic Workspaces.

**Options:** `--to <content-dir>` selects the new project-local generated content root. The destination must resolve inside the Project root, must not live inside `.isomer-labs/`, and must not collide with protected Project or Houmao paths.

```bash
pixi run isomer-cli project content-root move --to generated --dry-run
pixi run isomer-cli --print-json project content-root move --to generated --dry-run
pixi run isomer-cli --print-json project content-root move --to generated --yes
```

### `project cleanup`

Plan or apply cleanup of selected Isomer-managed Project material.

**Side effects:** without `--yes`, none. `--dry-run` always builds the same deterministic plan without deleting files, and omitting both `--dry-run` and `--yes` defaults to dry-run mode. With `--yes`, deletes only targets listed in the validated plan. `project cleanup` does not stop live Houmao agents, inspect gateways, infer unregistered Research Topics from directories, or remove the whole generated content root unless `--part content-root --purge-content-root --yes` is selected.

**Parts:** `project-config` removes `.isomer-labs/`; `houmao-overlay` removes the Isomer-managed `.isomer-labs/.houmao/` overlay; `content-policy` removes the selected content root's generated `README.md` and `.gitignore`; `topic-workspace` removes selected registered Topic Workspace directories; `runtime` removes `state.sqlite`, runtime-owned directories, and adapter runtime material under selected Topic Workspaces; `bootstrap` combines Project config, Houmao overlay, content policy files, and registered Topic Workspace directories; `content-root` removes the selected generated content root only with `--purge-content-root`.

```bash
pixi run isomer-cli project cleanup --part bootstrap --dry-run
pixi run isomer-cli project cleanup --part bootstrap --yes
pixi run isomer-cli --print-json project cleanup --part runtime --topic my-topic --dry-run
pixi run isomer-cli project cleanup --part content-root --purge-content-root --yes
```

When a valid Project Manifest exists, cleanup uses it as authority for path defaults, Research Topic registrations, and Topic Workspace registrations. If the manifest is missing or malformed, cleanup is limited to `.isomer-labs/`, `.isomer-labs/.houmao/`, root `.houmao/` as external state, and the built-in or explicitly selected content root policy files; it will not infer Research Topics from filesystem directories.

### `project doctor`

Run read-only dependency, Project, and topic diagnostics.

**Side effects:** none. Checks host Pixi availability, Project-level Pixi configuration, optional `requires-pixi`, `pixi.lock` presence, Project-root topic Pixi bindings, and Topic Workspace Pixi binding targets. If no explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` target exists, it checks the registered Topic Workspace directory as the implicit default target with Pixi environment `default`. Does not install Pixi environments, create lockfiles, create Topic Workspace runtime state, create Agent Workspaces, or edit Project config.

```bash
pixi run isomer-cli --print-json project doctor
pixi run isomer-cli --print-json project doctor --topic my-topic
```

### `project validate`

Validate the Project Manifest and registered configs.

**Side effects:** none.

```bash
pixi run isomer-cli --print-json project validate
pixi run isomer-cli --print-json project --root tests/fixtures/projects/deepsci-profile-use-cases validate
```

### `project topics list`

List registered Research Topics.

**Side effects:** none.

```bash
pixi run isomer-cli project topics list
pixi run isomer-cli --print-json project topics list
```

### `project topics create`

Create and register a Research Topic and its Topic Workspace.

**Side effects:** writes `.isomer-labs/research-topics/<topic-id>.toml`, updates `.isomer-labs/manifest.toml` with `[[research_topics]]` and `[[topic_workspaces]]`, and creates the Topic Workspace directory. It does not create Workspace Runtime state or live Houmao state.

```bash
pixi run isomer-cli project topics create my-topic --statement "Investigate the concrete research question."
pixi run isomer-cli project topics create my-topic --statement "Investigate the concrete research question." --workspace-dir topic-workspaces/my-topic --set-default
```

### `project topics show`

Show one registered Research Topic, its config, associated Topic Workspace registration, effective workspace path, status, and diagnostics.

**Side effects:** none.

```bash
pixi run isomer-cli --print-json project topics show my-topic
```

### `project topics update`

Update bounded Research Topic metadata. Supported updates are `--statement`, `--status active|archived`, and `--set-default`; topic rename is not supported by this command.

**Side effects:** updates `.isomer-labs/manifest.toml` for status/default changes and the Research Topic Config for statement changes. It preserves existing workspace contents.

```bash
pixi run isomer-cli project topics update my-topic --statement "Investigate the revised concrete research question."
pixi run isomer-cli project topics update my-topic --status archived
pixi run isomer-cli project topics update my-topic --set-default
```

### `project topics delete`

Plan or apply Research Topic deletion.

**Side effects:** `--dry-run` mutates nothing. `--yes` removes the Research Topic registration, associated Topic Workspace registration, matching Project Manifest defaults, and Research Topic Config file when no blockers remain. It preserves the Topic Workspace directory and reports cleanup guidance for filesystem removal.

```bash
pixi run isomer-cli --print-json project topics delete my-topic --dry-run
pixi run isomer-cli --print-json project topics delete my-topic --yes
```

### `project workspaces list`

List registered Topic Workspaces.

**Side effects:** none.

```bash
pixi run isomer-cli project workspaces list
pixi run isomer-cli --print-json project workspaces list
```

### `project context show`

Show resolved Effective Topic Context.

**Side effects:** none. The resolved context is process-local and is not stored as Workspace Runtime state.

```bash
pixi run isomer-cli --print-json project context show --topic my-topic
```

### `project paths preview`

Preview workspace paths, including the generated content root, without creating them.

**Side effects:** none.

```bash
pixi run isomer-cli project paths preview --topic my-topic
pixi run isomer-cli --print-json project paths preview --topic my-topic
```

### `schemas list`

List Isomer built-in schemas and contracts.

**Side effects:** none.

```bash
pixi run isomer-cli schemas list
pixi run isomer-cli --print-json schemas list
```

### `project runtime init`

Initialize or reopen the selected Workspace Runtime.

**Side effects:** creates or reopens `<topic-workspace>/state.sqlite`, stores schema metadata, records owner Research Topic and Topic Workspace refs, persists path plans for `state.sqlite`, `repos/`, `repos/topic-main/`, `agents/`, `records/`, `records/artifacts/`, `records/tasks/`, `records/runs/`, `records/views/`, `records/logs/`, and `runtime/`, and creates those default runtime directories. Reopening a current-schema runtime is idempotent. Unsupported older or newer schemas produce diagnostics and do not create directories or rewrite owner refs.

```bash
pixi run isomer-cli --print-json project runtime init --topic my-topic
```

### `project runtime prepare`

Record selected topic environment readiness.

**Side effects:** writes or updates a `TopicEnvironmentReadinessRecord` in Workspace Runtime. Checks explicit Project Manifest `topic_pixi_environment_bindings`, explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` targets, or the implicit registered Topic Workspace directory default when no explicit standalone target exists. Pixi must be installed and on `PATH`; online installation can use `curl -fsSL https://pixi.sh/install.sh | sh`, while offline hosts should receive a pre-downloaded `pixi` executable on `PATH`. Does not install Pixi environments or perform hidden repair.

```bash
pixi run isomer-cli --print-json project runtime prepare --topic my-topic
pixi run isomer-cli --print-json project runtime prepare --topic my-topic --actor operator
```

### `project runtime inspect`

Inspect Workspace Runtime metadata without mutation.

**Side effects:** none.

```bash
pixi run isomer-cli project runtime inspect --topic my-topic
pixi run isomer-cli --print-json project runtime inspect --topic my-topic
```

### `project runtime validate`

Validate Workspace Runtime records without mutation.

**Side effects:** none. Reports metadata, record counts, readiness summaries, path-plan mismatches, broken refs, missing Agent Workspace directories, stale handoffs, unresolved Gates, unsupported Research Claims, stale Provenance Records, schema mismatches, and cross-topic leakage.

```bash
pixi run isomer-cli project runtime validate --topic my-topic
pixi run isomer-cli --print-json project runtime validate --topic my-topic --require-ready-readiness
```

### `project team-instances create`

Create an Agent Team Instance record.

**Side effects:** writes Agent Team Instance record, Agent Instance records, Agent Workspace records, Agent Workspace path plans, initial Workflow Stage Cursor records, and provenance refs, and materializes Agent Workspace directories under `<topic-workspace>/agents/<agent-name>/`. Each Agent Workspace is expected to be the agent's launch cwd and, for Git-backed topics, a worktree of `repos/topic-main` on an agent-owned branch. Does not launch Houmao agents, create mailboxes, write launch dossiers, or store adapter-specific launch refs.

**Prerequisites:** Workspace Runtime must be initialized, the Research Topic's single Topic Agent Team Profile Bundle must be materialized, and readiness should be `ready` for launch-facing work.

```bash
pixi run isomer-cli --print-json project team-instances create \
  --topic my-topic \
  --id ati-my-topic-deepsci
```

### `project team-instances list`

List Agent Team Instance records.

**Side effects:** none.

```bash
pixi run isomer-cli project team-instances list --topic my-topic
pixi run isomer-cli --print-json project team-instances list --topic my-topic
```

### `project team-instances show`

Show one Agent Team Instance record.

**Side effects:** none.

```bash
pixi run isomer-cli --print-json project team-instances show ati-my-topic-deepsci --topic my-topic
```

### `project team-instances adapter-link export`

Write or print a Houmao adapter link JSON manifest.

**Side effects:** writes `adapter-link.json` under the Topic Workspace adapter directory unless `--print` is used. Does not launch agents.

```bash
pixi run isomer-cli --print-json project team-instances adapter-link export ati-my-topic-deepsci --topic my-topic
pixi run isomer-cli --print-json project team-instances adapter-link export ati-my-topic-deepsci --topic my-topic --print
```

### `project team-instances launch-material prepare`

Prepare Houmao launch material without launching agents.

**Side effects:** writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, and records materialization state in Workspace Runtime. Does not launch, stop, message, or inspect Houmao managed agents.

```bash
pixi run isomer-cli --print-json project team-instances launch-material prepare ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

### `project team-instances launch`

Quick-launch a Houmao-backed Agent Team Instance.

**Side effects:** runs preflight, writes shared launch material, creates or updates `adapter-link.json` and `launch-material-manifest.json`, launches one Houmao managed agent per Isomer Agent Instance, writes `adapter-runtime-manifest.json`, and records command runs, payload refs, a launch attempt, and reconciliation state in Workspace Runtime. This is a live mutation of external Houmao state.

```bash
pixi run isomer-cli --print-json project team-instances launch ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

### `project team-instances inspect-live`

Inspect Houmao adapter manifest integrity without mutation.

**Side effects:** none. Runs read-only Houmao CLI inspection and records a bounded adapter inspection snapshot in Workspace Runtime. The snapshot is a durable record of the observation; the underlying Houmao state is not modified.

```bash
pixi run isomer-cli --print-json project team-instances inspect-live ati-my-topic-deepsci \
  --topic my-topic --adapter houmao --integrity
```

### `project team-instances stop`

Stop a Houmao-backed Agent Team Instance.

**Side effects:** an explicit live mutation. Targets known mapped Houmao agent names from manifests or launch attempts and records a stopped, partial, failed, or stale outcome in Workspace Runtime.

```bash
pixi run isomer-cli --print-json project team-instances stop ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

### `project team-instances reconcile`

Record Houmao adapter manifest reconciliation state.

**Side effects:** writes or updates `adapter-runtime-manifest.json` and records an `AdapterReconciliationRecord` in Workspace Runtime. Does not start, stop, or message Houmao-managed agents.

```bash
pixi run isomer-cli --print-json project team-instances reconcile ati-my-topic-deepsci \
  --topic my-topic
```

### `project team-instances adopt`

Adopt externally launched Houmao runtime state.

**Side effects:** records an explicit decision to associate externally launched Houmao runtime state with the selected Agent Team Instance. Requires `--yes` to confirm.

```bash
pixi run isomer-cli --print-json project team-instances adopt ati-my-topic-deepsci \
  --topic my-topic --yes
```

### `project handoffs dispatch`

Dispatch a manual handoff through the selected Execution Adapter.

**Side effects:** writes or reuses a Run lifecycle record, writes a Handoff record, links the handoff and Run to the Agent Team Instance, writes durable handoff payload files, invokes Houmao mail dispatch for the Houmao adapter, and records adapter command and payload refs. Requires ready Workspace Runtime and a launched, adopted, or linked adapter context.

```bash
pixi run isomer-cli --print-json project handoffs dispatch \
  --topic my-topic \
  --agent-team-instance ati-my-topic-deepsci \
  --source-agent-instance ati-my-topic-deepsci-deepsci-org-master \
  --target-agent-instance ati-my-topic-deepsci-deepsci-org-experimenter \
  --run run-default-first-handoff \
  --message "Draft the first experiment execution plan." \
  --expected-output artifact:default:first-handoff
```

### `project handoffs observe`

Record a non-authoritative Signal Observation for a handoff.

**Side effects:** writes a Signal Observation record, durable observation payload files, and any adapter command/payload refs needed to read mail or gateway output. Observation alone does not complete a Run, accept a handoff, promote returned claims into Evidence Items, or accept an Artifact.

```bash
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source mail
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source gateway
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source file --payload-json handoff-observation.json
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source inspection
```

### `project handoffs normalize`

Record the Operator Agent decision for a handoff result.

**Side effects:** writes a handoff normalization record and payload ref, updates the Handoff record, records output Artifact lifecycle refs when supplied, and completes the linked Run only for `accepted`. Supported statuses are `accepted`, `rejected`, `blocked`, `superseded`, `repair_routed`, and `follow_up`.

```bash
pixi run isomer-cli --print-json project handoffs normalize <handoff-id> \
  --topic my-topic \
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

### `project team-templates list`

List registered Domain Agent Team Templates.

**Side effects:** none.

```bash
pixi run isomer-cli project team-templates list
pixi run isomer-cli --print-json project team-templates list
```

### `project team-templates inspect`

Inspect a registered Domain Agent Team Template.

**Side effects:** none. The output includes template roles, Workflow Stage ownership, placeholder catalog entries, instantiation schema paths, and copyable material declarations such as `execplan/` for templates that support Topic Team Specialization.

```bash
pixi run isomer-cli --print-json project team-templates inspect deepsci-org
```

### `project team-templates validate`

Validate a registered Domain Agent Team Template.

**Side effects:** none.

```bash
pixi run isomer-cli project team-templates validate deepsci-org
pixi run isomer-cli project --root tests/fixtures/projects/deepsci-profile-use-cases team-templates validate fixture-method-team
```

### `project team-profiles specialize`

Preview Topic Team Specialization for the selected Research Topic by deriving a candidate Topic Agent Team Profile.

**Side effects:** by default, prints preview or candidate material without writing files. `--profile-id` is preview-only and is not accepted by the packet-backed authoritative materialization path. Legacy preview-write behavior may write a single profile file, but authoritative Topic Team Specialization writes the Research Topic's one Topic Agent Team Profile Bundle under `team-profile/` in the owning Topic Workspace and keeps only the Project Manifest ref in Project Config. Does not launch Houmao agents, create an Agent Team Instance, or write Workspace Runtime state.

```bash
pixi run isomer-cli --print-json project team-profiles specialize \
  --topic my-topic --use-case UC-01
pixi run isomer-cli --print-json project team-profiles specialize \
  --topic my-topic --use-case UC-01 --write
```

### `project team-profiles materialize`

Materialize an approved packet-backed Topic Agent Team Profile Bundle for the selected Research Topic.

**Side effects:** without `--write`, previews validation and planned bundle paths. With `--write`, writes `<topic-workspace>/team-profile/profile.toml`, `instantiation-packet.toml`, `approval.toml`, validation output, provenance files, and copied topic-edited template material. It does not mutate Workspace Runtime, launch Houmao agents, or create an Agent Team Instance.

```bash
pixi run isomer-cli --print-json project team-profiles materialize \
  --topic flash-attention-gb10-peak-performance-optimization \
  --packet fixtures/uc01/topic-team-instantiation-packet.toml
pixi run isomer-cli --print-json project team-profiles materialize \
  --topic flash-attention-gb10-peak-performance-optimization \
  --packet fixtures/uc01/topic-team-instantiation-packet.toml --write
```

### `project team-profiles validate`

Validate a Topic Agent Team Profile file or a `profile.toml` file inside a Topic Agent Team Profile Bundle.

**Side effects:** none.

```bash
pixi run isomer-cli project team-profiles validate isomer-content/topic-ws/my-topic/team-profile/profile.toml
pixi run isomer-cli project --root tests/fixtures/projects/deepsci-profile-use-cases team-profiles validate topic-workspaces/novel-biomarker/team-profile/profile.toml
```

## Side-effect Summary

| Command | Mutates Project files | Mutates Workspace Runtime | Mutates adapter files | Mutates live Houmao state |
|---|---|---|---|---|
| `project init` | yes (`.isomer-labs/`, `.isomer-labs/.houmao/`, content root policy files) | no | no | no |
| `project doctor` | no | no | no | no |
| `project validate` | no | no | no | no |
| `project topics list` | no | no | no | no |
| `project topics create` | yes (topic config, manifest, workspace dir) | no | no | no |
| `project topics show` | no | no | no | no |
| `project topics update` | yes (manifest or topic config) | no | no | no |
| `project topics delete` | yes with `--yes`; `--dry-run` is read-only | no | no | no |
| `project workspaces list` | no | no | no | no |
| `project context show` | no | no | no | no |
| `project paths preview` | no | no | no | no |
| `schemas list` | no | no | no | no |
| `project runtime init` | yes (dirs, sqlite) | yes | no | no |
| `project runtime prepare` | no | yes | no | no |
| `project runtime inspect` | no | no | no | no |
| `project runtime validate` | no | no | no | no |
| `project team-instances create` | yes (dirs) | yes | no | no |
| `project team-instances list` | no | no | no | no |
| `project team-instances show` | no | no | no | no |
| `project team-instances adapter-link export` | yes (manifest) | yes (ref) | yes | no |
| `project team-instances launch-material prepare` | yes (material) | yes | yes | no |
| `project team-instances launch` | yes (material, manifests) | yes | yes | yes |
| `project team-instances inspect-live` | no | yes (snapshot) | no | no |
| `project team-instances stop` | no | yes (outcome) | no | yes |
| `project team-instances reconcile` | no | yes | yes (runtime manifest) | no |
| `project team-instances adopt` | no | yes | no | no |
| `project handoffs dispatch` | no | yes | yes (handoff payloads) | yes |
| `project handoffs observe` | no | yes | yes (observation payloads) | mail/gateway only |
| `project handoffs normalize` | no | yes | yes (normalization payloads) | no |
| `project team-templates list` | no | no | no | no |
| `project team-templates inspect` | no | no | no | no |
| `project team-templates validate` | no | no | no | no |
| `project team-profiles specialize` | only with `--write` | no | no | no |
| `project team-profiles materialize` | yes with `--write` | no | no | no |
| `project team-profiles validate` | no | no | no | no |

## Environment Variables

- `ISOMER_HOUMAO_COMMAND` — override the `houmao-mgr` executable path used by the Houmao adapter.
- `ISOMER_HOUMAO_CHECKOUT` — override the local Houmao checkout path used when `houmao-mgr` is not on `PATH`.

If `houmao-mgr` is not on `PATH`, the adapter falls back to `extern/orphan/houmao`, then `ISOMER_HOUMAO_CHECKOUT`, then `~/workspace/code/houmao`.
