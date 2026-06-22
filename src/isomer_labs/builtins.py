"""Milestone 1 built-in schema and contract registry."""

from __future__ import annotations

from isomer_labs.models import BuiltInSchema


BUILT_IN_SCHEMAS = (
    BuiltInSchema(
        name="isomer-project-manifest",
        kind="schema",
        schema_version="isomer-project-manifest.v1",
        description="Project Manifest registration contract for Research Topics and Topic Workspaces.",
    ),
    BuiltInSchema(
        name="isomer-research-topic-config",
        kind="schema",
        schema_version="isomer-research-topic-config.v1",
        description="Research Topic Config contract for topic defaults and declarative refs.",
    ),
    BuiltInSchema(
        name="isomer-local-active-context",
        kind="schema",
        schema_version="isomer-local-active-context.v1",
        description="Untracked local active context candidate identity refs.",
    ),
    BuiltInSchema(
        name="isomer-effective-topic-context",
        kind="contract",
        schema_version="isomer-effective-topic-context.v1",
        description="Process-local context consumed by topic-scoped commands.",
    ),
    BuiltInSchema(
        name="isomer-workspace-path-preview",
        kind="contract",
        schema_version="isomer-workspace-path-preview.v1",
        description="Side-effect-free Workspace Path Resolution preview output.",
    ),
    BuiltInSchema(
        name="isomer-workspace-runtime",
        kind="schema",
        schema_version="isomer-workspace-runtime.v1",
        description="Topic Workspace SQLite runtime state for paths, readiness, lifecycle, and team records.",
    ),
    BuiltInSchema(
        name="isomer-diagnostics",
        kind="contract",
        schema_version="isomer-diagnostics.v1",
        description="Stable diagnostic code, severity, path, concept, and message shape.",
    ),
    BuiltInSchema(
        name="isomer-artifact-format-profile",
        kind="schema",
        schema_version="isomer-artifact-format-profile.v1",
        description="Declarative Artifact Format Profile registration shape.",
    ),
    BuiltInSchema(
        name="isomer-artifact-extension",
        kind="schema",
        schema_version="isomer-artifact-extension.v1",
        description="Additive Artifact Extension registration shape.",
    ),
)


def list_built_in_schemas() -> list[BuiltInSchema]:
    return sorted(BUILT_IN_SCHEMAS, key=lambda schema: schema.name)
