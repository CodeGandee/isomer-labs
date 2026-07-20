# Derived TeX and PDF Build

Every PDF build is a distinct reproducible Run derived from accepted MyST state, its observed content-template identity, and an independent exact named LaTeX-template state. TeX is an inspected composition product, not canonical paper state.

## Composition Contract

MyST is canonical and complete: it holds every claim, citation, table, and section that appears in the TeX version, or more. TeX is a presentational projection; drift between MyST and TeX is permitted only for venue formatting. Composition is an agent fill, not a mechanical conversion — the agent reads the filled MyST and fills the real venue template by content judgment.

## Initialization and Fill

- Scaffold from the adopted LaTeX template tree; record the content-template identity and source checksum separately from presentation state.
- Resolve an explicit LaTeX template or LaTeX `main`; snapshot its exact multi-file tree, stable ref, name, state token, digest, authored metadata, entrypoint, composition contract, build profile, provenance, and license posture. Adoption packs the real venue tree; a hand-written shim that only names or checksums an external official template is rejected.
- Fingerprint LaTeX state, composition contract, converter identity, required directives, tables, citations, floats, raw blocks, and build profile. Do not include the content-template digest in the presentation fingerprint.
- The initializer extracts MyST frontmatter (title, authors, date) and the abstract into the fill manifest (`.isomer-kaoju-tex-fill.json`), marks table and directive locations, collects citation-map entries, and returns each composition obligation as pending. It does not pretend conversion succeeded.
- The agent then fills: frontmatter into the venue title and author constructs, abstract and keywords into their environments, sections mapped to venue structure, a venue bibliography materialized from citation-map entries so every `\cite` resolves, real venue tables for marked Markdown tables, venue-correct directive handling. Decisions go in the composition record.
- Raw frontmatter in the TeX body, placeholder or empty title and author, scaffold `Title` or `Abstract` sections, `\cite` keys without a bibliography, and leftover fill or repair markers are unfilled obligations reported by `tex-status`; `build-pdf` refuses a tree while any remain.
- Report working-copy drift, stocked-template drift, and paper-local repair drift separately; none triggers automatic mutation.

## Build Policy

- Route the exact command through the `document_build` Research Operation Extension Point and Execution Adapter Command Request.
- Verify that the TeX draft pins the supplied or implied snapshot ref and digest before execution, then compile its declared entrypoint with the registered build profile.
- Record the engine, exact entrypoint, logs, warnings, outputs, terminal status, and any concrete unavailable-tool or compile-failure reason.
- Post-authorization repair is limited to the paper-specific TeX draft. Canonical content, dependencies, build profile, or interpretation changes require a revised plan and human Gate. Named LaTeX stock changes require an explicit user-authorized template update.
- Never use browser print-to-PDF or a Markdown-to-PDF conversion as a substitute for the MyST-to-TeX build graph.

## Run and Output Records

Record canonical MyST refs and checksum, observed content-template identity, observed LaTeX-template identity, exact TeX snapshot and draft manifests, fill manifest and resolved obligations, composition contract, declared entrypoint, included-file digests, bibliography refs, engine and exact command, environment identity, compile log, template and repair drift, output PDF checksum and media type, inspection result, repair classification, resource use, terminal status, publication Gate, and Provenance Records.
