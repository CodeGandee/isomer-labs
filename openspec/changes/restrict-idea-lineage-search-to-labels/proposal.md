## Why

Idea lineage search currently indexes hidden node metadata, URLs, source paths, and realization details, so short user queries such as `ncu` can match every node. Users expect the graph search to filter what they can see on each idea node label.

## What Changes

- Restrict idea lineage search to visible node-label text only.
- Treat node labels as the search contract, currently title plus status.
- Remove hidden ids, paths, URLs, source JSON metadata, realization metadata, and detail refs from the idea lineage search index.
- Match short acronyms and terms by normalized substring/token logic instead of broad fuzzy matching.
- Keep filtering node-only and continue pruning edges whose endpoints are hidden.

## Capabilities

### New Capabilities
- `idea-lineage-visible-label-search`: Covers the idea lineage graph search surface, label-only matching semantics, and edge pruning after visible-label filtering.

### Modified Capabilities

## Impact

- Frontend idea lineage panel search helper and tests.
- Packaged frontend static bundle.
- No backend API change and no new dependency.
