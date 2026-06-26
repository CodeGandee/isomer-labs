# Resolve Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the project root from the user-provided path or current working directory, then confirm the Project Manifest and the bundled `references/isomer-domain-language.md` reference.
2. Read the supplied topic prompt, topic file, or explicit Research Topic ref, then list matching Research Topics and Topic Workspaces from Project Manifest-backed registrations. Do not treat an implicit Project Manifest default, the id `default`, or a generic `default Research Topic` statement as enough topic substance unless the user explicitly supplied it and it contains a concrete research question.
3. If no registered Research Topic matches but the user supplied enough topic material to seed a workspace, report that `init-topic` should create a provisional topic workspace seed and `<topic-dir>/topic-def/topic-overview.md`, followed by `ensure-topic-registration` before registration-dependent work.
4. If no registered Research Topic matches and the topic material is unclear, route to `clarify-topic` or ask for more topic detail before proposing topic workspace creation.
5. Inspect Project Manifest defaults, Research Topic Config refs, Domain Agent Team Templates, and Topic Agent Team Profile Bundle registrations needed for static material production.
6. If the selected Topic Workspace is missing or provisional, propose `ensure-topic-registration` as the minimal creation or registration action and keep mutations behind normal Isomer CLI or API surfaces.
7. Return the selected Project, Research Topic, Topic Workspace, Domain Agent Team Template, profile bundle, provisional topic status, and blockers for the next subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project root, topic material, and requested outcome, then execute the plan.

## Reference Routing

Read first:

- The Project Manifest and selected Research Topic Config when present.
- `references/isomer-domain-language.md` for canonical terms.

Read as needed:

- `references/runtime-and-file-boundaries.md` when path ownership or static/runtime boundaries are unclear.
- The selected Domain Agent Team Template manifest when template discovery matters.

## Exit Criteria

- The selected Project, Research Topic, Topic Workspace, Domain Agent Team Template, and profile bundle refs are explicit, or the provisional topic seed path is named.
- Any missing workspace, manifest, topic config, topic overview, or registration blockers are named.
- The next subcommand is explicit, usually `init-topic`, `clarify-topic`, `ensure-topic-registration`, `specialize-team`, or a lower-level helper.

## Guardrails

- Do not treat a Domain Agent Team Template as a complete static topic team.
- Do not infer credentials, live process state, or research results from configuration files.
- Do not mutate Project Config or Topic Workspace files except through validated Isomer commands or APIs.
