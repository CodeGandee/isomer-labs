# Deferred Venue Templates

DeepScientist `write/templates/` contains a broad venue LaTeX tree for AAAI, ACL, ASPLOS, COLM, ICLR, ICML, NeurIPS, NSDI, OSDI, and SOSP-style paper drafting. This slice does not import those files into `assets/`.

## Decision

Defer venue template import. The templates are useful upstream material, but they mix official venue samples, style files, example papers, TODO macros, source-local notes, and assumptions about a concrete paper layout. They are too large and venue-specific to make active Isomer assets without a separate sanitization pass.

## Why Not Import Now

- The templates imply concrete manuscript layouts that Isomer has not settled; use paper Artifact resolved by Workspace Path Resolution when a paper output must be named.
- Some files contain sample manuscript content, venue instructions, TODO macros, or source-local template notes that are not directly useful as an Isomer writing method.
- Importing multiple venue packages would increase bundle size without improving the core writing workflow.
- Venue style files can carry license and update obligations that should be checked in a resource-focused follow-up.

## Follow-up Import Criteria

Import a venue template only when the user or an accepted Isomer design chooses a venue, the license context is preserved, sample content is removed or clearly marked as upstream sample material, TODO macros and source-local notes are removed, required dependencies are documented, and the template is linked from the writing workflow as an optional asset rather than a default paper layout.

## Current Guidance

For now, use a user-provided manuscript source, a project-provided template, or a future accepted Isomer paper-layout asset. The writing skill should still produce LaTeX-ready replacement text, section plans, bibliography checks, and bundle readiness notes without assuming a specific venue tree.
