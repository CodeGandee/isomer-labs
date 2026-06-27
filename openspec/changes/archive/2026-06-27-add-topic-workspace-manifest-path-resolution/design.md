## Context

Project Manifest already acts as the outer discovery authority: it registers Research Topics, Topic Workspaces, topic config paths, environment bindings, and profile refs. Inside a Topic Workspace, however, many surfaces are still implied by fixed directory names such as `repos/topic-main`, `records/artifacts`, `runtime`, and `agents/<agent-name>`. That makes the current contract brittle for projects that already have equivalent directories, do not need every default Isomer-managed surface, or want agents to ask for semantic locations without memorizing layout details.

Workspace Runtime path plans already give durable records a stable historical path once a runtime action depends on that path. This change adds the missing layer before runtime dependence: a topic-owned manifest that maps semantic labels to concrete paths, plus a CLI query surface that resolves those labels for users, agents, skills, and adapters.

The pending `add-local-tmp-workspace-surfaces` change should be treated as downstream of this one. Its durable rule remains useful, but `tmp/` should become semantic labels with default bindings rather than only fixed directory additions.

## Goals / Non-Goals

**Goals:**

- Make semantic workspace surface labels the user-facing path contract.
- Add a Topic Workspace Manifest at the topic level to bind those labels to concrete paths or path templates.
- Keep the current directory structure as the built-in `isomer-default.v1` layout profile.
- Let `isomer-cli` answer direct path questions such as “where is `agent.private_artifacts`?”.
- Let an agent running inside its Agent Workspace query agent-scoped labels without passing an Agent Name.
- Preserve Workspace Runtime path plans as durable historical truth after runtime records depend on a path.
- Let operators materialize the default semantic directories when they explicitly ask for the default layout.

**Non-Goals:**

- Do not remove the existing default Topic Workspace and Agent Workspace layout.
- Do not require every Topic Workspace to create every default Isomer-managed directory.
- Do not make the Topic Workspace Manifest a substitute for Workspace Runtime state, Research Topic Config, or Project Manifest registrations.
- Do not infer managed Topic Workspaces by scanning directories.
- Do not treat cwd inference as filesystem-grade identity or access control.
- Do not implement the local `tmp/` surfaces in this change; only define the semantic-path foundation they should use.

## Decisions

### Decision: Add a topic-owned manifest at a stable Topic Workspace path

The standard manifest path is fixed as `<topic-workspace>/topic-workspace.toml`. It is owned by the Topic Workspace, not by `.isomer-labs/`, because it describes topic-internal surfaces rather than Project-wide registrations. The Project Manifest registers the Topic Workspace path and must not carry a per-topic manifest path override in this change. A missing manifest means the resolver can synthesize effective bindings from the selected built-in layout profile, but mutating materialization should write the manifest before creating or depending on manifest-backed surfaces.

Alternative considered: store all surface bindings in the Project Manifest. That would make `.isomer-labs/manifest.toml` a large topic-internal path registry and would put topic-local layout decisions in the Project Config Directory.

Alternative considered: allow a rare Project Manifest override for the manifest path. That remains deferred until there is an external-root or migration policy that needs it; adding it now would create two authorities for topic-owned layout before the manifest model has shipped.

### Decision: Use semantic labels as the stable public contract

The public label grammar uses dotted labels such as `topic.main_repo`, `topic.records`, `topic.records.artifacts`, `topic.runtime`, `topic.runtime.db`, `topic.agents_root`, `agent.workspace`, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.public_share`, and `agent.links`. Existing internal surface ids such as `topic_main_repo` and `agent_workspace:<agent-name>` can remain as compatibility path-plan names during migration, but the CLI, docs, skills, and new manifest fields should present semantic labels.

Alternative considered: continue exposing only existing snake-case surface ids. That would reduce code churn but would keep users tied to implementation-oriented names and would not make agent-scoped queries feel natural.

### Decision: Keep the current layout as `isomer-default.v1`

The current directory structure becomes a default layout profile that can generate bindings when the manifest is missing or when the user asks to create default semantic directories. A project may bind only the labels it uses, and validation should distinguish an omitted optional label from a required label that fails to resolve for a command.

Alternative considered: require a complete manifest for every standard surface at topic creation time. That would make fresh topics noisier and would force users to accept many unused paths.

### Decision: Keep required labels command-scoped

There is no global "minimal Topic Workspace manifest" that must list every standard label before Workspace Runtime exists. Runtime initialization requires only the labels for paths it will create or record: `topic.runtime.db`, `topic.runtime`, `topic.records`, and the specific record-class labels the initializer enables, such as `topic.records.artifacts`, `topic.records.tasks`, `topic.records.runs`, `topic.records.views`, and `topic.records.logs`. `topic.main_repo`, `topic.team_profile_bundle`, `topic.agents_root`, and `agent.workspace` become required only for commands that create or depend on those surfaces, such as repository setup, Topic Agent Team Profile materialization, or Agent Team Instance creation.

Alternative considered: require every default-layout label before runtime initialization. That would recreate the fixed-directory contract under a new name and would work against topics that intentionally use fewer Isomer-managed parts.

### Decision: Add direct semantic query commands

`isomer-cli project paths get <semantic-label>` is the final public command for returning one resolved path plus source metadata and diagnostics. `project paths list` should list resolvable labels for the selected Topic Workspace, and `project paths materialize-default` should create selected or standard default-layout bindings and directories when the operator explicitly asks for materialization. Existing `project paths preview` can continue to show the broader effective plan. The word "resolve" remains useful for API names and documentation, but this change does not add `project paths resolve` as a second public command.

Alternative considered: make users parse `paths preview` output. That keeps the implementation small but fails the core ergonomic goal.

Alternative considered: name the public command `project paths resolve`. That better matches implementation terminology, but `get` is shorter for the user-facing question this feature is built around: "where is this semantic surface?"

### Decision: Infer Effective Agent Context from cwd when safe

For agent-scoped labels, agent identity resolution should follow this order: explicit selector, supported environment context, cwd-derived Agent Workspace match, then error. Cwd inference should use recorded Agent Workspace path plans when runtime exists, Topic Workspace Manifest `agent.workspace` bindings when they can match uniquely, and the default layout profile only when default-layout inference is active. Manifest-based reverse matching is deliberately narrow in this change: `agent.workspace` templates can use one `{agent_name}` path segment placeholder, and cwd inference may derive that segment only when exactly one canonical Agent Workspace ancestor matches. If cwd is inside `repos/topic-main`, the resolver must not infer an Agent Workspace. If cwd matches an Agent Workspace but runtime has no Agent Instance record, the resolver may infer `agent_name` without claiming an `agent_instance_id`.

Alternative considered: require `--agent` for every agent-scoped query. That is precise but awkward for launched agents and daily agent workflows.

### Decision: Detect selector conflicts instead of guessing

Explicit selectors win. If environment context says one agent and cwd matches another, the command should report a conflict unless an explicit selector chooses the intended agent. If multiple manifest templates match cwd, the command should report ambiguity. The resolver should prefer the longest valid path match only when matches are otherwise consistent.

Alternative considered: silently prefer environment over cwd. That hides launch-context bugs and makes path answers hard to trust.

### Decision: Defer manifest-backed external roots

Manifest-backed paths must remain inside the Project root, avoid `.isomer-labs/`, and avoid other registered Topic Workspaces unless a later accepted external-root policy explicitly permits a surface. Existing safe project-local directories may be bound without being moved or reinitialized, but out-of-project workspace surfaces are outside this change.

Alternative considered: support external roots immediately for projects that already keep repositories or scratch areas elsewhere. That use case is real, but it needs a separate policy for ownership, cleanup, validation, sharing, and portability.

### Decision: Runtime path plans remain durable path truth

When a runtime record, handoff, Artifact, adapter payload, or Agent Workspace record depends on a path, the selected semantic label resolution must be written as a PathPlanRecord before the dependent record is created. New semantic path plan rows must store the semantic identity in first-class `semantic_label` and `scope_ref` fields, while preserving any compatibility surface id separately for older callers and migration output. `source_detail` remains source evidence such as manifest path, layout profile, or environment variable name; it must not be the only place that stores semantic identity. Later Topic Workspace Manifest changes should produce validation diagnostics for mismatched current resolution, not silently rewrite historical records.

Alternative considered: always resolve against the latest manifest. That would make old runtime records move under the user's feet.

Alternative considered: encode semantic identity in existing `surface` and `source_detail` fields. That would reduce schema churn but would keep the durable path contract difficult to query, validate, and migrate.

### Decision: `tmp/` becomes downstream semantic labels

The later `tmp/` change should add labels such as `topic.tmp`, `topic.main_repo.tmp`, and `agent.tmp` with local, ignored, disposable semantics. Their default bindings can still be `<topic-workspace>/tmp/`, `<topic-workspace>/repos/topic-main/tmp/`, and `<topic-workspace>/agents/<agent-name>/tmp/`.

Alternative considered: add fixed `tmp/` paths now and retrofit labels later. That would make the same path policy change twice.

## Risks / Trade-offs

- Manifest drift from existing runtime records -> Validation compares current semantic resolution with stored path plans and reports drift without rewriting records.
- Cwd inference may select the wrong agent in unusual directory layouts -> Explicit selectors override inference, and ambiguous or conflicting matches become diagnostics.
- A manifest can become another file users must understand -> Fresh topics can rely on the built-in default profile until the user materializes or customizes bindings.
- Semantic labels can proliferate -> Start with a bounded built-in catalog and require new labels to have owner, durability, sharing, and scope classification.
- Flexible paths may weaken worker visibility guidance -> Labels must preserve concepts such as Topic Main Repository, Agent Workspace, private artifacts, public share, topic-owned projection, and durable records even when paths differ.
- Existing docs and skills mention hard-coded directories heavily -> Update docs and skills to teach labels first and default paths second.

## Migration Plan

1. Add Topic Workspace Manifest models, parsing, validation, and default-profile synthesis.
2. Add semantic label catalog and mapping from current internal path surfaces to public labels.
3. Update Effective Topic Context resolution to derive Effective Agent Context from explicit selectors, environment context, and cwd.
4. Add semantic path query CLI behavior and keep `paths preview` compatible.
5. Update Workspace Runtime initialization and Agent Team Instance creation to write path plans from semantic resolution.
6. Update validation to report manifest drift, missing required labels, unsafe external paths, and agent selector conflicts.
7. Update docs and operator/service skill guidance to ask for semantic labels and report default paths only as one layout profile.
8. Revise `add-local-tmp-workspace-surfaces` so it adds `tmp/` semantic labels on top of this manifest-backed model.

Rollback before runtime schema changes is low risk: remove the new manifest/query code and keep default path resolution. After runtime path plans record `semantic_label` and `scope_ref` metadata, rollback should preserve existing path plan rows and ignore the extra metadata rather than deleting runtime history.
