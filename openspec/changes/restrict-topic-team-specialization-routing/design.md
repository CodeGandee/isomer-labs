## Context

Several system skills can route work toward `isomer-op-topic-team-specialize`. Most owner workflows already require an explicit Domain Agent Team Template or formal Agent Team request, but EntryPoint readiness fallback, generic launch-facing language, and one DeepSci missing-summary rule can select specialization without that evidence. Once selected, the specialization skill treats `prepare` as automatic-mode language and begins template discovery, which amplifies the original routing error.

The routing contract is expressed in packaged Markdown skill instructions and enforced by repository validators. The `skillset/operator`, `skillset/service`, and `skillset/research-paradigm` paths are symlinks to package assets, so implementation changes belong under `src/isomer_labs/assets/system_skills/`.

## Goals / Non-Goals

**Goals:**

- Establish one consistent positive-evidence gate for Topic Team Specialization routes.
- Preserve direct skill invocation and explicit Agent Team workflows.
- Keep ordinary topic preparation, manual Topic Actor work, runtime preparation, and extension bootstrap on their existing owners.
- Prevent formal-team recovery from being inferred solely from a missing `isomer-topic-summary.md` or Agent Workspace evidence.
- Add validation coverage that detects broad or unqualified specialization routes.

**Non-Goals:**

- Change Topic Team Specialization stages after a valid formal-team route is established.
- Add a runtime natural-language classifier or new CLI command.
- Change Domain Agent Team Template, Topic Agent Team Profile, or Agent Team Instance schemas.
- Alter Project, Topic Workspace, or research-record persistence.

## Decisions

### Use a semantic positive-evidence gate

A router may select `isomer-op-topic-team-specialize` only when the user explicitly invokes the skill or a specialization subcommand, or when the prompt or authoritative context establishes a formal Agent Team target. Valid contextual signals include a Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, selected formal-team material, or verbs such as deploy, specialize, instantiate, materialize, validate, repair, launch, or use when they apply to that Agent Team target.

Generic `prepare`, `launch-facing`, readiness, missing summary, missing Agent Workspace, topic name, or Topic Workspace context is insufficient. This semantic rule is preferable to a fixed keyword allowlist because context may establish a selected formal team without repeating one exact noun, while still requiring the router to name the evidence it used.

### Apply the gate at every inbound routing boundary

EntryPoint will state the invariant in its top-level guardrails, qualify its system-skill index, and split extension readiness recovery by topology. Welcome will qualify launch-facing recommendations. DeepSci workspace bootstrap will require selected formal-team context before treating a missing topic-team summary as a specialization blocker. Team Specialization will retain direct-invocation behavior but reject or return unqualified delegated preparation to Topic Creator or Topic Manager.

Applying the rule at every inbound boundary is preferred over relying only on Topic Team Specialization because the wrong handoff can cause planning, template discovery, or mutation intent before the downstream skill notices the mismatch.

### Validate both positive and negative routing language

Repository validation will check required invariant language and representative references. Tests will cover allowed explicit/team-context examples and denied topic-preparation, generic launch, and missing-summary examples. Validation should check semantic markers in the maintained skill bundles rather than attempt full natural-language inference.

## Risks / Trade-offs

- [Risk] Strict wording checks can become brittle when prose is reorganized. → Mitigation: validate a small set of stable routing clauses and use behavioral fixture assertions for representative prompts.
- [Risk] A selected formal team may be present only in authoritative context, not the prompt. → Mitigation: permit contextual formal-team evidence and require the route explanation to name it.
- [Risk] Overcorrection could block legitimate repair of an existing formal team. → Mitigation: explicitly allow selected profile, packet, template, summary, or Agent Team Instance evidence paired with a team-directed operation.
- [Risk] Generic launch requests span runtime, Topic Service Master, GUI, and Agent Team operations. → Mitigation: require the launch target to be an Agent Team before selecting specialization; otherwise retain the relevant runtime, service, or GUI owner.
