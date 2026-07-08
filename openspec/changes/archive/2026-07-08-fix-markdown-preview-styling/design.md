## Context

The Project Web GUI already renders Markdown with `react-markdown`, `remark-gfm`, `remark-math`, `rehype-katex`, KaTeX CSS, and custom Mermaid handling. The current viewer only gives `.markdown-view` a border and padding; it does not set a reading surface, text color, line height, heading rhythm, table style, or loading state.

Playwright inspection showed that the wrapper has `dockview-theme-light`, but the inner Dockview root still computes the Abyss dark variables and paints content with `#000c18`. The Markdown text then inherits the app body color `#14202e`, producing dark text on a dark surface. Markdown Live Preview and GitHub README rendering both use a white preview surface, dark readable text, 16px base type, 1.5 line height, bordered headings, light code blocks, muted blockquotes, and simple bordered tables.

## Goals / Non-Goals

**Goals:**

- Render Markdown records on a readable light preview surface inside Dockview.
- Apply Dockview's light theme through the Dockview API so panel chrome and content variables agree.
- Style Markdown common elements in a GitHub-like way, informed by Markdown Live Preview.
- Preserve existing Markdown libraries and support for GFM, math, KaTeX, Mermaid, images, and links.
- Show a loading state while Markdown render data is pending instead of showing an empty fallback too early.
- Verify with Playwright using the real Flash Attention topic record plus synthetic Markdown coverage examples.

**Non-Goals:**

- Do not add MDX, a new Markdown parser, syntax-highlighting dependency, or a full editor.
- Do not change backend record rendering, artifact storage, or query-index behavior.
- Do not redesign the whole Dockview workbench.
- Do not implement dark-mode Markdown styling in this slice.

## Decisions

### Use Dockview's Theme API

Import Dockview's `themeLight` and pass it to `DockviewReact`. This should make the internal `.dv-dockview` root use light theme variables instead of relying on an outer wrapper class that the component does not treat as its active theme.

Alternative considered: override Dockview CSS variables manually from `.dock-host`. That would be brittle because Dockview already exposes a theme contract and may compute layout details from the theme object.

### Make Markdown Preview a Self-contained Surface

Set explicit `background`, `color`, `font-size`, `line-height`, and font family on `.markdown-view`, with a white surface and GitHub-style text colors. This keeps the Markdown readable even if a future Dockview theme changes behind it.

Alternative considered: inherit panel colors from Dockview. That repeats the current failure mode and makes Markdown readability depend on workbench chrome theme.

### Use GitHub-like Element Rules

Style Markdown elements under `.markdown-view`: headings, paragraphs, lists, blockquotes, links, inline code, pre/code blocks, tables, images, horizontal rules, KaTeX display blocks, and Mermaid blocks. Keep values close to Markdown Live Preview/GitHub defaults: 16px body, 1.5 line-height, `#1f2328` body text, `#59636e` muted text, `#0969da` links, `#f6f8fa` code backgrounds, and `#d1d9e0` borders.

Alternative considered: import a third-party prose CSS package. The app only needs a compact viewer style now, and hand-written scoped CSS avoids a new dependency and keeps control of Dockview integration.

### Distinguish Loading from Empty Markdown

Pass Markdown render loading state into the viewer content path. While the render query is pending, show a neutral loading state on the preview surface. Only show "No rendered Markdown available." after the render query finishes with empty content.

Alternative considered: keep the current fallback. It incorrectly tells the user content is absent during slow but successful on-demand renders.

## Risks / Trade-offs

- Dockview theme imports may use a different export path than expected. → Use the installed Dockview type declarations to select the stable exported `themeLight` symbol.
- CSS scoped to `.markdown-view` can conflict with global `table`, `th`, and `td` rules. → Put Markdown-specific table selectors after the generic table rules or use more specific `.markdown-view table` selectors.
- Rendered Markdown may contain very long words, paths, JSON, or tables. → Add overflow handling, max image widths, and wrapping rules without hiding content.
- Visual checks can be subjective. → Add computed-style assertions for contrast-critical values and screenshot checks with real content examples.

## Migration Plan

1. Apply Dockview light theme through `DockviewReact`.
2. Update `ViewerContent` and `MarkdownView` to distinguish loading, empty, and rendered states.
3. Add scoped Markdown preview CSS modeled on Markdown Live Preview/GitHub README rendering.
4. Add frontend tests for Markdown loading and empty states.
5. Rebuild static assets and run Playwright checks against the real Flash Attention Markdown record and synthetic Markdown examples.
6. Rollback by removing the theme prop and scoped Markdown CSS; backend data is unaffected.
