## Context

The accepted manifested workspace design uses `.isomer-labs/manifest.toml` as the Project Manifest and discovery authority. Each Topic Workspace is scoped to one Research Topic and owns the Workspace Runtime, Research Inquiry graph, Research Tasks, Runs, Artifacts, View Manifests, Agent Workspaces, and logs for that topic. Workspace Path Resolution already defines how ordinary Project, Topic Workspace, Workspace Runtime, Run, Artifact, log, View Manifest, and Agent Workspace paths are resolved.

`isomer-cli` is intended to be a system-level utility, not a project-local script. That means it needs a deterministic way to behave differently per Project and per Research Topic. The missing layer is a topic-context contract: when the user runs a topic-scoped CLI command, the CLI must know which Research Topic, Topic Workspace, Topic Agent Team Profile defaults, Capability Binding refs, Gate policy refs, and Execution Adapter defaults apply before it resolves paths or asks an Execution Adapter to run anything.

The current research-paradigm skill gap plan still has open placeholders for command execution, scheduler policy, cost/privacy Gate policy, Skill Binding, baseline waiver policy, and literature providers. This change intentionally does not settle those surfaces. It defines the context object those future contracts can consume.

## Goals / Non-Goals

**Goals:**

- Define Project discovery and Research Topic selection for topic-scoped `isomer-cli` commands.
- Define Research Topic Config TOML as a Project Manifest-registered configuration file for topic-specific defaults and refs.
- Define Effective Topic Context as the resolved, process-local context that `isomer-cli`, Workspace Path Resolution, Run initialization, and future Execution Adapter command requests consume.
- Allow Research Topic Config to select topic-specific Artifact Format Profiles and Artifact Extensions for expected outputs.
- Preserve a generic, minimal Artifact Core Record so custom artifact formats do not fragment the durable Artifact graph.
- Define resolution precedence for topic selection and context values.
- Define validation and durability rules so topic context can be inspected and recovered without treating environment variables as durable truth.
- Keep the domain language aligned with Research Topic, Research Inquiry, Research Task, Run, Topic Workspace, Workspace Runtime, Topic Agent Team Profile, Agent Team Instance, Capability Binding, Gate, and Execution Adapter.

**Non-Goals:**

- Do not implement `isomer-cli` commands or a shell runner.
- Do not define the Execution Adapter command request or command result schema beyond naming the Effective Topic Context input.
- Do not define scheduler retry, queueing, continuation, resource allocation, or long-running job control.
- Do not define Skill Binding, credential binding, literature provider, baseline-waiver, cost/privacy Gate threshold, or package-manager schemas.
- Do not make Research Topic Config a replacement for Workspace Runtime, Run records, Artifacts, Provenance Records, or lifecycle state.
- Do not make topic-specific Artifact Format Profiles or Artifact Extensions mandatory core Artifact fields.
- Do not store secrets in the Project Manifest or Research Topic Config.

## Decisions

### Decision 1: Register Research Topic Config files in the Project Manifest

The Project Manifest should declare Research Topics and point to one Research Topic Config TOML file per topic. A minimal project shape is:

```text
<project>/
  .isomer-labs/
    manifest.toml
    research-topics/
      kernel-a-vs-b.toml
  topic-workspaces/
    kernel-a-vs-b/
      state.sqlite
      artifacts/
      agents/
      tasks/
      runs/
      views/
      logs/
```

Example Project Manifest fragment:

```toml
schema_version = "0.2"
project_id = "cuda-kernel-lab"
default_research_topic = "kernel-a-vs-b"

[[research_topics]]
id = "kernel-a-vs-b"
config_path = ".isomer-labs/research-topics/kernel-a-vs-b.toml"
topic_workspace_id = "kernel-a-vs-b"
status = "active"

[[topic_workspaces]]
id = "kernel-a-vs-b"
research_topic_id = "kernel-a-vs-b"
path = "topic-workspaces/kernel-a-vs-b"
runtime_db = "state.sqlite"
```

Rationale: the Project Manifest stays the discovery authority and avoids directory scanning. Research Topic Config can evolve independently without turning the manifest into a large inline workflow document.

Alternative considered: discover topic configs by scanning `.isomer-labs/research-topics/`. Rejected because it weakens the manifest authority and makes validation depend on directory contents.

### Decision 2: Keep Research Topic Config lightweight and reference-oriented

Research Topic Config should store topic-specific defaults and references, not runtime truth. A representative shape is:

```toml
schema_version = "0.1"
research_topic_id = "kernel-a-vs-b"

topic_statement = "Why is CUDA kernel A faster than kernel B?"
topic_statement_artifact_refs = [
  "artifact:topic-brief",
  "artifact:user-kernel-notes"
]
measurable_objectives = [
  "Identify the dominant performance cause",
  "Validate the explanation with profiling evidence"
]

default_topic_agent_team_profile = "cuda-kernel-investigation"
default_execution_adapter = "local-pixi"
default_control_mode = "manual"

[defaults]
research_inquiry_id = "compute-utilization"
artifact_tracking = "selective"

[capability_refs]
command_execution = "capability:local-pixi"
package_manager = "capability:pixi"
gpu_profiler = "capability:ncu-local"

[gate_policy_refs]
cost_privacy = "gate-policy:local-safe"
baseline_waiver = "gate-policy:baseline-required"

[artifact_format_defaults]
experiment_result = "artifact-format:cuda-ncu-profile"
analysis_report = "artifact-format:cuda-analysis-report"
figure = "artifact-format:paper-figure-svg-plus-source"

[artifact_extensions]
enabled = [
  "artifact-extension:cuda-kernel-metadata",
  "artifact-extension:gpu-hardware-context"
]
```

The config may include one short inline `topic_statement` for discovery, CLI previews, and human review. Richer topic material, evolving rationale, source notes, user briefs, and long-form context should be referenced through `topic_statement_artifact_refs` or other explicit Artifact refs. Inline Measurable Objective text is allowed for compact objectives, and richer objective material may use refs. The config must not contain secrets, command logs, Run outputs, live process ids, resolved command results, or mutable state that belongs in Workspace Runtime.

Rationale: the user and Operator Agent can review topic-specific defaults before launch, while Runs, Artifacts, Evidence Items, Gates, and Provenance Records remain durable state in the Topic Workspace.

Alternative considered: store topic defaults entirely in Workspace Runtime. Rejected because a topic needs reviewable project config before the Topic Workspace is created or before any Run starts.

### Decision 3: Resolve an Effective Topic Context before topic-scoped commands

Before executing a topic-scoped command, `isomer-cli` should produce an Effective Topic Context. It is not a new lifecycle object. It is a resolved context envelope used by the current process and recorded by downstream durable records when work begins.

The context should include:

- Project root, Project Config Directory, Project Manifest path, and schema versions.
- Research Topic id, Research Topic Config path, topic statement ref or short statement, and status.
- Topic Workspace id and path, with Workspace Path Resolution inputs.
- Optional active or explicit Research Inquiry, Research Task, and Run refs.
- Selected or default Topic Agent Team Profile refs.
- Selected or default Execution Adapter ref.
- Capability Binding refs and Gate policy refs by name.
- Control Mode default when a Run has not overridden it.
- Resolution sources for every value that can come from a flag, current directory, environment, local active context, manifest default, or topic config.

Rationale: the CLI, Workspace Path Resolver, Operator Agent, and Execution Adapter can all consume one neutral topic-context object without each component inventing topic selection behavior.

Alternative considered: let each CLI command load only the fields it needs. Rejected because commands would drift, and command records would be hard to compare across adapters.

When a Run, Run plan, or future Execution Adapter command request consumes Effective Topic Context, the durable record should store validated refs, resolution source metadata, and consumed config or default versions rather than the full Effective Topic Context snapshot. Required refs include the selected Project, Research Topic, Research Topic Config, Topic Workspace, Research Inquiry, Research Task, Run when known, Topic Agent Team Profile, Agent Team Instance or Agent Instance when known, Execution Adapter, Capability Binding refs, Gate policy refs, Artifact Format Profile refs, and Artifact Extension refs that influenced the action. Source metadata should identify whether each value came from an explicit selector, current directory, supported environment variable, `.isomer-labs/local.toml`, Project Manifest default, Research Topic Config, Topic Agent Team Profile, Domain Agent Team Template, built-in default, or Workspace Runtime record.

Rationale: refs plus sources are enough to audit why the action used a given topic, workspace, task, config, and default set. Full Effective Topic Context snapshots would duplicate config, create stale blobs when defaults change, and risk preserving values that should remain process-local.

The first implementation should use a narrow command-scope table. These are command families, not a final CLI spelling contract:

| Scope | Command families | Context rule |
| --- | --- | --- |
| Project-scoped | Project Manifest validation and inspection, registered Research Topic listing, Topic Workspace listing, built-in schema inspection, and project-level config checks | Resolve Project context only. Do not require Effective Topic Context. |
| Topic-scoped | Effective Topic Context show/validate, Research Inquiry commands, Research Task commands, Artifact commands, Gate commands, Topic Agent Team Profile commands, Agent Team Instance topic-participation commands, topic-scoped view commands, and topic-specific path previews | Resolve and validate Effective Topic Context before the action. |
| Run-scoped | Run inspect, resume, cancel, record, and export commands | Resolve and validate Effective Topic Context, then validate that the Run belongs to the selected Research Task, Research Inquiry, Research Topic, and Topic Workspace. |

Workspace path commands do not create a separate v1 scope. A command that lists registered Topic Workspaces is project-scoped. A command that previews or resolves paths for one selected Topic Workspace is topic-scoped.

### Decision 4: Use explicit topic selection precedence

Topic-scoped commands should select the Research Topic with this precedence:

1. Explicit CLI selectors such as `--topic`, `--topic-workspace`, `--task`, or `--run`.
2. Current working directory inside a Project Manifest-registered Topic Workspace.
3. Supported topic-context environment variables exported by an Execution Adapter for the current process.
4. User-local active context from untracked `.isomer-labs/local.toml`.
5. Project Manifest default Research Topic.

Explicit selectors must agree with lower-level refs. For example, if `--task` points to a task under topic `kernel-a-vs-b`, `--topic other-topic` is invalid.

Rationale: flags are predictable for automation, current-directory behavior is ergonomic, adapter environment supports launched processes, local active context supports interactive use, and manifest defaults make the first command usable.

Alternative considered: use a global active topic outside the Project. Rejected because `isomer-cli` is system-level but Project state is project-scoped.

The local active context file is a project-local user convenience file, not shared project truth. A representative shape is:

```toml
schema_version = "0.1"
active_research_topic_id = "kernel-a-vs-b"
active_topic_workspace_id = "kernel-a-vs-b"
active_research_inquiry_id = "compute-utilization"
active_research_task_id = "task:ncu-profile-baseline"
active_run_id = "run:profile-2026-06-18"
```

All fields are candidate identity refs that must validate against the Project Manifest, Research Topic Config, and Workspace Runtime before use. The file must stay untracked by default, must not replace the Project Manifest default Research Topic, and must not contain Run status, command outputs, live process ids, resolved command results, Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, credentials, tokens, API keys, passwords, or secret material.

### Decision 5: Add topic-context environment variables separately from path overrides

Workspace Path Resolution already owns path override variables such as `ISOMER_PROJECT_ROOT` and `ISOMER_CURRENT_TOPIC_WORKSPACE_DIR`. This change should add a small topic-context set for identity refs, not paths:

```text
ISOMER_RESEARCH_TOPIC_ID
ISOMER_TOPIC_WORKSPACE_ID
ISOMER_RESEARCH_INQUIRY_ID
ISOMER_RESEARCH_TASK_ID
ISOMER_RUN_ID
ISOMER_AGENT_TEAM_INSTANCE_ID
ISOMER_AGENT_INSTANCE_ID
```

These variables are candidate launch-time inputs. They are not durable truth. The Effective Topic Context records their source, and downstream Run, Artifact, Gate, Decision Record, Evidence Item, Finding, and Provenance Record refs remain the durable record.

Rationale: identity refs and path overrides have different validation rules. Keeping the names separate avoids overloading path variables with lifecycle selection behavior.

Alternative considered: infer lifecycle identity only from paths. Rejected because Topic Workspace paths can move, and a Run or Research Task cannot always be inferred from a directory.

### Decision 6: Make Workspace Path Resolution consume Effective Topic Context

Workspace Path Resolution should accept Effective Topic Context as an input before resolving paths. The resolver still follows its accepted precedence: recorded plan, environment path overrides, Project Manifest defaults, then built-in defaults. The Effective Topic Context supplies the selected Project, Research Topic, Topic Workspace, and optional Run or Agent Instance refs used to pick the applicable recorded plan and manifest defaults.

Rationale: topic selection and path resolution should stay separate. Topic context decides "which topic"; path resolution decides "where are this topic's paths."

Alternative considered: fold topic selection into the Workspace Path Resolver. Rejected because topic selection also controls capability refs, Gate policy refs, Topic Agent Team Profile defaults, and Execution Adapter defaults, not only paths.

### Decision 7: Keep Artifact Core Record generic and minimal

Topic-specific artifact customization should not change the fields every Artifact must carry. The core Artifact record should be only the durable index needed to locate, classify, and audit file-backed or external content:

```toml
artifact_id = "artifact:run-42-profile"
topic_workspace_id = "topic-workspace:kernel-a-vs-b"
artifact_kind = "experiment-result"
status = "active"
location_kind = "project_path"
location = "artifacts/experiments/run-42/profile.toml"
media_type = "application/toml"
created_at = "2026-06-18T02:00:00Z"
updated_at = "2026-06-18T02:00:00Z"
```

Lifecycle refs, producer refs, Run refs, Provenance Record refs, Evidence Item refs, supersession refs, format profile refs, extension refs, validation outcomes, and renderer hints may attach through link records, metadata records, or other accepted recording APIs. They should not be required fields on the Artifact Core Record.

Rationale: the platform must always be able to list, locate, validate existence, display generically, and trace an Artifact even when a topic-specific format is unknown, disabled, missing, or obsolete. Topic-specific formats improve validation, rendering, interpretation, and expected-output planning; they must not become the durable minimum required to understand the Artifact graph.

Alternative considered: include `format_profile_ref`, `format_version`, and `extension_refs` directly in every Artifact record. Rejected because it makes optional topic customization look mandatory and forces generic Artifacts to carry fields that may not apply.

### Decision 8: Attach Artifact Format Profiles and Extensions through topic defaults and output specs

Artifact Format Profiles should be declarative-only in the first version. They may describe optional content-level expectations such as media type, schema ref, template ref, validation hint, renderer hint, export hint, compatibility version, and opaque future capability refs. They must not define executable validators, renderers, exporters, command requests, provider contracts, or adapter-specific runtime behavior. Artifact Extensions should describe additive topic metadata fields, such as CUDA kernel metadata or GPU hardware context. Extensions must not shadow or redefine core Artifact fields.

Project Manifest can register available project-level profiles and extensions:

```toml
[[artifact_format_profiles]]
id = "cuda-ncu-profile"
path = ".isomer-labs/artifact-formats/cuda-ncu-profile.toml"
scope = "project"

[[artifact_extensions]]
id = "cuda-kernel-metadata"
path = ".isomer-labs/artifact-extensions/cuda-kernel-metadata.toml"
scope = "project"
```

Research Topic Config can select topic defaults by Artifact kind, and Research Task expected outputs or explicit Run command requests can override those defaults for a specific output. Resolution order should be:

1. Explicit Run plan or future Execution Adapter command request expected output format.
2. Research Task expected output spec.
3. Research Topic Config artifact defaults.
4. Topic Agent Team Profile or Domain Agent Team Template defaults.
5. Built-in Artifact kind defaults.

Rationale: format customization is topic-specific but should still support task- and run-level precision. This keeps CUDA profiling outputs, paper artifacts, figure outputs, benchmark records, and local lab formats out of the generic Artifact core while letting `isomer-cli` and the Operator Agent plan outputs coherently.

Alternative considered: make each skill choose its own output format. Rejected because it would duplicate policy across skills and make topic-level user customization ineffective.

## Risks / Trade-offs

- [Risk] Research Topic Config could grow into a second runtime database. Mitigation: validate that it contains defaults and refs only; Run status, command outputs, live process state, Artifacts, Evidence Items, and Provenance Records stay in Workspace Runtime and file-backed Artifacts.
- [Risk] Users may expect `isomer-cli` behavior to follow a global active topic. Mitigation: keep active context project-local, make explicit flags override it, and show the resolved Project and Research Topic in command previews.
- [Risk] Environment variables can conflict with CLI flags or manifest refs. Mitigation: require conflict validation and record resolution sources.
- [Risk] Topic config refs may point to missing Topic Workspaces, Topic Agent Team Profiles, Capability Bindings, or Gate policies. Mitigation: fail validation before Run creation or Execution Adapter dispatch.
- [Risk] Topic-specific artifact formats can fragment validation and GUI rendering. Mitigation: keep Artifact Core Record generic and minimal, require unknown formats to degrade to generic Artifact handling, and validate extensions as additive metadata only.
- [Risk] Format profiles can accidentally become command runners or provider contracts. Mitigation: make profiles declarative-only in the first version, allow only opaque future capability refs, and keep concrete command execution under the later Execution Adapter command surface.
- [Risk] This change touches command execution boundaries without defining the command API. Mitigation: only define the Effective Topic Context that future command requests consume and leave `api-execution-command` open.

## Migration Plan

1. Add the `cli-topic-context-resolution` spec and update Workspace Path Resolution with its Effective Topic Context input requirement.
2. Update architecture notes and domain language references that still describe topic discovery with stale Research Thread or Isomer Workspace terminology.
3. Add example Project Manifest and Research Topic Config fragments to documentation, including optional Artifact Format Profile and Artifact Extension registration.
4. Update Research Recording Contracts to distinguish minimal Artifact Core Records from optional format and extension attachments.
5. Update research-paradigm shared guidance so skills can name `isomer-cli` Effective Topic Context and topic artifact format defaults when a CLI command needs topic-specific behavior, while preserving unresolved execution placeholders.
6. Add validation expectations for topic registration, topic config parsing, artifact format and extension refs, path bounds, ref consistency, and source reporting.
7. Keep rollback documentation-only for this change: remove the topic-context and artifact-format spec deltas and restore guidance to Project Manifest plus Workspace Path Resolution only.
