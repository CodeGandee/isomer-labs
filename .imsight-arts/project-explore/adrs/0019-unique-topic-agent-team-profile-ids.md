# Unique Topic Agent Team Profile ids

Topic Agent Team Profile registrations in a Project Manifest must use unique ids, even when one registration is archived or otherwise inactive. Topic lineage, archival relationships, forks, and migrations should be represented by a future relationship or history record rather than by reusing a profile id, because duplicate registrations make default selection, validation diagnostics, and CLI lookup semantics ambiguous.

## Status

accepted

## Considered Options

- Allow inactive duplicate registrations: rejected because it mixes identity with relationship history and forces validators to infer which registration is authoritative.
- Reject all duplicate Topic Agent Team Profile ids: accepted because the Project Manifest remains a lookup surface, while profile relationships can be modeled explicitly later.

## Consequences

Validators should report duplicate Topic Agent Team Profile ids regardless of registration status. Future archive, fork, migration, or supersession features need a separate relationship/history surface.
