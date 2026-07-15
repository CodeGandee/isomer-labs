# Next Step

## Workflow

1. Confirm that the user asked for context-aware next-step guidance.
2. Announce that this subcommand performs read-only Project inspection and extension inspection only.
3. Run only the commands that materially improve routing, selected from **Read-Only Command Boundary**.
4. Interpret the evidence into one visible research path, active owner workflow, extension status route, or `isomer-op-entrypoint` recommendation.
5. Report blockers and the safest next route without running mutating commands.
6. Include commands run, context evidence, extension state distinctions, alternate routes, routing rationale, and retired-route exclusions only in Complete Output unless the user asks for them.

If the user's task does not map cleanly to these steps, use your native planning tool to decide whether a read-only Project or extension check would materially improve routing; if not, recommend `show-options`, `show-extensions`, or `choose-path` instead.

## Read-Only Command Boundary

Allowed inspection commands:

- `isomer-cli project validate`
- `isomer-cli doctor`
- `isomer-cli project topics list`
- `isomer-cli project context show`
- `isomer-cli project self show`
- `isomer-cli project outputs policy`
- `isomer-cli system-skills extensions list`
- `isomer-cli project system-extensions list`

Do not run Project initialization, topic creation, runtime initialization, package mutation, Topic Actor mutation, Toolbox mutation, system-skill installation or registration, Topic Team Specialization, Houmao launch, extension bootstrap, or research execution commands from this skill.

## Recommendation Rules

Missing Project config usually recommends `isomer-op-project-mgr`.

Existing Project but missing or partial Research Topic setup usually recommends `start-research-manually` through `isomer-op-topic-creator` unless formal Agent Team intent is established.

Existing prepared Topic Workspace plus explicit Domain Agent Team Template intent usually recommends `start-research-by-agent-team` through `isomer-op-topic-team-specialize`.

Existing initialized topic management, package mutation, environment verification, reset checkpoints, or diagnostics usually recommends `isomer-op-topic-mgr`.

A hypothesis-driven goal usually recommends `start-deepsci-research`. An evidence-led survey, source examination, bounded method trial, comparison, paper, or wiki goal usually recommends `start-kaoju-survey`. These paradigm choices do not decide manual versus formal Agent Team topology.

A catalog-known but undeclared extension recommends `Use $isomer-op-system-skill-mgr detect-extensions` for read-only resolution or a concrete `isomer-op-entrypoint` request when additive reconciliation is authorized by the task. A declared extension remains authoritative routing intent. A confirmed load failure recommends `Use $isomer-op-system-skill-mgr repair` without automatically forgetting the declaration.

Do not infer host usability from `system-skills extensions list` or Project declaration state. Receipt, compatibility, live inventory, installation, registration, and host refresh belong to `isomer-op-system-skill-mgr`.

When the user supplied a concrete task and the next owner can be identified, recommend `Use $isomer-op-entrypoint` with that task so it can route and proceed. The welcome skill does not execute the owner workflow itself.

Houmao Project bootstrap or check questions usually recommend `isomer-op-project-mgr`. Houmao runtime, mailbox, gateway, launch profile, or template-mapping questions recommend `isomer-op-topic-team-specialize` only when the selected work concerns a formal Agent Team target established by the prompt or authoritative context. Other launch-facing work retains its runtime, Topic Service Master, GUI, topic, or service owner.

Missing readiness, missing `isomer-topic-summary.md`, missing Agent Workspace evidence, a Research Topic, or generic preparation or launch-facing language does not establish a formal Agent Team target by itself.
