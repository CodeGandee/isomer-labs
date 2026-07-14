# Kaoju Paper Templates Are Agent-Generated, Editable Artifacts

Kaoju paper writing needs reproducible LaTeX templates, but the project does not want to ship bundled venue templates or assume host-provided templates exist. We decided that `isomer-kaoju-pipeline` will expose a public `create-paper-template` subcommand that generates a LaTeX template tree under `intent/derived/writing-template/<template-name>/`. `main` is the reserved default template name: when no name is specified, the command operates on `main`, and `paper-pass` resolves to `main` when no explicit template is named. Multiple named templates may coexist for different venues, paper types, or revision experiments, but `main` is the single default per topic. The generated template is an editable artifact: the user may modify the LaTeX files, and `paper-pass` consumes the latest accepted template ref without opening a dedicated Gate. The command also produces a proof-of-compilation PDF preview to verify the template builds before drafting begins.

## Status

Accepted

## Considered Options

- **Ship bundled venue templates** (like DeepSci does). Rejected because it adds maintenance burden for venue-specific `.sty`/`.cls`/`.bst` files and does not solve the general case.
- **Require host-provided templates only**. Rejected because it makes acceptance tests and CI non-deterministic.
- **Generate a template inside `paper-pass` without a public subcommand**. Rejected because it prevents users from inspecting, editing, or reusing a template independently of a full paper pass.
- **Open a human Gate before template use**. Rejected because Gates are for irreversible or claim-shaping decisions; template edits are ordinary artifact revisions.
- **Treat the generated PDF as the final paper PDF**. Rejected because it would break the immutable `paper-build-run` lineage and conflate template verification with manuscript publication.

## Consequences

- `isomer-kaoju-pipeline` gains an eighth procedural subcommand, `create-paper-template`.
- The Kaoju skill inventory grows from eleven to twelve skills, and the pipeline command surface now includes `paper-pass` and `create-paper-template`.
- The paper contract records the accepted template ref, `.tex` entry point, document class or template posture, and included-file refs.
- `create-paper-template` must itself use the existing `document_build` extension point to compile a preview, recording the attempt as a Run or template-internal build record distinct from `kaoju:paper-build-run`.
- Template generation failures block template acceptance, but template edits do not require Gate approval.
- The `intent/derived/writing-template/<template-name>/` path becomes a stable convention for derived paper-writing templates. `main` is the reserved default template name; `create-paper-template` and `paper-pass` resolve to `main` when no explicit name is given, and there is one default template per topic at a time.
