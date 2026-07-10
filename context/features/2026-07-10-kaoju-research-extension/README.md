# Kaoju Research Extension

Status: Draft use cases and skill-family interface

## Purpose

Design an optional built-in Isomer system-skill extension named `kaoju` (考据) for evidence-led literature, codebase, model, dataset, reproduction, and comparative investigation. Kaoju treats reports as views over durable Research Claims, Evidence Items, Artifacts, Runs, and Provenance Records rather than as substitutes for first-hand evidence.

## Artifacts

- [Use Cases](usecases/README.md)
- [Design](design/README.md)
- [Kaoju Pipeline and Skill Family Design Overview](design/isomer-kaoju-pipeline/design-overview.md)

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
