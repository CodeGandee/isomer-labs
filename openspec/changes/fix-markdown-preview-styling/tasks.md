## 1. Viewer Theme and State

- [x] 1.1 Apply Dockview's light theme through the Dockview React API.
- [x] 1.2 Update Markdown viewer state handling so pending renders show loading and completed empty renders show the empty fallback.
- [x] 1.3 Keep existing GFM, math, KaTeX, Mermaid, image, link, and table rendering paths working.

## 2. Markdown Preview Styling

- [x] 2.1 Add scoped light-surface Markdown preview CSS with GitHub-like base typography and colors.
- [x] 2.2 Style headings, paragraphs, lists, blockquotes, links, inline code, code blocks, tables, images, horizontal rules, KaTeX, and Mermaid blocks.
- [x] 2.3 Ensure long paths, wide code blocks, wide tables, and images wrap or scroll without overlapping other UI.
- [x] 2.4 Keep surrounding detail headings, detail columns, and JSON blocks readable inside Dockview.

## 3. Tests and Verification

- [x] 3.1 Add frontend tests for Markdown loading, empty, and rendered states.
- [x] 3.2 Add or update Playwright checks with a synthetic Markdown example covering common elements.
- [x] 3.3 Verify the real Flash Attention Markdown record is readable after render completion.
- [x] 3.4 Compare the resulting visual treatment against Markdown Live Preview or GitHub README-style rendering.
- [x] 3.5 Run frontend build/tests, Playwright verification, and OpenSpec validation.
