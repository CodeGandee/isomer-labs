## Why

Topic Workspaces are already intended to be standalone Pixi workspaces by default (ADR-0027), yet every Topic Workspace currently needs an explicit `topic_standalone_pixi_bindings` entry in `.isomer-labs/manifest.toml` before `isomer-cli doctor`, `isomer-srv-env-setup`, or runtime preparation can proceed. This forces operators and skills to mutate the Project Manifest for the common case where the Topic Workspace itself is the Pixi workspace root. Isomer also should not reimplement Pixi's manifest discovery rules. Making the explicit binding target optional, and letting Pixi resolve a directory target, removes friction without weakening the rule that explicit bindings override defaults.

## What Changes

- Introduce Topic Workspace Pixi binding target resolution for `topic_standalone_pixi_bindings`. The canonical target field is `manifest_path_or_dir`, and the target may be either a manifest file or a directory to pass to Pixi.
- Replace superseded standalone Pixi binding target fields with `manifest_path_or_dir`; this is a breaking Project Manifest schema change for explicit standalone Pixi bindings.
- If an explicit binding target is a directory, Isomer asks Pixi to resolve the workspace with `pixi info --json --manifest-path <target-dir>` instead of manually searching for `pixi.toml` or `pyproject.toml`.
- Introduce an implicit default Topic Workspace Pixi binding target that applies when a registered Research Topic has a registered Topic Workspace and no explicit `topic_standalone_pixi_bindings` entry is present.
- The implicit default binding target is the registered Topic Workspace directory, with Pixi environment `default`.
- A resolved Topic Workspace Pixi binding is accepted only when Pixi resolves a manifest and environment prefix confined to the registered Topic Workspace.
- Pixi is required for binding-target resolution. If Pixi is unavailable or cannot produce usable JSON, diagnostics report a Pixi tooling failure with online and offline install guidance rather than treating the Topic Workspace as unbound.
- Explicit `topic_standalone_pixi_bindings` entries continue to take precedence over the default.
- `isomer-cli doctor` passes the topic Pixi binding check when Pixi resolves the explicit or implicit binding target as a valid Topic Workspace Pixi workspace, and reports the binding source as `explicit` or `implicit-default`.
- `isomer-srv-env-setup` accepts the implicit default and no longer blocks on a missing binding for the default layout.
- The `isomer-admin-topic-team-specialize` `ensure-topic-registration` subcommand no longer needs to create or verify a standalone Pixi binding when the default layout applies.
- ADR-0027 and the Project Manifest schema documentation are updated to describe the default.

## Capabilities

### New Capabilities

- `topic-pixi-environment-default-binding`: Resolution of Topic Workspace Pixi binding targets, including explicit file or directory targets and the implicit Topic Workspace directory default when no explicit `topic_standalone_pixi_bindings` entry exists.

### Modified Capabilities

- `isomer-cli-doctor-diagnostics`: Topic-level Pixi binding diagnostic must accept an implicit default binding and must not fail solely because the manifest lacks an explicit entry.
- `topic-team-specialization-module-skill`: The `ensure-topic-registration` subcommand must treat a missing explicit binding as acceptable when the Topic Workspace follows the default Pixi workspace layout.

## Impact

- `src/isomer_labs/manifest.py` and `src/isomer_labs/models.py`: represent explicit and implicit Topic Workspace Pixi binding targets, using `manifest_path_or_dir` as the only explicit target field.
- `src/isomer_labs/doctor.py`: update `inspect_topic_pixi` to resolve binding targets through Pixi and enforce Topic Workspace confinement.
- `src/isomer_labs/context.py`: expose the resolved Topic Workspace Pixi binding object in `EffectiveTopicContext` if not already present.
- `skillset/service/isomer-srv-env-setup/`: update skill references to accept implicit defaults.
- `skillset/operator/isomer-admin-topic-team-specialize/`: update `ensure-topic-registration` references.
- `.imsight-arts/project-explore/adrs/0027-topic-workspaces-are-default-pixi-workspaces.md`: document default binding semantics.
- Existing Project Manifest examples or tests that use superseded standalone Pixi binding target fields are updated to `manifest_path_or_dir`.
- Tests for doctor, context resolution, and topic specialization skill.
