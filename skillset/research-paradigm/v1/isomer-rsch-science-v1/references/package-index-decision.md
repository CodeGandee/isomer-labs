# Package Index Decision

The DeepScientist source includes a generated package index and 169 package cards derived from a scientific-package catalog. This Isomer skill does not import the full generated catalog in this change.

## Decision

Defer the large package-card catalog.

## Rationale

- The generated package-card directory is bulky and mostly routing metadata.
- Package cards do not prove local solver availability, so they cannot replace package checks.
- The core workflow value is preserved through the domain index, package-check playbook, claim discipline, HPC Execution Adapter guidance, science task brief, and evidence-recording contract.
- A future resource-focused change can import a curated subset or generated catalog if the Isomer platform accepts a package-catalog surface.

## Follow-Up Boundary

A follow-up package-catalog import should decide:

- accepted storage location and update process.
- whether package cards are local references, generated assets, or a Capability Binding.
- how to validate source URL, license, upstream version, and package-card freshness.
- how package-card lookup records a Provenance Record without implying runtime availability.
