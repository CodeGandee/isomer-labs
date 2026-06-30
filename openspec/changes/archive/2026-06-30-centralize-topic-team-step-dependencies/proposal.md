## Why

Topic Team Specialization now needs targeted recovery paths, but those paths are described repeatedly across the entrypoint, `fast-forward`, and many subcommand pages. This makes the process easy to drift: one prose path can change while another still names an old predecessor chain.

## What Changes

- Add a centralized step dependency contract for `isomer-admin-topic-team-specialize`, stored as a machine-readable JSON reference inside the skill bundle.
- Add a small Python query script inside the skill bundle so agents can ask for prerequisite artifacts, dependency paths, inclusive targeted recovery paths, exclusive targeted recovery paths, produced artifacts, and unrecoverable blockers.
- Teach the skill entrypoint and subcommands to query that centralized contract instead of repeating full dependency paths in prose.
- Keep prose for human meaning, local context, and blocker explanations, but make the JSON the source of truth for step order and recovery routing.
- Update validation so repository checks verify the JSON/script contract instead of relying only on scattered prose phrases.

## Capabilities

### New Capabilities

### Modified Capabilities
- `topic-team-specialization-module-skill`: Add a centralized step dependency manifest and query script for Topic Team Specialization dependency and recovery routing.

## Impact

- Affects `skillset/operator/isomer-admin-topic-team-specialize` references and scripts.
- Affects repository skill validation for the topic-team specialization operator skill.
- Does not change Project Manifest storage, Workspace Path Resolution, service skill APIs, or runtime team launch behavior.
