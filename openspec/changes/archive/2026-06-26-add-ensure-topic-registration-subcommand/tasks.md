## 1. Skill Entrypoint and Metadata

- [x] 1.1 Update `skillset/operator/isomer-admin-topic-team-specialize/SKILL.md` description, overview, user-facing flow, procedural subcommand table, output contract, and guardrails to include `ensure-topic-registration`.
- [x] 1.2 Update `skillset/operator/isomer-admin-topic-team-specialize/agents/openai.yaml` so the default prompt includes topic registration assurance.
- [x] 1.3 Add output fields or wording for registration status, registration command evidence, registered Research Topic refs, registered Topic Workspace refs, environment binding status, and blockers.

## 2. New Subcommand Page

- [x] 2.1 Add `skillset/operator/isomer-admin-topic-team-specialize/references/ensure-topic-registration.md` with a near-top numbered `## Workflow` and fallback plan.
- [x] 2.2 Make the subcommand idempotently verify existing Project Manifest-backed Research Topic and Topic Workspace registrations.
- [x] 2.3 Teach the subcommand to register a clear provisional topic seed through `isomer-cli project topics create <topic-id> --statement "<research topic>" --workspace-dir <topic-workspace-dir>` or an equivalent supported Isomer CLI/API surface.
- [x] 2.4 Require the subcommand to stop with blockers for missing concrete topic statements, unsafe workspace paths, duplicate or colliding registrations, or unsupported Project Config mutation.
- [x] 2.5 Require the subcommand to verify the active Topic Workspace Pixi binding required by `isomer-srv-env-setup` and to report a precise blocker when no supported surface can create a missing binding.
- [x] 2.6 Ensure the subcommand does not instruct agents to hand-edit `.isomer-labs/manifest.toml` or Research Topic Config files.

## 3. Flow Integration

- [x] 3.1 Update `references/help.md` to show the new flow and public subcommand table entry for `ensure-topic-registration`.
- [x] 3.2 Update `references/fast-forward.md` to run `ensure-topic-registration` after `init-topic` and optional `clarify-topic`, before `specialize-team`.
- [x] 3.3 Update `references/step-by-step.md` so its progress tracker and confirmation prompts include `ensure-topic-registration`.
- [x] 3.4 Update `references/init-topic.md` so provisional topic output names `ensure-topic-registration` as the next registration action.
- [x] 3.5 Update `references/specialize-team.md` to require registered topic evidence or refuse with guidance to run `ensure-topic-registration` first.
- [x] 3.6 Update `references/setup-topic-env.md` so it requires `ensure-topic-registration` evidence and refuses before service delegation when the Topic Workspace or Pixi binding is not manifest-backed.
- [x] 3.7 Update `references/setup-agent-workspace.md`, `validate-topic-team.md`, `finalize-topic-team.md`, and `materialize-profile.md` so registration blockers are carried forward and registration-dependent steps do not proceed silently from provisional seeds.

## 4. Validation and Tests

- [x] 4.1 Update repository skill validation expectations or fixtures that enumerate the topic-team specialization subcommands.
- [x] 4.2 Validate the revised topic-team specialization skill with the skill-creator quick validator.
- [x] 4.3 Run repository skillset validation.
- [x] 4.4 Run `openspec validate add-ensure-topic-registration-subcommand --strict`.
- [x] 4.5 Review the final diff to confirm the skill routes Project Config mutation only through supported CLI/API surfaces and reports blockers for missing Pixi binding support.
