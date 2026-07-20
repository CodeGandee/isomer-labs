# Derived TeX and PDF Build

Every PDF build is a distinct reproducible Run derived from accepted MyST state, its observed content-template identity, and an independent exact named LaTeX-template state. TeX is an inspected composition product, not canonical paper state.

## Initialization and Inspection

- Parse MyST structurally and record its content-template identity and source checksum separately from presentation state.
- Resolve an explicit LaTeX template or LaTeX `main`; snapshot its exact multi-file tree, stable ref, name, state token, digest, authored metadata, entrypoint, composition contract, build profile, provenance, and license posture.
- Fingerprint LaTeX state, composition contract, converter identity, required directives, tables, citations, floats, raw blocks, and build profile. Do not include the content-template digest in the presentation fingerprint.
- Compose preamble, marker, or include mode into a self-contained TeX draft, preserve template-owned classes and styles, and require direct agent inspection before build readiness.
- Report working-copy drift, stocked-template drift, and paper-local repair drift separately; none triggers automatic mutation.

## Build Policy

- Route the exact command through the `document_build` Research Operation Extension Point and Execution Adapter Command Request.
- Verify that the TeX draft pins the supplied or implied snapshot ref and digest before execution, then compile its declared entrypoint with the registered build profile.
- Record the engine, exact entrypoint, logs, warnings, outputs, terminal status, and any concrete unavailable-tool or compile-failure reason.
- Post-authorization repair is limited to the paper-specific TeX draft. Canonical content, dependencies, build profile, or interpretation changes require a revised plan and human Gate. Named LaTeX stock changes require an explicit user-authorized template update.
- Never use browser print-to-PDF or a Markdown-to-PDF conversion as a substitute for the MyST-to-TeX build graph.

## Run and Output Records

Record canonical MyST refs and checksum, observed content-template identity, observed LaTeX-template identity, exact TeX snapshot and draft manifests, composition contract, declared entrypoint, included-file digests, bibliography refs, engine and exact command, environment identity, compile log, template and repair drift, output PDF checksum and media type, inspection result, repair classification, resource use, terminal status, publication Gate, and Provenance Records.
