# Use Case 04: Write Paper From Digested Materials

## Actor Goal

As a researcher or Topic Actor, I want the agent to write a survey paper from the digested materials, so that I get a content-first MyST draft that I can review, revise, and later convert to Markdown or LaTeX/PDF.

## Use Case

The system reads the accepted synthesis records (`KAOJU:FIELD-SUMMARY`, `KAOJU:RELATED-WORK-CATALOG`, `KAOJU:CLAIM-STATUS-TABLE`) and the approved `KAOJU:SOURCE-DIGEST` artifacts produced by UC-03. The agent first builds a paper structure: a MyST document with section headings and placeholders for each part of the survey paper. It stores this as a durable `KAOJU:PAPER-STRUCTURE-MYST` artifact and asks the human to approve or refine the structure. Once approved, the agent fills the placeholders section by section, grounding every claim in the source digests and synthesis records. The result is a content-focused MyST paper draft stored as `KAOJU:PAPER-DRAFT-MYST`. The system can also derive a Markdown view (`KAOJU:PAPER-DRAFT-MD`) for human review. The human can review, ask for revisions, or approve the draft. LaTeX formatting, PDF rendering, and citation styling are handled in UC-06.

## Supported Actions

### Produce Paper Structure

Generate a MyST paper structure with placeholders from the digested materials.

- context
  - Actor **has** accepted synthesis records and source digests from prior use cases.
  - System **has** the `KAOJU:FIELD-SUMMARY`, `KAOJU:RELATED-WORK-CATALOG`, `KAOJU:CLAIM-STATUS-TABLE`, and approved `KAOJU:SOURCE-DIGEST` artifacts.
- intent
  - Actor **wants** an outline-level plan for the paper before the agent writes full prose.
  - Actor **wonders** "How will the paper be organized, and what will each section cover?"
- action
  - Actor then **asks** the system to produce a paper structure from the digested materials.
- result
  - Actor **gets** a durable `KAOJU:PAPER-STRUCTURE-MYST` artifact — a MyST file with section headings and placeholders — plus a rendered Markdown preview.

### Fill Paper Structure

Fill the approved paper structure with content grounded in the digested materials.

- context
  - Actor **has** an approved `KAOJU:PAPER-STRUCTURE-MYST` artifact.
  - System **has** the structure artifact and all source digests and synthesis records.
- intent
  - Actor **wants** the agent to write the actual paper content.
  - Actor **wonders** "Can you write the paper now?"
- action
  - Actor then **approves** the structure and asks the system to fill it.
- result
  - Actor **gets** a durable `KAOJU:PAPER-DRAFT-MYST` artifact in MyST, and optionally a derived `KAOJU:PAPER-DRAFT-MD` artifact for review.

### Review And Refine Paper

Review the draft and ask for section-level revisions.

- context
  - Actor **has** the rendered `KAOJU:PAPER-DRAFT-MYST` or derived `KAOJU:PAPER-DRAFT-MD`.
  - System **has** the draft artifact and the underlying source digests.
- intent
  - Actor **wants** to correct claims, improve flow, or add emphasis before finalizing.
  - Actor **wonders** "This section is too long; can you tighten it and add a comparison table?"
- action
  - Actor then **requests** revisions, **approves** the draft, or **asks** for a specific section to be rewritten.
- result
  - Actor **gets** an updated `KAOJU:PAPER-DRAFT-MYST` (and derived Markdown if enabled) and, once approved, a handoff ref to the next stage (PDF generation or submission).

## Main Flow

1. Actor asks the system to write a paper from the currently digested materials.
2. System reads the accepted synthesis records and approved source digests from the state database.
3. System proposes a paper structure: title, abstract, introduction, background, related work, method comparison, discussion, conclusion, references, and any appendices.
4. System writes the `KAOJU:PAPER-STRUCTURE-MYST` artifact as a MyST file with placeholders for each section.
5. Human reviews the structure (optionally via a derived Markdown preview) and approves it or asks for changes.
6. System fills the placeholders section by section, citing source digests and synthesis records.
7. System writes the `KAOJU:PAPER-DRAFT-MYST` artifact as a MyST file, and optionally derives `KAOJU:PAPER-DRAFT-MD`.
8. Human reviews the draft and requests revisions or approves it.
9. System updates the draft and reports the next allowed stage (PDF generation or submission).

## Alternative And Exception Flows

- **A1. No synthesis records**: If the required synthesis records are missing or unaudited, the system routes to the audit/synthesis stage and reports a blocker.
- **A2. Structure rejected**: If the human rejects the proposed structure, the system rewrites it and repeats the approval step.
- **A3. Section-level fill**: If the human asks for only one section to be filled at a time, the system fills that section and updates the draft incrementally.
- **A4. Formatting request**: If the human asks for LaTeX/PDF formatting, the system explains that formatting is handled by UC-06 and routes there.
- **E1. Claim without source**: If the agent cannot ground a drafted claim in an approved source digest, it flags the claim with a `citation-needed` marker rather than inventing a source.

## Mermaid Flow Diagram

```mermaid
flowchart LR
  Actor[Researcher / Topic Actor]

  subgraph System[Kaoju Survey Workflow]
    ReadSynthesis[Read synthesis records & digests]
    Propose[Produce paper structure]
    WriteStructure[Write KAOJU:PAPER-STRUCTURE-MYST]
    ReviewStructure[Review structure]
    Fill[Fill paper structure]
    WriteDraft[Write KAOJU:PAPER-DRAFT-MYST]
    ReviewDraft[Review draft]
  end

  Actor --> ReadSynthesis
  ReadSynthesis --> Propose
  Propose --> WriteStructure
  WriteStructure --> ReviewStructure
  ReviewStructure -->|approved| Fill
  ReviewStructure -->|refine| Propose
  Fill --> WriteDraft
  WriteDraft --> ReviewDraft
  ReviewDraft -->|approved| Next["Export / format / submit"]
  ReviewDraft -->|revise| Fill
```

## Mermaid Sequence Diagram

```mermaid
sequenceDiagram
  autonumber
  actor Researcher as "Researcher / Topic Actor"
  participant System as "Kaoju Survey Use Case"

  Researcher->>System: Write a paper from the digested materials
  System-->>Researcher: Reading synthesis records and source digests...
  System->>System: Build paper structure from field summary and claim table
  System-->>Researcher: KAOJU:PAPER-STRUCTURE-MYST ref + section outline
  Researcher->>System: Approve structure
  System->>System: Fill placeholders section by section
  System-->>Researcher: KAOJU:PAPER-DRAFT-MYST ref + MyST draft
  Researcher->>System: Tighten the method comparison section
  System-->>Researcher: Updated KAOJU:PAPER-DRAFT-MYST
  Researcher->>System: Approve
  System-->>Researcher: Handoff to export / formatting / submit
```

## Durable Outputs

Each durable output below is registered as an entry in the topic workspace state database. The entry contains the artifact metadata and a link to the actual file stored in the topic workspace filesystem, so the agent can look it up by querying the state DB rather than scanning directories.

- `KAOJU:PAPER-STRUCTURE-MYST` — MyST file with section headings and placeholders, approved before full drafting.
- `KAOJU:PAPER-DRAFT-MYST` — content-filled MyST survey paper grounded in source digests and synthesis records. This is the canonical paper artifact.
- `KAOJU:PAPER-DRAFT-MD` — optional derived Markdown view of the paper draft for human review.
- `KAOJU:CITATION-MAP` — mapping from draft claims and statements to source-digest locators.
- `KAOJU:PAPER-REVISION-LOG` — record of structure and draft revisions requested by the human.

## Paper Structure Placeholders

A `KAOJU:PAPER-STRUCTURE-MYST` artifact contains at minimum these sections as MyST/Markdown headings with placeholders:

| Section | Placeholder Content |
| --- | --- |
| `title` | Proposed paper title. |
| `abstract` | `{{abstract}}` — summary of scope, methods, and key findings. |
| `introduction` | `{{introduction}}` — motivation, problem statement, survey scope. |
| `background` | `{{background}}` — definitions, taxonomy, and concepts. |
| `related work` | `{{related_work}}` — overview of selected works grouped by theme. |
| `method comparison` | `{{method_comparison}}` — comparative analysis of approaches. |
| `discussion` | `{{discussion}}` — trends, gaps, contradictions, limitations. |
| `conclusion` | `{{conclusion}}` — summary and future directions. |
| `references` | `{{references}}` — list of cited sources with stable links. |

## Example Prompt And Expected AI Response

### Event 001 - Produce Paper Structure

> Time: `2026-07-14T10:40:00Z` · Session: `topic:predictive-memory-tiering-survey`

User Prompt:

> Write a paper from the digested materials.

AI:

> I read the Field Summary, Related-Work Catalog, Claim Status Table, and 6 approved Source Digests. I produced `KAOJU:PAPER-STRUCTURE-MYST` (`structure-...`) with the following sections:
>
> 1. Title
> 2. Abstract — `{{abstract}}`
> 3. Introduction — `{{introduction}}`
> 4. Background: Predictive Memory Tiering for LLM Inference — `{{background}}`
> 5. Related Work: OS-Level Far Memory — `{{related_work_os}}`
> 6. Related Work: LLM Inference Offloading — `{{related_work_llm}}`
> 7. Method Comparison — `{{method_comparison}}`
> 8. Discussion — `{{discussion}}`
> 9. Conclusion — `{{conclusion}}`
> 10. References — `{{references}}`
>
> Approve the structure or ask me to change it.

### Event 002 - Fill And Review Paper Draft

> Time: `2026-07-14T10:45:00Z` · Session: `topic:predictive-memory-tiering-survey`

User Prompt:

> Approve the structure and fill it.

AI:

> Structure approved. I filled every section and wrote `KAOJU:PAPER-DRAFT-MYST` (`draft-...`). A derived Markdown view `KAOJU:PAPER-DRAFT-MD` is also available.
>
> The draft is 2,800 words in MyST. Every claim is tied to a Source Digest or Claim Status Table entry. You can ask for section-level revisions or approve the draft.

## Assumptions And Decisions

- Assumption: Synthesis records (`KAOJU:FIELD-SUMMARY`, `KAOJU:RELATED-WORK-CATALOG`, `KAOJU:CLAIM-STATUS-TABLE`) have been produced and audited before paper writing begins.
- Assumption: Source digests are approved before their claims are used in the paper draft.
- Assumption: The paper is written in MyST, which is the canonical format; a Markdown view can be derived automatically for review; LaTeX/PDF rendering is handled in UC-06.
- Decision: The agent selects and explains an adaptive typed MyST structure profile based on the accepted survey direction, such as taxonomy, comparison, empirical survey, or general survey; the actor can revise it through the template workflow.
- Decision: Figures and tables are separate file-backed Artifacts. The MyST structure and draft use typed placeholders that reference those Artifacts, and the citation map preserves their evidence and display roles.
