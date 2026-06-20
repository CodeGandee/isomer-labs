## 1. Domain Models and Parsing

- [x] 1.1 Add typed models for Domain Agent Team Template refs, template package metadata, template artifacts, Agent Role definitions, Workflow Stage routes, template parameters, and template validation reports.
- [x] 1.2 Add typed models for Topic Agent Team Profile refs, profile records, selected roles, role bindings, expected Artifacts, profile constraints, fanout policy, and profile validation reports.
- [x] 1.3 Add structured TOML and JSON parsing helpers for generated `deepsci-org` execplan files while preserving source path metadata for diagnostics.
- [x] 1.4 Add diagnostic codes for template registration, template validation, profile specialization, profile isolation, and template/profile boundary violations.

## 2. Domain Agent Team Template Registration

- [x] 2.1 Implement built-in discovery for the seed `deepsci-org` Domain Agent Team Template at `teams/deepsci-org/execplan/`.
- [x] 2.2 Implement Project Manifest parsing for optional Domain Agent Team Template refs with stable ids, source paths, source kind, schema version, and enabled status.
- [x] 2.3 Validate template source paths are project-scoped unless they are recognized built-in template sources.
- [x] 2.4 Validate duplicate Domain Agent Team Template ids and report Project Manifest diagnostics.
- [x] 2.5 Ensure template registration does not copy template files into Topic Workspaces or create Workspace Runtime state.

## 3. Template Package Validation

- [x] 3.1 Validate `teams/deepsci-org/execplan/manifest.toml` metadata, source posture, generated stage list, and artifact path list.
- [x] 3.2 Validate the `deepsci-org` participant contract, including the seven role ids, required status, role kinds, scalable flags, required skills, optional skills, Capability Binding placeholders, and Skill Binding Projection placeholders.
- [x] 3.3 Validate role profile files and notifier prompt files referenced by `execplan/agents/bindings.toml`.
- [x] 3.4 Validate generated skill package paths, harness schema paths, workspace contract, state contract, and run contract exist and are readable.
- [x] 3.5 Validate topic-specific placeholders are accepted at the template layer while concrete Research Topic, Topic Workspace, Topic Agent Team Profile, Agent Team Instance, mailbox, gateway, credential, launch, or Run truth is rejected.
- [x] 3.6 Integrate optional generated harness validation output from `teams/deepsci-org/execplan/harness/bin/deepsci-org validate` as additional diagnostics.

## 4. Template CLI Surface

- [x] 4.1 Add Click commands for `isomer-cli team-templates list`, `isomer-cli team-templates inspect <template-id>`, and `isomer-cli team-templates validate <template-id>`.
- [x] 4.2 Add deterministic text and JSON rendering for template list, inspect, and validate outputs.
- [x] 4.3 Ensure template CLI commands reuse existing Project selection, `--project`, `--manifest`, `--format`, and `--json` behavior.
- [x] 4.4 Ensure template CLI diagnostics use Isomer diagnostic codes rather than Click parser errors for domain validation failures.

## 5. Manifest, Topic Config, and Effective Context Extensions

- [x] 5.1 Extend Project Manifest parsing for optional Topic Agent Team Profile refs with stable ids, source paths, template refs, Research Topic associations, and schema versions.
- [x] 5.2 Extend Research Topic Config parsing for default Domain Agent Team Template refs, default Topic Agent Team Profile refs, policy refs, provider refs, Capability Binding refs, and Skill Binding Projection refs.
- [x] 5.3 Validate Topic Agent Team Profile paths are project-scoped and are not located under a Topic Workspace `teams/` directory.
- [x] 5.4 Validate each Research Topic Config default Topic Agent Team Profile belongs to the same Research Topic and specializes a registered Domain Agent Team Template.
- [x] 5.5 Extend Effective Topic Context output to include selected Domain Agent Team Template refs, selected Topic Agent Team Profile refs, profile selection source, and related policy or binding refs.
- [x] 5.6 Add deterministic profile selection precedence from explicit selectors, Research Topic Config defaults, Project Manifest defaults, and template defaults.

## 6. Topic Agent Team Profile Specialization

- [x] 6.1 Implement `isomer-cli team-profiles specialize` to derive a candidate profile from `deepsci-org`, Effective Topic Context, selected role options, expected Artifacts, policy refs, binding refs, and Agent Workspace refs.
- [x] 6.2 Implement `isomer-cli team-profiles validate` for existing profile files and generated profile previews.
- [x] 6.3 Validate required profile placeholders resolve or produce bounded diagnostics without requiring launch-time Agent Team Instance, mailbox, gateway, live Houmao agent, or adapter launch refs.
- [x] 6.4 Validate required role activation, role binding consistency, required skills, optional skills, reviewer read-access policy, manual-mode defaults, and automatic-mode opt-in refs.
- [x] 6.5 Validate task-level fanout policy for `deepsci-org-experimenter` and `deepsci-org-analyzer`, including Research Task Parallel Execution Scope and distinct Agent Workspace refs or allocation rules.
- [x] 6.6 Reject runtime truth, live adapter state, command outputs, rich research records, and secret-like fields from Topic Agent Team Profile files.

## 7. Multi-Topic and Use-Case Fixtures

- [x] 7.1 Add fixture Projects with at least two Research Topics specializing the same `deepsci-org` Domain Agent Team Template with distinct profile ids, Topic Workspace refs, Agent Workspace refs, policies, and expected Artifacts.
- [x] 7.2 Add static UC-01 Topic Agent Team Profile fixtures for exploring a new research direction.
- [x] 7.3 Add static UC-02 Topic Agent Team Profile fixtures for baseline reproduction and optimization.
- [x] 7.4 Add static UC-03 Topic Agent Team Profile fixtures for paper revision planning.
- [x] 7.5 Add static UC-05 Topic Agent Team Profile fixtures for mixed manual and automatic Runs.
- [x] 7.6 Add negative fixtures for duplicate profile ids, cross-topic Topic Workspace refs, cross-topic Agent Workspace refs, unresolved required placeholders, and forbidden runtime truth.

## 8. Tests, Documentation, and Validation

- [x] 8.1 Add unit tests for template registration, template package validation, template boundary rejection, role and Workflow Stage mapping, and harness diagnostic integration.
- [x] 8.2 Add unit tests for manifest and topic config extensions, Effective Topic Context profile selection, and deterministic JSON outputs.
- [x] 8.3 Add unit tests for Topic Agent Team Profile specialization, profile validation, role binding validation, fanout validation, reviewer read-access policy validation, and multi-topic isolation.
- [x] 8.4 Add CLI tests for `team-templates list`, `team-templates inspect`, `team-templates validate`, `team-profiles specialize`, and `team-profiles validate`.
- [x] 8.5 Update README or developer notes with the Milestone 2 and 3 template/profile command examples.
- [x] 8.6 Run `openspec validate --all`.
- [x] 8.7 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills`.
