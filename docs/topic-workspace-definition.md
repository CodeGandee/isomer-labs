# Topic Workspace Definition

This page defines the standard Topic Workspace and Agent Workspace filesystem structure. It is the canonical documentation page for directory meanings, expected ownership, per-agent Git worktrees, launch working directories, and topic-owned collaboration channels.

## Scope

A Topic Workspace is a project-local directory declared by the Project Manifest for one Research Topic. It owns the topic's Workspace Runtime, Pixi workspace, Topic Agent Team Profile Bundle, Topic Main Repository, Agent Workspaces, owner-preserved records, and adapter material.

Only two Isomer filesystem areas should be called workspaces:

- **Topic Workspace**: the topic-level work area declared by the Project Manifest.
- **Agent Workspace**: a per-agent work area inside one Topic Workspace.

Do not call `repos/topic-main`, `.isomer-labs/`, `team-profile/`, `records/`, `runtime/`, or an ordinary Git branch a workspace. Use more specific terms such as Topic Main Repository, Project Config Directory, Topic Agent Team Profile Bundle, Workspace Runtime, Topic Workspace Records Root, Topic Workspace Runtime Support Root, Run record directory, Research Task record directory, or Git branch.

## Topic Workspace Root

Fresh Projects usually place Topic Workspaces under `isomer-content/topic-ws/<topic-workspace-id>/`, or under `<content-dir>/topic-ws/<topic-workspace-id>/` when project initialization selected a custom content root. A Topic Workspace may live elsewhere inside the Project when the Project Manifest explicitly declares that path.

Isomer must not infer managed Topic Workspaces by scanning directories. A directory becomes a Topic Workspace only when the Project Manifest declares it.

## Standard Layout

The standard Topic Workspace layout is:

```text
<topic-workspace>/                         # Project Manifest-declared root for one Research Topic
  pixi.toml                                # Topic Workspace Pixi manifest; use pyproject.toml instead when Python package metadata is needed
  pixi.lock                                # Topic Workspace Pixi lockfile
  .pixi/                                   # generated Pixi environment directory, rebuildable and not durable research state
  state.sqlite                             # Workspace Runtime database
  team-profile/                            # Topic Agent Team Profile Bundle, not a running team
    profile.toml                           # authoritative Topic Agent Team Profile
    instantiation-packet.toml              # optional Topic Team Instantiation Packet
    approval.toml                          # optional bundle-local approval provenance
    execplan/                              # copied and topic-edited template material
    validation/                            # profile and packet validation outputs
    provenance/                            # specialization and materialization provenance refs
  repos/                                   # topic-level repositories, not workspaces
    topic-main/                            # shared normal non-bare Git repository for worker-visible topic work
      shared/                              # optional worker-visible shared files, tracked or intentionally ignored by Git policy
      artifacts/                           # worker-visible topic outputs before owner preservation
      tasks/                               # worker-visible task coordination material
      runs/                                # worker-visible run coordination material
      views/                               # worker-visible view support material
      logs/                                # worker-visible logs selected for collaboration
      tools/                               # topic-owned worker-facing tools and wrappers
  agents/                                  # Agent Workspace root
    <agent-name>/                          # Agent Workspace Git worktree and launch cwd for one named agent
  records/                                 # owner-preserved records, not normal worker input
    artifacts/                             # preserved Artifacts, Evidence Items, reports, figures, decisions, and handoff outputs
    tasks/                                 # preserved Research Task support records
    runs/                                  # preserved Run support records
    views/                                 # preserved View Manifests and GUI view material
    logs/                                  # preserved topic-level logs and diagnostics
  runtime/                                 # durable runtime support material outside state.sqlite, not normal worker input
    adapters/                              # Execution Adapter material
      houmao/                              # Houmao adapter records
        <agent-team-instance-id>/          # adapter material for one Agent Team Instance
```

Not every directory must exist before the workflow that owns it runs. Mutating commands should create only the directories they are responsible for and should record path plans or provenance when the created path becomes durable runtime truth.

## Directory Meanings

| Path | Meaning | Notes |
|---|---|---|
| `pixi.toml` or `pyproject.toml` | Topic Workspace Pixi manifest | Declares topic-scoped Python, research dependencies, and optional named environments. |
| `pixi.lock` | Topic Workspace Pixi lockfile | Durable lockfile for the topic environment. |
| `.pixi/` | Pixi-managed environment directory | Generated and rebuildable. It is not durable research state. |
| `state.sqlite` | Workspace Runtime database | Stores compact runtime records, refs, lifecycle state, validation state, readiness records, and path plans. |
| `team-profile/` | Topic Agent Team Profile Bundle | Stores the Research Topic's one authoritative topic-specialized profile bundle. It is design-time material, not a running team. |
| `team-profile/profile.toml` | Topic Agent Team Profile | The authoritative profile file inside the bundle. |
| `team-profile/instantiation-packet.toml` | Topic Team Instantiation Packet | Optional reviewable planning and provenance material used before or during bundle materialization. |
| `team-profile/approval.toml` | Bundle-local approval provenance | Optional approval metadata, actor or session ref, review summary, and validation result. |
| `team-profile/execplan/` | Copied and topic-edited template material | May include `team-specialization-guide.md`, `team-specialization-plan.md`, or other launch-facing static planning material. |
| `team-profile/validation/` | Profile validation outputs | Validation outputs for profile and packet material. |
| `team-profile/provenance/` | Profile provenance refs | Provenance material for specialization and materialization. |
| `repos/topic-main/` | Topic Main Repository | Shared normal, non-bare Git repository for worker-visible code-bearing topic work. It is not a workspace. |
| `repos/topic-main/shared/` | Worker-visible shared files | Optional shared material exposed through Git or approved `.isomer-agent/links/` symlinks. |
| `repos/topic-main/artifacts/` | Worker-visible topic outputs | Collaboration-facing outputs before owner preservation or promotion into durable records. |
| `repos/topic-main/tasks/` | Worker-visible task coordination material | Git-shared task plans or notes that agents should see. |
| `repos/topic-main/runs/` | Worker-visible run coordination material | Git-shared run notes or coordination files that agents should see. |
| `repos/topic-main/views/` | Worker-visible view support material | Git-shared view material when a topic intentionally exposes it to workers. |
| `repos/topic-main/logs/` | Worker-visible selected logs | Logs deliberately published for worker collaboration, not raw runtime logs by default. |
| `repos/topic-main/tools/` | Worker-facing tools | Topic-owned wrappers, scripts, or docs that worker agents can use from their worktrees. |
| `agents/` | Agent Workspace root | Contains one Git worktree per agent, named as `<agent-name>`. |
| `records/artifacts/` | Owner-preserved research Artifacts | Durable topic-level files such as notes, reports, data summaries, figures, decisions, evidence material, and normalized handoff outputs. |
| `records/tasks/` | Owner-preserved Research Task records | Stores task support material outside canonical runtime rows when a task needs durable file-backed context. |
| `records/runs/` | Owner-preserved Run records | Stores per-Run prompts, summaries, command support, outputs, and other file-backed execution material. |
| `records/views/` | Owner-preserved View Manifest support files | Stores generated View Manifests and GUI view material. |
| `records/logs/` | Owner-preserved logs | Stores topic-level diagnostics and logs that are durable records but not normal worker input. |
| `runtime/adapters/houmao/<agent-team-instance-id>/` | Houmao adapter material | Stores adapter manifests, command payloads, launch material, snapshots, stop outcomes, handoff payloads, observations, and normalizations. |

The Topic Workspace must not contain a workspace-local `teams/` directory. Domain Agent Team Templates live as built-in or Project Config references. The one topic-specialized profile bundle lives under `team-profile/`, and runtime Agent Team Instance state lives in Workspace Runtime records plus adapter material.

## Topic Main Repository

`repos/topic-main` is the shared topic repository used by Agent Workspace preparation. It is a normal non-bare Git repository and acts as the Git anchor for per-agent worktrees under `agents/`.

`repos/topic-main` is the primary cross-agent information channel. Different agents work in different Git worktrees of this single repository, on agent-owned branches. Agents can inspect, fetch, merge, or otherwise integrate peer branches according to the topic's coordination rules.

`repos/topic-main` is a topic-level support surface. It is not an Agent Workspace, not Workspace Runtime state, and not a separate Topic Workspace. Its branch state is ordinary Git state. Research lifecycle branching remains represented through Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, and Decision Records, not through a domain concept named Research Branch.

## Agent Workspace Roots

An Agent Workspace is a per-agent work area inside a Topic Workspace. The standard Agent Workspace path is:

```text
<topic-workspace>/agents/<agent-name>
```

Each Agent Workspace is a Git worktree of `repos/topic-main`, checked out to an agent-owned branch. The agent is launched with this directory as its current working directory. The launch cwd convention makes the per-agent worktree the agent's normal world: the agent should read, write, run tools, and produce local outputs from inside that directory unless an explicit workflow or topic-owned tool asks it to use another surface.

The cwd convention is not filesystem-grade isolation. An agent with broad system tools may still access other paths. Isomer records expected behavior through Workspace Boundaries, branch rules, topic-owned tasks, Artifacts, and Provenance Records rather than claiming hard sandboxing.

## Agent Name

An Agent name is a topic-local, path-safe name used to identify the per-agent worktree path, launch cwd, and Git branch namespace. Examples include `alice`, `scout-a`, and `experimenter-gpu`.

An Agent name is not a substitute for every runtime ref. Workspace Runtime may still record Agent Instance ids, Agent Role ids, Agent Profile refs, Agent Team Instance ids, and adapter refs. The filesystem convention is simpler: the per-agent working directory is always `agents/<agent-name>`.

Agent names should be normalized to safe lowercase path segments. Empty segments, `..`, leading or trailing slash, path separators, normalized collisions, and unsafe Git ref suffixes such as `.lock` are blockers.

## Agent-Owned Worktrees and Branches

Each prepared Agent Workspace normally has this shape:

```text
<topic-workspace>/
  repos/
    topic-main/
  agents/
    <agent-name>/              # Git worktree of repos/topic-main and launch cwd
```

The default branch for an Agent name is:

```text
per-agent/<agent-name>/main
```

Future per-agent branches must stay under:

```text
per-agent/<agent-name>/<branch-name>
```

A branch request outside the owning `per-agent/<agent-name>/` prefix is a blocker. A duplicate checkout of the same branch in another worktree is also a blocker.

The branch namespace is ordinary Git state. It is not Research Inquiry lifecycle state and should not be called Research Branch.

## Agent Communication Channels

Agents should collaborate through three channels, in this order of preference.

1. **Shared Git repository and branches**: this is the primary channel. Agents work in separate worktrees of `repos/topic-main` on separate branches. They can inspect, fetch, merge, cherry-pick, or otherwise integrate peer branches according to the topic's coordination rules.
2. **Symlinked shared directories**: this is the secondary channel. Approved shared directories under `repos/topic-main/` may be symlinked into each per-agent worktree under `.isomer-agent/links/` when agents need read-mostly shared file surfaces that are not naturally represented as branch exchange.
3. **Topic-owned Pixi tasks**: this is the most principled shared interface. Agents should use topic-owned Pixi tasks when the topic provides tools, scripts, or APIs for sharing information, publishing state, querying shared services, or validating integration. These tasks run from the Topic Workspace's Pixi environment and keep shared operations explicit and auditable.

## Agent Workspace Internal Layout

The standard Agent Workspace support layout inside each worktree is:

```text
<topic-workspace>/agents/<agent-name>/
  README.md                                # human-readable Workspace Boundary and launch notes
  boundary.toml                            # optional machine-readable Workspace Boundary
  .isomer-agent/                           # ignored agent-local support area
    runtime/                               # Agent Runtime state and recovery files
    artifacts/                             # Agent Artifacts before promotion to topic records or Git-shared outputs
    scratch/                               # local drafts and temporary work
    logs/                                  # agent-local logs and diagnostics
    links/                                 # optional approved symlinks into repos/topic-main
      <shared-link>/ -> ../../../../repos/topic-main/<name>/
```

| Path | Meaning | Notes |
|---|---|---|
| `README.md` | Human-readable Workspace Boundary note | Declares ownership, expected writes, Peer Read Access, branch expectations, and safe integration notes. |
| `boundary.toml` | Machine-readable Workspace Boundary declaration | Optional until a later accepted schema makes it required. |
| `.isomer-agent/runtime/` | Agent Runtime state | Prompt records, tool traces, recovery files, and agent-local execution support. |
| `.isomer-agent/artifacts/` | Agent Artifacts | Files produced, curated, or owned by the agent before promotion to topic records or Git-shared outputs. |
| `.isomer-agent/scratch/` | Local scratch | Drafts and temporary work that are not durable research state unless promoted or referenced. |
| `.isomer-agent/logs/` | Agent-local logs | Diagnostics and local logs for the agent. |
| `.isomer-agent/links/` | Approved symlink links | Optional advisory links into `repos/topic-main`, not hard access-control boundaries. |

Projects should decide through boundary material and repository policy which support paths are tracked, ignored, symlinked, or promoted. Scratch files and generated logs should not be treated as durable research state merely because they live under a worktree.

## Environment Inheritance

Agent Workspaces inherit the selected Topic Workspace Pixi environment by default. Agent Workspaces must not contain their own `pixi.toml`, `pyproject.toml`, `pixi.lock`, or `.pixi/` directory unless an explicit Service Request records per-agent environment divergence and the Service Agent Instance records support Artifacts and Provenance Records.

Git worktrees do not change this rule. An Agent Workspace worktree still uses the parent Topic Workspace environment by default.

## Workspace Boundary and Peer Read Access

Workspace Boundaries are advisory collaboration contracts. They declare intended write ownership, launch cwd expectations, branch namespace expectations, `.isomer-agent/` support layout, symlinked shared-directory expectations, Peer Read Access, and integration notes. They are not filesystem-grade security isolation.

Agents should write inside their own Agent Workspace. Peer information should usually arrive through Git branch integration, symlinked shared directories, or topic-owned Pixi tasks. Durable dependencies on peer material should be recorded through handoffs, promoted Artifacts, Evidence Items, or Provenance Records.

If validation detects peer writes without an explicit repair, migration, cleanup, or integration task, Isomer should report a workspace issue or Provenance Record rather than claiming that filesystem controls prevented the write.

## Path Resolution

Commands should resolve Topic Workspace and Agent Workspace paths through Workspace Path Resolution rather than assembling paths ad hoc. The resolver uses recorded workspace plans first, then supported `ISOMER_*` environment variables exported by an Execution Adapter, then Project Manifest defaults, then built-in defaults.

For Agent Workspaces, Agent Team Instance creation should record an Agent Workspace Path Plan for `<topic-workspace>/agents/<agent-name>` and launch the agent with that path as cwd.

## Durability

The following Topic Workspace material is durable by default:

- Topic Workspace Pixi manifest and lockfile.
- Topic Agent Team Profile Bundle under `team-profile/`.
- Workspace Runtime `state.sqlite` and path plan records.
- Owner-preserved research records under `records/*`.
- Agent Workspace records and Agent Workspace Path Plans.
- Promoted Agent Artifacts, Evidence Items, Decision Records, and Provenance Records.
- Adapter manifests and command payload refs under `runtime/adapters/` or `records/*`.

The following material is generated, local, or policy-dependent:

- `.pixi/`.
- uncommitted scratch files inside Agent Workspaces.
- generated logs that have not been recorded as Artifacts or Provenance Records.
- ordinary Git branch state inside `repos/topic-main` and per-agent worktrees, except where branch state is explicitly captured as an Artifact, Evidence Item, Decision Record, or Provenance Record.

## Legacy Layout Migration

Older Topic Workspace drafts and fixtures may contain root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` directories. Treat these as legacy root collaboration surfaces. Worker-visible content should move into `repos/topic-main/` through explicit operator action. Owner-preserved records should move into `records/*` through explicit migration or repair work. Validation must report these paths without deleting, moving, resetting, or rewriting user files.

Older profile or packet material may also use `agent-workspaces/`, `agents/<agent-instance-id>`, `agent-key`, or authored `agent_workspace_ref` values as the primary workspace planning language. New material should use topic-local Agent Names and derived Agent Workspace paths under `agents/<agent-name>`. Compatibility `agent_workspace_ref` values may remain only as derived or validated material while older schemas still need them.
