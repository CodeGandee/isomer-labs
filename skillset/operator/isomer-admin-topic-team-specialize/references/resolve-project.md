# Resolve Project

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the project root from the user-provided path or current working directory, then confirm the Project Manifest and the bundled `references/isomer-domain-language.md` reference.
2. Read the supplied topic prompt, topic file, or Research Topic ref, then list matching Research Topics and Topic Workspaces.
3. Inspect Project Manifest defaults, Research Topic Config refs, Domain Agent Team Templates, Topic Agent Team Profile Bundle registrations, and Workspace Runtime refs.
4. If the selected Topic Workspace is missing, propose the minimal creation or registration action and keep mutations behind normal Isomer CLI or API surfaces.
5. Return the selected Project, Research Topic, Topic Workspace, Domain Agent Team Template, profile bundle, and runtime refs with blockers for the next subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project root, topic material, and requested outcome, then execute the plan.

## Reference Routing

Read first:

- The Project Manifest and selected Research Topic Config.
- `references/isomer-domain-language.md` for canonical terms.

Read as needed:

- `references/runtime-and-file-boundaries.md` when path ownership or runtime placement is unclear.
- The selected Domain Agent Team Template manifest when template discovery matters.

## Exit Criteria

- The selected Project, Research Topic, Topic Workspace, Domain Agent Team Template, profile bundle, and runtime refs are explicit.
- Any missing workspace, manifest, or topic config blockers are named.

## Guardrails

- Do not treat a Domain Agent Team Template as a launchable topic team.
- Do not infer credentials, live process state, or research results from configuration files.
- Do not mutate Project Config or Topic Workspace files except through validated Isomer commands or APIs.
