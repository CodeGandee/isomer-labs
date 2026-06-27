# Topic Workspace Definition

This page defines the Topic Workspace path contract by semantic workspace surface labels first and by the standard filesystem layout second. The default directories shown here are the built-in `isomer-default.v1` layout profile, not the only valid structure.

## Scope

A Topic Workspace is a project-local directory declared by the Project Manifest for one Research Topic. It owns the topic's Workspace Runtime, Pixi workspace, Topic Agent Team Profile Bundle, Topic Main Repository, Agent Workspaces, owner-preserved records, and adapter material.

Only two Isomer filesystem areas should be called workspaces:

- **Topic Workspace**: the topic-level work area declared by the Project Manifest.
- **Agent Workspace**: a per-agent work area inside one Topic Workspace.

Do not call `repos/topic-main`, `.isomer-labs/`, `team-profile/`, `records/`, `runtime/`, or an ordinary Git branch a workspace. Use more specific terms such as Topic Main Repository, Project Config Directory, Topic Agent Team Profile Bundle, Workspace Runtime, Topic Workspace Records Root, Topic Workspace Runtime Support Root, Run record directory, Research Task record directory, or Git branch.

## Topic Workspace Root

Fresh Projects usually place Topic Workspaces under `isomer-content/topic-ws/<topic-workspace-id>/`, or under `<content-dir>/topic-ws/<topic-workspace-id>/` when project initialization selected a custom content root. A Topic Workspace may live elsewhere inside the Project when the Project Manifest explicitly declares that path.

Isomer must not infer managed Topic Workspaces by scanning directories. A directory becomes a Topic Workspace only when the Project Manifest declares it.

## Topic Workspace Manifest and Semantic Labels

Each Topic Workspace may contain a topic-owned Topic Workspace Manifest at `<topic-workspace>/topic-workspace.toml`. The manifest binds semantic workspace surface labels such as `topic.repos.main`, `topic.records.artifacts`, `topic.runtime.db`, `topic.agents_root`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.scratch` to concrete paths or agent path templates inside the selected Topic Workspace.

The Project Manifest remains the outer discovery authority for Research Topics and Topic Workspaces. It does not carry a per-topic manifest path override. The Topic Workspace Manifest is topic-owned configuration and must not be stored inside `.isomer-labs/`.

A missing Topic Workspace Manifest is valid for read-only resolution. In that case, Workspace Path Resolution synthesizes effective bindings from `isomer-default.v1` without creating files. Materializing default paths is explicit: use `isomer-cli project paths materialize-default` to write or update `topic-workspace.toml` and create selected default-owned directories.

Semantic labels are the public contract. Existing snake-case surfaces such as `records_artifacts`, `topic_main_repo`, and `agent_workspace:<agent-name>` remain compatibility identifiers for path plans and older callers.

Reserved roots such as `project`, `topic`, and `agent` are Isomer-owned. The Topic Main Repository label is `topic.repos.main`, and additional topic repositories may be registered under the grouped reserved family `topic.repos.<group...>.<repo-name>`, for example `topic.repos.inner_group.some_repo_name`. User-defined labels must live under `custom.*`, for example `custom.datasets.raw`.

Active manifest bindings use only three authoring fields: `label`, `path`, and `storage_profile`. `storage_profile` is explicit because a path string cannot reliably imply ownership, lifecycle, visibility, safety policy, or Git semantics. Built-in labels have Isomer-defined storage profiles; custom labels and grouped repository labels must declare one when registered.

```toml
[[bindings]]
label = "custom.datasets.raw"
path = "data/raw"
storage_profile = "topic_records_dir"

[[bindings]]
label = "topic.repos.inner_group.some_repo_name"
path = "repos/inner_group/some_repo_name"
storage_profile = "topic_repo"
```

## Standard Layout

The `isomer-default.v1` Topic Workspace layout is:

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
      isomer-managed/                      # one Isomer-specific worker-facing namespace inside topic-main
        .gitignore                         # ignores agent-owned/, topic-owned/, and links/ while keeping tracked/ trackable
        tracked/                           # Git-tracked Isomer-injected coordination material
          shared/                          # small shared notes or indexes intended for Git exchange
          artifacts/                       # small Git-shared artifacts before or after promotion
          tasks/                           # Git-shared task coordination material
          runs/                            # Git-shared run coordination material
          views/                           # Git-shared view support material
          tools/                           # topic-owned worker-facing wrappers and scripts intended for Git
          boundaries/                      # Workspace Boundary notes and manifests intended for Git
          manifests/                       # small Isomer manifests and indexes intended for Git
        agent-owned/                       # ignored owner area for the current worktree's large or local material
          runtime/                         # Agent Runtime state and recovery files
          scratch/                         # local drafts and temporary work
          logs/                            # agent-local logs and diagnostics
          artifacts/                       # unpromoted Agent Artifacts
          public/                          # peer-readable large or temporary material
          inbox/                           # peer-writable only when boundary policy grants it
        topic-owned/                       # ignored projections of topic-owned non-Git material
          readonly/                        # read-only projections for workers
          writable/                        # writable projections only with explicit policy
        links/                             # ignored generated peer or topic convenience links
          peers/                           # advisory links to peer public shares
          topic/                           # advisory links to topic-owned projections
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

- `pixi.toml` or `pyproject.toml`
  - Meaning: Topic Workspace Pixi manifest.
  - Notes: Declares topic-scoped Python, research dependencies, and optional named environments.
- `pixi.lock`
  - Meaning: Topic Workspace Pixi lockfile.
  - Notes: Durable lockfile for the topic environment.
- `.pixi/`
  - Meaning: Pixi-managed environment directory.
  - Notes: Generated and rebuildable. It is not durable research state.
- `state.sqlite`
  - Meaning: Workspace Runtime database.
  - Notes: Stores compact runtime records, refs, lifecycle state, validation state, readiness records, and path plans.
- `team-profile/`
  - Meaning: Topic Agent Team Profile Bundle.
  - Notes: Stores the Research Topic's one authoritative topic-specialized profile bundle. It is design-time material, not a running team.
- `team-profile/profile.toml`
  - Meaning: Topic Agent Team Profile.
  - Notes: The authoritative profile file inside the bundle.
- `team-profile/instantiation-packet.toml`
  - Meaning: Topic Team Instantiation Packet.
  - Notes: Optional reviewable planning and provenance material used before or during bundle materialization.
- `team-profile/approval.toml`
  - Meaning: Bundle-local approval provenance.
  - Notes: Optional approval metadata, actor or session ref, review summary, and validation result.
- `team-profile/execplan/`
  - Meaning: Copied and topic-edited template material.
  - Notes: May include `team-specialization-guide.md`, `team-specialization-plan.md`, or other launch-facing static planning material.
- `team-profile/validation/`
  - Meaning: Profile validation outputs.
  - Notes: Validation outputs for profile and packet material.
- `team-profile/provenance/`
  - Meaning: Profile provenance refs.
  - Notes: Provenance material for specialization and materialization.
- `repos/topic-main/`
  - Meaning: Topic Main Repository.
  - Notes: Shared normal, non-bare Git repository for worker-visible code-bearing topic work. It is not a workspace.
- `repos/topic-main/isomer-managed/`
  - Meaning: Isomer-managed worker namespace.
  - Notes: The only standard Isomer-specific worker-facing namespace inside `topic-main`.
- `repos/topic-main/isomer-managed/.gitignore`
  - Meaning: Namespace ignore policy.
  - Notes: Ignores `agent-owned/`, `topic-owned/`, and `links/` while keeping `.gitignore` and `tracked/` eligible for Git tracking.
- `repos/topic-main/isomer-managed/tracked/`
  - Meaning: Git-tracked Isomer material.
  - Notes: Small coordination files, task notes, tool wrappers, boundary material, manifests, indexes, and small artifacts intentionally shared through Git.
- `repos/topic-main/isomer-managed/tracked/{shared,artifacts,tasks,runs,views,tools,boundaries,manifests}/`
  - Meaning: Tracked collaboration surfaces.
  - Notes: Standard subdirectories for Isomer-injected material that should follow normal Git branch exchange.
- `repos/topic-main/isomer-managed/agent-owned/`
  - Meaning: Current worktree owner area.
  - Notes: Ignored material owned by the current agent worktree, including runtime, scratch, logs, unpromoted artifacts, public share, and policy-controlled inbox.
- `repos/topic-main/isomer-managed/topic-owned/`
  - Meaning: Topic-owned projections.
  - Notes: Ignored worker-visible projections of topic-owned non-Git material, split into `readonly/` and `writable/` policy surfaces.
- `repos/topic-main/isomer-managed/links/`
  - Meaning: Generated convenience links.
  - Notes: Ignored advisory links to peer public shares or topic-owned projections; links are not durable path truth or isolation.
- `agents/`
  - Meaning: Agent Workspace root.
  - Notes: Contains one Git worktree per agent, named as `<agent-name>`.
- `records/artifacts/`
  - Meaning: Owner-preserved research Artifacts.
  - Notes: Durable topic-level files such as notes, reports, data summaries, figures, decisions, evidence material, and normalized handoff outputs.
- `records/tasks/`
  - Meaning: Owner-preserved Research Task records.
  - Notes: Stores task support material outside canonical runtime rows when a task needs durable file-backed context.
- `records/runs/`
  - Meaning: Owner-preserved Run records.
  - Notes: Stores per-Run prompts, summaries, command support, outputs, and other file-backed execution material.
- `records/views/`
  - Meaning: Owner-preserved View Manifest support files.
  - Notes: Stores generated View Manifests and GUI view material.
- `records/logs/`
  - Meaning: Owner-preserved logs.
  - Notes: Stores topic-level diagnostics and logs that are durable records but not normal worker input.
- `runtime/adapters/houmao/<agent-team-instance-id>/`
  - Meaning: Houmao adapter material.
  - Notes: Stores adapter manifests, command payloads, launch material, snapshots, stop outcomes, handoff payloads, observations, and normalizations.

The Topic Workspace must not contain a workspace-local `teams/` directory. Domain Agent Team Templates live as built-in or Project Config references. The one topic-specialized profile bundle lives under `team-profile/`, and runtime Agent Team Instance state lives in Workspace Runtime records plus adapter material.

## Topic Main Repository

`repos/topic-main` is the shared topic repository used by Agent Workspace preparation. It is a normal non-bare Git repository and acts as the Git anchor for per-agent worktrees under `agents/`.

`repos/topic-main` is the primary cross-agent information channel. Different agents work in different Git worktrees of this single repository, on agent-owned branches. Agents can inspect, fetch, merge, or otherwise integrate peer branches according to the topic's coordination rules.

`repos/topic-main` is a topic-level support surface. It is not an Agent Workspace, not Workspace Runtime state, and not a separate Topic Workspace. Its branch state is ordinary Git state. Research lifecycle branching remains represented through Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, and Decision Records, not through a domain concept named Research Branch.

## Agent Workspace Roots

An Agent Workspace is a per-agent work area inside a Topic Workspace. The `isomer-default.v1` Agent Workspace binding is:

```text
<topic-workspace>/agents/<agent-name>
```

Each Agent Workspace is a Git worktree of `repos/topic-main`, checked out to an agent-owned branch. The agent is launched with this directory as its current working directory. The launch cwd convention makes the per-agent worktree the agent's normal world: the agent should read, write, run tools, and produce local outputs from inside that directory unless an explicit workflow or topic-owned tool asks it to use another surface.

The cwd convention is not filesystem-grade isolation. An agent with broad system tools may still access other paths. Isomer records expected behavior through Workspace Boundaries, branch rules, topic-owned tasks, Artifacts, and Provenance Records rather than claiming hard sandboxing.

## Agent Name

An Agent name is a topic-local, path-safe name used to resolve `agent.*` labels, launch cwd, and Git branch namespace. Examples include `alice`, `scout-a`, and `experimenter-gpu`.

An Agent name is not a substitute for every runtime ref. Workspace Runtime may still record Agent Instance ids, Agent Role ids, Agent Profile refs, Agent Team Instance ids, and adapter refs. The default filesystem convention maps `agent.workspace` to `agents/<agent-name>`, but a Topic Workspace Manifest may bind that label to another safe project-local template such as `worktrees/{agent_name}`.

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
2. **Isomer-managed untracked shares and projections**: this is the secondary channel for large or temporary material. Agents use owner-approved `isomer-managed/agent-owned/public/`, policy-controlled `isomer-managed/topic-owned/`, or generated `isomer-managed/links/` surfaces when peer inspection is useful before a commit or promotion.
3. **Topic-owned Pixi tasks**: this is the most principled shared interface. Agents should use topic-owned Pixi tasks when the topic provides tools, scripts, or APIs for sharing information, publishing state, querying shared services, or validating integration. These tasks run from the Topic Workspace's Pixi environment and keep shared operations explicit and auditable.

## Agent Workspace Internal Layout

The standard Agent Workspace support layout inside each worktree is:

```text
<topic-workspace>/agents/<agent-name>/
  README.md                                # human-readable Workspace Boundary and launch notes
  boundary.toml                            # optional machine-readable Workspace Boundary
  isomer-managed/                          # Isomer-specific worker-facing namespace
    .gitignore                             # ignores untracked owner, topic projection, and generated-link regimes
    tracked/                               # Git-shared Isomer coordination material
      shared/
      artifacts/
      tasks/
      runs/
      views/
      tools/
      boundaries/
      manifests/
    agent-owned/                           # ignored material owned by this Agent Workspace
      runtime/                             # Agent Runtime state and recovery files
      scratch/                             # local drafts and temporary work
      logs/                                # agent-local logs and diagnostics
      artifacts/                           # Agent Artifacts before promotion
      public/                              # peer-readable large or temporary material
      inbox/                               # peer-writable only with explicit boundary policy
    topic-owned/                           # ignored topic-owned projections
      readonly/                            # read-only worker projection
      writable/                            # writable worker projection with explicit policy
    links/                                 # generated advisory links
      peers/
        <peer-agent>/public -> ../../../<peer-agent>/isomer-managed/agent-owned/public/
      topic/
```

- `README.md`
  - Meaning: human-readable Workspace Boundary note.
  - Notes: Declares ownership, expected writes, Peer Read Access, branch expectations, and safe integration notes.
- `boundary.toml`
  - Meaning: machine-readable Workspace Boundary declaration.
  - Notes: Optional until a later accepted schema makes it required.
- `isomer-managed/tracked/`
  - Meaning: Git-tracked Isomer material.
  - Notes: Small Isomer-specific coordination material intended for normal branch exchange.
- `isomer-managed/agent-owned/runtime/`
  - Meaning: Agent Runtime state.
  - Notes: Prompt records, tool traces, recovery files, and agent-local execution support.
- `isomer-managed/agent-owned/artifacts/`
  - Meaning: Agent Artifacts.
  - Notes: Files produced, curated, or owned by the agent before promotion to topic records or Git-shared outputs.
- `isomer-managed/agent-owned/scratch/`
  - Meaning: local scratch.
  - Notes: Drafts and temporary work that are not durable research state unless promoted or referenced.
- `isomer-managed/agent-owned/logs/`
  - Meaning: agent-local logs.
  - Notes: Diagnostics and local logs for the agent.
- `isomer-managed/agent-owned/public/`
  - Meaning: peer-readable owner share.
  - Notes: Large or temporary files that peer agents may inspect before Git commit or promotion; peer writes are diagnostics unless boundary policy grants them.
- `isomer-managed/agent-owned/inbox/`
  - Meaning: policy-controlled peer write area.
  - Notes: Optional write surface that must name allowed writers, file naming, cleanup, and promotion policy in boundary material.
- `isomer-managed/topic-owned/readonly/`
  - Meaning: read-only topic projection.
  - Notes: Worker-visible projection of topic-owned non-Git material for reads only.
- `isomer-managed/topic-owned/writable/`
  - Meaning: writable topic projection.
  - Notes: Worker-visible projection for shared writes only when boundary policy grants it; structured updates should prefer topic-owned Pixi tasks.
- `isomer-managed/links/`
  - Meaning: generated links.
  - Notes: Optional advisory links to peer public shares or topic projections, not hard access-control boundaries.

Projects should decide through boundary material and repository policy which support paths are tracked, ignored, symlinked, or promoted. Scratch files and generated logs should not be treated as durable research state merely because they live under a worktree.

## Environment Inheritance

Agent Workspaces inherit the selected Topic Workspace Pixi environment by default. Agent Workspaces must not contain their own `pixi.toml`, `pyproject.toml`, `pixi.lock`, or `.pixi/` directory unless an explicit Service Request records per-agent environment divergence and the Service Agent Instance records support Artifacts and Provenance Records.

Git worktrees do not change this rule. An Agent Workspace worktree still uses the parent Topic Workspace environment by default.

## Workspace Boundary and Peer Read Access

Workspace Boundaries are advisory collaboration contracts. They declare intended write ownership, launch cwd expectations, branch namespace expectations, `isomer-managed/` tracked, agent-owned, topic-owned, and generated-link expectations, Peer Read Access, and integration notes. They are not filesystem-grade security isolation.

Agents should write inside their own Agent Workspace. Peer information should usually arrive through Git branch integration, owner-approved `isomer-managed/` shares or projections, generated links, or topic-owned Pixi tasks. Durable dependencies on peer material should be recorded through handoffs, promoted Artifacts, Evidence Items, or Provenance Records.

If validation detects peer writes without an explicit repair, migration, cleanup, or integration task, Isomer should report a workspace issue or Provenance Record rather than claiming that filesystem controls prevented the write.

## Path Resolution

Commands should resolve Topic Workspace and Agent Workspace paths through Workspace Path Resolution rather than assembling paths ad hoc. The resolver uses recorded Path Plans first, then supported `ISOMER_PATH__...` semantic environment variables and compatibility `ISOMER_*` variables exported by an Execution Adapter, then Topic Workspace Manifest bindings, then Project Manifest defaults where applicable, then `isomer-default.v1`. A generated environment variable for `custom.*` applies only after the label exists in the effective catalog.

Use `isomer-cli project paths get <semantic-label>` for one path answer and `isomer-cli project paths list` to inspect known labels. These commands and `project paths preview` are read-only. Add `--configured` to `project paths get` when you need the current manifest or environment answer instead of a stored Path Plan. Use `project paths default <semantic-label>` to ask for the default-layout path of a built-in reserved label without override precedence, and use `project paths explain <semantic-label>` to inspect candidate sources and the selected source.

Use `project paths materialize-default` only when you intend to write or update `topic-workspace.toml` and create selected default directories. Use `project paths materialize <semantic-label>` to create the currently configured target for an existing label according to its `storage_profile` while ignoring stored Path Plans. Use `project paths register`, `project paths update`, `project paths unregister`, and `project paths reset` for manifest binding lifecycle operations instead of editing the manifest by hand. `unregister` removes dynamic `custom.*` and grouped repository slots; `reset` removes a built-in override. Neither command deletes filesystem targets or rewrites historical Path Plans.

To register a new repository under `repos/<custom-repo>`, prefer `isomer-cli project repos create <repo-label> --topic <topic-id>`. A bare label such as `inner_group.some_repo_name` registers `topic.repos.inner_group.some_repo_name`, uses `storage_profile = "topic_repo"`, creates `repos/inner_group/some_repo_name` by default, and makes the path queryable through `isomer-cli project paths get topic.repos.inner_group.some_repo_name --topic <topic-id>`.

For Agent Workspaces, Agent Team Instance creation records an Agent Workspace Path Plan for `agent.workspace` and support path plans for labels such as `agent.isomer_managed`, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.public_share`, and `agent.links`. An agent running inside its own Agent Workspace can query agent-scoped labels without passing an Agent Name because cwd-derived Effective Agent Context can identify the owning workspace. Cross-agent queries still require an explicit Agent Name or Agent Instance selector. Cwd inference is a convenience for path resolution, not filesystem-grade identity or access control.

Implemented Local Tmp Surface labels are `topic.tmp`, `topic.repos.main.tmp`, and `agent.tmp`. Under `isomer-default.v1`, `topic.tmp` resolves to `<topic-workspace>/tmp/`, `topic.repos.main.tmp` resolves to `<resolved topic.repos.main>/tmp/`, and `agent.tmp` resolves to `<resolved agent.workspace>/tmp/`. These labels are local, ignored, disposable, not shared, and not durable evidence unless explicitly promoted to another accepted semantic surface.

Local Tmp Surfaces are different from `agent.scratch`: scratch is agent-owned draft material that can become an intentional input to promotion, while tmp is sweepable posture for transient files. Tmp material is not Peer Read Access, generated-link target material, owner-preserved records, Workspace Runtime evidence, Provenance Records, Evidence Items, Decision Records, or Git-tracked Isomer material.

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
- untracked `isomer-managed/agent-owned/`, `isomer-managed/topic-owned/`, and generated `isomer-managed/links/` material until it is promoted or recorded.
- ordinary Git branch state inside `repos/topic-main` and per-agent worktrees, except where branch state is explicitly captured as an Artifact, Evidence Item, Decision Record, or Provenance Record.

## Legacy Layout Migration

Older Topic Workspace drafts and fixtures may contain `repos/topic-main/shared/`, `repos/topic-main/artifacts/`, `repos/topic-main/tasks/`, `repos/topic-main/runs/`, `repos/topic-main/views/`, `repos/topic-main/logs/`, or `repos/topic-main/tools/` as top-level worker collaboration surfaces. Treat these as legacy layout diagnostics. Current worker-visible Isomer material belongs under `repos/topic-main/isomer-managed/tracked/`, `repos/topic-main/isomer-managed/agent-owned/`, `repos/topic-main/isomer-managed/topic-owned/`, or owner-preserved `records/*` according to ownership and durability. Validation must report these paths without deleting, moving, resetting, or rewriting user files.

Older profile or packet material may also use `agent-workspaces/`, `agents/<agent-instance-id>`, `agent-key`, or authored `agent_workspace_ref` values as the primary workspace planning language. New material should use topic-local Agent Names and derived Agent Workspace paths under `agents/<agent-name>`. Compatibility `agent_workspace_ref` values may remain only as derived or validated material while older schemas still need them.

Older Agent Workspace drafts may contain `.isomer-agent/` support roots. Treat them as legacy support material and migrate only through explicit operator instruction. Current Agent Runtime, scratch, logs, Agent Artifacts, peer-readable public shares, optional inboxes, topic projections, and generated links belong under `isomer-managed/`.
