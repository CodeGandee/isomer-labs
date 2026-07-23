# Topic Workspaces

This manual page defines the Topic Workspace path contract by semantic workspace surface labels first and by the standard filesystem layout second. The default directories shown here are the built-in `isomer-default.v1` layout profile, not the only valid structure.

## Scope

A Topic Workspace is a project-local directory declared by the Project Manifest for one Research Topic. It owns the topic's Workspace Runtime, Pixi workspace, Topic Agent Team Profile Bundle, Topic Main Development Repository, registered topology for Canonical External Repositories, Agent Workspaces, owner-preserved records, and adapter material. The user or agent, not an Isomer repository service, controls how external repository content is acquired and verified.

Only three Isomer filesystem areas should be called workspaces:

- **Topic Workspace**: the topic-level work area declared by the Project Manifest.
- **Topic Actor Workspace**: a per-Topic Actor work area for human-orchestrated workers outside formal Agent Instance identity.
- **Agent Workspace**: a per-agent work area inside one Topic Workspace.

Do not call `repos/topic-main`, `.isomer-labs/`, `team-profile/`, `records/`, `runtime/`, an ordinary Git branch, or a Topic Publication Copy a workspace. Source Topic Workspace is a contextual role of the canonical Topic Workspace, and Topic Publication Copy is a disposable derived projection. See [Topic Workspace Git](topic-workspace-git.md) for the independent local-tracking and remote-publication layers.

## Topic Workspace Root

Fresh Projects usually place Topic Workspaces under `isomer-content/topic-ws/<topic-workspace-id>/`, or under `<content-dir>/topic-ws/<topic-workspace-id>/` when project initialization selected a custom content root. A Topic Workspace may live elsewhere inside the Project when the Project Manifest explicitly declares that path.

Isomer must not infer managed Topic Workspaces by scanning directories. A directory becomes a Topic Workspace only when the Project Manifest declares it.

## Topic Workspace Manifest and Semantic Labels

Each Topic Workspace may contain a topic-owned Topic Workspace Manifest at `<topic-workspace>/topic-workspace.toml`. The manifest binds semantic workspace surface labels such as `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records.artifacts`, `topic.runtime.db`, `topic.agents_root`, `agent.workspace`, `agent.private_artifacts`, `agent.public_share`, and `agent.scratch` to concrete paths or agent path templates inside the selected Topic Workspace. It may also carry topic-scope Toolbox registrations, Toolbox Runtime Param imports, and Toolbox Runtime Params for Research Topic, Topic Actor, and Topic Agent specialization.

The Project Manifest remains the outer discovery authority for Research Topics and Topic Workspaces. It does not carry a per-topic manifest path override. The Topic Workspace Manifest is topic-owned configuration and must not be stored inside `.isomer-labs/`.

A missing Topic Workspace Manifest is valid for read-only resolution. In that case, Workspace Path Resolution synthesizes effective bindings from `isomer-default.v1` without creating files. Materializing default paths is explicit: use `isomer-cli project paths materialize-default` to write or update `topic-workspace.toml` and create selected default-owned directories.

Semantic labels are the public contract. Existing snake-case surfaces such as `records_artifacts`, `topic_main_repo`, and `agent_workspace:<agent-name>` remain compatibility identifiers for path plans and older callers.

Reserved roots such as `project`, `topic`, and `agent` are Isomer-owned. The Topic Main Development Repository label is `topic.repos.main`, and its projection labels under `topic.repos.main.projections.*` are fixed built-ins, not grouped repository labels. Additional topic repositories may be registered under the grouped reserved family `topic.repos.<group...>.<repo-name>`, for example `topic.repos.inner_group.some_repo_name`. Helper-created non-main topic repositories default under `repos/extern/...`; the semantic label remains the path contract. User-defined labels must live under `custom.*`, for example `custom.datasets.raw`.

Active manifest bindings use only three authoring fields: `label`, `path`, and `storage_profile`. `storage_profile` is explicit because a path string cannot reliably imply ownership, lifecycle, visibility, safety policy, or Git semantics. Built-in labels have Isomer-defined storage profiles; custom labels and grouped repository labels must declare one when registered.

```toml
[[bindings]]
label = "custom.datasets.raw"
path = "data/raw"
storage_profile = "topic_records_dir"

[[bindings]]
label = "topic.repos.inner_group.some_repo_name"
path = "repos/extern/inner_group/some_repo_name"
storage_profile = "topic_repo"
```

Toolbox configuration tables use the same shape in the Project Manifest and the Topic Workspace Manifest. File location and `scope` determine the layer: the Project Manifest accepts only `scope = "project"`, while the Topic Workspace Manifest accepts `scope = "research_topic"`, `scope = "topic_actor"`, and `scope = "topic_agent"`. Topic Actor rows require `topic_actor_name`. Topic Agent rows require `topic_agent_name`, selected from the topic-local Effective Agent Context Agent Name rather than a new durable actor type.

```toml
[[toolboxes]]
toolbox_id = "gpu-analytical-modeling"
scope = "research_topic"
status = "active"
source_path = "skillset/toolboxes/gpu-analytical-modeling"

[[toolbox_runtime_param_imports]]
toolbox_id = "gpu-analytical-modeling"
path = "profiles/gpu-defaults.toml"
scope = "research_topic"
status = "active"

[[toolbox_runtime_params]]
toolbox_id = "gpu-analytical-modeling"
key = "evidence/mode"
value = "strict"
value_type = "enum"
allowed_values = ["strict", "relaxed"]
scope = "topic_agent"
topic_agent_name = "coder"
status = "active"
```

Runtime param imports are defaults for Toolbox runtime params, not installers. An imported TOML file may contain `schema_version = "isomer-toolbox-runtime-params.v1"` and `[[toolbox_runtime_params]]` rows only. Import paths are relative to the manifest file that declares them: Project Manifest imports resolve relative to `.isomer-labs/`, and Topic Workspace Manifest imports resolve relative to the Topic Workspace root. Effective values resolve as Project imports, Project explicit rows, Topic imports, then Topic explicit rows.

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
            extern-projections.toml        # tracked metadata for external repo projections
        agent-owned/                       # ignored owner area for the current worktree's large or local material
          runtime/                         # Agent Runtime state and recovery files
          scratch/                         # local drafts and temporary work
          logs/                            # agent-local logs and diagnostics
          artifacts/                       # unpromoted Agent Artifacts
          public/                          # peer-readable large or temporary material
          inbox/                           # peer-writable only when boundary policy grants it
        topic-owned/                       # ignored topic-owned projections
          readonly/                        # read-only projections for workers
            extern/                        # read-only external repository projections
          writable/                        # writable projections only with explicit policy
            extern/                        # writable external repository projections
        links/                             # ignored generated peer or topic convenience links
          peers/                           # advisory links to peer public shares
          topic/                           # advisory links to topic-owned projections
    extern/                                # default home for canonical non-main topic repositories
      <repo-label-path>/                   # supporting topic-local repository, resolved through topic.repos.<group...>.<repo-name>
  agents/                                  # Agent Workspace root
    <agent-name>/                          # Agent Workspace Git worktree and launch cwd for one named agent
  records/                                 # owner-preserved records, not normal worker input
    artifacts/                             # preserved Artifacts, Evidence Items, reports, figures, decisions, and handoff outputs
    tasks/                                 # preserved Research Task support records
    runs/                                  # preserved Run support records
    views/                                 # preserved View Manifests and GUI view material
    logs/                                  # preserved topic-level logs and diagnostics
  runtime/                                 # durable runtime support material outside state.sqlite, not normal worker input
    topic-git/                             # schema-validated optional local-tracking and publication support files
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
  - Meaning: Topic Main Development Repository.
  - Notes: Topic-owned normal, non-bare Git repository for worker-visible code-bearing topic work. Topic environment setup creates, configures, and verifies it before Agent Workspace worktrees are created. It is not a workspace.
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
- `repos/topic-main/isomer-managed/tracked/manifests/extern-projections.toml`
  - Meaning: external projection manifest.
  - Notes: Tracked metadata for external repository projections. Entries name the canonical source label, source path, projection path, intended access, projection mode, mutation policy, status, blockers, and source evidence.
- `repos/topic-main/isomer-managed/agent-owned/`
  - Meaning: Current worktree owner area.
  - Notes: Ignored material owned by the current agent worktree, including runtime, scratch, logs, unpromoted artifacts, public share, and policy-controlled inbox.
- `repos/topic-main/isomer-managed/topic-owned/`
  - Meaning: Topic-owned projections.
  - Notes: Ignored worker-visible projections of topic-owned material, split into `readonly/` and `writable/` policy surfaces.
- `repos/topic-main/isomer-managed/topic-owned/readonly/extern/`
  - Meaning: read-only external repository projections.
  - Notes: Developer-facing projections of canonical external repositories for read use. The policy is read-only even when the filesystem cannot enforce read-only access.
- `repos/topic-main/isomer-managed/topic-owned/writable/extern/`
  - Meaning: writable external repository projections.
  - Notes: Developer-facing projections for write use only when the target spec or user explicitly grants write policy. Writable projections should use a copy, dedicated clone, dedicated worktree, or another isolated materialization unless writes to the canonical source are explicitly authorized.
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

The Topic Workspace must not contain a workspace-local `teams/` directory. Domain Agent Team Templates come from Project registrations or configured Team Repositories. The one topic-specialized profile bundle lives under `team-profile/`, and runtime Agent Team Instance state lives in Workspace Runtime records plus adapter material.

Topic Publication Copies live outside Topic Workspaces under ignored Project temporary storage. They are not part of this canonical layout and do not change Topic Main, Topic Actor Workspace, or Agent Workspace topology.

## Topic Main Development Repository

`repos/topic-main` is the default Topic Main Development Repository. The semantic label is `topic.repos.main`; a Topic Workspace Manifest may bind that label to a safe custom existing repository path. Topic environment setup owns creating, configuring, and verifying this repository. Agent environment setup consumes the resulting predecessor evidence and does not initialize or repair topic-main in the normal flow.

`topic.repos.main` is the primary development repository for code-bearing topic work. Different agents work in different Git worktrees of this single repository, on agent-owned branches. Agents can inspect, fetch, merge, or otherwise integrate peer branches according to the topic's coordination rules.

Isomer-created material belongs under the resolved `topic.repos.main.isomer_managed` namespace. This keeps existing user-provided repositories root-clean: topic env setup should not add top-level `extern/`, `shared/`, `tasks/`, `runs/`, or similar Isomer directories to topic-main. Canonical external repositories stay under semantic non-main `topic.repos.*` paths, defaulting to `<topic-workspace>/repos/extern/...`, and are exposed inside topic-main only through `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, and `topic.repos.main.projections.manifest`.

`topic.repos.main` is a topic-level support surface. It is not an Agent Workspace, not Workspace Runtime state, and not a separate Topic Workspace. Its branch state is ordinary Git state. Research lifecycle branching remains represented through Research Inquiries, Research Inquiry Relationships, Research Tasks, Runs, and Decision Records, not through a domain concept named Research Branch.

## Agent Workspace Roots

An Agent Workspace is a per-agent work area inside a Topic Workspace. The `isomer-default.v1` Agent Workspace binding is:

```text
<topic-workspace>/agents/<agent-name>
```

Each Agent Workspace is a Git worktree of the prepared `topic.repos.main`, checked out to an agent-owned branch. The agent is launched with this directory as its current working directory. The launch cwd convention makes the per-agent worktree the agent's normal world: the agent should read, write, run tools, and produce local outputs from inside that directory unless an explicit workflow or topic-owned tool asks it to use another surface.

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

1. **Shared Git repository and branches**: this is the primary channel. Agents work in separate worktrees of the prepared `topic.repos.main` on separate branches. They can inspect, fetch, merge, cherry-pick, or otherwise integrate peer branches according to the topic's coordination rules.
2. **Isomer-managed untracked shares and projections**: this is the secondary channel for large or temporary material. Agents use owner-approved `isomer-managed/agent-owned/public/`, policy-controlled external repo projections under `isomer-managed/topic-owned/{readonly,writable}/extern/`, or generated `isomer-managed/links/` surfaces when peer inspection is useful before a commit or promotion.
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
  - Notes: Worker-visible projection of topic-owned or external repository material for reads only.
- `isomer-managed/topic-owned/writable/`
  - Meaning: writable topic projection.
  - Notes: Worker-visible projection for shared writes only when boundary policy grants it; external repository writes require explicit projection access intent and should use isolated writable materialization unless the user authorizes source mutation.
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

If validation detects peer writes without an explicit repair, cleanup, or integration task, Isomer should report a workspace issue or Provenance Record rather than claiming that filesystem controls prevented the write.

## Path Resolution

Commands should resolve Topic Workspace and Agent Workspace paths through Workspace Path Resolution rather than assembling paths ad hoc. The resolver uses recorded Path Plans first, then supported `ISOMER_PATH__...` semantic environment variables and compatibility `ISOMER_*` variables exported by an Execution Adapter, then Topic Workspace Manifest bindings, then Project Manifest defaults where applicable, then `isomer-default.v1`. A generated environment variable for `custom.*` applies only after the label exists in the effective catalog.

Use `isomer-cli project paths get <semantic-label>` for one path answer and `isomer-cli project paths list` to inspect known labels. These commands and `project paths preview` are read-only. Add `--configured` to `project paths get` when you need the current manifest or environment answer instead of a stored Path Plan. Use `project paths default <semantic-label>` to ask for the default-layout path of a built-in reserved label without override precedence, and use `project paths explain <semantic-label>` to inspect candidate sources and the selected source.

Use `project paths materialize-default` only when you intend to write or update `topic-workspace.toml` and create selected default directories. Use `project paths materialize <semantic-label>` to create the currently configured target for an existing label according to its `storage_profile` while ignoring stored Path Plans. Use `project paths register`, `project paths update`, `project paths unregister`, and `project paths reset` for manifest binding lifecycle operations instead of editing the manifest by hand. `unregister` removes dynamic `custom.*` and grouped repository slots; `reset` removes a built-in override. Neither command deletes filesystem targets or rewrites historical Path Plans.

Projection labels are built-in Topic Main Development Repository support surfaces. Under `isomer-default.v1`, `topic.repos.main.projections.readonly` resolves to `<resolved topic.repos.main>/isomer-managed/topic-owned/readonly/extern/`, `topic.repos.main.projections.writable` resolves to `<resolved topic.repos.main>/isomer-managed/topic-owned/writable/extern/`, and `topic.repos.main.projections.manifest` resolves to `<resolved topic.repos.main>/isomer-managed/tracked/manifests/extern-projections.toml`. Unknown labels under `topic.repos.main.*` are reserved unless the catalog defines them.

For an externally sourced non-main repository, first query its unbound candidate with `isomer-cli project paths default topic.repos.<group...>.<repo-name> --topic <topic-id>`. Acquire and verify the content outside Isomer, then call `isomer-cli project repos register <group...>.<repo-name> --topic <topic-id> --path <existing-path>`. Registration writes topology only and does not run Git or alter the existing directory. Use `project repos create` only when the intended result is a new empty support directory; it creates a directory but does not initialize or acquire Git content. Use `project paths materialize-default --label topic.repos.main` or explicit path binding commands for the built-in Topic Main Development Repository. Topic environment setup decides whether a verified Canonical External Repository also needs a read-only or writable projection inside topic-main.

For Agent Workspaces, Agent Team Instance creation records an Agent Workspace Path Plan for `agent.workspace` and support path plans for labels such as `agent.isomer_managed`, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.public_share`, and `agent.links`. An agent running inside its own Agent Workspace can query agent-scoped labels without passing an Agent Name because cwd-derived Effective Agent Context can identify the owning workspace. Cross-agent queries still require an explicit Agent Name or Agent Instance selector. Cwd inference is a convenience for path resolution, not filesystem-grade identity or access control.

Implemented Local Tmp Surface labels are `topic.tmp`, `topic.repos.main.tmp`, and `agent.tmp`. Under `isomer-default.v1`, `topic.tmp` resolves to `<topic-workspace>/tmp/`, `topic.repos.main.tmp` resolves to `<resolved topic.repos.main>/tmp/`, and `agent.tmp` resolves to `<resolved agent.workspace>/tmp/`. These labels are local, ignored, disposable, not shared, and not durable evidence unless explicitly promoted to another accepted semantic surface.

Local Tmp Surfaces are different from `agent.scratch`: scratch is agent-owned draft material that can become an intentional input to promotion, while tmp is sweepable posture for transient files. Tmp material is not Peer Read Access, generated-link target material, owner-preserved records, Workspace Runtime evidence, Provenance Records, Evidence Items, Decision Records, or Git-tracked Isomer material.

## Durability

The following Topic Workspace material is durable by default:

- Topic Workspace Pixi manifest and lockfile.
- Topic Agent Team Profile Bundle under `team-profile/`.
- Workspace Runtime `state.sqlite` and path plan records.
- Topic Main Development Repository readiness evidence from topic environment setup.
- External projection metadata in `topic.repos.main.projections.manifest`.
- Owner-preserved research records under `records/*`.
- Agent Workspace records and Agent Workspace Path Plans.
- Promoted Agent Artifacts, Evidence Items, Decision Records, and Provenance Records.
- Adapter manifests and command payload refs under `runtime/adapters/` or `records/*`.

Durable does not mean selected for reset preservation. Extension bootstrap records and user-selected research state survive a Topic Workspace reset only when `project topic-reset update-checkpoint` records their exact record ids, structured payload ids and files, export paths, semantic labels, actor refs, and provenance refs. Ordinary post-checkpoint records remain subject to the accepted reset plan.

The following material is generated, local, or policy-dependent:

- `.pixi/`.
- uncommitted scratch files inside Agent Workspaces.
- generated logs that have not been recorded as Artifacts or Provenance Records.
- untracked `isomer-managed/agent-owned/`, `isomer-managed/topic-owned/`, and generated `isomer-managed/links/` material until it is promoted or recorded.
- ordinary Git branch state inside `repos/topic-main` and per-agent worktrees, except where branch state is explicitly captured as an Artifact, Evidence Item, Decision Record, or Provenance Record.

## Breaking Generated Layout

This layout revision is breaking for generated Topic Workspace internals. Older generated `isomer-content/` material, old source gate paths, old topic-main support paths, and old projection locations may fail validation. The accepted resolution is to recreate generated topic content under the revised layout instead of preserving compatibility shims.

Older Topic Workspace drafts and fixtures may contain `repos/topic-main/shared/`, `repos/topic-main/artifacts/`, `repos/topic-main/tasks/`, `repos/topic-main/runs/`, `repos/topic-main/views/`, `repos/topic-main/logs/`, `repos/topic-main/tools/`, or `repos/topic-main/extern/` as top-level worker collaboration surfaces. These paths are replaced by `repos/topic-main/isomer-managed/tracked/`, `repos/topic-main/isomer-managed/agent-owned/`, `repos/topic-main/isomer-managed/topic-owned/{readonly,writable}/extern/`, and owner-preserved `records/*` according to ownership and durability.

Older profile or packet material may also use `agent-workspaces/`, `agents/<agent-instance-id>`, `agent-key`, or authored `agent_workspace_ref` values as the primary workspace planning language. New material should use topic-local Agent Names and derived Agent Workspace paths under `agents/<agent-name>`. Older Agent Workspace drafts may contain `.isomer-agent/` support roots; current Agent Runtime, scratch, logs, Agent Artifacts, peer-readable public shares, optional inboxes, topic projections, and generated links belong under `isomer-managed/`.
