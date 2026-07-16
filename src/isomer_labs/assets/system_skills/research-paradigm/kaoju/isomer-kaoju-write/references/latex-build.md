# Derived TeX and PDF Build

Every PDF build is a distinct reproducible Run derived from accepted MyST state and the selected named template's stable ref and observed tree digest. TeX is an inspected conversion product, not canonical paper state.

## Initialization and Inspection

- Parse MyST structurally and record the selected template name, stable ref, observed tree digest, source checksums, citations, included files, unsupported constructs, and conversion diagnostics.
- Fingerprint the selected template identity and observed digest, venue or document class, toolchain policy, required directives, tables, citations, floats, raw blocks, and venue structure.
- Reuse a compatible TeX template. Revise an incompatible template and preserve both versions.
- Require direct agent inspection of derived TeX before claiming build readiness.

## Build Policy

- Route the exact command through the `document_build` Research Operation Extension Point and Execution Adapter Command Request.
- Attempt the selected compatible engine and record its version, logs, warnings, outputs, and terminal status.
- Record a concrete unavailable-tool, template, venue, or compile-failure reason before any fallback.
- Automatic post-authorization repair is limited to presentation-only or TeX syntax changes. Canonical content, dependencies, toolchain policy, or interpretation changes require a revised plan and human Gate.
- Never use browser print-to-PDF or a Markdown-to-PDF conversion as a substitute for the MyST-to-TeX build graph.

## Run and Output Records

Record the canonical MyST refs, selected template name, stable ref and observed digest, TeX template and draft manifests, included-file digests, bibliography refs, engine and exact command, environment identity, compile log, output PDF checksum and media type, inspection result, repair classification, fallback rationale, resource use, terminal status, publication Gate, and Provenance Records.
