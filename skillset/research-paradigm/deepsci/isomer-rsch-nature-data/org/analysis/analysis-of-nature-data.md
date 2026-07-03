# nature-data Skill Analysis

Source skill: [nature-data](../../../extern/orphan/DeepScientist/src/skills/nature-data/SKILL.md)

Role: companion

Purpose: prepare, audit, or revise Nature-ready data availability statements, repository plans, dataset citations, and FAIR metadata.

## Mermaid UML Workflow

```mermaid
stateDiagram-production DeepSci
    [*] --> Identify_Journal_And_Article_Type
    Identify_Journal_And_Article_Type --> Inventory_Datasets
    Inventory_Datasets --> Classify_Access_Routes
    Classify_Access_Routes --> Choose_Repository_Strategy
    Choose_Repository_Strategy --> Draft_Data_Availability
    Draft_Data_Availability --> Add_Dataset_Citations
    Add_Dataset_Citations --> FAIR_Metadata_Audit
    FAIR_Metadata_Audit --> Ready_Statement: no blockers
    FAIR_Metadata_Audit --> Missing_Info: author confirmation needed
    Ready_Statement --> [*]
    Missing_Info --> [*]
```

## State Step Meanings

| Step | Meaning |
| --- | --- |
| `Identify_Journal_And_Article_Type` | Check the target journal and article constraints. |
| `Inventory_Datasets` | List every dataset or source file supporting results. |
| `Classify_Access_Routes` | Assign each dataset to a public, controlled, supplement, reused, restricted, request, or N/A route. |
| `Choose_Repository_Strategy` | Pick repositories and stable identifiers before writing. |
| `Draft_Data_Availability` | Write explicit dataset-to-location availability text. |
| `Add_Dataset_Citations` | Add formal citations for public data. |
| `FAIR_Metadata_Audit` | Check metadata, licenses, provenance, and reuse clarity. |
| `Ready_Statement` | Return ready-to-paste text. |
| `Missing_Info` | Flag fields the author must confirm. |

## Inner Working

The skill maps every dataset that supports the paper's results to a concrete availability route. It covers generated raw data, processed data, figure source data, secondary data, software outputs, models, tables, images, and statistical-analysis files.

It classifies each dataset as public repository, controlled access repository, within paper or supplement, reused public source, third-party restricted, available on justified request, or not applicable. Repository and identifier strategy is chosen before drafting prose.

The output is not just polished text. It includes repository/citation actions and missing fields or risk flags, often with Chinese author-facing checks when useful.

## Durable Outputs

- Ready-to-paste Data Availability statement.
- Repository and citation action list.
- Missing information and risk flags.
- FAIR metadata checklist guidance.

## Key Constraints

- Do not invent repositories, accession numbers, DOIs, licenses, embargoes, access committees, or ethics approvals.
- Treat "available upon request" as weak unless a real restriction justifies it.
- Follow target journal instructions over generic guidance.
- Keep this skill focused on data availability, not manuscript rewriting or statistics.
