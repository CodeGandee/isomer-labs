# Migration Placeholders

| Placeholder | Source Artifact or Route | Meaning | Producer or Caller | Consumer or Callee | Kind |
| --- | --- | --- | --- | --- | --- |
| DEEPSCI:DATA-AVAILABILITY-CONTEXT | journal and article constraints | Target journal, article type, policy source, and author constraints. | isomer-rsch-nature-data | nature-data | runtime state |
| DEEPSCI:DATASET-INVENTORY | every dataset or source file supporting results | Inventory of result-supporting data and data-like materials. | isomer-rsch-nature-data | nature-data, write, finalize | evidence |
| DEEPSCI:DATA-ACCESS-CLASSIFICATION | public, controlled, supplement, reused, restricted, request, N/A routes | Access route classification for each dataset. | isomer-rsch-nature-data | nature-data | decision |
| DEEPSCI:REPOSITORY-STRATEGY | repository, identifier, embargo, versioning, license plan | Repository and identifier plan chosen before prose drafting. | isomer-rsch-nature-data | nature-data, finalize | handoff |
| DEEPSCI:DATA-AVAILABILITY-STATEMENT | ready-to-paste Data Availability statement | Draft or final data availability statement. | isomer-rsch-nature-data | write, finalize, user | draft |
| DEEPSCI:DATASET-CITATION-ACTIONS | dataset citations and missing identifiers | Formal citation actions for public or reused data. | isomer-rsch-nature-data | write, finalize | report |
| DEEPSCI:FAIR-METADATA-AUDIT | FAIR metadata checklist guidance | Metadata, license, provenance, README, and reuse clarity audit. | isomer-rsch-nature-data | nature-data, finalize | report |
| DEEPSCI:DATA-AVAILABILITY-BLOCKER | missing information and risk flags | Missing author confirmations, repository actions, or policy blockers. | isomer-rsch-nature-data | user, decision, finalize | decision |
