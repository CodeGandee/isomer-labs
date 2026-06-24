## Context

`isomer-cli init` currently initializes only Isomer Project files. It writes `.isomer-labs/manifest.toml`, one Research Topic Config, and one Topic Workspace directory, then stops before Workspace Runtime creation. The Houmao adapter already has a CLI-backed `project_init` command catalog entry, but that command is used in adapter launch paths rather than Project bootstrap.

The operator skillset now has `isomer-admin-topic-team-specialize` for adapting a Domain Agent Team Template to a Research Topic. It does not yet have a companion Project lifecycle skill for the earlier steps: create the Project, confirm `.isomer-labs/`, confirm `.houmao/`, validate configs, list topics and workspaces, resolve context, and prepare runtime before specialization or launch.

## Goals / Non-Goals

**Goals:**

- Add `isomer-admin-project-mgr` as the operator-facing Project lifecycle skill.
- Keep the skill lean, self-contained, and formatted like the existing Imsight-style topic-team specialization skill.
- Make successful `isomer-cli init` create or validate both Isomer Project config and the Project-level Houmao overlay.
- Keep Project bootstrap distinct from Workspace Runtime creation, adapter launch materialization, and live Houmao agent operations.
- Report deterministic CLI text and JSON output for Houmao bootstrap status and diagnostics.

**Non-Goals:**

- Do not launch Houmao managed agents during `isomer-cli init`.
- Do not create `state.sqlite`, runtime directories, Agent Workspaces, adapter manifests, mailboxes, gateways, or launch dossiers during `isomer-cli init`.
- Do not promote Houmao-specific terms into generic Isomer schemas beyond the Project-level bootstrap boundary.
- Do not fold Topic Team Specialization into the new Project manager skill; the new skill should hand off to `isomer-admin-topic-team-specialize` when team adaptation begins.

## Decisions

### Use a strict Project bootstrap for Houmao

`isomer-cli init` should validate the topic id and existing-manifest guard first, then initialize the Project-level Houmao overlay through the CLI-backed Houmao command boundary before writing `.isomer-labs/`. If Houmao command resolution or `houmao-mgr --print-json project --project-dir <project-root> init` fails, the command returns diagnostics and does not claim that an Isomer Project was initialized.

Alternative considered: write `.isomer-labs/` first and report Houmao failure as a warning. That leaves a confusing half-initialized state for operators and repeats the current failure mode where project discovery and Houmao readiness diverge.

### Treat `<project-root>/.houmao/` as Project bootstrap state

The Project-level Houmao overlay created by `init` should live at `<project-root>/.houmao/`, selected by passing `<project-root>` as `--project-dir` to Houmao. This is separate from per-Agent Team Instance adapter material such as `<topic-workspace>/runtime/adapters/houmao/<agent-team-instance-id>/houmao-project-overlay/`.

Alternative considered: initialize Houmao only inside topic adapter runtime paths. That works for launch material, but it does not give the Project Operator Session a stable Houmao project foundation before topic-team work begins.

### Reuse the CLI-backed Houmao adapter boundary

The implementation should not import Houmao Python internals. It should reuse the existing command-resolution posture and `HoumaoCommandCatalog.project_init(project_root)` shape, or a small Project-bootstrap helper built on the same command runner and diagnostic conventions.

Alternative considered: shell directly to `houmao-mgr` from `init_project.py`. That would duplicate command parsing, JSON validation, timeout handling, environment hints, and diagnostics already present in the adapter layer.

### Keep the new skill as a Project lifecycle front door

`isomer-admin-project-mgr` should own Project setup and inspection workflows, not topic-template adaptation. Its local subcommands should include `help`, `init-project`, `check-project`, `list-topics`, `show-context`, `init-runtime`, `prep-runtime`, and `specialize-team`. The last subcommand should resolve enough context to hand off to `isomer-admin-topic-team-specialize` rather than duplicating specialization logic.

Alternative considered: add Project initialization subcommands to `isomer-admin-topic-team-specialize`. That would make a topic specialization skill responsible for earlier Project lifecycle operations and would blur the boundary between Project setup and topic-team adaptation.

### Validate the skill with the repository operator-skill validator

The existing validator has specialized checks for `isomer-admin-topic-team-specialize`. This change should add equivalent focused checks for `isomer-admin-project-mgr`: required bundle files, no `evals/`, required local subcommands, near-top workflows, short subcommand names, self-contained references, no required external support refs, and UI metadata that invokes the correct skill name.

Alternative considered: rely only on `skill-creator` quick validation. That catches basic skill shape but not this repository's operator-skill contracts or self-contained support-reference rule.

## Risks / Trade-offs

- Houmao unavailability blocks fresh Project init -> Mitigate with deterministic diagnostics that name the missing command or checkout and with tests that cover failure before `.isomer-labs/` is written.
- Strict init can surprise tests and scripts that previously initialized an Isomer-only Project -> Mitigate by updating docs, unit tests, and JSON output to show Houmao bootstrap as part of Project init.
- Project-level `.houmao/` can be confused with adapter launch overlay directories -> Mitigate through docs, skill help, and spec language that separates Project bootstrap from per-team adapter runtime material.
- New skill can duplicate topic-team specialization behavior -> Mitigate by making `specialize-team` a handoff subcommand and preserving `isomer-admin-topic-team-specialize` as the specialization authority.

## Migration Plan

Existing Isomer Projects without `.houmao/` should not be silently rewritten by unrelated commands. Operators can run the new Project manager skill or the documented Houmao project init command to add the Project-level overlay explicitly. Fresh `isomer-cli init` creates both sides.

Rollback is straightforward: revert the CLI bootstrap change and the new skill bundle. Project directories that already received `.houmao/` remain valid Houmao project overlays and do not affect `.isomer-labs/` discovery.

## Open Questions

- Should a future command provide `isomer-cli project repair-houmao` for existing Isomer-only Projects, or should the operator skill continue to route that through explicit Houmao CLI guidance?
