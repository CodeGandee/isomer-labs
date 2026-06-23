---
name: isomer-admin-project-aware
description: Resolve an Isomer Project, read supplied topic material, discover topic surfaces, templates, profiles, runtimes, and Topic Service Agents before orchestration.
---

# Isomer Project Awareness

## Workflow

When this skill is invoked, execute the following steps in order.

1. Resolve the project root from the user-provided path or current working directory, then confirm the Project Manifest and canonical domain language path.
2. Read the supplied topic prompt, topic file, or Research Topic ref, then list matching Research Topics and Topic Workspaces.
3. Inspect Project Manifest defaults, Research Topic Config refs, Domain Agent Team Templates, Topic Agent Team Profile registrations, Workspace Runtime refs, and known Topic Service Agent surfaces.
4. If the selected Topic Workspace is missing, propose the minimal creation or registration action and keep mutations behind the normal Isomer CLI or API.
5. Return the selected project, topic, workspace, template, profile, runtime, and service-agent refs with any blockers for the next operator skill.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the project root, topic material, and requested outcome, then execute the plan.

## Reference Routing

Read first:

- The Project Manifest and selected Research Topic Config.
- `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` for canonical terms.

Read as needed:

- `docs/runtime-and-files.md` when path ownership or runtime placement is unclear.
- `teams/*/execplan/manifest.toml` when Domain Agent Team Template discovery matters.

## Entry Signals

- A user points an agent at an Isomer Project root and asks it to operate the project.
- Topic material is provided as a prompt, file, or Research Topic ref.
- The next action depends on knowing available templates, profiles, workspaces, runtimes, or service actors.

## Exit Criteria

- The selected Project, Research Topic, Topic Workspace, Domain Agent Team Template, and runtime refs are explicit.
- Topic Service Agent discovery status is recorded.
- Any missing workspace, manifest, or topic config blockers are named.

## Guardrails

- Do not treat a Domain Agent Team Template as a launchable topic team.
- Do not infer credentials, live process state, or research results from configuration files.
- Do not mutate Project Config or Topic Workspace files except through validated Isomer commands or APIs.
