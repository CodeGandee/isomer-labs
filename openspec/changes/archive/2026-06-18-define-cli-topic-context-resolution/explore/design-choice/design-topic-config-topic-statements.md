# Research Topic Config Topic Statements

The accepted first-version design lets Research Topic Config carry a short inline topic statement and optional Artifact refs for richer topic material.

## Accepted Choice

Option A: Research Topic Config may include one short inline `topic_statement` for discovery, CLI previews, and human review. Longer briefs, evolving rationale, source notes, user notes, and rich objective material should use `topic_statement_artifact_refs` or other explicit Artifact refs.

## Rationale

The Research Topic needs enough inline shape for a user and `isomer-cli` to recognize the topic before any Run exists. Long or evolving topic material needs Artifact identity, provenance, and normal research-recording behavior instead of growing the config into a second runtime store.

## Consequences

- Topic setup stays lightweight for simple topics.
- Rich topic material can still be durable, file-backed, and provenance-friendly.
- Research Topic Config remains a defaults-and-refs document, not Workspace Runtime state.

## Rejected Alternatives

- Require all non-trivial topic statements to be Artifact refs. This improves provenance but makes simple topics heavier to create and review.
- Allow only inline topic statements in v1. This simplifies the schema but weakens support for long, evolving, or evidence-linked topic context.
