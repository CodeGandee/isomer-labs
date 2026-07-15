# Build Paper PDF

## Workflow

1. Resolve the accepted canonical MyST template and draft, citation map, paper line, current TeX compatibility fingerprint, and publication Gate policy.
2. Invoke `ext kaoju paper init-tex`. Parse MyST structurally, initialize or reuse `KAOJU:PAPER-TEMPLATE-TEX`, and regenerate `KAOJU:PAPER-DRAFT-TEX`. Record conversion identity, source checksums, citations, included files, lineage, and unsupported directive, table, citation, float, raw-block, or venue diagnostics.
3. Require the write agent to inspect and repair derived TeX directly. Initialization never claims build readiness.
4. After build authorization, invoke `build-pdf` through the `document_build` extension point. Record a distinct Run, exact toolchain, fallback rationale, compile log, and outputs.
5. Permit bounded automatic presentation-only or TeX-syntax repair that preserves canonical MyST and evidence meaning. Any canonical content, dependency, toolchain policy, or interpretation change requires a revised plan and human Gate.
6. Validate PDF media type, digest, extracted text, hierarchy, citations, page sequence, displays, clipping, overflow, blank pages, density, and publication-quality profile before the publication Gate.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-write`. Outputs: derived TeX template and draft, immutable build Run and compile log, PDF, PDF revision log, validation report, and publication bundle refs.

## Gates, Blockers, and Resume

Build and publication Gates are distinct. Resume at MyST validation, TeX initialization, agent repair, build authorization, build repair, PDF inspection, or publication acceptance.
