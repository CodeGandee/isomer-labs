## Context

Isomer Labs already treats Houmao as the underlying agent construction and management layer. Project initialization creates an Isomer-managed Houmao Project at `<project-root>/.isomer-labs` with the Houmao overlay under `<project-root>/.isomer-labs/.houmao`, while root-level `.houmao/` remains external user-owned state.

The Topic Service Master proposal needs Houmao-owned procedures for credentials, tool choice, system skills, launch profiles, mailbox, gateway, prompt overlays, and managed-agent lifecycle. Exposing those procedures as direct operator prerequisites would leak implementation detail into the Isomer operator experience. It would also break Houmao's discovery expectations if copied under `.isomer-labs/.houmao/...` or if an agent starts from a Topic Workspace cwd and expects Houmao to discover a project root `.houmao/`.

The correct boundary is that Isomer exposes an Isomer-facing workflow, resolves Project and Topic context, and returns explicit paths. Houmao-owned skill material remains procedural authority for Houmao-specific steps, but Isomer chooses where that material is projected and how agents are told to invoke it.

## Goals / Non-Goals

**Goals:**

- Keep the user and Project Operator Session operating Isomer Labs concepts rather than direct Houmao administration.
- Store Houmao-owned skill material under an Isomer-managed projection root at `.isomer-labs/houmao-skills/`.
- Provide an `isomer-cli` context surface that returns the absolute Houmao skill path, explicit Houmao Project path, Topic Workspace path, and skip state.
- Let Isomer system skills route to Houmao skill procedures by saying: read `<houmao_skill_path>` and run Houmao commands with `--project-dir <houmao_project_path>`.
- Record Project-level Houmao integration enablement or disablement in the Project Manifest so Houmao-aware workflows can skip deterministically.
- Preserve Houmao's contract by not relying on implicit project discovery from Topic Workspace cwd.

**Non-Goals:**

- Do not expose Houmao system-skill installation as a normal user-facing prerequisite for basic Isomer operator use.
- Do not duplicate Houmao credential, mailbox, gateway, launch-profile, or managed-agent recipes inside `isomer-cli`.
- Do not move Houmao Project state out of `.isomer-labs/` or create a root-level Isomer-owned `.houmao/`.
- Do not launch Topic Service Masters during ordinary Topic Workspace creation unless a skill explicitly requests launch.

## Decisions

### Decision: Isomer-managed Houmao skill projection

Project initialization or an explicit integration preparation command will create `.isomer-labs/houmao-skills/` and populate it with selected Houmao-owned system skills. This root is not the Houmao Project overlay and must not contain `.houmao/`. It is a read-only instruction library from Isomer's perspective, with ownership metadata so later preparation can update Isomer-managed projections without overwriting user-authored files.

Alternative considered: install Houmao skills into the Project Operator's normal skill root. This leaks Houmao into the operator environment and makes Project behavior depend on user-home installation state. The Project-scoped projection keeps the integration local, inspectable, and controlled by Isomer.

### Decision: CLI returns routing context, not embedded procedure

Add an Isomer CLI surface such as:

```bash
isomer-cli --print-json project integrations houmao status
isomer-cli --print-json project integrations houmao prepare-skills
isomer-cli --print-json project integrations houmao skill-context <skill-name> --topic <topic-id>
```

`skill-context` returns absolute paths and instructions:

```json
{
  "integration_status": "enabled",
  "houmao_project_path": "/repo/.isomer-labs",
  "houmao_overlay_path": "/repo/.isomer-labs/.houmao",
  "houmao_skill_path": "/repo/.isomer-labs/houmao-skills/prepare-topic-service-master/SKILL.md",
  "topic_workspace_path": "/repo/isomer-content/topic-ws/topic-a",
  "instructions": "Read houmao_skill_path. Run houmao-mgr with --project-dir houmao_project_path."
}
```

Alternative considered: add rich `isomer-cli project houmao prepare-agent` commands that encode launch profile creation, credentials, skills, mailbox, and gateway choices. That would duplicate Houmao's procedural surface and make Isomer CLI own too much adapter implementation.

### Decision: Explicit Project Manifest integration state

The Project Manifest will store a durable Houmao integration state, for example:

```toml
[operator.integrations.houmao]
status = "enabled"
skill_root = ".isomer-labs/houmao-skills"
project_dir = ".isomer-labs"
```

`status = "disabled"` means Houmao-aware Isomer skills skip Houmao-related work and report a skip reason. Missing state should be treated as not yet configured, not silently enabled.

Alternative considered: reuse `operator.system_extensions.installed = ["houmao"]` as the only switch. That table records optional operator skill extension declarations, not integration policy. A Project can have Isomer Houmao support material available while choosing to disable Houmao-backed operations for that Project.

### Decision: Skill routing stays Isomer-facing

`isomer-srv-topic-service-agent-support` and `isomer-srv-houmao-interop` remain Isomer system skills. When they need Houmao-specific procedure, they call the Isomer CLI context command, then instruct the active agent to read and follow the returned Houmao skill file with explicit context. The prompt wording should name Isomer concepts first and include Houmao only as the internal provider context.

These Isomer-facing bridge/support skills remain in the core Isomer system-skill group. They are safe in core because they do not require Houmao-owned skill material, credentials, or live Houmao state to exist; they can report disabled, not-configured, or blocked integration in Isomer language. The opt-in artifact is the Project-local `.isomer-labs/houmao-skills/` projection plus Project Manifest integration policy.

`isomer-srv-topic-service-agent-support` owns the Isomer-facing Topic Service Master lifecycle command surface:

- `prepare-topic-service-master`
- `launch-topic-service-master`
- `inspect-topic-service-master`
- `stop-topic-service-master`
- `repair-topic-service-master`

Each subcommand resolves the selected Project and Topic Workspace through Isomer context, checks Houmao integration policy, requests a matching Houmao skill context from `isomer-cli`, and routes the agent to the returned `houmao_skill_path` with the returned `houmao_project_path`.

The mapping is route-specific rather than mode-specific. `prepare-topic-service-master` resolves a different stable route entry from `launch-topic-service-master`, `inspect-topic-service-master`, `stop-topic-service-master`, and `repair-topic-service-master`. `isomer-cli` must read those route entries from the projection manifest and must not infer projected file paths by interpolating the requested route name.

Alternative considered: make the Project Operator Session directly invoke Houmao skill names. That turns an implementation layer into a user workflow and creates avoidable coupling to Houmao's skill catalog.

### Decision: Topic Service Master preparation is definition-first

Topic Workspace creation and actor setup may register a Houmao-backed `operator` Topic Actor and request Topic Service Master preparation, but they should define and validate project/profile material before launch. Launch remains an explicit skill step such as `launch-topic-service-master`, using the prepared skill-context output.

Alternative considered: automatically start a live Houmao-managed agent as part of topic creation. That would surprise users, add credential and process lifecycle blockers to topic creation, and make tests much heavier.

## Risks / Trade-offs

- Skill projection drift → Store ownership metadata and expose `prepare-skills` as an idempotent repair/update command.
- Ambiguous Project state when no integration table exists → Return `not_configured` and a clear next action instead of assuming enabled.
- Agents may ignore explicit `--project-dir` guidance → Put the instruction in both CLI JSON and Isomer skill routing text; validate docs and tests for that phrase.
- Houmao skill names may change → Isomer should map stable Isomer route names to projected Houmao skill paths through a small manifest under `.isomer-labs/houmao-skills/`; route names are lifecycle-specific and validated against that manifest.
- Projection may fail when Houmao is unavailable → Report an integration blocker during `prepare-skills`, but allow Projects with `status = "disabled"` to proceed without Houmao checks.

## Migration Plan

1. Add Project Manifest parsing and writing support for `operator.integrations.houmao`.
2. Add CLI commands for Houmao integration status, enable/disable, skill preparation, and skill-context resolution.
3. Add `.isomer-labs/houmao-skills/` projection support with metadata and collision protection.
4. Update Isomer service skills to request skill context from `isomer-cli` and route to returned skill paths.
5. Keep Isomer-facing Houmao bridge/support skills in the core packaged system-skill group while ensuring their guidance is inert when Project Houmao integration is disabled or not configured.
6. Update Topic Creator and Topic Manager guidance to skip Houmao-backed Topic Service Master work when integration is disabled.
7. Add command-style Topic Service Master reference pages to `isomer-srv-topic-service-agent-support` for prepare, launch, inspect, stop, and repair.
6. Add unit tests for manifest state, CLI JSON payloads, projection safety, disabled skips, and skill text validation.

Rollback is straightforward because the new projection root is under `.isomer-labs/` and can be ignored by older flows. Disabling the Project integration should stop new Houmao-aware skill routing without deleting projection files or Houmao overlay state.

## Open Questions

- Which exact Houmao skill set names should `prepare-skills` project for Topic Service Master preparation?
- Should `project init` prompt or default to `not_configured`, leaving enablement to a later explicit command?
- Should `skill-context` expose only `SKILL.md` paths or also structured metadata for available subcommands inside each projected Houmao skill?
