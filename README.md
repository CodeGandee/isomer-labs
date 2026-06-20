# isomer-labs

艾索幕实验室

## Sketch

Isomer Labs is a private lab for developing an automatic research platform powered by multi-agent technology.

## Project Goal

Isomer Labs aims to develop an interactive, semi-automatic research conduction platform. The platform uses multi-agent research teams as a research engine, while a human user sets goals and steers the work at critical steps.

The project is inspired by DeepScientist, available locally under `extern/orphan/DeepScientist`, but it differs in several design goals:

- support multi-agent teamwork from the start, including predefined research teams and user-defined agent teams
- keep agent-team composition open to customization as a core platform capability
- expose a modular, white-box system rather than a fully system-controlled workflow
- decouple the research engine from the GUI
- drive the research engine through an operator agent controlled by the user
- generate task-specific GUI views for visualizing research artifacts
- organize projects so they can integrate into user-owned workspaces

## Name

`Isomer Labs` reflects the platform's core idea: research work can be reorganized into different agent structures depending on the problem.

The same base capabilities can form different research teams, workflows, and feedback loops. One task may need discovery, synthesis, and review agents; another may need planning, data analysis, and report-writing agents. The platform should make those structures easy to create, run, observe, and improve.

The name points to that adaptive structure: a research system that changes shape around the question while staying coherent as one platform.

The repository starts intentionally light:

- collect platform ideas before they become product features
- sketch multi-agent research workflows and interfaces
- keep experiments private until they are ready to split out

## External References

Local-only external checkouts live under `extern/orphan/` and are not committed.
The current reference package is:

- `DeepScientist`: cloned from `https://github.com/ResearAI/DeepScientist` into
  `extern/orphan/DeepScientist` with `--depth=1`.

## Milestone 1-4 CLI

The package exposes `isomer-cli` for Project discovery, Project Manifest validation, Effective Topic Context inspection, side-effect-free Workspace Path Resolution previews, Milestone 2/3 Domain Agent Team Template and Topic Agent Team Profile checks, and read-only Milestone 4 Pixi readiness diagnostics.

Common examples:

```bash
pixi run isomer-cli init
pixi run isomer-cli doctor --json
pixi run isomer-cli validate --json
pixi run isomer-cli topics list
pixi run isomer-cli workspaces list
pixi run isomer-cli context show --topic default --json
pixi run isomer-cli paths preview --topic default
pixi run isomer-cli schemas list
pixi run isomer-cli team-templates list
pixi run isomer-cli team-templates inspect deepsci-org --json
pixi run isomer-cli team-templates validate deepsci-org
pixi run isomer-cli team-profiles specialize --topic default --profile-id default-deepsci --use-case UC-01 --json
pixi run isomer-cli team-profiles validate .isomer-labs/team-profiles/default-deepsci.toml
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases validate --json
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases team-templates validate fixture-method-team
pixi run isomer-cli --project tests/fixtures/projects/deepsci-profile-use-cases team-profiles validate .isomer-labs/team-profiles/uc-01-novel-biomarker.toml
```

`isomer-cli init` creates `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/default.toml`, and `topic-workspaces/default/`. It does not create `state.sqlite` or Workspace Runtime subdirectories.

`isomer-cli doctor` checks host Pixi availability, Project-level Pixi configuration, optional `requires-pixi`, `pixi.lock` presence, and selected Research Topic environment bindings. It is read-only: it does not install Pixi environments, create lockfiles, create Topic Workspace runtime state, create Agent Workspaces, or edit Project config. When no Project is discoverable, it still runs dependency-only host checks. JSON output uses the existing `isomer-cli-output.v1` wrapper and reports `mutated: false`.

Project Manifest records topic-to-Pixi intent explicitly. Project-root Pixi environments use repeated `[[topic_pixi_environment_bindings]]` entries, and standalone topic isolation uses repeated `[[topic_standalone_pixi_bindings]]` entries. A Research Topic can bind to multiple Project-root Pixi environments through multiple active rows. Isomer never infers topic-to-environment relationships from Research Topic ids, Pixi environment names, or naming conventions such as `<topic-slug>-<env-purpose>`.

```toml
[[topic_pixi_environment_bindings]]
research_topic_id = "default"
pixi_environment = "default"
purpose = "runtime"

[[topic_standalone_pixi_bindings]]
research_topic_id = "default"
manifest_path = "topic-workspaces/default/pixi.toml"
pixi_environment = "default"
purpose = "isolated-check"
```

`team-templates` exposes the repository-local `teams/deepsci-org/execplan/` package as the seed Domain Agent Team Template and validates project-local templates through the same CLI. The reusable Milestone 2/3 fixture Project lives at `tests/fixtures/projects/deepsci-profile-use-cases/`; it registers two Research Topics, four static `deepsci-org` Topic Agent Team Profiles for UC-01, UC-02, UC-03, and UC-05, and a minimal `fixture-method-team` project-local Domain Agent Team Template.

`team-profiles specialize` derives a design-time Topic Agent Team Profile preview from Effective Topic Context, policy refs, Capability Binding refs, Skill Binding Projection refs, and Agent Workspace refs. It does not launch Houmao agents, create an Agent Team Instance, or write Workspace Runtime state. When `--write` is explicitly requested, it writes only the profile TOML file and reports a deterministic `registration_suggestion` object for adding the profile to the Project Manifest.

## Status

Initial sketch. Structure and scope are expected to change.
