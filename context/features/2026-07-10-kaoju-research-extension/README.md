# Kaoju Research Extension

Status: Draft use cases and skill-family interface

## Purpose

Design an optional built-in Isomer system-skill extension named `kaoju` (考据) for evidence-led literature, codebase, model, dataset, reproduction, and comparative investigation. Kaoju treats reports as views over durable Research Claims, Evidence Items, Artifacts, Runs, and Provenance Records rather than as substitutes for first-hand evidence.

## Artifacts

- [Use Cases](usecases/README.md)
- [Design](design/README.md)
- [Kaoju Pipeline and Skill Family Design Overview](design/isomer-kaoju-pipeline/design-overview.md)
- [ADR 0001: Use Literature-First Related-Work Catalogs](adrs/0001-use-literature-first-related-work-catalogs.md)
- [ADR 0002: Survey Five Source Classes](adrs/0002-survey-five-source-classes.md)
- [ADR 0003: Separate Capability Probes from Reproduction](adrs/0003-separate-capability-probes-from-reproduction.md)
- [ADR 0004: Derive Theory-Comparison Dimensions from Domain Evidence](adrs/0004-derive-theory-comparison-dimensions-from-domain-evidence.md)
- [ADR 0005: Expand Seed Directions Backward and Forward](adrs/0005-expand-seed-directions-backward-and-forward.md)
- [ADR 0006: Honor Explicit Clarification-First Requests](adrs/0006-honor-explicit-clarification-first-requests.md)
- [ADR 0007: Require a Comparison Intent Before Empirical Runs](adrs/0007-require-a-comparison-intent-before-empirical-runs.md)
- [ADR 0008: Register External Local Datasets by Manifest and Link](adrs/0008-register-external-local-datasets-by-manifest-and-link.md)
- [ADR 0009: Treat User-Supplied Sources as Priority Candidates](adrs/0009-treat-user-supplied-sources-as-priority-candidates.md)
- [ADR 0010: Model Survey Intents, Not Generic Lifecycle Tasks](adrs/0010-model-survey-intents-not-generic-lifecycle-tasks.md)

## Current Stage

The feature has a first use-case batch and a proposed public interface for the `isomer-kaoju-*` skill family. No production skill files, manifest entries, record-format providers, validators, or team templates are implemented by this design stage.

## Related Context

- [Canonical Isomer Platform Language](../../../.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md)
- [Packaged System-Skill Manifest](../../../src/isomer_labs/assets/system_skills/manifest.toml)
- [Research-Paradigm Skill Layout](../../../src/isomer_labs/assets/system_skills/research-paradigm/README.md)
- [Research Execution Extension Examples](../../design/research-execution-extension-examples.md)
- [Packaged System-Skill Specification](../../../openspec/specs/packaged-system-skills/spec.md)
- [Research-Paradigm Skills Specification](../../../openspec/specs/research-paradigm-skills/spec.md)

## Open Questions

- Whether every full comparative pass must include an independent `isomer-kaoju-audit` stage, or whether a user may explicitly waive it for exploratory work.
- Which provider-neutral storage contract should preserve large model and dataset material while keeping immutable locator, revision, checksum, license, and access evidence durable.
- Whether a future `kaoju-mini` Domain Agent Team Template is warranted after the skill family has usage evidence; it is outside the initial extension design.
