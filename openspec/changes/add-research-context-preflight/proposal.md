## Why

V2 research skills that write durable Isomer research records can be invoked after the user has changed the Research Topic, Measurable Objective, Topic Workspace state, or latest route records. The skills currently say "recover", "refresh", or "read state" in uneven ways, so an executing agent can still start from prompt memory or an older rendered record instead of resolving the latest Isomer context first.

## What Changes

- Add a shared v2 latest-context preflight contract that tells agents how to resolve Effective Topic Context, inspect Workspace Runtime, and read the latest relevant research records before accepted durable record work starts.
- Add a shared semantic object for a context snapshot or freshness verdict that stage skills can cite without treating it as a hard storage binding.
- Revise active non-shared v2 research skills with durable record bindings so their entry guidance imports the shared preflight before accepted record writes, record refreshes, or durable stage decisions trust chat, prompt-provided context, remembered state, or prior stage prose.
- Require stage context briefs, contracts, or route decisions to state whether prompt context matches durable context, conflicts with it, implies a scope change, or requires scout, decision, or blocker routing.
- Add validation coverage so future v2 research skill entrypoints cannot omit the latest-context preflight.
- Coordinate with the archived worker-output-root policy: plain generated files use the resolved worker output root, while accepted research records use the latest-context preflight before promotion or durable recording.

## Capabilities

### New Capabilities
- `research-context-preflight`: Defines the shared latest-context preflight contract for resolving current Research Topic context, Workspace Runtime state, relevant record freshness, and conflict routing before accepted v2 durable research record work.

### Modified Capabilities
- `research-paradigm-skills`: Requires active non-shared v2 research skills with durable record bindings to reference and apply the shared latest-context preflight before accepted record writes, record refreshes, or durable stage decisions.

## Impact

- Affects `skillset/research-paradigm/v2/isomer-rsch-shared-v2/` shared references and semantic-placeholder registry.
- Affects active non-shared v2 research skill `SKILL.md` entry workflows and selected references that have durable record bindings, especially scout, baseline, idea, optimize, experiment, analysis, decision, finalize, write, review, rebuttal, paper-outline, paper-plot, figure-polish, Nature-facing skills, science, and workspace manager coordination.
- Affects `scripts/validate_research_paradigm_skillset.py` and its unit tests if validation is added for the new entry contract.
- Does not require new `isomer-cli` commands; it standardizes use of existing commands such as `isomer-cli --print-json project context show`, `project self queries`, `project runtime inspect`, path resolution, and `ext research records list/show`.
- Builds on `worker-output-root-policy`: this change does not replace `project outputs policy`, operation output sets, or `commit_after_operation` guidance for plain generated files.
