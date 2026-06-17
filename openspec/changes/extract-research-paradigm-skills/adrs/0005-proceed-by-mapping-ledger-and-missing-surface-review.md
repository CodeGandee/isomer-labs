# Proceed by Mapping Ledger and Missing-Surface Review

## Status

accepted

## Context

The migration needs a concrete process. The risk is that implementation will either copy DeepScientist-specific surfaces too directly or guess Isomer paths and APIs before the platform design is settled.

The user clarified that missing concepts must be reviewed. They may become new Isomer concepts later, but they may also be reframed using existing Isomer language.

## Decision

Proceed with a mapping-ledger workflow during skill extraction.

For each DeepScientist source skill, the implementer should record:

- Source behavior to preserve.
- Source-specific concepts and runtime dependencies encountered.
- Isomer concept mapping for each retained behavior.
- Omitted DeepScientist implementation details.
- Unsettled paths, files, commands, APIs, providers, schemas, storage roots, runner homes, prompt-injection mechanisms, and generated layouts.
- Candidate platform gaps for later Isomer review.

Every encountered source term or surface should be classified as:

| Classification | Action |
| --- | --- |
| Existing Isomer concept | Use the canonical Isomer term in the skill |
| Source implementation detail | Omit from instructions or keep only in provenance notes |
| Unsettled concrete surface | Mark with `yet-to-be-determined`; optional review ledgers may use suffixes such as `yet-to-be-determined:api` or `yet-to-be-determined:path` |
| Candidate platform gap | Add to a review list; do not introduce it as a settled Isomer concept |

## Concrete Plan

1. Start with `isomer-labs-research-shared` and encode the authoritative mapping rules from these ADRs.
2. Create a compact mapping ledger under the shared skill references or another directly linked reference location during implementation.
3. Extract core stage skills before optional publication extensions: intake, scout, baseline, idea, optimize, experiment, analysis, decision, finalize, then write, review, rebuttal, paper-outline, paper-plot, figure-polish, and science.
4. For each skill, preserve purpose, entry signals, exit criteria, durable outputs, Gates, and pitfalls from the source analysis.
5. Replace DeepScientist runtime operations with Isomer concept language and `yet-to-be-determined` markers for concrete surfaces.
6. Update generic team documentation only after the core shared mapping is stable.
7. Run validation searches for `DeepScientist`, `artifact.`, `memory.`, `bash_exec`, `DeepXiv`, `quest`, `worktree`, `Houmao`, concrete DeepScientist paths, runner homes, and guessed Isomer paths.
8. Review the missing-surface list after the first extraction pass. Promote only accepted gaps into new Isomer ADRs or specs.

## Considered Options

- Extract all skills first and review terminology afterward.
- Block extraction until every Isomer API and path is settled.
- Use a mapping ledger with explicit missing-surface markers.

## Consequences

- Implementation can move forward without pretending unresolved platform surfaces are settled.
- Reviewers can search for `yet-to-be-determined` to find missing decisions.
- New Isomer concepts remain gated by Isomer review, not by DeepScientist migration pressure.
- The extracted skills can be useful as research-method instructions before the full runtime API surface exists.
