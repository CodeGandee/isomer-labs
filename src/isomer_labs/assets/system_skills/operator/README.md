# Operator Public Pack

This subtree contains the two public core siblings, `isomer-op-welcome` and `isomer-op-entrypoint`. Installers project both top-level host skills as one atomic pack. The 19 operator, service, shared-support, and research-recording capabilities below `isomer-op-entrypoint/subskills/` are protected members, not independent install units.

Ordinary users invoke the public parent:

```text
$isomer-op-entrypoint use help to show available workflows
$isomer-op-entrypoint use project to validate the Project
$isomer-op-entrypoint use topic-create to prepare a Research Topic
$isomer-op-entrypoint use system-skills to inspect Kaoju readiness
```

The parent route table maps scoped names such as `project`, `gui`, `identity`, `system-skills`, `toolbox`, `topic-create`, `topic-manage`, `topic-team`, `topic-env`, `agent-env`, `houmao`, and `operation-sets` to stable protected logical ids. Internal object designators use bare subskills, for example `isomer-op-entrypoint->project`; commands add `()`, for example `isomer-op-entrypoint->project->check-project()`.

## Owner and Support Boundaries

Operator members own user-facing Project, Topic, identity, GUI, Toolbox, extension-management, and formal-team workflows. Protected service members provide bounded support only after an owner delegates them. Protected shared members provide reusable guidance or recording workflows without becoming first-click public skills.

The public `isomer-op-welcome` sibling remains read-only and teaches typical use cases and commands. The entrypoint handles concrete route-and-proceed requests and delegates empty, help, and retained orientation commands to welcome. Project declarations remain authoritative routing intent; the `system-skills` member separately evaluates receipt v5 public-pair integrity, explicit-root integrity, limited live inventory, and refresh state when host usability matters.

Houmao remains an implementation and adapter layer. Isomer owner routes resolve Isomer context and authority before delegating bounded work through the protected `houmao` member.

## Authoring Rules

Keep a member self-contained. Its `SKILL.md`, `agents/`, scripts, references, templates, and assets must resolve without reading siblings. Declare logical-id dependencies in `manifest.toml` rather than using relative sibling paths.

Use a protected subskill when a capability owns private resources. Use a command when a procedure uses its containing bundle's resources. Parent commands may expose child commands as object generators.

Do not add top-level `isomer-op-*`, `isomer-srv-*`, `isomer-misc-*`, or `isomer-research-*` compatibility folders. Preserve logical ids in frontmatter and metadata because callbacks, bindings, provenance, compatibility checks, and private projection use them.
