# Topic Config Short Topic Statements

Research Topic Config may include one short inline `topic_statement` and optional Artifact refs for richer topic material. The inline field supports discovery, CLI previews, and human review, while long briefs, evolving rationale, source notes, user notes, and rich objective material belong in file-backed Artifacts referenced by the config.

## Status

accepted

## Considered Options

- Short inline statement plus optional Artifact refs.
- Require all non-trivial topic statements to be Artifact refs.
- Inline topic statements only.

## Consequences

Topic setup stays simple without turning Research Topic Config into Workspace Runtime state. Rich topic context can carry Artifact identity and provenance when needed.
