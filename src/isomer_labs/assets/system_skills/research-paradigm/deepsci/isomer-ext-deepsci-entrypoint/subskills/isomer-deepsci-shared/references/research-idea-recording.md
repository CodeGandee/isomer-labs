---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# DeepSci Research Idea Mapping

Use `isomer-op-entrypoint->research-ideas` as the authoritative contract and follow its Recording Contract before accepting any DeepSci output that creates, classifies, selects, defers, closes, reopens, explores, supports, refutes, revises, derives, merges, or archives a durable concept. This page only maps DeepSci profiles to that contract; it does not redefine canonical vocabulary.

Raw Idea Slate entries use `$.sections.raw_ideas[<index>]`. Candidate Frontier entries use `$.sections.serious_candidates[<index>]` or `$.sections.candidate_ideas[<index>]`. Rejected and deferred ledgers use the exact rejected or deferred idea item. Selected Hypothesis, Selected Idea Draft, outline seed, follow-up, analysis, and optimization profiles use their declared single idea object or exact idea-bearing list item. Pass that exact object path through `--source-json-path`; for example, `$.sections.filter_notes` is context and must not be recorded as an Idea Realization. Context sections, filter notes, route notes, rationale sections, metrics, result lists, and rendered Markdown are not Idea Realizations.

Before accepting a raw slate or candidate pass, record every durable concept with semantic `idea_id`, exact realization, explicit known facets, one sibling generation, and justified parent edges. Before accepting a selection or route decision, record the Decision Record and every considered option with outcome and rationale, then apply the justified transitions with the same operation correlation. `not_selected` alone leaves an idea open.

Analysis, experiment, optimize, scout, and review outputs update exploration or evidence only when accepted terminal result refs such as an Artifact, Evidence Item, Finding, Research Task, or Run justify the change. Cite those refs on the transition. Evidence does not select, defer, or close a concept. Create a new Research Idea and an explicit `follow_up_to`, `derived_from`, `merged_from`, `alternative_to`, or `subsumes` edge only when the output changes the concept; ordinary wording, boundary-detail, or evidence revisions retain identity and add a realization.

Use `research_idea_effects` in an idea-bearing structured payload when its profile promises canonical effects. Otherwise use the canonical CLI operations before declaring acceptance. Do not use a status-only write, a Markdown completion claim, query-index extraction, or a later import as a substitute.

Finish by inspecting returned canonical refs, querying the affected idea facets and Decision Record option set, resolving exact realization paths, and running `isomer-cli --print-json ext research ideas validate`.
