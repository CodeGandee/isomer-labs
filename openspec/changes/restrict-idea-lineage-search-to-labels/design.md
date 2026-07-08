## Context

The idea lineage graph recently moved from backend filters to a single frontend search input. The first implementation indexed broad graph node metadata, including source paths, detail URLs, realization metadata, and identifiers, which caused short searches such as `ncu` to match unrelated nodes through hidden text.

Users read the graph visually. The search box should therefore answer "which visible node labels contain this text?" rather than "which graph payload fields fuzzily resemble this text?"

## Goals / Non-Goals

**Goals:**
- Make idea lineage search match only visible ReactFlow node label text.
- Keep short acronym searches deterministic, including `ncu`.
- Keep multi-word searches intuitive by requiring all normalized terms to appear in the visible label.
- Keep edge pruning based on the filtered node set.

**Non-Goals:**
- Do not add full-text search over opened idea details, JSON, markdown, records, or supporting artifacts.
- Do not change the backend graph endpoint.
- Do not change dense graph filtering.
- Do not remove Fuse.js from dependencies in this small follow-up.

## Decisions

Use a single helper to compute the visible searchable label from the same fields rendered on ReactFlow nodes. The current visible label is title plus status, so search should normalize and match only those strings.

Prefer normalized substring/token matching for this view. For a single query term, the normalized label must include that term. For multiple query terms, every term must appear somewhere in the normalized label. This handles acronyms and middle-label words without broad fuzzy false positives.

Keep fuzzy matching out of the default label filter. Fuse.js can remain installed for future richer search modes, but this idea lineage control should not use metadata or loose fuzzy matching because it violates the visible-label mental model.

Filter graph payloads before `layoutFlowGraph()` as before. After visible nodes are selected, keep only edges whose `source` and `target` are both visible, and trim groups to visible node ids.

## Risks / Trade-offs

- Typo-tolerant search becomes less permissive -> Users get predictable label filtering; richer typo search can be introduced later as a distinct mode with clear scope.
- Hidden identifiers no longer match -> This is intended; users should open the node or use a future advanced search for metadata.
- Label/search drift can return -> Use a shared helper for ReactFlow label generation and search tests that assert `ncu` filters the live-style graph to NCU-labeled nodes only.

## Migration Plan

1. Replace idea lineage Fuse document matching with visible-label token filtering.
2. Share the visible label helper with ReactFlow node conversion or mirror its exact title/status semantics in the panel.
3. Add tests for `ncu`, separated middle words, hidden metadata non-matches, and edge pruning.
4. Rebuild packaged frontend assets.

## Open Questions

- None. The search surface is the visible node label.
