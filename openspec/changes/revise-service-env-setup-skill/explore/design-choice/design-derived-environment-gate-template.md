# Derived Environment Gate Template

## Decision

`<topic-workspace-dir>/user-intent/derived/isomer-env-gate.md` should use a fixed Markdown section template.

## Rationale

The derived gate is read by later agents and humans to understand what the setup workflow inferred, installed, and verified. A fixed Markdown structure keeps it easy to inspect without requiring a parser, while still making the critical fields predictable enough for agents to execute.

## Template Sections

The generated `isomer-env-gate.md` should include these top-level sections:

- `# Isomer Environment Gate`
- `## Source Intent`
- `## Runnable Target`
- `## Repo Requirements`
- `## Inferred Source Warnings`
- `## Dependency Plan`
- `## Pixi Install Commands`
- `## Verification Commands`
- `## Expected Results`
- `## Blockers`
- `## Execution Log`

## Implementation Impact

The service skill should teach agents to fill every section. If a section does not apply, the agent should write `None.` or a short reason rather than omit it. Inferred repo sources must be warning-labeled in `## Inferred Source Warnings`.
