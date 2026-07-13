# Create Paper Template

## Workflow

1. **Resolve context**. Identify the Research Topic, Research Inquiry, Topic Workspace, user request, and requested template name (default `main`).
2. **Determine template posture**. Use the venue, paper type, and target from the user request or paper contract to select a document class and engine posture.
3. **Generate files**. Write a `.tex` entry point, bibliography stub, style and included files, and `README.md` under `intent/derived/writing-template/<template-name>/`.
4. **Compile preview**. Run a Tectonic-first LaTeX build on the generated source. Record the command, engine, version, logs, warnings, outputs, and terminal result.
5. **Record template artifact**. Create or update a research record of kind `artifact` with semantic-id `kaoju:writing-template` and profile `kaoju:writing-template`. Store `template_name`, `venue`, `paper_type`, `tex_entry`, `preview_pdf_ref`, `source` (`generated`), `engine_posture`, and `status`.
6. **Return**. Report the template name, record id, file refs, and preview build status. If the preview cannot compile, return `blocked` with diagnostics.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a bounded template-generation plan while keeping files under `intent/derived/writing-template/`.

## Trigger

Use when the user asks to generate, create, or prepare a LaTeX paper-writing template for a Kaoju paper.

## Inputs

Require a Research Topic and Topic Workspace. Accept optional `--name`, `--venue`, `--paper-type`, and `--from-record`.

## Outputs

- Generated LaTeX template files under `intent/derived/writing-template/<template-name>/`.
- Proof-of-compilation PDF preview.
- `kaoju:writing-template` research record.

## Stop Conditions

Stop at `complete` when the template compiles and the record is stored, or at `blocked` when generation or preview compilation fails. Do not treat the preview PDF as the final paper PDF.

## Common Mistakes

- Treating the generated template files as canonical survey state.
- Treating the preview PDF as the paper's publication PDF.
- Skipping the preview compile and storing a broken template as `ready`.
