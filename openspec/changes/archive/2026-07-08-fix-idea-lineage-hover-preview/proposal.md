## Why

Idea lineage graph hover previews currently show a shortened metadata summary, cannot be entered or scrolled, and may remain visible after a node is opened. Users need the hover preview to behave like a small Markdown reader for the idea itself, while still keeping the graph quick to scan.

## What Changes

- Show an immediate fixed-size hover popup with a loading state while full idea Markdown preview data loads.
- Render loaded tooltip content through the normal Markdown preview renderer, including GFM, code, Mermaid, and KaTeX support.
- Keep the popup size bounded and scroll content internally without shortening the Markdown.
- Let users move the pointer from a node into the popup and scroll it with the wheel or scrollbar.
- Clear hover previews when a node opens and prevent stale async preview loads from reappearing after navigation.

## Capabilities

### New Capabilities
- `project-web-idea-hover-preview`: Covers interactive Markdown-capable hover previews for idea lineage graph nodes in the Project Web GUI.

### Modified Capabilities
- None.

## Impact

- Affects the Project Web React UI, idea graph hover state, Markdown preview reuse, CSS for hover overlays, and Playwright smoke coverage for the idea lineage graph.
- Reuses existing topic idea detail APIs and frontend Markdown preview utilities; no backend API or storage contract change is expected.
