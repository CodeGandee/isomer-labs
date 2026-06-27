## Context

The canonical language already names Topic Workspace paths through Semantic Workspace Surface Labels and Workspace Path Resolution. The current implementation has a built-in `SemanticSurface` catalog, Topic Workspace Manifest bindings, `project paths get/list/preview/materialize-default`, compatibility surface ids, supported `ISOMER_*` environment variables, and Workspace Runtime Path Plans. Those pieces work for the default layout, but the contract remains leaky: several default child surfaces encode `repos/topic-main/...` directly, user-defined labels are rejected as unknown, environment overrides are bounded to hand-written mappings, and docs or skills can still imply that agents may remember default paths.

This change treats Workspace Path Resolution as the storage-layer contract without introducing a replacement domain term. The public API is a semantic label plus scope context. Physical paths are resolved answers with source metadata and storage-profile-derived traits.

```text
caller
  |
  v
semantic label + required context selectors
  |
  v
Workspace Path Resolution
  |
  +-- recorded Path Plan
  +-- supported environment override
  +-- Topic Workspace Manifest binding
  +-- Project Manifest default where applicable
  +-- isomer-default.v1 binding
  |
  v
resolved path + source + storage_profile + expanded storage profile traits
```

## Goals / Non-Goals

**Goals:**

- Make Semantic Workspace Surface Labels the only public path contract for Project, Topic Workspace, and Agent Workspace storage surfaces.
- Allow topic owners to bind built-in labels to custom safe project-local paths through `topic-workspace.toml`.
- Allow topic owners to declare `custom.*` labels with explicit storage profiles.
- Define create, read, update, and delete behavior for semantic path bindings without making filesystem deletion part of normal binding management.
- Derive default child surfaces from resolved parent labels where the relationship is semantic, especially `topic.repos.main` children.
- Provide a general 12-factor environment override convention for any supported semantic label while preserving existing compatibility variables.
- Expose enough CLI evidence for agents and services to query paths instead of assembling them.
- Preserve Path Plans as durable historical snapshots for records that already depend on paths.

**Non-Goals:**

- This change does not add filesystem-grade access control or sandboxing.
- This change does not allow arbitrary external storage roots by default.
- This change does not replace Project Manifest discovery authority for Topic Workspaces.
- This change does not migrate or move existing user files automatically.
- This change does not add generic destructive filesystem deletion for registered storage targets.
- This change does not remove compatibility surface ids or existing `ISOMER_*` path variables.

## Decisions

### Decision 1: Workspace Path Resolution Is the Storage API

Agents, services, skills, and adapter code must request paths by semantic label through `isomer-cli project paths get/list/preview` or the equivalent resolver API. Documentation may show concrete directories only as `isomer-default.v1` examples.

Alternative considered: document the default layout more carefully while keeping default path assembly in skills and scripts. That would preserve the coupling that caused the problem, so it does not solve customization.

### Decision 2: Bindings Use Label, Path, and storage_profile

User-authored Topic Workspace Manifest bindings must use a compact schema:

```toml
[[bindings]]
label = "topic.repos.custom_repo"
path = "repos/custom-repo"
storage_profile = "topic_repo"
```

`label` is the stable semantic name. `path` is the concrete storage location. `storage_profile` names an Isomer-defined storage profile that owns the storage semantics.

Bindings must not duplicate storage profile traits such as required context, owner, durability, sharing, path kind, lifecycle, visibility, safety policy, or Git semantics. The resolver may expose expanded storage profile traits in output, and Workspace Runtime may snapshot those traits for audit, but `storage_profile` remains the source of truth for binding semantics.

Examples of storage profile traits include:

```text
storage_profile: topic_repo
  context: topic
  kind: repository
  lifecycle: durable
  visibility: topic
  safety_policy: topic_workspace_local
  git_semantics: repository

storage_profile: agent_disposable_dir
  context: agent
  kind: directory
  lifecycle: disposable
  visibility: private
  safety_policy: agent_workspace_local
```

Alternative considered: store `required_context`, `owner`, `durability`, `sharing`, and `path_kind` directly on every binding. That duplicates storage profile functionality, makes manifests noisy, and creates drift when a binding field disagrees with its storage profile.

### Decision 3: Effective Catalog Combines Built-ins and Manifest-declared Custom Labels

The resolver will build an effective catalog from the built-in `SemanticSurface` catalog plus valid custom labels declared in the Topic Workspace Manifest. Built-in labels keep their current storage profile unless the manifest overrides their path binding with another accepted storage profile. Custom labels must use `custom.*` and must declare a valid `storage_profile`.

This namespace keeps future Isomer-owned labels free while still giving users real semantic extension points. Later extension systems can add registered provider namespaces through a separate accepted design, but arbitrary user-defined semantics stay under `custom.*`.

Alternative considered: allow any dotted label. That makes collisions with future built-ins likely and weakens validation.

### Decision 4: Label Roots Declare Required Context and Reserved Ownership

Semantic label roots are not implicitly topic-scoped. They declare which context selectors the resolver needs:

```text
project.*  -> requires Project context only
topic.*    -> requires Effective Topic Context
agent.*    -> requires Effective Topic Context and Effective Agent Context
custom.*   -> requires the context declared by the binding's storage_profile
```

When `isomer-cli` is invoked inside a Topic Workspace, it may infer the selected Research Topic and Topic Workspace for `topic.*` and `agent.*` labels. When invoked from the Project root, outside a Topic Workspace, or from an ambiguous location, callers must pass an explicit topic selector before resolving `topic.*`, `agent.*`, or `custom.*` labels whose storage profile requires topic context.

The first label segment is a reserved namespace root. Isomer owns `project`, `topic`, and `agent`. The `custom` root is reserved as the only user-defined semantic namespace. Unknown roots and undeclared labels below reserved roots are rejected unless an accepted Isomer rule defines that grouped label family.

Alternative considered: treat all labels in a Topic Workspace Manifest as topic-scoped by default. That blocks future project-level storage labels and makes `topic.*` redundant instead of meaningful.

### Decision 5: Topic Repositories Use a Grouped Reserved Label Family

Repository storage under a Topic Workspace uses the reserved `topic.repos.*` family. The canonical Topic Main Repository label is `topic.repos.main`; the previous `topic.main_repo` label is not retained by this change.

Grouped repository labels may contain nested dotted groups, such as:

```text
topic.repos.main
topic.repos.inner_group.some_repo_name
```

Each repository slot still requires a catalog or manifest binding with an accepted `storage_profile` before it becomes effective. The grouping syntax is semantic, not a direct directory contract.

Alternative considered: keep `topic.main_repo` and add `topic.repos.main` as an alias. That would carry two labels for the same storage surface into the new contract and weaken the namespace cleanup.

### Decision 6: Parent-derived Defaults Replace Hard-coded Child Paths

Some default labels semantically live below another resolved label. For those labels, the default binding must be computed from the parent result, not from a duplicated physical default string. The first required parent-derived family is:

```text
topic.repos.main
  topic.repos.main.tmp
  topic.repos.main.isomer_managed
    topic.repos.main.tracked
      topic.repos.main.tracked.shared
      topic.repos.main.tracked.artifacts
      topic.repos.main.tracked.tasks
      topic.repos.main.tracked.runs
      topic.repos.main.tracked.views
      topic.repos.main.tracked.tools
      topic.repos.main.tracked.boundaries
      topic.repos.main.tracked.manifests
```

When `topic.repos.main` resolves to `source/main`, default child labels resolve under `source/main`, not under `repos/topic-main`. Agent support labels already mostly behave this way through the resolved `agent.workspace`; the implementation should make that relationship explicit in the catalog model.

Alternative considered: require every child label to be repeated in the manifest when a parent is customized. That is tedious and easy to get wrong.

### Decision 7: CLI Exposes Default Paths, Default Materialization, and Binding Registration

System-defined reserved labels that have default-layout bindings must support an explicit default-path query. This query answers the built-in/default-layout path for the selected context and ignores Path Plans, environment overrides, and Topic Workspace Manifest bindings.

```bash
isomer-cli project paths default topic.repos.main --topic <topic-id>
```

Reserved labels with default path definitions must also support default materialization. Materialization creates the default filesystem path for that label, using the label's storage profile to decide whether to create a directory, file parent, repository surface, or other supported path kind. It does not invent new semantic labels.

```bash
isomer-cli project paths materialize-default topic.repos.main --topic <topic-id>
```

Users must also be able to register path bindings through `isomer-cli` instead of editing `topic-workspace.toml` directly. Registration validates the label namespace, storage profile, path safety, duplicate binding status, and context requirements before writing the manifest. With `--create`, registration also creates the target path according to the storage profile.

```bash
isomer-cli project paths register topic.repos.custom_repo \
  --path repos/custom-repo \
  --storage-profile topic_repo \
  --create
```

For grouped repository labels, a repository-specific command may wrap the same registration flow:

```bash
isomer-cli project repos create custom_repo
```

That command is equivalent to registering `topic.repos.custom_repo` with a generated default path such as `repos/custom_repo`, `storage_profile = "topic_repo"`, and `--create`. The semantic contract remains the path binding; the repository command is a convenience.

Alternative considered: require users to create directories manually and edit `topic-workspace.toml`. That keeps the manifest correct but makes the storage contract harder to discover and easier to mistype.

### Decision 8: Semantic Label CRUD Mutates Bindings; Materialization Mutates Filesystem

The storage-layer lifecycle must distinguish three objects:

```text
semantic label definition -> Isomer-owned catalog entry, accepted grouped label family, or manifest-declared custom label
path binding record       -> label + path + storage_profile
filesystem target         -> directory, repository, file parent, runtime database path, or other storage-profile-defined target
```

Create, read, update, and delete operations apply to path binding records. They do not directly create or destroy semantic label definitions except where a manifest binding is the source of a dynamic label, and they do not delete filesystem content.

The CLI lifecycle is:

```bash
isomer-cli project paths register <label> --path <path> --storage-profile <id> [--create]
isomer-cli project paths update <label> --path <path> [--storage-profile <id>] [--create]
isomer-cli project paths unregister <label>
isomer-cli project paths reset <label>
isomer-cli project paths materialize <label>
```

`register` creates a user-controlled binding after validation. For `custom.*`, the binding also creates the label identity. For accepted grouped reserved families such as `topic.repos.*`, the binding creates a concrete label slot inside the Isomer-owned family. For built-in labels, registration creates a user override binding only when that label permits user rebinding.

`update` changes an existing user-controlled binding. It may change `path` and may change `storage_profile` only to another accepted profile for that label family. It does not move existing files, and it does not rewrite historical Path Plans. An implementation may spell replacement as `register --replace`, but the operation must remain explicit.

`unregister` removes a user-controlled binding. For `custom.*` labels and dynamic grouped labels without a built-in default, the label disappears from the effective catalog after unregistering. For built-in labels, callers should use `reset`, which removes the manifest override and lets remaining precedence sources apply, such as environment overrides or default-layout bindings. Built-in label definitions cannot be deleted.

`materialize` creates the currently configured filesystem target for an existing effective label according to its storage profile, ignoring stored Path Plans unless a later explicit recorded-target mode is added. `materialize-default` remains the operation for creating the default-layout target of a reserved label with a default definition. Neither operation deletes old targets.

Read operations are side-effect-free:

```bash
isomer-cli project paths list
isomer-cli project paths get <label>
isomer-cli project paths explain <label>
isomer-cli project paths default <label>
```

Environment variables are transient resolution candidates. They do not create, update, or delete binding records. A generated environment variable for `custom.datasets.raw` is valid only if `custom.datasets.raw` already exists in the effective catalog.

Destructive filesystem cleanup is intentionally outside generic binding CRUD. If Isomer later supports deleting a repository, records root, runtime support directory, Agent Workspace, or custom storage surface, that operation must be separate, storage-profile-aware, explicit about data loss, and gated where the profile is durable or shared.

Alternative considered: model CRUD as direct filesystem CRUD on the resolved path. That makes a normal configuration operation too dangerous because deleting or changing a binding could accidentally delete durable research evidence, repositories, or historical runtime material.

### Decision 9: Environment Overrides Use a Universal Semantic Convention

For every effective semantic label, Workspace Path Resolution will support a generated path environment variable:

```text
topic.repos.main -> ISOMER_PATH__TOPIC__REPOS__MAIN
topic.records.artifacts -> ISOMER_PATH__TOPIC__RECORDS__ARTIFACTS
agent.private_artifacts -> ISOMER_PATH__AGENT__PRIVATE_ARTIFACTS
custom.datasets.raw -> ISOMER_PATH__CUSTOM__DATASETS__RAW
```

Existing variables such as `ISOMER_TOPIC_MAIN_REPO_DIR` remain compatibility aliases. If a canonical semantic env var and a compatibility env var are both set to different paths for the same label, the resolver reports a conflict instead of guessing.

Alternative considered: keep only the hand-written environment map. That blocks user-defined semantic labels and does not scale.

### Decision 10: Path Plans Are Recorded Mode, Configured Resolution Is Current Mode

`project paths get <label>` remains recorded-aware by default: if a matching Path Plan exists for the selected scope, it wins. This protects durable records. The CLI will also expose current configured resolution that ignores stored Path Plans, either as `project paths get <label> --configured` or an equivalent option chosen during implementation. `project paths explain <label>` should show all candidates and the reason the winner won.

This makes drift explainable:

```text
recorded mode:   path_plan -> old/path
configured mode: manifest  -> new/path
validation:      drift diagnostic, no automatic rewrite
```

Alternative considered: always use the latest manifest. That silently rebases durable records onto new paths and risks losing the ability to locate historical evidence.

### Decision 11: Durable File Locators Preserve Semantic Surface Evidence

When an Artifact, Provenance Record, adapter payload ref, or runtime record depends on a project-local file, the durable record should preserve the semantic label and Path Plan id when available, plus the relative path beneath that surface. Absolute paths can remain in resolved output for operator visibility, but they should not be the only durable identity for project-local files.

Alternative considered: keep storing only absolute paths. That works until a Topic Workspace moves, a content root changes, or a custom binding is introduced.

### Decision 12: Validation Blocks Unsafe Bindings and Reports Missing storage_profile

Manifest validation must reject unsafe bindings outside the Project root, inside the Project Config Directory, inside another Topic Workspace, or outside the selected Topic Workspace for agent-scoped labels unless a later external-root policy explicitly permits them. A binding without a valid `storage_profile` is invalid because downstream code cannot know the storage-profile-derived context, kind, lifecycle, visibility, safety policy, or Git semantics for that surface.

Alternative considered: infer storage profile traits from the path, such as treating paths under `records/` as durable or paths with `{agent_name}` as agent-scoped. That makes directory shape a hidden source of semantic truth and breaks when users choose different layouts.

## Risks / Trade-offs

- Custom labels can become a loose escape hatch -> restrict arbitrary user-defined semantics to `custom.*`, require accepted `storage_profile` values, and validate boundaries.
- Parent-derived defaults can produce surprising paths when a parent binding changes -> report source details and add `paths explain` so operators can see the derivation.
- Binding unregister/reset can be mistaken for filesystem cleanup -> document that binding deletion leaves files untouched and reserve destructive cleanup for separate profile-aware commands.
- Environment overrides can hide manifest mistakes -> emit source detail for every override and report conflicts between aliases.
- Path Plan versus configured resolution can confuse users -> document recorded mode and configured mode in CLI docs and runtime docs.
- Storing semantic locator evidence touches several runtime paths -> implement incrementally by preserving current fields and adding semantic metadata where records already carry Path Plan refs.

## Migration Plan

1. Keep existing manifests, compatibility surface ids, Path Plans, and environment variables valid.
2. Add storage profile definitions and compact binding parsing before changing existing callers.
3. Add reserved namespace parsing, grouped label validation, and effective catalog validation before changing existing callers.
4. Rename the canonical Topic Main Repository label to `topic.repos.main` and update dependent child labels without retaining `topic.main_repo`.
5. Convert default child resolution to parent-derived behavior while keeping `isomer-default.v1` output unchanged when parents use default bindings.
6. Add default-path query, default materialization, and CLI registration flows.
7. Add binding lifecycle commands for register, update, unregister, reset, and configured-target materialization.
8. Add universal semantic env var support and conflict diagnostics.
9. Add configured/explain path CLI behavior and update docs.
10. Update runtime recording and validation to preserve semantic locator evidence for new records while leaving historical rows intact.
11. Update skills and validation scripts so workflow text rejects default-path-only guidance.

Rollback is straightforward because no automatic file moves are part of this design. If a later step fails, existing Path Plans and compatibility env variables continue to resolve previous paths.

## Open Questions

- Should the configured path query be spelled `project paths get <label> --configured`, `project paths configured <label>`, or `project paths explain <label> --ignore-path-plan`?
- Which existing durable record types should receive semantic locator fields in the first pass beyond records that already reference Path Plans?
