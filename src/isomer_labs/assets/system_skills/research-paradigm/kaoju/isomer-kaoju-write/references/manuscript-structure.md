# Manuscript Structure

The survey manuscript separates a reader-facing paper view from an evidence view. The bound publication source is a LaTeX `.tex` tree.

## Reader-Facing Paper View

- **Introduction**: motivation, audience, scope, survey questions, contribution posture.
- **Survey Method**: discovery channels, cutoff, eligibility, screening, identity resolution, evidence depth, known blind spots.
- **Taxonomy or Field Map**: categories and boundary cases.
- **Comparative Study**: dimensions, comparability status, results.
- **Synthesis**: patterns, contradictions, negative evidence, gaps, calibrated conclusions.
- **Limitations**: coverage and method constraints propagated from the Audit Report.
- **Conclusion**: answers to survey questions at the strength permitted by accepted evidence.

## Evidence View

A separate structured view containing source identities, discovery and screening accounting, verification depths, exact locators, comparison cells, contradictions, audit findings, and appendix support. Moving detail to an appendix does not erase its effect on the main-text conclusion.

## LaTeX Source Requirements

- Use `\section{Introduction}`, `\subsection{Scope}`, etc., without authored numeric prefixes.
- Title and author metadata use `\title{}`, `\author{}`, `\date{}`, and `\maketitle`, not a numbered section.
- Abstract, acknowledgments, references, and appendices use the template-native unnumbered or appendix structure.
- Appendices use the template's `\appendix` posture, not authored letter or number prefixes.
- Citations use verified bibliography data through the template's supported citation workflow.

## Citation and Claim Lineage

- Every paper-facing claim maps to accepted Research Claim, Evidence Item, Artifact, Finding, or Run refs.
- Citations are prepared before prose is accepted.
- Unresolved citation keys, duplicate identities, inaccessible sources, and bibliography mismatches are blockers or named limitations.
