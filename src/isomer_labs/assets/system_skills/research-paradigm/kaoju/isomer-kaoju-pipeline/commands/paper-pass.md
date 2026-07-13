# Paper Pass

## Workflow

1. **Resolve context**. Identify the Research Topic, Research Inquiry, Topic Workspace, user request, clarification mode, accepted prior refs, and requested template name (default `main`).
2. **Validate prerequisites**. Require an accepted Audit Report and the exact accepted synthesis records needed by the paper, normally a Field Summary, Claim Status Table, Related-Work Catalog, Source Digests or Claim-Evidence Ledger, and optionally a Kaoju Dossier or comparison records. Verify record identity, latest and supersession posture, lineage, worker-output policy, format-profile support, build capability, and applicable Gate policy.
3. **Resolve the template**. Use the latest accepted template ref for the requested name; if none exists, return `paused` or `blocked` with the missing ref and a resume point.
4. **Invoke the writer**. Delegate manuscript and publication work to `$isomer-kaoju-write` with the verified refs and template.
5. **Apply the Gate**. Route publication-facing actions through the applicable Gate policy. A successful local build does not authorize external publication.
6. **Validate the result**. Require a successful build and an accepted validation report before accepting a Publication Bundle.
7. **Return terminal report**. Report `complete`, `paused`, or `blocked`, accepted output refs, stage outcomes, validation verdict, Gates, blockers, and a resume point when applicable.

If the request does not map cleanly to this recipe, use the native planning tool to build and execute a bounded paper-writing plan while preserving the audit-before-writing boundary.

## Trigger

Use when the user asks to write, draft, revise, build, validate, or bundle a survey paper from accepted Kaoju audit and synthesis records.

## Inputs

Require an accepted Audit Report, accepted synthesis refs, a resolved template ref, and a paper contract target or venue.

## Outputs

- `kaoju:paper-contract`
- `kaoju:survey-manuscript`
- `kaoju:paper-build-run`
- `kaoju:paper-validation-report`
- `kaoju:publication-bundle`
- Terminal resource, Gate, blocker, and resume information.

## Stop Conditions

Stop at `complete` when the bundle is accepted, or at `paused`/`blocked` when prerequisites, template, build, validation, or Gate policy is not satisfied. Do not invent evidence, skip validation, or start another survey procedure.

## Common Mistakes

- Treating compilation success as publication readiness.
- Allowing Markdown-to-PDF as the publication build path.
- Letting the writer strengthen verdicts or hide audited limitations.
- Skipping the Gate for submission-facing output.
