# project-web-markdown-preview Specification

## Purpose
TBD - created by archiving change fix-markdown-preview-styling. Update Purpose after archive.
## Requirements
### Requirement: Markdown records render on a readable preview surface
The Project Web GUI SHALL render Markdown record content on an explicit readable preview surface rather than relying on inherited Dockview colors.

#### Scenario: Markdown preview uses light readable colors
- **WHEN** a user opens a Markdown record detail tab
- **THEN** the Markdown preview has a light background, dark readable body text, and sufficient contrast for headings, paragraphs, lists, code, and detail labels
- **AND** the content remains readable even when Dockview is mounted inside the workbench

#### Scenario: Dockview workbench uses intended light theme
- **WHEN** the Project Web GUI mounts the Dockview workbench
- **THEN** Dockview panel chrome and content variables use the intended light theme
- **AND** Markdown panel content is not placed over an unintended dark Dockview surface

### Requirement: Markdown preview follows GitHub-like document styling
The Project Web GUI SHALL style Markdown preview elements in a manner comparable to Markdown Live Preview and GitHub README rendering.

#### Scenario: Common Markdown elements are styled
- **WHEN** Markdown content includes headings, paragraphs, links, emphasis, unordered lists, ordered lists, blockquotes, inline code, code blocks, tables, images, horizontal rules, math, or Mermaid blocks
- **THEN** each element renders with readable spacing, typography, borders, and overflow behavior appropriate for a document preview

#### Scenario: Large or wide Markdown content stays usable
- **WHEN** Markdown content includes long paths, long words, wide code blocks, tables, or images
- **THEN** the preview preserves the content and provides wrapping or scrolling without causing incoherent overlap

### Requirement: Markdown render state is accurate
The Project Web GUI SHALL distinguish pending Markdown rendering from completed empty Markdown rendering.

#### Scenario: Render query is pending
- **WHEN** a Markdown record has a render request in flight
- **THEN** the preview shows a loading state
- **AND** it does not claim that rendered Markdown is unavailable

#### Scenario: Render query completes with empty content
- **WHEN** a Markdown record render request finishes successfully with no Markdown content
- **THEN** the preview shows the empty Markdown fallback

#### Scenario: Render query completes with content
- **WHEN** a Markdown record render request finishes successfully with Markdown content
- **THEN** the preview replaces the loading state with the rendered Markdown document

