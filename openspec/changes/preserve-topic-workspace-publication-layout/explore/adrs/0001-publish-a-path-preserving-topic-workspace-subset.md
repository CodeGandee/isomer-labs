# Publish a Path-Preserving Topic Workspace Subset

Topic publication will retain every selected source-backed path at the same normalized Topic Workspace-relative path. Privacy and selection policy may omit a path, but publication will not relocate retained siblings or create placeholders for excluded or empty directories; this preserves reproduction paths without exposing private structure or inventing a semantic export taxonomy.

## Status

accepted

## Considered Options

- Publish a path-preserving subset.
- Reproduce the literal directory skeleton with placeholders for excluded content.
- Reorganize retained content into publication-specific directories such as `environment/`.

## Consequences

- Structural validation compares retained source paths directly with publication paths.
- Custom Topic Workspace layouts remain valid because publication preserves resolved paths rather than hard-coding the default layout.
- Git-empty directories and directories containing only excluded content are absent.
- Publication-only generated files require a separately defined namespace and do not weaken the source-path identity rule.
