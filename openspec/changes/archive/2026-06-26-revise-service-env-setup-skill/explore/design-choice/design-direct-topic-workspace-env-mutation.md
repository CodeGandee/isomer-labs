# Direct Topic Workspace Environment Mutation

## Decision

`isomer-srv-env-setup` may directly mutate the selected Topic Workspace Pixi environment when the user invokes the skill for environment setup. The workflow does not require a separate Service Request boundary before it infers dependencies, updates Pixi dependencies, installs packages, or runs the desired gate command.

## Rationale

The skill exists to prepare a runnable Topic Workspace environment. Requiring a separate support request for every dependency change would make the service skill mostly advisory and would slow the user-facing setup path.

## Boundaries

Direct mutation remains scoped to the selected Project Manifest-declared Topic Workspace and its active `topic_standalone_pixi_bindings` entry. The skill still must not launch agents, create Agent Instances, mutate unrelated Workspace Runtime records, perform GUI work, make research decisions, or install into the Project root or an Agent Workspace as if it were the Topic Workspace environment.

## Implementation Impact

The revised skill should replace old wording that routes dependency repair or lockfile changes through a separate Service Request. It should instead report the commands run, files changed, readiness status, and blockers through the parent skill output contract.
