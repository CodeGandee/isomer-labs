## Context

`isomer-admin-topic-team-specialize` currently exposes implementation-oriented subcommands such as `resolve-project`, `inspect-template`, `map-placeholders`, and `draft-profile`. Those are useful internal steps, but they are not the clean user-facing flow for creating a topic team. From the user's perspective, the work starts with a topic, may need topic clarification, then selects and specializes a domain-level agent team, may need specialized-team clarification, then prepares topic environment and per-agent workspaces before validating and finalizing the team.

The current skill also resolves an existing Research Topic through supplied topic material or Project Manifest-backed registrations. That is enough when the Research Topic already exists, but it leaves a gap when an operator starts from a fresh research topic idea and needs a topic workspace seed before template specialization can proceed.

The repository currently treats the Project Manifest as the authority for managed Research Topics and Topic Workspaces. The CLI has `isomer-cli init` for fresh Project bootstrap and read-only topic/workspace listing, but it does not expose a supported command for adding a new Research Topic to an existing Project Manifest. The new `init-topic` subcommand should therefore create provisional topic material while clearly preserving the registration boundary.

## Goals / Non-Goals

**Goals:**

- Add a short local `init-topic` subcommand to `isomer-admin-topic-team-specialize`.
- Add `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile` as user-facing procedural boundaries through static topic and team setup.
- Classify subcommands into procedural, helper, and misc groups so the entrypoint and help page distinguish the public workflow API from finer-grained implementation helpers and shortcuts.
- Require `init-topic` or `clarify-topic` to clarify the Research Topic when missing or unclear.
- Require the subcommand to ask for the topic workspace directory when missing.
- Create `<topic-dir>/topic-def/topic-overview.md` from the agent's understanding of the Research Topic.
- Make the output clear about whether the topic is a provisional topic workspace seed or an already registered Isomer Research Topic.
- Guide topic-specific development environment setup and per-agent workspace creation as explicit setup stages.
- Validate topic-team readiness before claiming that the team can start.
- Write `isomer-topic-summary.md` as the final human-readable summary of topic, team, working logic, environment setup, workspace layout, blockers, and next actions.
- Keep lower-level subcommands such as `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile` available as internal/manual implementation steps.
- Keep all required support knowledge inside the skill directory and preserve Imsight workflow style.

**Non-Goals:**

- Do not add or require a new `isomer-cli topics add` command in this change.
- Do not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files from the skill.
- Do not treat an unregistered topic directory as authoritative Project Manifest state.
- Do not hide environment setup, per-agent workspace setup, readiness validation, or profile materialization behind earlier topic clarification commands.
- Do not claim live runtime readiness from `finalize-topic-team`; live operation remains outside this skill.

## Decisions

### Add `init-topic` to the topic-team specialization skill

`init-topic` belongs in `isomer-admin-topic-team-specialize` because it prepares the topic material needed before Topic Team Specialization. It should be available as a manual subcommand and as an early step for `fast-forward` or `step-by-step` when no registered topic can be resolved.

Alternative considered: place the behavior in `isomer-admin-project-mgr`. That skill owns Project lifecycle checks and first Project bootstrap, but the requested behavior is tied to topic-team specialization and produces a topic overview for later specialization rather than a full Project registration workflow.

### Use user-facing subcommands for the main flow

The skill should define the primary user-facing flow as:

```text
init-topic
  -> clarify-topic (optional)
  -> specialize-team
  -> clarify-topic-team (optional)
  -> setup-topic-env
  -> setup-agent-workspace
  -> validate-topic-team
  -> finalize-topic-team
  -> approve-profile / materialize-profile when explicitly requested
```

`specialize-team` should be the user-facing command that selects a Domain Agent Team Template and runs the internal specialization path. Existing lower-level pages such as `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile` remain useful for manual operation and for implementing `specialize-team`, `fast-forward`, and `step-by-step`.

Alternative considered: keep `fast-forward` as the main automatic user-facing command. Rejected because `fast-forward` describes execution style, while `specialize-team` describes the user's intent.

### Group subcommands by public contract

The skill should divide subcommands into three groups:

- Procedural subcommands are public, single-step workflow commands that represent the user's normal static topic-team setup path and explicit profile-material boundaries: `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile`.
- Helper subcommands are five finer-grained implementation commands called by procedural subcommands: `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile`. They remain callable for manual operation and should stay documented in the skill entrypoint, but the `help` subcommand should not list them because it is the public usage surface. The help output should list public subcommands as a three-column table: `Subcommand`, `Purpose`, and `Produces`.
- Misc subcommands are public supporting commands or shortcuts that are not single workflow stages: `help`, `fast-forward`, and `step-by-step`.

Alternative considered: list helper subcommands in help. Rejected because help should present the public API, while the skill entrypoint can still expose private implementation commands to agents and advanced manual callers.

### Keep setup and validation as explicit stages

`setup-topic-env` should install or prepare the topic development environment only as an explicit setup step. `setup-agent-workspace` should create per-agent workspace directories and boundary notes only after team specialization defines expected agents or roles. `validate-topic-team` should check topic overview, specialized team material, environment posture, agent workspaces, deferrals, and blockers. `finalize-topic-team` should create `isomer-topic-summary.md` after validation so the user has one readable handoff summary.

Alternative considered: have `specialize-team` perform setup and finalization automatically. Rejected because it would hide environment mutation and workspace creation inside a design-time specialization command.

### Refuse procedural steps with missing predecessor artifacts

Each procedural subcommand page should name the artifacts expected from earlier steps. Except for `init-topic`, which starts the flow, a procedural subcommand should refuse to run when its predecessor artifacts are missing, tell the user which artifacts are missing, and name the previous subcommand that should create them.

Alternative considered: let later subcommands implicitly backfill earlier artifacts. Rejected because hidden backfill would make manual operation hard to reason about and could mutate topic, setup, approval, or materialization material out of order.

### Treat created topic dirs as provisional unless registered

The subcommand should create the requested directory and overview file, but it should report that the topic is provisional until the Project Manifest and Research Topic Config are updated by a supported Isomer CLI/API path. This keeps the existing authority model intact.

Alternative considered: have the skill edit the Project Manifest directly. Rejected because current skill guardrails require validated Isomer commands or APIs for Project Config mutation, and no supported topic-registration command exists yet.

### Keep `topic-overview.md` intentionally human-readable

The overview file should summarize the Research Topic, the agent's understanding, scope, initial objectives, assumptions, open questions, and source prompt. It is a topic definition artifact, not a structured Research Topic Config or runtime record.

Alternative considered: write TOML or JSON in `topic-def/`. Rejected for this change because the user specifically requested Markdown and because structured Project registration remains out of scope.

## Risks / Trade-offs

- Provisional directories can be mistaken for registered Topic Workspaces → Mitigate by requiring output text to label provisional status and by keeping `resolve-project` tied to Project Manifest authority.
- Asking for a directory can lead to paths outside the Project root → Mitigate by requiring explicit user confirmation and reporting path status before creation; implementation can reject or warn on unsafe paths based on existing repo conventions.
- Generated topic understanding may overstate the agent's certainty → Mitigate by requiring assumptions and open questions in `topic-overview.md`.
- `fast-forward` could accidentally continue from an unregistered seed as if it were authoritative → Mitigate by requiring `fast-forward` and `step-by-step` to stop or report blockers when registration is needed before specialization can proceed.
- Adding `specialize-team` near existing `fast-forward` can duplicate vocabulary → Mitigate by making `specialize-team` the intent-level subcommand and `fast-forward` the execution-mode shortcut that calls the same required path without interactive pauses.
- Environment installation can be slow or system-mutating → Mitigate by keeping it inside `setup-topic-env`, reporting commands run, and preserving validation output.
- Per-agent workspaces can drift from the specialized team shape → Mitigate by making `validate-topic-team` compare expected agent roles/workspaces against created workspace paths.

## Migration Plan

Add the subcommand pages and update the skill entrypoint, help, workflow pages, validator checks, tests, and operator documentation. Existing lower-level manual workflows continue to use `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile` without behavior changes.

Rollback is straightforward: remove `init-topic` from the skill and validator, and leave any created topic seed directories as ordinary user-authored topic notes.

## Open Questions

- Should a later change add `isomer-cli topics add` to register a new Research Topic and Topic Workspace in the Project Manifest?
- Should `init-topic` default the topic workspace directory under `topic-workspaces/<derived-topic-id>/` when the user asks for a suggestion, or should it always require a user-provided path?
