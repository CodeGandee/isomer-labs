# Topic Agent Team Profile Bundles Store Deep Specialization

Isomer Labs will store a deeply specialized topic team as a Topic Agent Team Profile Bundle inside the owning Topic Workspace at the fixed path `<topic-workspace>/team-profile/`, with `profile.toml`, an approved instantiation packet, copied topic-edited template material such as `execplan/`, validation outputs, and provenance refs. The Project Manifest remains the discovery authority by holding a ref to the bundle, but the topic-specialized source lives with the Topic Workspace because it is tightly coupled to that Research Topic, its environment, and its runtime records.

## Status

accepted

## Considered Options

- Store only a thin `.isomer-labs/team-profiles/<profile-id>.toml` file.
- Store a Topic Agent Team Profile Bundle under `.isomer-labs/team-profiles/<profile-id>/`.
- Store a Topic Agent Team Profile Bundle under `<topic-workspace>/team-profiles/<profile-id>/`.
- Store the Research Topic's one Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/`.

## Consequences

- Deep specialization can copy and rewrite template prompts, skills, workflow contracts, and execplan material without mutating `teams/<template-id>/`.
- The Project Manifest should register the bundle's `profile.toml`, usually `topic-workspaces/<topic-id>/team-profile/profile.toml`.
- The Project Config Directory keeps refs and project-level defaults, not the topic-specific profile source body.
- Topic Workspaces store their topic-level profile bundle alongside Workspace Runtime, Agent Workspaces, Artifacts, and adapter material.
