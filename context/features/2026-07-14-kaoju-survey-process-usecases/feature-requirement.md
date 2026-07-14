# Kaoju Survey Process Use Cases Feature Requirement

## Goal

Define a coherent set of user-facing use cases for the Kaoju evidence-led survey process. The use cases must cover the full lifecycle from an initial topic or research interest through proposing a survey direction, collecting online information, analyzing collected materials, optionally testing claims with code, forming structured records, and producing a survey paper or dossier.

## Non-Goals

- Re-implementing the underlying Kaoju stage skills (frame, discover, acquire, examine, audit, synthesize, write).
- Replacing the existing `isomer-kaoju-pipeline` public procedures.
- Defining a new storage backend or artifact format; use existing `kaoju:*` semantic ids.
- Covering DeepSci hypothesis-driven research workflows.

## Users And Workflows

- **Human Researcher / Topic Actor**: Has a topic or question and wants the system to help scope, collect, analyze, and record a survey.
- **Project Operator**: Wants to launch or supervise a survey workflow for a registered Research Topic without manually invoking each Kaoju stage skill.
- **Reviewing Agent**: Needs to verify that survey records are well-formed, auditable, and ready for synthesis or paper writing.

## Functional Requirements

- Accept a topic or research question and propose one or more bounded survey directions.
- For an accepted direction, collect online information from papers, technical reports, documentation, repositories, and other primary sources.
- Analyze collected information to extract claims, evidence, contradictions, limitations, and source locators.
- Form structured records (Source Digests, Claim-Evidence Ledger entries, Discovery Ledger) that conform to Kaoju artifact semantics and are registered in the topic workspace state database with metadata and filesystem links.
- Optionally route executable claims to code testing or first-hand trials.
- Support iteration: return to discovery or examination when audit identifies gaps.
- Produce synthesis records (Field Summary, Related-Work Catalog, Claim Status Table) and, when requested, a MyST paper draft via a two-stage structure-then-fill workflow. Markdown and LaTeX/PDF are derived views.

## System Boundaries

- In scope: user-facing workflow orchestration, direction proposal, online collection, analysis, structured record formation, audit-before-synthesis gate, and paper production.
- Out of scope: low-level web search provider implementation, LaTeX engine internals, Topic Workspace environment setup, Houmao agent team launch.

## Operational Constraints

- Each claim-bearing procedure must be audited before synthesis.
- Online collection must record query provenance and source identity.
- Structured records must use canonical Kaoju semantic ids and profiles.
- Paper production is MyST-first and content-focused. Markdown is an automatically derived review view; LaTeX formatting, PDF rendering, and citation styling are handled separately by converting the MyST draft to TeX.

## Assumptions

- The host project has the Kaoju extension installed and declared.
- A Topic Workspace and Topic Main Development Repository exist or can be created.
- Internet access is available for online source collection.
- Users accept clarification-first mode for material ambiguities.

## Decisions

- Direction proposal is agent-driven, clarification-first for material ambiguity, and subject to explicit human selection before the direction set becomes accepted input.
- `isomer-kaoju-pipeline` remains a thin intent router to capability-owning Kaoju skills. The skills use typed `isomer-cli project` and `isomer-cli ext kaoju` services for deterministic operations defined by the OpenSpec design.
- The use cases do not introduce another top-level workflow skill. They are public intent procedures with compatibility routes from existing pipeline procedures and operator-facing documentation.
