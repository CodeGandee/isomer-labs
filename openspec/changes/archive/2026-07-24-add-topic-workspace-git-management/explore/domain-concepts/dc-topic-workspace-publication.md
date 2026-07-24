# Topic Workspace Publication Language

These terms distinguish canonical topic state from its sanitized publication projection without expanding Isomer's three managed workspace types.

## Language

**Source Topic Workspace**:
The contextual role of the canonical Topic Workspace when it supplies content to local root tracking or a Topic Publication Copy. It is not a separate registered object, subtype, or fourth workspace type.
_Avoid_: Source Workspace, publication-source workspace type, source Topic Workspace subtype

**Topic Publication Copy**:
An ignored, Project-local, rebuildable projection derived from a Source Topic Workspace for sanitization and remote publication. It is not a Topic Workspace, managed workspace type, Workspace Runtime, research record authority, or canonical source.
_Avoid_: Publication Workspace, remote Topic Workspace, cloned Topic Workspace

## Relationships

- A canonical **Topic Workspace** may act as the **Source Topic Workspace** during Topic Git operations.
- A **Topic Publication Copy** is derived from one **Source Topic Workspace** and never replaces it.
- **Source Topic Workspace** and **Topic Publication Copy** do not add workspace types beyond Topic Workspace, Topic Actor Workspace, and Agent Workspace.

## Flagged Ambiguities

- “Source Topic Workspace” describes a role in a comparison, not a lifecycle state or schema subtype.
- “Topic Publication Copy” contains a representation of topic material but must not be shortened to “Publication Workspace.”
