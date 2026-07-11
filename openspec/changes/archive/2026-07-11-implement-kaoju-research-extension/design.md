## Context

The packaged system-skill catalog currently contains the always-available core group and the optional DeepSci research extension. Its manifest, installer, callback catalog, and Project extension declarations already support additional optional extension groups without new CLI or persistence code. Research-paradigm validation, however, assumes that every active family is DeepSci, and there is no packaged skill family for evidence-led literature and codebase surveys.

The approved feature design in `context/features/2026-07-10-kaoju-research-extension/` defines nine survey use cases, a compact complex-procedure coordinator, ten peer stage skills, grouped dataset and survey helpers, and evidence rules that distinguish source inspection from first-hand execution. Implementation must turn that design into self-contained package assets while preserving generic Isomer ownership of Topic Workspace mutation, research records, provider calls, execution, and Gates.

## Goals / Non-Goals

**Goals:**

- Ship an installable optional extension with id `kaoju` and the active namespace `isomer-kaoju-*`.
- Implement the seven survey procedures, two grouped helper managers, clarification-first interaction mode, and terminal-report contract defined by the approved use cases.
- Keep stage guidance self-contained, concise, provider-neutral, and reusable outside one agent-team topology.
- Preserve exact source identity, evidence depth, evidence verdict, execution fidelity, Run purpose, comparison intent, failures, and provenance across stage handoffs.
- Extend the research-paradigm validator and package tests without changing existing DeepSci behavior.

**Non-Goals:**

- Add a Kaoju-specific database, CLI command group, execution adapter, literature provider, scheduler, or Artifact Format provider.
- Implement a Kaoju Domain Agent Team Template or require Houmao.
- Vendor papers, repositories, models, or datasets into the Python package.
- Turn repository refresh, environment repair, claim tracing, or generic resume into separate survey procedures.
- Implement new generic Topic Workspace, research-recording, artifact-format, installer, or Project extension-declaration mechanisms.

## Decisions

### 1. Package Kaoju as an Asset-Only Optional Extension

Create `src/isomer_labs/assets/system_skills/research-paradigm/kaoju/` and register one manifest group with `kind = "extension"`, `extension_id = "kaoju"`, and `always_available = false`. Existing system-skill discovery, installation, Project declaration, and callback code will consume the new catalog data.

This is preferred to a new Python extension module because the initial functionality is procedural agent guidance composed over existing provider, execution, workspace, and recording contracts. Runtime code is added only where the shared validator and tests must become family-aware.

### 2. Keep the Coordinator and Stage Skills Separate

Ship these eleven skills:

- `isomer-kaoju-pipeline`
- `isomer-kaoju-shared`
- `isomer-kaoju-workspace-mgr`
- `isomer-kaoju-frame`
- `isomer-kaoju-discover`
- `isomer-kaoju-acquire`
- `isomer-kaoju-examine`
- `isomer-kaoju-reproduce`
- `isomer-kaoju-compare`
- `isomer-kaoju-audit`
- `isomer-kaoju-synthesize`

Each directory contains `SKILL.md` and `agents/openai.yaml`; directly loaded commands and references stay inside that directory. The pipeline owns orchestration, while stage skills retain their input, output, stop, and blocker contracts. A monolithic skill was rejected because it would duplicate stage logic across procedures and make independent validation or direct stage invocation difficult.

### 3. Use a Small Complex-Procedure Command Surface

The pipeline exposes procedural command pages for `landscape-pass`, `curated-intake-pass`, `direction-expansion-pass`, `theory-comparison-pass`, `method-trial-pass`, `comparative-pass`, and `audit-survey-pass`.

It exposes helper command pages for `manage-survey` with actions `list`, `show`, `status`, and `export`, and `manage-dataset` with actions `register`, `list`, `show`, `refresh`, and `remove`. CRUD-like operations remain grouped by object. `help` stays in the entrypoint, clarification-first remains an interaction mode, and resume remains pipeline context rather than separate commands.

Standalone source-audit, reproduction, full-Kaoju, list-pass, refresh, and resume procedures are intentionally absent because they do not correspond to approved survey use cases.

### 4. Centralize Evidence and Handoff Rules

`isomer-kaoju-shared` owns directly linked references for evidence semantics, survey artifact vocabulary, source identity, interaction and Gate rules, external-owner routing, and terminal status. Every stage skill links to the shared rules and states only its stage-specific procedure.

The pipeline and stage skills use canonical Artifacts, Evidence Items, Research Claims, Findings, Runs, Decision Records, Gates, and Provenance Records. They may produce file-backed Markdown or JSON Artifacts through existing recording APIs, but the first release does not add Kaoju-specific schemas or a record-format provider. This avoids a premature storage model while preserving durable refs and the canonical `title` and `summary` display contract when structured records are written.

All normal procedures include audit before synthesis. Direct invocation of synthesize requires an accepted Audit Report; the initial implementation does not expose an audit waiver that can claim audited readiness.

### 5. Route Mutations and Expensive Work to Existing Owners

Repository registration, managed dataset links, Topic Workspace topology, environment mutation, credentials, private data, large downloads, builds, and accelerator Runs remain governed by existing operator, service, provider-binding, execution-adapter, and Gate contracts. Kaoju records the requested action and consumes the returned refs; it does not teach agents to bypass the owner.

`manage-dataset register`, `refresh`, and `remove` therefore route mutation to `isomer-op-topic-mgr` or the resolved Topic Workspace owner. Method trials and empirical comparisons route environment work to the existing environment setup skills and resource-heavy work through `isomer-misc-bounded-run-tips`.

### 6. Register Begin and End Callback Metadata

Every manifest-listed Kaoju skill exposes the existing `begin` and `end` callback insertion points. Skills apply callbacks after mandatory context checks and before their first stage-specific action, and again after tentative outputs but before final handoff. This matches the packaged callback catalog without inventing Kaoju-specific callback stages.

### 7. Make Research-Paradigm Validation Family-Aware

Refactor `scripts/validate_research_paradigm_skillset.py` around explicit family configuration rather than broadening DeepSci regexes. The DeepSci configuration retains its current inventory, placeholder, source-lineage, and structured-output checks. The Kaoju configuration adds its exact eleven-skill inventory, `isomer-kaoju-*` folder and manifest identity checks, near-top workflow requirements, direct-reference integrity, forbidden hard-coded provider or local paths, canonical Isomer terminology, command-surface coverage, and no-extra-procedure checks.

Shared validation remains common where rules truly match, such as frontmatter, `agents/openai.yaml`, self-contained references, global CLI spelling, and deterministic diagnostics. Family-specific tests protect DeepSci behavior from regression.

### 8. Validate Through Catalog, Installer, and Contract Tests

Update system-skill asset tests to expect `core`, `deepsci`, and `kaoju`; verify all Kaoju paths resolve and all callback metadata is discoverable. Update installer tests to select `--extension kaoju`, install all eleven flat skill directories, and preserve core-plus-extension selection semantics. Add validator fixtures for valid Kaoju bundles and failures involving wrong namespace, missing skills, broken references, command drift, and stale domain terms.

No networked paper search, repository clone, model download, or GPU Run belongs in unit tests. Skill text and package integration are deterministic test targets; live research behavior remains manual or future acceptance work.

## Risks / Trade-offs

- **Skill text may drift across eleven directories** → Keep shared rules in `isomer-kaoju-shared`, make stage files short, and validate direct reference integrity and command inventory.
- **Agents may overstate search snippets, generated-data results, or repaired Runs** → Encode evidence depth, Run purpose, execution fidelity, and exact-ref red flags in shared guidance and each relevant stage.
- **Kaoju validation could weaken or break DeepSci checks** → Use family-specific configuration and retain the full existing DeepSci regression suite.
- **External providers or executable materials may be unavailable** → Require explicit blockers and terminal `paused` or `blocked` reports instead of hidden substitutions.
- **Dataset symlinks could be mistaken for identity or authority** → Require Topic Dataset Manifest identity and route all link mutation through the Topic Workspace owner.
- **Asset-only implementation cannot enforce every runtime rule mechanically** → State this boundary, test the procedural contracts, and rely on existing Gates, recording validation, and owner skills for enforceable runtime behavior.

## Migration Plan

1. Add the Kaoju asset tree and validate every skill independently.
2. Add the `kaoju` manifest group and begin/end callback metadata.
3. Extend research-paradigm documentation and family-aware validation.
4. Update asset, installer, callback, namespace, and validator tests.
5. Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and the research-paradigm validation script.
6. Existing installations remain unchanged until users install or upgrade with the Kaoju extension selected. Rollback removes the catalog group and packaged assets; already projected user copies remain user-controlled and can be removed through the existing system-skill uninstaller.

## Open Questions

No implementation-blocking questions remain. Kaoju-specific Artifact Format profiles and a fixed Domain Agent Team Template are deferred until usage demonstrates a stable need.
