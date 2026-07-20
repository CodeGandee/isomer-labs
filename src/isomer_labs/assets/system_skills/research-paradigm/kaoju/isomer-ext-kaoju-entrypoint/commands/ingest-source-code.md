---
skill_invocation_notation: >
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Ingest Source Code

## Workflow

1. Resolve a repository URL, repository name, paper ref, or Reading List item to candidate repository identities. Report ambiguity before acquisition.
2. Perform bounded associated-paper metadata discovery. Present normal selection and approval before deep paper ingestion; do not treat a repository README as a primary work when a paper or report exists.
3. Choose a valid non-main `topic.repos.*` label and query `isomer-cli --print-json project paths default <label>` for a non-mutating candidate unless the user supplied another safe target.
4. Honor the user's exact repository commands. Otherwise, let `isomer-ext-kaoju-entrypoint->acquire` select external commands suited to the source, revision, credentials, submodules, LFS, sparse or partial posture, history needs, and resource limits. Run them through the ordinary user or agent command surface outside Isomer.
5. Verify the resolved source locator, intended relationship, target, and immutable commit or digest with external checks. On failure or partial content, leave the target under external ownership, create a sanitized blocker, and stop before registration.
6. Register the verified existing target with `isomer-cli --print-json project repos register <label> --path <target>`. A registration conflict leaves the target unchanged and pauses at registration.
7. Create or revise `KAOJU:ASSOCIATED-SOURCE-CODE` and `KAOJU:ARTIFACT-LIBRARY` with the semantic label, requested and resolved locators, immutable identity, selected external method, sanitized command evidence, observation time, access, license, relationship basis, limitations, blockers, and provenance refs.
8. Use `isomer-ext-kaoju-entrypoint->examine` for code findings. Every finding cites repository ref, immutable commit, file, and line range and stays distinct from paper claims and executed behavior.
9. If an associated paper is selected for ingestion, route it through `ingest-reading-item` after approval.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owners: `isomer-ext-kaoju-entrypoint->acquire` and `isomer-ext-kaoju-entrypoint->examine`. Outputs: canonical repository, associated-source-code, artifact-library, Source Digest, blocker, and provenance refs.

## Gates, Blockers, and Resume

Repository and paper selection require approval when ambiguous. Inaccessible source, authentication failure, external command failure, partial content, identity mismatch, relationship uncertainty, registration conflict, or Artifact failure creates a blocker. Resume at resolve, select, acquire, verify, register, record, relate, inspect, or approve-paper-ingestion. Isomer never removes or repairs partial external content.
