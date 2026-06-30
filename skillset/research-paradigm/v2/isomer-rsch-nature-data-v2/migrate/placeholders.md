# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| <DATA_AVAILABILITY_CONTEXT> | journal and article constraints | Target journal, article type, policy source, and author constraints. | isomer-rsch-nature-data-v2 | nature-data | runtime state |
| <DATASET_INVENTORY> | every dataset or source file supporting results | Inventory of result-supporting data and data-like materials. | isomer-rsch-nature-data-v2 | nature-data, write, finalize | evidence |
| <DATA_ACCESS_CLASSIFICATION> | public, controlled, supplement, reused, restricted, request, N/A routes | Access route classification for each dataset. | isomer-rsch-nature-data-v2 | nature-data | decision |
| <REPOSITORY_STRATEGY> | repository, identifier, embargo, versioning, license plan | Repository and identifier plan chosen before prose drafting. | isomer-rsch-nature-data-v2 | nature-data, finalize | handoff |
| <DATA_AVAILABILITY_STATEMENT> | ready-to-paste Data Availability statement | Draft or final data availability statement. | isomer-rsch-nature-data-v2 | write, finalize, user | draft |
| <DATASET_CITATION_ACTIONS> | dataset citations and missing identifiers | Formal citation actions for public or reused data. | isomer-rsch-nature-data-v2 | write, finalize | report |
| <FAIR_METADATA_AUDIT> | FAIR metadata checklist guidance | Metadata, license, provenance, README, and reuse clarity audit. | isomer-rsch-nature-data-v2 | nature-data, finalize | report |
| <DATA_AVAILABILITY_BLOCKER> | missing information and risk flags | Missing author confirmations, repository actions, or policy blockers. | isomer-rsch-nature-data-v2 | user, decision, finalize | decision |
