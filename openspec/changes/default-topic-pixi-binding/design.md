## Context

ADR-0027 established that every Topic Workspace is a standalone Pixi workspace by default. The Project Manifest still records explicit relationships through a `topic_standalone_pixi_bindings` table. For the common case where the Topic Workspace directory itself is the Pixi workspace root, the explicit entry adds boilerplate without adding information. The current implementation in `isomer-cli doctor`, `isomer-srv-env-setup`, and the topic-team specialization skill treats a missing explicit binding as a hard blocker, which forces hand-written manifest edits or additional registration surfaces for the default layout. The previous draft also described manually checking `pixi.toml` and `pyproject.toml`, but Pixi already owns that resolution logic.

## Goals / Non-Goals

**Goals:**

- Allow `topic_standalone_pixi_bindings` to be omitted when the registered Topic Workspace directory is itself a valid Pixi workspace root.
- Replace superseded explicit standalone Pixi binding target fields with the canonical `manifest_path_or_dir` field.
- Allow explicit `topic_standalone_pixi_bindings.manifest_path_or_dir` targets to be either manifest files or directories.
- Use Pixi to resolve directory binding targets instead of reimplementing Pixi manifest discovery in Isomer.
- Define the default binding target as the registered Topic Workspace directory when no explicit standalone Pixi binding exists.
- Use Pixi environment `default` for implicit bindings.
- Require resolved Topic Workspace Pixi manifests and environment prefixes to stay confined to the registered Topic Workspace.
- Keep explicit bindings authoritative: an explicit `topic_standalone_pixi_bindings` entry always overrides the default.
- Update `doctor`, `isomer-srv-env-setup`, and `isomer-admin-topic-team-specialize` to accept the implicit default.
- Preserve existing validation behavior for malformed explicit bindings.

**Non-Goals:**

- Changing the Project-level Pixi environment binding semantics (`topic_pixi_environment_bindings`).
- Adding implicit defaults for Project-root Pixi environment bindings.
- Auto-creating a Pixi manifest when none exists.
- Supporting per-Agent-Workspace default Pixi manifests.
- Removing the explicit binding table from the manifest schema.
- Preserving superseded standalone Pixi binding target aliases such as `manifest_path` or `path`.

## Decisions

### Binding target selection is separate from Pixi resolution

The manifest model layer will select an effective Topic Workspace Pixi binding target for a Research Topic. If an active explicit `topic_standalone_pixi_bindings` entry exists, its `manifest_path_or_dir` value is the target. Superseded `manifest_path` and `path` target fields are rejected instead of accepted as compatibility aliases. If no active explicit entry exists, the target is the registered Topic Workspace directory and the source is `implicit-default`.

```python
# Pseudo-code
def effective_topic_standalone_pixi_binding_target(
    self, topic_id: str, workspace_path: Path
) -> TopicPixiBindingTarget | None:
    explicit = self.active_topic_standalone_pixi_bindings(topic_id)
    if explicit:
        return TopicPixiBindingTarget(
            research_topic_id=topic_id,
            target_path_input=explicit[0].manifest_path_or_dir_input,
            pixi_environment=explicit[0].pixi_environment or "default",
            source="explicit",
        )
    return TopicPixiBindingTarget(
        research_topic_id=topic_id,
        target_path_input=str(workspace_path.relative_to(project_root)),
        pixi_environment="default",
        source="implicit-default",
    )
```

Pixi resolution then runs against that target rather than living inside the manifest dataclass. This preserves a pure manifest-selection step while keeping Pixi-specific behavior in the diagnostics/runtime resolution layer.

Rationale: centralizing target selection prevents drift between `doctor`, `isomer-srv-env-setup`, and runtime code, while avoiding subprocess behavior inside basic model objects.

### Pixi is required for binding resolution

Topic Workspace Pixi binding resolution requires a working Pixi executable. If Pixi is missing, cannot be executed, returns invalid JSON, or lacks the fields needed to identify `project_info.manifest_path` and the selected environment prefix, Isomer reports a Pixi tooling diagnostic instead of reporting “no effective binding.” The diagnostic includes online guidance for installing Pixi from the normal distribution channel and offline guidance to provision a pre-downloaded Pixi executable on `PATH` before rerunning the command.

Rationale: a missing Pixi executable is a host setup problem, not evidence that the Topic Workspace lacks a Pixi binding. Failing closed keeps diagnostics honest and makes the operator fix the required toolchain first.

### Pixi resolves file and directory targets

The resolver will pass the selected binding target to Pixi, for example `pixi info --json --manifest-path <target>`. A target can be a manifest file such as `pixi.toml` or `pyproject.toml`, or a directory that Pixi treats as a workspace root. Isomer accepts the result only when Pixi returns `project_info.manifest_path` and the selected environment in `environments_info`.

Rationale: Pixi owns its manifest discovery behavior. Isomer should validate that the resolved workspace belongs to the Topic Workspace rather than duplicate Pixi's file-selection rules.

### Topic Workspace confinement is mandatory

For both explicit and implicit standalone bindings, Isomer must canonicalize the binding target, Pixi's resolved manifest path, and the selected environment prefix. The target must remain inside the Project root. The resolved manifest path and environment prefix must remain inside the registered Topic Workspace; the expected prefix shape is under `<topic-workspace>/.pixi/`, normally `<topic-workspace>/.pixi/envs/<environment>`.

Rationale: this allows directory targets while preventing a Topic Workspace binding from accidentally selecting a Project-root Pixi workspace, a sibling topic workspace, or a global Pixi environment.

### Default binding is reported with source `implicit-default`

Consumers such as `doctor` and `isomer-srv-env-setup` should distinguish between explicit and implicit bindings so operators can see when the default is in use. The resolved binding should also report the original target, target kind (`file` or `directory`), Pixi's resolved manifest path, selected environment, and environment prefix.

Rationale: transparency. A silent default can surprise users when they later add an explicit binding and behavior changes.

### Resolved binding object is the shared contract

Consumers should share one resolved Topic Workspace Pixi binding object rather than recomputing binding details independently. The object includes `source`, `target_path`, `target_kind`, `resolved_manifest_path`, `pixi_environment`, and `environment_prefix`. `doctor`, `EffectiveTopicContext`, runtime readiness records, and service setup handoff material may render different subsets for users, but they should derive them from the same resolved object.

Rationale: the binding source and confinement checks matter to later service work. A shared payload prevents doctor, runtime readiness, and service setup from drifting.

### `doctor` treats a valid implicit default as a pass

`inspect_topic_pixi` will check the effective binding target rather than only explicit bindings. When no explicit binding exists but Pixi resolves the registered Topic Workspace directory as a confined Pixi workspace, it emits a passing check with source `implicit-default`. When no explicit binding exists and Pixi cannot resolve the Topic Workspace directory, it fails with a clear message naming the Topic Workspace directory as the default binding target.

Rationale: the default is the new normal; failure should only happen when the workspace truly lacks a Pixi manifest.

### `ensure-topic-registration` no longer blocks on missing bindings

The `isomer-admin-topic-team-specialize` skill's `ensure-topic-registration` subcommand currently plans to verify the standalone Pixi binding. With this change, it only needs to verify that the Research Topic and Topic Workspace are registered. The environment setup step will handle the implicit default.

Rationale: registration assurance and environment setup are separate concerns; the default binding removes the need to couple them.

## Risks / Trade-offs

- [Risk] Users may be unaware that the Topic Workspace directory is being used as the implicit Pixi binding target. → Mitigation: `doctor` and `isomer-srv-env-setup` report the binding source as `implicit-default`, original target, and resolved manifest path.
- [Risk] A directory binding might accidentally resolve to an ancestor Project-root Pixi workspace if a consumer relies on current-directory discovery. → Mitigation: every resolver call passes `--manifest-path <binding-target>` explicitly and rejects resolved manifests or environment prefixes outside the Topic Workspace.
- [Risk] Pixi CLI output may change across Pixi versions. → Mitigation: parse only stable JSON fields needed for manifest path, environment name, and prefix, and fail closed when the required fields are absent.
- [Risk] The implicit directory default may confuse users who intended to use the Project-root environment. → Mitigation: `topic_pixi_environment_bindings` still exists for Project-root environments, and explicit standalone bindings override the default.
- [Risk] Multiple consumers must be updated consistently. → Mitigation: centralize target selection and Pixi resolution helpers, then update each consumer to use the resolved binding object.

## Migration Plan

No runtime migration is required for Workspaces that rely on the implicit Topic Workspace directory default. This is a breaking Project Manifest schema change for explicit `topic_standalone_pixi_bindings`: existing entries that use superseded target fields such as `manifest_path` or `path` must be rewritten to `manifest_path_or_dir`. Explicit bindings may point directly at `pixi.toml`, at Pixi-enabled `pyproject.toml`, or at a Topic Workspace directory. After the code change, Topic Workspaces that Pixi recognizes from their registered directory will immediately pass `doctor` and `isomer-srv-env-setup` without a manifest edit.

## Resolved Questions

- Pixi is mandatory for binding-target resolution; missing or unusable Pixi is a tooling diagnostic with online and offline install guidance.
- The implicit default uses Pixi environment `default`.
- `topic_pixi_environment_bindings` remain explicit Project-root bindings and do not receive implicit defaults in this change.
- The shared resolved binding object includes source, target path, target kind, resolved manifest path, Pixi environment, and environment prefix.
- The explicit target field is `manifest_path_or_dir`; superseded standalone Pixi binding target aliases are rejected as a breaking cleanup.
- Existing docs that state only explicit bindings are valid will be updated during implementation, not in this planning-only edit.
