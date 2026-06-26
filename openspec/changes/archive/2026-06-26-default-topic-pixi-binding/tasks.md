## 1. Model and Pixi Binding Target Resolution

- [x] 1.1 Add an effective Topic Workspace Pixi binding target helper that returns an explicit active `topic_standalone_pixi_bindings` target or defaults to the registered Topic Workspace directory when no explicit binding exists.
- [x] 1.2 Add `manifest_path_or_dir` as the explicit standalone Pixi binding target field, allowing targets to be either manifest files or directories.
- [x] 1.3 Implement a Pixi-backed resolver that runs `pixi info --json --manifest-path <binding-target>` and records the target path, target kind, resolved manifest path, selected environment, environment prefix, and source.
- [x] 1.4 Enforce Topic Workspace confinement for the resolved manifest path and selected environment prefix.
- [x] 1.5 Ensure the effective binding preserves the `source` distinction between `explicit` and `implicit-default`.
- [x] 1.6 Treat missing Pixi, Pixi execution failure, invalid Pixi JSON, and missing required Pixi JSON fields as Pixi tooling failures rather than missing bindings.
- [x] 1.7 Reject superseded explicit standalone Pixi binding target fields such as `manifest_path` and `path` with clear validation diagnostics.
- [x] 1.8 Add unit tests for explicit file targets, explicit directory targets, implicit Topic Workspace directory defaults, fixed implicit `default` environment, explicit override, unresolvable targets, Pixi tooling failures, superseded target field rejection, and confinement failures.

## 2. Doctor Diagnostics

- [x] 2.1 Update `inspect_topic_pixi` in `src/isomer_labs/doctor.py` to use the effective standalone binding target and Pixi-backed resolver.
- [x] 2.2 Emit a passing `topic.pixi.standalone.default` check when the implicit Topic Workspace directory target resolves through Pixi.
- [x] 2.3 Update failure messages to name the binding target and distinguish Pixi tooling failures, unresolvable targets, and confinement failures.
- [x] 2.4 Add online and offline Pixi install guidance to Pixi tooling failure diagnostics.
- [x] 2.5 Add unit tests for doctor output with implicit default binding, explicit `manifest_path_or_dir` file target, explicit `manifest_path_or_dir` directory target, explicit binding precedence, missing default target resolution, Pixi tooling failure, and confinement failure.

## 3. Service Environment Setup Skill

- [x] 3.1 Update `isomer-srv-env-setup` skill references (`resolve-workspace.md`, `setup-for-topic-workspace.md`) to describe `manifest_path_or_dir`, explicit file or directory targets, and implicit Topic Workspace directory default acceptance.
- [x] 3.2 Adjust skill guardrails so that missing explicit binding is not a blocker when Pixi resolves the registered Topic Workspace directory as a confined Pixi workspace.
- [x] 3.3 Add skill-level examples showing explicit file target, explicit directory target, and implicit Topic Workspace directory default resolution.

## 4. Topic Team Specialization Skill

- [x] 4.1 Update `setup-topic-env.md` reference in `isomer-admin-topic-team-specialize` to remove the requirement for an explicit binding when Pixi resolves the registered Topic Workspace directory as a confined Pixi workspace.
- [x] 4.2 Update `ensure-topic-registration.md` reference (if present) to state that standalone Pixi binding verification accepts explicit `manifest_path_or_dir` file targets, explicit `manifest_path_or_dir` directory targets, or the implicit Topic Workspace directory default.
- [x] 4.3 Update skill validation expectations in `tests/unit/test_validate_skillsets.py` if any binding-specific guardrail text changed.

## 5. Documentation and ADRs

- [x] 5.1 Update `.imsight-arts/project-explore/adrs/0027-topic-workspaces-are-default-pixi-workspaces.md` to document implicit default binding semantics.
- [x] 5.2 Update relevant `docs/` pages (`assumptions-and-roadmap.md`, `isomer-cli.md`, `runtime-and-files.md`) to mention `manifest_path_or_dir`, the implicit Topic Workspace directory default, fixed implicit `default` environment, and Pixi install guidance.

## 6. Validation

- [x] 6.1 Run `pixi run test` and ensure existing tests pass.
- [x] 6.2 Run `pixi run lint` and `pixi run typecheck`.
- [x] 6.3 Run `openspec validate default-topic-pixi-binding --strict` and fix any schema or scenario-format errors.
