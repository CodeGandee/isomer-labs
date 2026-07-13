# LaTeX Build

Every publication build is a reproducible Run that compiles the bound `.tex` source through a Tectonic-first LaTeX workflow.

## Build Policy

- Attempt Tectonic first when the source and template are compatible.
- Record the exact command, engine version, logs, warnings, outputs, and terminal result.
- If Tectonic is unavailable, incompatible, prohibited by the venue, or fails for a concrete reason, record that reason before falling back to `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, Biber, or a venue-required workflow.
- Do not invoke Pandoc, browser print-to-PDF, or any Markdown-to-PDF conversion as a compilation substitute.

## Build Run Record

- `.tex` entry point and included-file digests
- bibliography and style file refs
- template digest
- engine and version
- exact command and environment
- output PDF and log refs
- warnings, resource use, terminal status
- Provenance Records

## Pre-Build Validation

Reject the build when the source contains:
- authored numeric section prefixes such as `\section{1. Introduction}`
- malformed section hierarchy
- unresolved title metadata
- invalid citation or display refs
- direct Markdown-to-PDF commands
- template-incompatible structural commands

## Fallback Disclosure

Every fallback records the unavailable tool, template constraint, venue requirement, or concrete Tectonic failure before execution.
