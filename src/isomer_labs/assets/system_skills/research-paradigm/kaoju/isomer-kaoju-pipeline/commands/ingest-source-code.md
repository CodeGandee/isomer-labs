# Ingest Source Code

## Workflow

1. Resolve a repository URL, repository name, paper ref, or Reading List item to candidate repository identities. Report ambiguity before acquisition.
2. Perform bounded associated-paper metadata discovery. Present normal selection and approval before deep paper ingestion; do not treat a repository README as a primary work when a paper or report exists.
3. Invoke `isomer-cli project repos acquire` for the selected remote and semantic label. Record verified remote, immutable commit, depth posture, command request, and provenance only after successful clone validation.
4. Create or revise `KAOJU:ASSOCIATED-SOURCE-CODE` with associated paper refs and relationship verification, and update `KAOJU:ARTIFACT-LIBRARY`.
5. Use `$isomer-kaoju-examine` for code findings. Every finding cites repository ref, immutable commit, file, and line range and stays distinct from paper claims and executed behavior.
6. If an associated paper is selected for ingestion, route it through `ingest-reading-item` after approval.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owners: `$isomer-kaoju-acquire` and `$isomer-kaoju-examine`. Outputs: canonical repository, associated-source-code, artifact-library, Source Digest, blocker, and provenance refs.

## Gates, Blockers, and Resume

Repository and paper selection require approval when ambiguous. Inaccessible remote, authentication failure, clone failure, relationship uncertainty, or source access creates a blocker. Resume at resolve, select, acquire, relate, inspect, or approve-paper-ingestion.
