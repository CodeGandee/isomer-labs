## Context

`isomer-admin-topic-team-specialize` currently has two different topic states in play. `init-topic` can create a provisional topic directory and `topic-def/topic-overview.md`, while `isomer-srv-env-setup` requires manifest-backed context from a registered Research Topic, Topic Workspace, and active `topic_standalone_pixi_bindings` entry. Agents can therefore reach `setup-topic-env` with a useful directory but no authoritative Project Manifest registration, and the service skill correctly refuses to infer the topic or Pixi manifest from directory names.

The CLI already exposes `isomer-cli project topics create <topic-id> --statement "<research topic>"` for Research Topic and Topic Workspace registration. That command does not currently guarantee the standalone Topic Workspace Pixi binding required by `isomer-srv-env-setup`. The skill should not paper over that gap by editing `.isomer-labs/manifest.toml`; it should verify the binding and report a precise blocker when no supported CLI/API surface can create it.

## Goals / Non-Goals

**Goals:**

- Add a public procedural `ensure-topic-registration` subcommand to the topic-team specialization skill.
- Make the subcommand idempotent: it should verify existing registrations, create missing Research Topic and Topic Workspace registrations through supported surfaces when possible, and return registered status when no mutation is needed.
- Insert `ensure-topic-registration` into `fast-forward`, `step-by-step`, help, and normal flow text after topic initialization and optional topic clarification.
- Require registration assurance before `specialize-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, and `materialize-profile` when those steps need manifest-backed Topic Workspace refs.
- Preserve the current rule that agents must not hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files.
- Surface missing `topic_standalone_pixi_bindings` as a named blocker before calling `isomer-srv-env-setup`.

**Non-Goals:**

- Do not change Isomer CLI topic CRUD implementation in this change.
- Do not add a new CLI command for Pixi binding creation from this skill change alone.
- Do not allow the operator skill to infer registered topics from directories under `isomer-content/topic-ws/`.
- Do not make `init-topic` itself responsible for all authoritative registration work.

## Decisions

Add `ensure-topic-registration` as a procedural subcommand, not a helper. It is user-facing because registration is a meaningful boundary: it mutates Project Config through supported Isomer surfaces or stops with a blocker.

Place `ensure-topic-registration` immediately after `init-topic` and optional `clarify-topic` in the full flow:

```text
init-topic
  -> clarify-topic (optional)
  -> ensure-topic-registration
  -> specialize-team
  -> clarify-topic-team (optional)
  -> setup-topic-env
  -> setup-agent-workspace
  -> validate-topic-team
  -> finalize-topic-team
```

`ensure-topic-registration` should read the Project Manifest, the provisional topic overview, and any explicit topic id or workspace directory. If the Research Topic and Topic Workspace are already registered, it reports `topic_registration_status: registered` and carries the registered refs forward. If they are missing and the topic statement and workspace path are clear, it runs or instructs the agent to run the supported topic creation surface:

```bash
isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>
```

The `--workspace-dir` argument matters when `init-topic` already created a provisional directory. Without it, topic creation may derive the same path, but the skill should not rely on that coincidence when it has an explicit provisional seed path.

After Research Topic and Topic Workspace registration, the subcommand must verify downstream environment setup prerequisites. For `setup-topic-env`, that means an active `topic_standalone_pixi_bindings` entry whose `manifest_path` points to the selected Topic Workspace Pixi manifest and whose `pixi_environment` is known or defaults safely. If the binding is missing and no supported Isomer CLI/API surface can create it, `ensure-topic-registration` reports `topic_registration_status: blocked` and names the missing binding rather than calling `isomer-srv-env-setup`.

Registration assurance should be re-runnable. If a user directly invokes `setup-topic-env`, the subcommand should either require prior `ensure-topic-registration` evidence or run the same verification logic before service delegation. Later steps should refuse with a clear predecessor message when registration evidence is missing.

## Risks / Trade-offs

- [Risk] The skill may still block after `project topics create` because standalone Pixi binding creation has no supported surface. Mitigation: make that blocker explicit and avoid hand-edited manifest fixes in the skill.
- [Risk] Adding another procedural step lengthens the user-facing flow. Mitigation: `fast-forward` runs it automatically when safe, and direct subcommands can still call it idempotently.
- [Risk] Existing provisional topic directories may already contain material. Mitigation: pass the explicit `--workspace-dir` when registering a provisional seed and refuse if the path collides with another registered workspace.
- [Risk] Agents may try to skip registration for local-only experiments. Mitigation: allow `init-topic` and topic clarification to remain provisional, but require registration before steps that need manifest-backed Topic Workspace refs.
