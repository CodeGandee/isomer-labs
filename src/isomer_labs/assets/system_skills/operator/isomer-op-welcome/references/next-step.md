# Next Step

## Workflow

1. Confirm that the user asked for context-aware next-step guidance.
2. Announce that this subcommand performs read-only Project inspection only.
3. Run only useful read-only commands, such as `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project topics list`, or `isomer-cli project context show`.
4. Interpret the read-only result into a recommended visible usage path or active owner workflow.
5. Report blockers and the safest next owner skill without running mutating commands.
6. Include commands run, context evidence, alternate owner workflows, routing rationale, and retired-route exclusions only in Complete Output unless the user asks for them.

If the user's task does not map cleanly to these steps, use your native planning tool to decide whether a read-only check would materially improve routing; if not, recommend `show-options` or `choose-path` instead.

## Read-Only Command Boundary

Allowed inspection commands:

- `isomer-cli project validate`
- `isomer-cli project doctor`
- `isomer-cli project topics list`
- `isomer-cli project context show`

Do not run `isomer-cli project init`, `isomer-cli project topics create`, `isomer-cli project runtime init`, package mutation commands, Topic Actor mutation commands, Topic Team Specialization commands, Houmao launch commands, or research-paradigm v2 bootstrap commands from this skill.

## Recommendation Rules

Missing Project config usually recommends `isomer-op-project-mgr`.

Existing Project but missing or partial Research Topic setup usually recommends `start-research-manually` through `isomer-op-topic-creator`.

Existing prepared Topic Workspace plus explicit Domain Agent Team Template intent usually recommends `start-research-by-agent-team` through `isomer-op-topic-team-specialize`.

Existing initialized topic management, package mutation, environment verification, reset checkpoints, or diagnostics usually recommends `isomer-op-topic-mgr`.

Houmao Project bootstrap or check questions usually recommend `isomer-op-project-mgr`. Houmao runtime, mailbox, gateway, launch profile, or template-mapping questions during Topic Team Specialization or launch-facing work usually recommend `isomer-op-topic-team-specialize`, which may delegate bounded adapter support to `isomer-srv-houmao-interop`.
