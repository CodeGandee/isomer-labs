# Start Research Manually

## Workflow

1. Interpret this usage path as human-orchestrated research setup, not formal Topic Team Specialization.
2. Recommend owner skill `isomer-admin-topic-creator`.
3. Use safe first command `Use $isomer-admin-topic-creator fast-forward` when the user has approved automatic setup, or `Use $isomer-admin-topic-creator step-by-step` when they want guided acknowledgement.
4. Mention that the owner skill handles or delegates Project readiness, concrete Research Topic input, Research Topic and Topic Workspace registration, Workspace Runtime readiness, topic environment setup, default or requested Topic Actors, Topic Actor Workspaces, actor onboarding, and `topic.workspace.summary`.
5. Route lower-level initialized-topic storage, Topic Actor repair, package mutation, environment verification, reset checkpoints, and diagnostics to `isomer-admin-topic-mgr` after Topic Creator handoff.
6. Report the mutation boundary: this welcome skill does not initialize the Project, create the Research Topic, mutate the Topic Workspace, or create Topic Actor Workspaces.

If the user's task does not map cleanly to these steps, use your native planning tool to decide whether the user is asking for manual Topic Actor research or formal Domain Agent Team Template specialization, then recommend the matching visible usage path or ask for that distinction.

## Output Fields

- `status`: `recommended`.
- `interpreted_goal`: `start-research-manually`.
- `recommended_workflow`: `start-research-manually`.
- `owner_skill`: `isomer-admin-topic-creator`.
- `safe_first_command`: `Use $isomer-admin-topic-creator fast-forward` or `Use $isomer-admin-topic-creator step-by-step`.
- `blockers`: missing concrete Research Topic, missing Project decision, or unapproved mutation.
- `next_action`: invoke the owner skill directly or provide missing topic substance.

Do not route this usage path to `isomer-admin-topic-team-specialize` unless the user explicitly asks for a Domain Agent Team Template.
