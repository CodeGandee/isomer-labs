---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
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
2. Require the Run-scoped `source-code.ingest` Mindset Record handed off by the public entrypoint. Verify its pinned Research Topic, Survey Contract, Run scope, Source path and digest, and immutable materialized inventory. Do not re-read a changed Mindset Source during this Run.
3. Perform bounded associated-paper metadata discovery. Present normal selection and approval before deep paper ingestion; do not treat a repository README as a primary work when a paper or report exists.
4. Choose a valid non-main `topic.repos.*` label and query `isomer-cli --print-json project paths default <label>` for a non-mutating candidate unless the user supplied another safe target.
5. Honor the user's exact repository commands. Otherwise, let `isomer-ext-kaoju-entrypoint->acquire` select external commands suited to the source, revision, credentials, submodules, LFS, sparse or partial posture, history needs, and resource limits. Run them through the ordinary user or agent command surface outside Isomer.
6. Verify the resolved source locator, intended relationship, target, and immutable commit or digest with external checks. On failure or partial content, leave the target under external ownership, create a sanitized blocker, and stop before registration.
7. Register the verified existing target with `isomer-cli --print-json project repos register <label> --path <target>`. A registration conflict leaves the target unchanged and pauses at registration.
8. Create or revise `KAOJU:ASSOCIATED-SOURCE-CODE` and `KAOJU:ARTIFACT-LIBRARY` with the semantic label, requested and resolved locators, immutable identity, selected external method, sanitized command evidence, observation time, access, license, relationship basis, limitations, blockers, and provenance refs.
9. Use `isomer-ext-kaoju-entrypoint->examine` for code findings and pass the Mindset Record ref. Every finding cites repository ref, immutable commit, file, and line range and stays distinct from paper claims and executed behavior.
10. Answer and checkpoint every materialized question, mark unsupported answers unresolved or not applicable with rationale, cite exact evidence refs, and check the `additional-questions` collector. Ordinary mid-reading questions remain in Source Digest, Claim-Evidence Ledger, Associated Source Code, or another applicable reading Artifact unless the user explicitly targets the Record or both Record and Source.
11. If an associated paper is selected for ingestion, route it through `ingest-reading-item` after approval and materialize the applicable paper Mindset Record separately.
12. Before completing, pausing, or blocking, checkpoint a terminal Mindset Record with every materialized and explicitly assigned supplemental question classified, the collector checked, evidence retained, and unresolved questions visible. Claim-bearing acceptance requires this terminal Record.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owners: `isomer-ext-kaoju-entrypoint->acquire` and `isomer-ext-kaoju-entrypoint->examine`. Input: Run-scoped `source-code.ingest` Mindset Record ref. Outputs: terminal Mindset Record, canonical repository, associated-source-code, artifact-library, Source Digest, blocker, and provenance refs.

## Gates, Blockers, and Resume

Repository and paper selection require approval when ambiguous. Inaccessible source, authentication failure, external command failure, partial content, identity mismatch, relationship uncertainty, registration conflict, or Artifact failure creates a blocker. Resume at resolve, select, acquire, verify, register, record, relate, inspect, or approve-paper-ingestion. Isomer never removes or repairs partial external content.
