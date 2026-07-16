# Project Web GUI

The project web service starts a local FastAPI backend and TypeScript frontend over one Isomer Project directory. It is designed for one user inspecting active topic work while agents or operators continue to write artifacts.

```bash
isomer-cli project web serve --root .
```

The GUI shows semantic project views instead of raw filesystem browsing. Use it for topic overviews, idea lineage, record inspection, markdown preview, JSON payload inspection, PDFs, diagnostics, and future control surfaces.

Idea Graph and Idea Timeline use the canonical [Research Idea Portfolio](research-idea-portfolio.md). Both show exploration, decision, evidence, archive, and visibility independently. They share fixed preset semantics and visible-versus-source counts, while each view restores its own browser filter state. Graph layout controls remain collapsed by default. Portfolio controls, node selection, ancestry or descendant traversal, decision review, detail inspection, and layout changes are read-only.

`Explore this idea` and `Explore instead` are separate confirmed mutations. Their dialog names the exact affected ideas, expected transitions, rationale, reopening or Gate requirements, canonical result refs, and dispatch state. A blocked actor delivery does not erase an accepted canonical decision or Research Task.

When a file path appears in the UI, it should be displayed relative to the Topic Workspace when possible. Full absolute paths belong in diagnostics or copyable details, not primary labels.
