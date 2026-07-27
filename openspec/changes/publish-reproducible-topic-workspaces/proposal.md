## Why

Topic Workspace publication currently protects source state but can omit the intent, durable research records, environment declarations, and external repository identities required to reproduce a survey or trace its decisions. The publication contract must become reproduction-complete by default while continuing to exclude raw payload bytes unless selected and removing the individual researcher's local identity and credentials.

## What Changes

- Publish current intent, reproducible environment declarations, and the complete sanitized durable research-record lineage by default.
- Publish sanitized Topic Main, Topic Actor, and Agent components by default, and represent registered GitHub reference repositories as exact-commit submodules without copying their local checkout history.
- Publish raw-material identities, versions, locators, checksums, access, and license posture by default while requiring explicit plan settings for downloaded material bytes and raw experiment-output bytes.
- Always generate a root publication `README.md` with a deterministic latest-paper line, and publish the latest validated paper PDF through a stable path when it exists.
- Sanitize credentials, individual researcher identity, local host and network identity, absolute local paths, and identity-bearing metadata while preserving credential-free public or private GitHub repository identities and other organization or source provenance.
- Export a portable sanitized research-record index so readers can follow revisions, evidence links, decisions, failures, and supersession without publishing Workspace Runtime or `state.sqlite`.
- Replace path-only and blanket-binary decisions with semantic publication classes, typed payload handling, and explicit reproduction limitations.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `topic-workspace-git-publication`: Change the default publication scope, external-repository topology, raw-payload opt-in policy, README and latest-paper behavior, portable decision-lineage export, and individual-identity sanitization requirements.

## Impact

- Updates the Topic Workspace Git publication specification and operator skill guidance.
- Extends `isomer_labs.topic_git` publication and projection planning, materialization, manifests, and validation.
- Adds focused unit, integration, and skill-contract coverage for default research artifacts, raw-byte opt-ins, reference submodules, README generation, latest-paper selection, and contextual identity sanitization.
- Preserves the Source Topic Workspace, Workspace Runtime, original Git histories, and external authentication mechanisms.
