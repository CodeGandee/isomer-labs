## Why

The Project Web GUI Markdown record viewer is hard to read because panel content inherits dark body text while Dockview renders a dark content surface. Research records are often reviewed as Markdown, so the preview needs a reliable light reading surface and GitHub-like typography.

## What Changes

- Apply the intended light Dockview theme through Dockview's theme API instead of relying only on a wrapper class.
- Give Markdown record panels explicit light-surface foreground, background, spacing, and typography.
- Style common Markdown elements in the manner of Markdown Live Preview and GitHub README rendering: headings, paragraphs, lists, blockquotes, links, inline code, code blocks, tables, images, rules, KaTeX, and Mermaid blocks.
- Show a loading state while Markdown rendering is pending, then show the empty fallback only after a completed empty render.
- Add tests and Playwright checks with real Markdown examples and a live topic record.

## Capabilities

### New Capabilities
- `project-web-markdown-preview`: Defines readable Markdown preview behavior for Project Web record viewers.

### Modified Capabilities
- None.

## Impact

- Affects `web/ui/src/App.tsx`, `web/ui/src/styles.css`, frontend tests, built static assets, and Playwright smoke coverage.
- Does not change backend APIs, record storage, Markdown rendering libraries, or query-index data.
- Uses the existing React Markdown, remark, rehype, KaTeX, and Mermaid stack.
