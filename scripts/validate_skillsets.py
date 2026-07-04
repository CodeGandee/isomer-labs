#!/usr/bin/env python3
"""Validate Isomer skillset namespaces."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import validate_research_paradigm_skillset as research_validator


FRONTMATTER_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
LOCAL_REFERENCE_PREFIXES = ("references/", "assets/", "scripts/", "subcommands/")
TOPIC_TEAM_SPECIALIZATION_SKILL = "isomer-op-topic-team-specialize"
PROJECT_MANAGER_SKILL = "isomer-op-project-mgr"
TOPIC_CREATOR_SKILL = "isomer-op-topic-creator"
TOPIC_MANAGER_SKILL = "isomer-op-topic-mgr"
WELCOME_SKILL = "isomer-op-welcome"
PACKAGE_SPECIFICS_SKILL = "isomer-misc-pkg-specifics"
HOUMAO_INTEROP_SERVICE_SKILL = "isomer-srv-houmao-interop"

MIGRATED_OPERATOR_SKILLS = (
    "isomer-rsch-project-aware",
    "isomer-rsch-service-request-route",
    "isomer-rsch-template-inspect",
    "isomer-rsch-topic-context-resolve",
    "isomer-rsch-placeholder-reconcile",
    "isomer-rsch-topic-profile-draft",
    "isomer-rsch-profile-review-approval",
    "isomer-rsch-profile-materialize",
    "isomer-rsch-team-launch-orchestrate",
    "isomer-rsch-topic-service-agent-support",
)
STALE_SKILL_NAMESPACE_REPLACEMENTS = {
    "isomer-admin-": "isomer-op-",
    "isomer-rsch-": "isomer-deepsci-",
}
STALE_EXACT_SKILL_REPLACEMENTS = {
    "isomer-op-houmao-interop": HOUMAO_INTEROP_SERVICE_SKILL,
}
PASSIVE_STALE_REF_PARTS = frozenset({"migrate", "org"})

ACTIVE_REF_ROOTS = (
    ".imsight-arts",
    "docs",
    "openspec/specs",
    "skillset",
    "src",
    "teams",
    "tests",
)
ACTIVE_REF_FILES = ("AGENTS.md", "ROADMAP.md", "pyproject.toml")
ACTIVE_REF_SUFFIXES = {".md", ".toml", ".yaml", ".yml", ".py", ".json"}
FORBIDDEN_REPO_LOCAL_ISOMER_CLI = "pixi run isomer-cli"
COPIED_TOPIC_MAIN_GUIDANCE_TERMS = (
    "This repository is an Isomer Topic Main Development Repository.",
    "This repository uses Pixi as the primary package manager and execution environment. Invoke Python through Pixi",
    "Avoid system Python, ambient virtualenvs, plain `python`, plain `pip`, shell activation, and local `.venv` environments",
)

TOPIC_TEAM_SPECIALIZATION_REQUIRED_SKILL_TERMS = (
    "Default help mode",
    "invoked without a prompt",
    "Manual mode",
    "Automatic mode",
    "## Subcommands",
    "Procedural Subcommands",
    "Helper Subcommands",
    "Misc Subcommands",
    "references/help.md",
    "init-topic",
    "clarify-topic",
    "ensure-topic-registration",
    "adapt-team-template",
    "clarify-topic-team",
    "setup-topic-env",
    "setup-agent-workspace",
    "validate-topic-team",
    "finalize-topic-team",
    "fast-forward",
    "step-by-step",
    "load only its detail page",
    "static material readiness",
    "durable setup state",
    "topic-overview.md",
    "concrete Research Topic",
    "default Research Topic",
    "provisional topic workspace seed",
    "isomer-content/topic-ws/<topic-slug>/",
    "team-specialization-guide.md",
    "team-specialization-plan.md",
    "```generated-guide",
    "Generated Guide",
    "Final Report",
    "<topic-workspace>/team-profile/execplan/",
    "isomer-topic-summary.md",
    "selected_domain_team_template_ref",
    "topic_environment_status",
    "semantic label evidence",
    "topic.repos.main",
    "agent.workspace",
    "required `agent.*` support paths",
    "agent_workspace_paths",
    "semantic_paths",
    "semantic labels",
    "path sources",
    "topic_team_validation_status",
    "isomer_topic_summary_path",
    "isomer-managed/",
)

TOPIC_TEAM_SPECIALIZATION_REFERENCE_REQUIRED_TERMS = {
    "help.md": (
        "semantic path evidence",
        "semantic_paths",
        "topic.repos.main",
        "agent.workspace",
    ),
    "setup-topic-env.md": (
        "complete required `## Gate Checklist` evidence",
        "required checklist item",
        "weaker smoke test",
        "blocked, failed, or not checked",
        "operation_classification",
        "owns the classification decision",
    ),
    "setup-agent-workspace.md": (
        "topic.repos.main",
        "agent.workspace",
        "required `agent.*` support paths",
        "semantic_paths",
    "local_tmp_path_status",
    "agent.tmp",
    "path sources",
    "topic.intent.agent_env_requirements",
    "topic.env.agent_setup_target_spec",
    "isomer-srv-agent-env-setup",
    "generate",
    "default-looking directories without semantic labels and path sources",
    "every required per-agent `## Gate Checklist` item",
    "selected-agent partial",
    "weaker smoke-test substitution",
    "operation_classification",
    "classification source",
    ),
    "validate-topic-team.md": (
        "topic.repos.main",
        "agent.workspace",
        "required `agent.*` support labels",
        "semantic_paths",
        "local_tmp_path_status",
        "agent.tmp",
        "path sources",
        "hard-coded default-only paths without semantic labels",
        "every required topic gate checklist item",
        "every required per-agent checklist item",
        "weaker smoke-test downgrade",
        "operation classification evidence",
    ),
    "finalize-topic-team.md": (
        "semantic labels first",
        "topic.repos.main",
        "topic.repos.main.tmp",
        "agent.workspace",
        "agent.tmp",
        "path sources",
        "isomer-default.v1",
        "hard-coded default-only paths without semantic label",
        "required topic `## Gate Checklist` completion evidence",
        "required per-agent `## Gate Checklist` completion evidence",
        "smoke-test downgrades",
    ),
}

TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS = (
    "help.md",
    "init-topic.md",
    "clarify-topic.md",
    "resolve-topic-intent.md",
    "ensure-topic-registration.md",
    "resolve-topic-env-gate.md",
    "adapt-team-template.md",
    "clarify-topic-team.md",
    "resolve-agent-env-gate.md",
    "setup-topic-env.md",
    "setup-agent-workspace.md",
    "validate-topic-team.md",
    "finalize-topic-team.md",
    "resolve-project.md",
    "inspect-template.md",
    "resolve-context.md",
    "map-placeholders.md",
    "draft-profile.md",
    "approve-profile.md",
    "materialize-profile.md",
    "fast-forward.md",
    "step-by-step.md",
)

CORE_OWNED_HEAVY_OPERATION_FORBIDDEN_TERMS = (
    "Treat compilation, deep model inference",
    "Classify each per-agent verification command as light or heavy",
    "Classify each setup or verification command as light or heavy",
    "resource-heavy work such as compilation, deep model inference",
    "heavy setup or verification command such as compilation",
    "heavy per-agent cwd verification command such as compilation",
)

OUTPUT_CONTRACT_SECTION_HEADINGS = ("## Output Contract", "## Reporting Contract")
OUTPUT_CONTRACT_REQUIRED_TERMS = (
    "Default to **Essential Output** in chat.",
    "Essential Output",
    "Complete Output",
    "complete, verbose, audit, debug, full handoff, JSON, or full output",
)

TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS = (
    "init-topic.md",
    "clarify-topic.md",
    "resolve-topic-intent.md",
    "ensure-topic-registration.md",
    "resolve-topic-env-gate.md",
    "adapt-team-template.md",
    "clarify-topic-team.md",
    "resolve-agent-env-gate.md",
    "setup-topic-env.md",
    "setup-agent-workspace.md",
    "validate-topic-team.md",
    "finalize-topic-team.md",
    "approve-profile.md",
    "materialize-profile.md",
)

TOPIC_TEAM_SPECIALIZATION_HELP_FORBIDDEN_SUBCOMMANDS = (
    "launch-team",
    "resolve-project",
    "inspect-template",
    "resolve-context",
    "map-placeholders",
    "draft-profile",
)

TOPIC_TEAM_SPECIALIZATION_HELP_TABLE_TERMS = (
    "| Subcommand | Purpose | Produces |",
    "| --- | --- | --- |",
)

TOPIC_TEAM_SPECIALIZATION_NAMING_EXCEPTIONS = {"help", "step-by-step"}
TOPIC_TEAM_SPECIALIZATION_LENGTH_EXCEPTIONS = {"ensure-topic-registration"}
TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_MANIFEST = "step-dependencies.json"
TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT = "query_step_dependencies.py"

TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES = (
    "isomer-domain-language.md",
    "runtime-and-file-boundaries.md",
)

TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS = (
    ".imsight-arts/",
    "docs/",
    "extern/",
    "/data/",
    "/home/",
)

PROJECT_MANAGER_REQUIRED_SKILL_TERMS = (
    "Default help mode",
    "invoked without a prompt",
    "## Subcommands",
    "references/help.md",
    "init-project",
    "cleanup-project",
    "move-content",
    "check-project",
    "list-topics",
    "show-context",
    "init-runtime",
    "prep-runtime",
    "prepare-topic",
    "manual-research",
    "specialize-team",
    "load only the selected subcommand page",
    ".isomer-labs/",
    "isomer-content/",
    "isomer-content/topic-ws/<topic-id>/",
    "--content-dir <content-dir>",
    "<content-dir>/topic-ws/<topic-id>/",
    ".isomer-labs/.houmao/",
    "external user-owned",
    "Isomer-managed Houmao overlay",
    "isomer-cli project init",
    "isomer-cli project cleanup --part <part> --dry-run",
    "isomer-cli project cleanup --part <part> --yes",
    "--purge-content-root",
    "isomer-cli project content-root move --to <content-dir> --dry-run",
    "isomer-cli project content-root move --to <content-dir> --yes",
    "unknown files",
    "isomer-cli project validate",
    "isomer-cli project doctor",
    "isomer-cli project runtime init",
    "isomer-cli project runtime prepare",
    "isomer-op-topic-creator",
    "isomer-op-topic-mgr",
    "isomer-op-topic-team-specialize",
)

PROJECT_MANAGER_FORBIDDEN_CLI_TERMS = (
    "isomer-cli init",
    "isomer-cli validate",
    "isomer-cli doctor",
    "isomer-cli topics",
    "isomer-cli workspaces",
    "isomer-cli context",
    "isomer-cli paths",
    "isomer-cli runtime",
    "isomer-cli team-",
    "isomer-cli handoffs",
    "isomer-cli cleanup",
    "isomer-cli --project",
)

PROJECT_MANAGER_SUBCOMMANDS = (
    "help.md",
    "init-project.md",
    "cleanup-project.md",
    "move-content.md",
    "check-project.md",
    "list-topics.md",
    "show-context.md",
    "init-runtime.md",
    "prep-runtime.md",
    "prepare-topic.md",
    "manual-research.md",
    "specialize-team.md",
)

PROJECT_MANAGER_NAMING_EXCEPTIONS = {"help"}

PROJECT_MANAGER_SUPPORT_REFERENCES = (
    "project-concepts.md",
    "cli-command-boundaries.md",
    "houmao-bootstrap.md",
    "runtime-boundaries.md",
)

PROJECT_MANAGER_FORBIDDEN_SUPPORT_REFS = TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS

TOPIC_CREATOR_REQUIRED_SKILL_TERMS = (
    "Default help mode",
    "invoked without a prompt",
    "## Subcommands",
    "Procedural Subcommands",
    "Helper Subcommands",
    "Misc Subcommands",
    "lower-level ladder stages",
    "references/help.md",
    "fast-forward",
    "ensure-project",
    "resolve-topic-input",
    "register-topic",
    "create-research-intent",
    "init-runtime",
    "define-topic-env",
    "setup-topic-env",
    "define-actors",
    "setup-actors",
    "finalize",
    "step-by-step",
    "run-to",
    "status",
    "repair",
    "prepared Topic Workspace",
    "Project Manifest-backed context",
    "topic.repos.main",
    "topic.intent.overview",
    "topic.intent.topic_env_requirements",
    "topic.intent.actor_definitions",
    "topic.env.actor_env_gates",
    "topic.workspace.summary",
    "structured reset checkpoint",
    "Workspace Runtime",
    "Topic Actor roster",
    "actor cwd",
    "actor onboarding",
    "isomer-op-project-mgr",
    "isomer-srv-topic-env-setup",
    "isomer-op-topic-mgr",
    "isomer-op-topic-team-specialize",
    "Essential Output",
    "Complete Output",
)

TOPIC_CREATOR_COMMANDS = (
    "help.md",
    "fast-forward.md",
    "ensure-project.md",
    "resolve-topic-input.md",
    "register-topic.md",
    "create-research-intent.md",
    "clarify-research-intent.md",
    "init-runtime.md",
    "define-topic-env.md",
    "setup-topic-env.md",
    "define-actors.md",
    "setup-actors.md",
    "finalize.md",
    "step-by-step.md",
    "run-to.md",
    "status.md",
    "repair.md",
)

TOPIC_CREATOR_REFERENCE_REQUIRED_TERMS = {
    "help.md": (
        "Subcommand Functionalities",
        "Procedural Subcommands",
        "Helper Subcommands",
        "Misc Subcommands",
        "Default to **Essential Output** in chat.",
        "complete, verbose, audit, debug, full handoff, JSON, or full output",
    ),
    "fast-forward.md": (
        "fast-forward",
        "stops at the first blocker",
        "finalize",
        "define-topic-env",
        "define-actors",
    ),
    "resolve-topic-input.md": (
        "concrete Research Topic",
        "does not write",
        "topic.intent.overview",
    ),
    "create-research-intent.md": (
        "topic.intent.overview",
        "only",
        "topic.intent.topic_env_requirements",
        "templates/topic-overview.md",
        "Research Topic",
        "Motivation",
        "Topic Breakdown",
        "Do's",
        "Don'ts",
        "Expected Outcome",
        "Related Links",
        "Strip",
    ),
    "clarify-research-intent.md": (
        "topic.intent.overview",
        "Coverage and Clarity Scan",
        "Question Format",
        "Sequential Clarification Loop",
        "Direct Topic Overview Integration",
        "Prerequisite Artifacts",
        "Guardrails",
        "Research Topic",
        "Motivation",
        "Topic Breakdown",
        "Do's",
        "Don'ts",
        "Expected Outcome",
        "Related Links",
    ),
    "define-topic-env.md": (
        "topic.intent.topic_env_requirements",
        "user verification",
        "fast-forward",
    ),
    "define-actors.md": (
        "topic.intent.actor_definitions",
        "operator",
        "source env gate",
    ),
    "setup-topic-env.md": (
        "isomer-srv-topic-env-setup",
        "topic.repos.main",
        "topic.intent.topic_env_requirements",
        "topic.env.topic_setup_target_spec",
    ),
    "setup-actors.md": (
        "isomer-op-topic-mgr",
        "topic.actors.workspace",
        "topic.intent.actor_definitions",
        "topic.env.actor_env_gates",
    ),
    "finalize.md": (
        "topic.workspace.summary",
        "isomer-cli project topic-reset checkpoint",
        "structured reset checkpoint",
        "operator-level readiness evidence",
        "ready",
        "verified",
        "blocked",
        "Do not recommend a next research step",
    ),
    "step-by-step.md": (
        "same main workflow order as `fast-forward`",
        "option table",
        "Recommended",
        "acknowledgement",
    ),
    "run-to.md": (
        "Valid targets",
        "included by default",
        "explicit exclusion",
        "missing user input",
    ),
    "status.md": (
        "ready",
        "blocked",
        "topic.workspace.summary",
    ),
    "repair.md": (
        "first blocked",
        "without rerunning ready",
    ),
}

TOPIC_MANAGER_REQUIRED_SKILL_TERMS = (
    "isomer-op-topic-creator",
    "initialized-topic",
    "Default subcommand",
    "## Subcommands",
    "Status Subcommands",
    "Storage Subcommands",
    "Actor Subcommands",
    "Team Subcommands",
    "Environment Mutation Subcommands",
    "Environment Verification Subcommands",
    "Reset Subcommands",
    "references/status.md",
    "status",
    "doctor",
    "help",
    "storage-resolve",
    "storage-inspect-main",
    "storage-validate",
    "storage-register-repo",
    "actors-manage",
    "actors-materialize",
    "actors-diagnose",
    "team-plan",
    "team-materialize-workspaces",
    "team-write-boundaries",
    "team-create-branch",
    "team-validate-workspaces",
    "env-install-packages",
    "env-update-packages",
    "env-remove-packages",
    "env-verify-topic",
    "env-verify-actors",
    "env-verify-agents",
    "reset-plan",
    "reset-inspect",
    "reset-apply",
    "isomer-cli project topic-reset",
    "structured records",
    "reset checkpoint",
    "canonical Topic Main Development Repository setup belongs to `isomer-srv-topic-env-setup`",
    "canonical per-agent worktree creation plus cwd proof belong to `isomer-srv-agent-env-setup`",
    "isomer-deepsci-workspace-mgr",
    "semantic workspace labels",
    "Topic Workspace Manifest",
    "topic-workspace.toml",
    "project paths register",
    "project repos create",
    "project topic-actors",
    "storage_profile",
    "custom.*",
    "topic.repos.*",
    "topic.repos.main",
    "topic.repos.main.tmp",
    "topic.repos.main.isomer_managed",
    "topic.actors.workspace",
    "topic.actors.tmp",
    "topic.actors.isomer_managed",
    "topic.actors.private_artifacts",
    "topic.actors.logs",
    "topic.actors.links",
    "agent.workspace",
    "agent.tmp",
    "agent.private_artifacts",
    "agent.public_share",
    "agent.links",
    "semantic_paths",
    "local_tmp_path_status",
    "topic-owner/main",
    "per-topic-actor/<topic-actor-name>/main",
    "per-agent/<agent-name>/main",
    "per-agent/<agent-name>/<branch-name>",
    "topic_actor",
    "agent_name",
    "agent_branch",
    "agent_workspace_ref",
    "isomer-managed/",
    "topic.records.*",
    "Agent Instance",
    "Workspace Runtime",
    "Houmao",
    "Execution Adapter",
    "Workspace Boundary",
    "Peer Read Access",
    "blockers",
    "next_operator_action",
)

TOPIC_MANAGER_SUBCOMMANDS = (
    "status.md",
    "doctor.md",
    "help.md",
    "storage-resolve.md",
    "storage-inspect-main.md",
    "storage-validate.md",
    "storage-register-repo.md",
    "actors-manage.md",
    "actors-materialize.md",
    "actors-diagnose.md",
    "team-plan.md",
    "team-materialize-workspaces.md",
    "team-write-boundaries.md",
    "team-create-branch.md",
    "team-validate-workspaces.md",
    "env-install-packages.md",
    "env-update-packages.md",
    "env-remove-packages.md",
    "env-verify-topic.md",
    "env-verify-actors.md",
    "env-verify-agents.md",
    "reset-plan.md",
    "reset-inspect.md",
    "reset-apply.md",
)

TOPIC_MANAGER_HELP_TABLE_TERMS = (
    "| Subcommand | Purpose | Produces |",
    "| --- | --- | --- |",
    "`reset-plan`",
    "`reset-inspect`",
    "`reset-apply`",
)

TOPIC_MANAGER_NAMING_EXCEPTIONS = {"help", "status", "doctor"}

TOPIC_MANAGER_REFERENCE_REQUIRED_TERMS = (
    "blocker",
)

WELCOME_USAGE_PATHS = (
    "start-research-manually",
    "start-research-by-agent-team",
)

WELCOME_ACTIVE_OWNER_SKILLS = (
    PROJECT_MANAGER_SKILL,
    TOPIC_CREATOR_SKILL,
    TOPIC_MANAGER_SKILL,
    TOPIC_TEAM_SPECIALIZATION_SKILL,
)

WELCOME_RETIRED_ROUTE_SKILLS = (
    "isomer-op-topic-workspace-mgr",
    "isomer-op-topic-prepare",
    "isomer-op-manual-research-session",
)

WELCOME_REQUIRED_SKILL_TERMS = (
    "## Overview",
    "## When to Use",
    "Manual invocation only",
    "Default option mode",
    "Visible usage path mode",
    "Routing and support mode",
    "Read-only context mode",
    "## Usage Path Subcommands",
    "## Routing and Support Subcommands",
    "Do not hide them inside `choose-path`",
    "references/show-options.md",
    "references/choose-path.md",
    "references/show-skill-map.md",
    "references/next-step.md",
    "references/start-research-manually.md",
    "references/start-research-by-agent-team.md",
    "isomer-cli project validate",
    "isomer-cli project doctor",
    "isomer-cli project topics list",
    "isomer-cli project context show",
    "Default to **Essential Output** in chat.",
    "Complete Output",
    "status",
    "interpreted_goal",
    "recommended_workflow",
    "owner_skill",
    "safe_first_command",
    "blockers",
    "next_action",
    "isomer-misc-tool-packs",
)

WELCOME_SUBCOMMANDS = (
    "help.md",
    "show-options.md",
    "choose-path.md",
    "show-skill-map.md",
    "next-step.md",
    "start-research-manually.md",
    "start-research-by-agent-team.md",
)

WELCOME_REFERENCE_REQUIRED_TERMS = {
    "help.md": (
        "| Subcommand | Purpose | Produces |",
        "start-research-manually",
        "start-research-by-agent-team",
        "show-options",
        "choose-path",
        "show-skill-map",
        "next-step",
    ),
    "show-options.md": (
        "visible usage paths first",
        "Project setup or checks",
        "Research Topic",
        "Topic Team",
        "Houmao",
        "invoke the named owner skill directly",
    ),
    "choose-path.md": (
        "recommends visible paths",
        "manual research",
        "Domain Agent Team Template",
        "status",
        "interpreted_goal",
        "recommended_workflow",
        "owner_skill",
        "safe_first_command",
        "blockers",
        "next_action",
    ),
    "show-skill-map.md": (
        "Direct Invocation",
        "Use $isomer-op-project-mgr",
        "Use $isomer-op-topic-creator",
        "Use $isomer-op-topic-mgr",
        "Use $isomer-op-topic-team-specialize",
        "isomer-srv-houmao-interop",
        "not first-click owner routes",
    ),
    "next-step.md": (
        "read-only Project inspection",
        "isomer-cli project validate",
        "isomer-cli project doctor",
        "isomer-cli project topics list",
        "isomer-cli project context show",
        "Do not run",
    ),
    "start-research-manually.md": (
        "human-orchestrated research",
        "isomer-op-topic-creator",
        "Use $isomer-op-topic-creator fast-forward",
        "Use $isomer-op-topic-creator step-by-step",
        "mutation boundary",
    ),
    "start-research-by-agent-team.md": (
        "Domain Agent Team Template",
        "isomer-op-topic-team-specialize",
        "Use $isomer-op-topic-team-specialize fast-forward",
        "mutation boundary",
        "isomer-srv-houmao-interop",
    ),
}

WELCOME_ALLOWED_RETIRED_ROUTE_MARKERS = (
    "do not",
    "not active",
    "not list",
    "not ask",
    "not active routes",
    "retired",
    "exclude",
)

WELCOME_TOOL_PACK_ALLOWED_MARKERS = (
    "do not automatically",
    "manual",
    "manually",
    "explicitly",
)

TOPIC_MANAGER_SEMANTIC_REFERENCE_REQUIRED_TERMS = {
    "storage-resolve.md": (
        "isomer-cli project paths get",
        "project paths explain",
        "semantic_paths",
        "topic.repos.main",
        "agent.workspace",
    ),
    "storage-inspect-main.md": (
        "topic.repos.main",
        "topic.repos.main.tmp",
        "topic.repos.main.isomer_managed",
        "isomer-default.v1",
        "predecessor evidence",
        "manual topology operation",
        "AGENTS.md",
        "CLAUDE.md",
        "isomer-cli --print-json project topic-main-guidance inspect --topic <topic>",
        "isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes",
        "isomer-cli project topic-main-guidance",
        "isomer-labs-topic-main-guidance.v1.md.j2",
        ".j2",
        "canonical large-text template asset",
        "must not carry a duplicate full copy",
    ),
    "storage-validate.md": (
        "Workspace Path Resolution",
        "topic.repos.main.tmp",
        "custom.*",
        "path source",
    ),
    "storage-register-repo.md": (
        "topic.repos.*",
        "storage_profile",
        "project repos create",
        "project paths register",
    ),
    "actors-manage.md": (
        "project topic-actors",
        "topic.actors.workspace",
        "topic.actors.tmp",
        "per-topic-actor/<topic-actor-name>/main",
        "Topic Workspace Manifest",
        "Workspace Runtime",
        "alternate source repositories",
        "blocker",
    ),
    "actors-materialize.md": (
        "topic.actors.workspace",
        "per-topic-actor/<topic-actor-name>/main",
        "Topic Actor names separate from Agent Names",
    ),
    "actors-diagnose.md": (
        "topic.actors.workspace",
        "runtime audit refs",
        "actor readiness",
    ),
    "team-plan.md": (
        "agent.workspace",
        "Workspace Path Resolution",
        "path sources",
    ),
    "team-materialize-workspaces.md": (
        "agent.workspace",
        "agent.tmp",
        "topic.repos.main",
        "prepared Topic Main Development Repository predecessor evidence",
        "path sources",
        "semantic support paths",
    ),
    "team-write-boundaries.md": (
        "topic.repos.main",
        "agent.workspace",
        "path source",
        "without passing Agent Name",
    ),
    "team-validate-workspaces.md": (
        "semantic label bindings",
        "topic.repos.main.tmp",
        "agent.tmp",
        "tracked tmp contents",
        "hard-coded default-only evidence",
    ),
    "env-install-packages.md": (
        "pixi add --manifest-path <manifest_path>",
        "Do not require a formal package request schema",
        "Do not use local `venv`",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
        "package_specifics",
    ),
    "env-update-packages.md": (
        "Pixi-scoped",
        "broad environment upgrades",
        "verification",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
        "package_specifics",
    ),
    "env-remove-packages.md": (
        "dependency",
        "post-removal verification",
        "blocker",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
        "package_specifics",
    ),
    "env-verify-topic.md": (
        "isomer-srv-topic-env-setup",
        "topic.env.topic_setup_target_spec",
        "not prove per-Topic Actor cwd readiness",
    ),
    "env-verify-actors.md": (
        "topic.intent.actor_definitions",
        "topic.env.actor_env_gates",
        "actor cwd",
    ),
    "env-verify-agents.md": (
        "isomer-srv-agent-env-setup",
        "agent.workspace",
        "runtime launch readiness",
    ),
    "status.md": (
        "semantic_paths",
        "Topic Manager evidence",
        "read-only",
    ),
    "doctor.md": (
        "diagnostic",
        "storage diagnostics",
        "retired-skill",
    ),
    "reset-plan.md": (
        "isomer-cli project topic-reset plan",
        "structured reset plan",
        "Workspace Runtime",
        "read-only",
        "Git operations",
    ),
    "reset-inspect.md": (
        "isomer-cli project topic-reset list",
        "isomer-cli project topic-reset show",
        "isomer-cli project topic-reset show-plan",
        "structured records",
        "Workspace Runtime",
    ),
    "reset-apply.md": (
        "isomer-cli project topic-reset apply",
        "--yes",
        "approved structured reset plan",
        "destructive",
        "Workspace Runtime",
        "Git operations",
    ),
}

TOPIC_MANAGER_FORBIDDEN_PUBLIC_TERMS = (
    "agent-key",
    "agent key",
    "<agent-key>",
    ".isomer-agent/",
)

TOPIC_MANAGER_FORBIDDEN_SUPPORT_REFS = tuple(
    ref for ref in TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS if ref != "extern/"
)

TOPIC_ENV_SETUP_SERVICE_SKILL = "isomer-srv-topic-env-setup"

TOPIC_ENV_SETUP_REQUIRED_SKILL_TERMS = (
    "setup-topic-env",
    "resolve-topic-workspace",
    "read-env-gate",
    "derive-env-gate",
    "ensure-topic-main-repository",
    "ensure-topic-repos",
    "project-extern-repos",
    "install-topic-deps",
    "verify-env-gate",
    "single capable agent or operator",
    "Topic environment setup is independent of Topic Agent Team structure",
    "Do not require or inspect Topic Agent Team Profile material",
    "agent count",
    "pixi run --manifest-path <manifest_path> --environment <pixi_environment>",
    "pixi add --manifest-path <manifest_path>",
    "pixi install --manifest-path <manifest_path> --environment <pixi_environment>",
    ".isomer-user-env/",
    "sudo",
    "semantic_paths",
    "topic.workspace",
    "topic.repos.main",
    "topic.repos.main.projections.readonly",
    "topic.repos.main.projections.writable",
    "topic.repos.main.projections.manifest",
    "topic.records",
    "topic.runtime",
    "topic.intent.topic_env_requirements",
    "topic.env.topic_setup_target_spec",
    "explicit manual target spec",
    "Topic Workspace predecessor evidence",
    "Topic Main Development Repository Git state",
    "external repo projection",
    "per_agent_readiness_status",
    "resolve the appropriate topic repository label",
    "bounded real-path verification",
    "isomer-misc-bounded-run-tips",
    "operation_classification",
    "classification source",
    "classification result",
    "unknown-risk",
    "generic best-effort judgment",
    "A generic smoke test is allowed only as supporting evidence",
)

TOPIC_ENV_SETUP_REFERENCE_REQUIRED_TERMS = {
    "resolve-topic-workspace.md": (
        "semantic_paths",
        "topic.repos.main",
        "topic.repos.main.projections.readonly",
        "topic.repos.main.projections.writable",
        "topic.repos.main.projections.manifest",
        "topic.records",
        "topic.runtime",
        "topic.intent.topic_env_requirements",
        "topic.env.topic_setup_target_spec",
        "path source",
    ),
    "ensure-topic-main-repository.md": (
        "Topic Main Development Repository",
        "topic.repos.main",
        "topic.repos.main.isomer_managed",
        "topic.repos.main.projections.readonly",
        "topic.repos.main.projections.writable",
        "topic.repos.main.projections.manifest",
        "normal non-bare",
        "AGENTS.md",
        "CLAUDE.md",
        "isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes",
        "isomer-cli --print-json project topic-main-guidance inspect --topic <topic>",
        "isomer-cli project topic-main-guidance render",
        "isomer-labs-topic-main-guidance.v1.md.j2",
        ".j2",
        "canonical large-text template asset",
        "must not duplicate the full rendered prose",
        "guidance block version",
    ),
    "ensure-topic-repos.md": (
        "semantic_paths",
        "non-main `topic.repos.*`",
        "repos/extern",
        "read-only by default",
        "semantic label, path, and path source",
        "Do not place task repos",
    ),
    "project-extern-repos.md": (
        "external repo projection",
        "topic.repos.main.projections.readonly",
        "topic.repos.main.projections.writable",
        "topic.repos.main.projections.manifest",
        "read-only projections",
        "writable projections",
    ),
    "setup-topic-env.md": (
        "semantic_paths",
        "topic.repos.main",
        "ensure-topic-main-repository",
        "project-extern-repos",
        "AGENTS.md",
        "CLAUDE.md",
        "agent guidance posture",
        "guidance block version",
        "topic.tmp",
        "resolved `topic.tmp`",
        "local, ignored, disposable, not shared, and not durable evidence",
        "per_agent_readiness_status: not checked",
        "Do not read `topic.intent.agent_env_requirements`",
        "bounded real-path",
        "generic smoke test",
    ),
    "read-env-gate.md": (
        "topic.intent.topic_env_requirements",
    ),
    "derive-env-gate.md": (
        "topic.env.topic_setup_target_spec",
        "explicit manual target spec",
        "## Gate Checklist",
        "`- [ ]`",
        "`- [x]`",
        "required readiness work contract",
        "pass condition",
        "evidence source",
        "optional diagnostics",
        "Preserve every source-intent runnable target",
        "bounded real-path",
        "isomer-misc-bounded-run-tips",
        "classification_source",
        "classification_result",
        "classification_reason",
        "resource_dimensions",
        "unknown-risk",
        "bounded-run guidance source",
        "generic best-effort judgment",
        "simple smoke test",
        "user explicitly records a downgrade",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
    ),
    "install-topic-deps.md": (
        "topic.env.topic_setup_target_spec",
        "enclosure strategy",
        "classification evidence",
        "unknown-risk",
        "bounded-run guidance source",
        "generic best-effort",
        "bounded real setup path",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
    ),
    "verify-env-gate.md": (
        "per-Agent Workspace cwd verification is not checked here",
        "Topic Workspace predecessor evidence",
        "Topic Main Development Repository",
        "projection",
        "bounded real-path coverage",
        "operation classification evidence",
        "unknown-risk",
        "bounded-run guidance source",
        "generic best-effort",
        "source-intent runnable target",
        "every required `## Gate Checklist` item",
        "checked with supporting evidence",
        "exact checklist item",
        "weaker smoke test",
        "user downgrade",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
    ),
}

TOPIC_ENV_SETUP_SUBCOMMANDS = (
    "resolve-topic-workspace.md",
    "read-env-gate.md",
    "derive-env-gate.md",
    "ensure-topic-main-repository.md",
    "ensure-topic-repos.md",
    "project-extern-repos.md",
    "install-topic-deps.md",
    "verify-env-gate.md",
    "setup-topic-env.md",
)

TOPIC_ENV_SETUP_REMOVED_SUBCOMMANDS = (
    "resolve-workspace.md",
    "read-gate.md",
    "ensure-repos.md",
    "derive-gate.md",
    "install-deps.md",
    "verify-gate.md",
    "setup-for-topic-workspace.md",
)

TOPIC_ENV_SETUP_INDEPENDENCE_TERMS = (
    "Do not block solely because `<topic-workspace>/team-profile/`",
    "non-blocking for this subcommand unless",
    "one agent or operator",
    "Do not require `team-profile/`",
    "Do not require or verify `team-profile/`",
)

AGENT_ENV_SETUP_SERVICE_SKILL = "isomer-srv-agent-env-setup"

HOUMAO_INTEROP_SERVICE_SUBCOMMANDS = (
    "help.md",
    "explain-loop.md",
    "customize-loop.md",
    "map-template-to-houmao.md",
    "inspect-runtime.md",
)

HOUMAO_INTEROP_SERVICE_REQUIRED_SKILL_TERMS = (
    "bounded Service Team support",
    "Service Request",
    "Default help mode",
    "Explain-loop mode",
    "Customize-loop mode",
    "Map-template mode",
    "Inspect-runtime mode",
    "isomer-op-project-mgr",
    "isomer-op-topic-team-specialize",
    "next_action",
    "Do not own Project lifecycle",
)

HOUMAO_INTEROP_SERVICE_REFERENCE_REQUIRED_TERMS = {
    "help.md": (
        "Project Operator Session",
        "Service Request",
        "next_action",
    ),
    "explain-loop.md": (
        "gateway-driven request queue",
        "TUI-tracking lifecycle kernel",
    ),
    "customize-loop.md": (
        "Main Houmao CLI",
        "project overlay",
    ),
    "map-template-to-houmao.md": (
        "Domain Agent Team Templates",
        "single-agent",
    ),
    "inspect-runtime.md": (
        "Houmao CLI",
        "Execution Adapter boundary",
    ),
}

AGENT_ENV_SETUP_REQUIRED_SKILL_TERMS = (
    "setup-agent-env",
    "resolve-agent-env-context",
    "require-topic-env-ready",
    "read-agent-env-gate",
    "plan-agent-workspaces",
    "derive-agent-env-gate",
    "require-topic-main-ready",
    "create-agent-worktrees",
    "verify-agent-env-gate",
    "topic.intent.agent_env_requirements",
    "topic.env.agent_setup_target_spec",
    "topic.env.topic_setup_target_spec",
    "explicit manual target spec",
    "Topic Main Development Repository",
    "projection predecessor evidence",
    "topic.repos.main",
    "authoritative Agent Names",
    "agent.workspace",
    "pixi run --manifest-path <manifest_path> --environment <pixi_environment>",
    "selected-agent partial",
    "Service Request",
    "Provenance refs",
    "overall_readiness_status",
    "bounded real-path verification",
    "isomer-misc-bounded-run-tips",
    "operation_classification",
    "classification source",
    "classification result",
    "unknown-risk",
    "generic best-effort judgment",
    "A generic smoke test is only supporting evidence",
    "Do not initialize, repair, or configure the Topic Main Development Repository",
    "Do not create per-agent Pixi manifests",
    "Do not install or mutate Topic Workspace dependencies",
    "mutate Workspace Runtime records",
)

AGENT_ENV_SETUP_REFERENCE_REQUIRED_TERMS = {
    "resolve-agent-env-context.md": (
        "topic.repos.main",
        "topic.repos.main.isomer_managed",
        "topic.agents_root",
        "topic.records",
        "topic.runtime",
        "requester",
        "confirmation_source",
        "Service Request refs",
        "Provenance refs",
    ),
    "require-topic-env-ready.md": (
        "topic.env.topic_setup_target_spec",
        "pixi.lock",
        ".pixi/",
        "not Agent Workspace cwd readiness",
        "isomer-srv-topic-env-setup",
    ),
    "read-agent-env-gate.md": (
        "topic.intent.agent_env_requirements",
        "required command set",
        "expected results",
        "success criteria",
        "Topic Main Development Repository predecessor requirements",
        "projection visibility requirements",
        "cwd assumptions",
        "Workspace Runtime mutation",
    ),
    "plan-agent-workspaces.md": (
        "Topic Team Instantiation Packet",
        "Topic Agent Team Profile material",
        "authority for Agent Names",
        "corroborating evidence",
        "agent-plan-conflict",
        "agent.workspace",
        "agent.private_artifacts",
        "agent.public_share",
    ),
    "derive-agent-env-gate.md": (
        "topic.env.agent_setup_target_spec",
        "explicit manual target spec",
        "## Source Agent Gate",
        "## Gate Checklist",
        "## Topic Env Gate",
        "## Topic Pixi Binding",
        "## Topic Main Development Repository Predecessor",
        "projection predecessor",
        "## Agent Plan",
        "## Semantic Paths",
        "## Worktree Plan",
        "## Verification Matrix",
        "## Expected Results",
        "## Blockers",
        "## Execution Log",
        "pixi run --manifest-path <manifest_path> --environment <pixi_environment>",
        "gate-cwd-incompatible",
        "`- [ ]`",
        "`- [x]`",
        "required per-agent readiness work contract",
        "pass condition",
        "evidence source",
        "affected Agent Name or matrix scope",
        "optional diagnostics",
        "bounded real-path",
        "isomer-misc-bounded-run-tips",
        "classification_source",
        "classification_result",
        "classification_reason",
        "resource_dimensions",
        "unknown-risk",
        "bounded-run guidance source",
        "generic best-effort judgment",
        "simple smoke test",
        "isomer-srv-topic-env-setup",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
        "do not invent a separate per-agent package install plan",
    ),
    "require-topic-main-ready.md": (
        "Topic Main Development Repository predecessor evidence",
        "projection predecessor",
        "isomer-srv-topic-env-setup",
        "Do not initialize, repair, or configure",
        "topic.repos.main.isomer_managed",
    ),
    "create-agent-worktrees.md": (
        "per-agent/<agent-name>/main",
        "worktree",
        "agent.workspace",
        "agent.private_artifacts",
        "agent.public_share",
        "cwd-friendly self-query guidance",
        "Do not claim Agent Workspace environment readiness until",
    ),
    "verify-agent-env-gate.md": (
        "selected-agent partial readiness evidence",
        "without passing Agent Name",
        "overall_readiness_status",
        "pixi run --manifest-path <manifest_path> --environment <pixi_environment>",
        "Agent Workspace cwd",
        "classification source",
        "classification evidence",
        "unknown-risk",
        "bounded real-path",
        "bounded-run guidance source",
        "source-agent required",
        "every targeted required `## Gate Checklist` item",
        "checked with cwd evidence",
        "exact checklist item",
        "user downgrade",
        "isomer-srv-topic-env-setup",
        "isomer-misc-pkg-specifics",
        "no package-specific rule",
        "Do not write or run independent PyPI, Pixi, Conda, or runtime-wiring package install commands",
    ),
    "setup-agent-env.md": (
        "resolve-agent-env-context",
        "require-topic-env-ready",
        "read-agent-env-gate",
        "plan-agent-workspaces",
        "derive-agent-env-gate",
        "require-topic-main-ready",
        "create-agent-worktrees",
        "verify-agent-env-gate",
        "repos/",
        "topic-main/",
        "agents/",
        "<agent-name>/",
        "bounded real-path",
        "classification evidence",
        "unknown-risk",
        "generic best-effort",
        "generic smoke test",
    ),
    "help.md": (
        "| Subcommand | Purpose | Produces |",
        "no per-agent Pixi environments",
        "no dependency mutation by default",
        "no Workspace Runtime mutation",
        "no Execution Adapter operation",
    ),
}

AGENT_ENV_SETUP_SUBCOMMANDS = (
    "resolve-agent-env-context.md",
    "require-topic-env-ready.md",
    "read-agent-env-gate.md",
    "plan-agent-workspaces.md",
    "derive-agent-env-gate.md",
    "require-topic-main-ready.md",
    "create-agent-worktrees.md",
    "verify-agent-env-gate.md",
    "setup-agent-env.md",
    "help.md",
)

REMOVED_OPERATOR_SKILLS = (
    "isomer-op-project-aware",
    "isomer-op-template-inspect",
    "isomer-op-topic-context-resolve",
    "isomer-op-service-request-route",
    "isomer-op-placeholder-reconcile",
    "isomer-op-topic-profile-draft",
    "isomer-op-profile-review-approval",
    "isomer-op-profile-materialize",
    "isomer-op-team-launch-orchestrate",
    "isomer-op-topic-prepare",
    "isomer-op-manual-research-session",
    "isomer-op-topic-workspace-mgr",
)

DEEPSCI_MINI_GUIDE_REQUIRED_TERMS = (
    "placeholder",
    "assumption",
    "workflow",
    "contract",
    "cooperation example",
    "deepsci-mini-lead",
    "deepsci-mini-scout",
    "deepsci-mini-synth-reviewer",
    "<topic-workspace>/team-profile/execplan/",
)

RESET_GUIDANCE_TERMS = (
    "topic-reset",
    "reset checkpoint",
    "structured reset checkpoint",
    "reset plan",
    "reset apply",
    "Topic Workspace reset",
)

RESET_FORBIDDEN_RESEARCH_TERMS = (
    "skillset/research-paradigm",
    "research-paradigm",
    "isomer-deepsci-",
)

PACKAGE_SPECIFICS_REQUIRED_TERMS = (
    "First lookup",
    "operational env gate derivation",
    "package mutation",
    "package-specific runtime verification",
    "before applying a generic PyPI, Conda, local-package, or system-Python source ladder",
    "no package-specific rule",
    "selected source or unresolved source",
    "required variant",
    "verification expectation",
    "generic Pixi mechanics",
    "package-source reachability checks",
    "bounded-run classification",
    "env gate writing",
    "final readiness reporting",
)

RESET_FORBIDDEN_GIT_COMMAND_RE = re.compile(r"\bgit\s+(?:stash|reset|checkout|branch|commit|tag)\b", re.IGNORECASE)
RESET_FORBIDDEN_GIT_REF_RE = re.compile(r"stash@\{", re.IGNORECASE)
RESET_RESEARCH_COUPLING_RE = re.compile(r"\b(?:route|depend|require|use|delegate|load|call|inspect)\w*\b", re.IGNORECASE)


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    line: int
    code: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.code} {self.message}"


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "skillset").exists():
            return candidate
        if (candidate / ".git").exists():
            return candidate
    return current


def relpath(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def read_lines(path: Path) -> tuple[str, ...]:
    return tuple(path.read_text(encoding="utf-8").splitlines())


def first_line_containing(lines: tuple[str, ...], term: str) -> int:
    for line_number, line in enumerate(lines, start=1):
        if term in line:
            return line_number
    return 1


def line_index_containing(lines: tuple[str, ...], term: str) -> int | None:
    for index, line in enumerate(lines):
        if term in line:
            return index
    return None


def has_numbered_step_after(lines: tuple[str, ...], start_index: int) -> bool:
    for line in lines[start_index + 1 :]:
        if line.startswith("## ") and line.strip() != "## Workflow":
            return False
        if re.match(r"^\d+\.\s+", line):
            return True
    return False


def add_forbidden_heavy_operation_diagnostics(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    path: Path,
    lines: tuple[str, ...],
    *,
    code: str,
) -> None:
    text = "\n".join(lines)
    for forbidden_term in CORE_OWNED_HEAVY_OPERATION_FORBIDDEN_TERMS:
        if forbidden_term in text:
            add(
                diagnostics,
                repo_root,
                path,
                first_line_containing(lines, forbidden_term),
                code,
                f"{path.name} must delegate heavy-operation classification to isomer-misc-bounded-run-tips instead of using fixed core-owned lists",
            )


def _line_has_reset_context(path: Path, line: str) -> bool:
    line_lower = line.lower()
    if path.name.startswith("reset-"):
        return True
    return any(term.lower() in line_lower for term in RESET_GUIDANCE_TERMS)


def _line_is_negated_git_boundary(line: str) -> bool:
    line_lower = line.lower()
    return any(marker in line_lower for marker in ("do not", "does not", "must not", "never", " no git", "without git"))


def add_forbidden_reset_guidance_diagnostics(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    path: Path,
    lines: tuple[str, ...],
    *,
    code: str,
) -> None:
    for line_number, line in enumerate(lines, start=1):
        if not _line_has_reset_context(path, line):
            continue
        if (RESET_FORBIDDEN_GIT_COMMAND_RE.search(line) or RESET_FORBIDDEN_GIT_REF_RE.search(line)) and not _line_is_negated_git_boundary(line):
            add(
                diagnostics,
                repo_root,
                path,
                line_number,
                code,
                "reset checkpoint workflows must not recommend Git reset, stash, branch, commit, tag, or ref commands",
            )
        line_lower = line.lower()
        for forbidden_term in RESET_FORBIDDEN_RESEARCH_TERMS:
            if forbidden_term.lower() in line_lower and RESET_RESEARCH_COUPLING_RE.search(line) and not _line_is_negated_git_boundary(line):
                add(
                    diagnostics,
                    repo_root,
                    path,
                    line_number,
                    code,
                    "operator reset guidance must not route to or depend on research-paradigm skills",
                )


def add_copied_topic_main_guidance_diagnostics(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    path: Path,
    lines: tuple[str, ...],
    *,
    code: str,
) -> None:
    for line_number, line in enumerate(lines, start=1):
        for copied_term in COPIED_TOPIC_MAIN_GUIDANCE_TERMS:
            if copied_term in line:
                add(
                    diagnostics,
                    repo_root,
                    path,
                    line_number,
                    code,
                    "topic-main guidance docs must route to `isomer-cli project topic-main-guidance` and the packaged .j2 template instead of copying the rendered block body",
                )


def output_contract_section(lines: tuple[str, ...]) -> tuple[int, str] | None:
    for index, line in enumerate(lines):
        if line.strip() not in OUTPUT_CONTRACT_SECTION_HEADINGS:
            continue
        end_index = len(lines)
        for next_index in range(index + 1, len(lines)):
            if lines[next_index].startswith("## "):
                end_index = next_index
                break
        return index, "\n".join(lines[index:end_index])
    return None


def add_split_output_contract_diagnostics(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    path: Path,
    lines: tuple[str, ...],
    *,
    code: str,
    require_contract: bool = False,
) -> None:
    section = output_contract_section(lines)
    if section is None:
        if require_contract:
            add(
                diagnostics,
                repo_root,
                path,
                1,
                code,
                f"{path.name} must include a split ## Output Contract with Essential Output and Complete Output",
            )
        return
    start_index, section_text = section
    for required_term in OUTPUT_CONTRACT_REQUIRED_TERMS:
        if required_term not in section_text:
            add(
                diagnostics,
                repo_root,
                path,
                start_index + 1,
                code,
                f"{path.name} output contract must document '{required_term}'",
            )


def validate_split_output_contract_docs(repo_root: Path, roots: tuple[Path, ...], *, code: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            if "research-paradigm" in path.parts:
                continue
            add_split_output_contract_diagnostics(
                diagnostics,
                repo_root,
                path,
                read_lines(path),
                code=code,
            )
    return diagnostics


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(lines: tuple[str, ...]) -> dict[str, str]:
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break
    if end is None:
        return {}
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        match = FRONTMATTER_RE.match(line)
        if match:
            fields[match.group(1)] = strip_scalar(match.group(2))
    return fields


def parse_interface_fields(lines: tuple[str, ...]) -> dict[str, tuple[str, int]]:
    fields: dict[str, tuple[str, int]] = {}
    in_interface = False
    for line_number, line in enumerate(lines, start=1):
        if re.match(r"^interface:\s*$", line):
            in_interface = True
            continue
        if in_interface and line and not line.startswith((" ", "\t")):
            in_interface = False
        if not in_interface:
            continue
        match = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            fields[match.group(1)] = (strip_scalar(match.group(2)), line_number)
    return fields


def add(
    diagnostics: list[Diagnostic],
    repo_root: Path,
    path: Path,
    line: int,
    code: str,
    message: str,
) -> None:
    diagnostics.append(Diagnostic(relpath(path, repo_root), max(line, 1), code, message))


def validate_global_isomer_cli_invocation(repo_root: Path, roots: tuple[Path, ...], *, code: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skillset_root = repo_root / "skillset"
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(candidate for candidate in root.rglob("*") if candidate.is_file() and candidate.suffix in ACTIVE_REF_SUFFIXES):
            try:
                rel_to_skillset = path.resolve().relative_to(skillset_root.resolve())
            except ValueError:
                rel_to_skillset = None
            if rel_to_skillset is not None and rel_to_skillset.parts and rel_to_skillset.parts[0] == "dev":
                continue
            for line_number, line in enumerate(read_lines(path), start=1):
                if FORBIDDEN_REPO_LOCAL_ISOMER_CLI in line:
                    add(
                        diagnostics,
                        repo_root,
                        path,
                        line_number,
                        code,
                        "non-dev skills must call global isomer-cli directly instead of 'pixi run isomer-cli'",
                    )
    return diagnostics


def clean_reference(raw: str) -> str | None:
    value = raw.strip().strip("<>").strip()
    if "://" in value or value.startswith("#"):
        return None
    value = value.split("#", 1)[0].strip()
    value = value.strip(".,;:)")
    if any(value.startswith(prefix) for prefix in LOCAL_REFERENCE_PREFIXES):
        return value
    return None


def local_references_from_line(line: str) -> Iterable[str]:
    for match in CODE_SPAN_RE.finditer(line):
        cleaned = clean_reference(match.group(1))
        if cleaned:
            yield cleaned
    for match in MARKDOWN_LINK_RE.finditer(line):
        destination = match.group(1).split()[0]
        cleaned = clean_reference(destination)
        if cleaned:
            yield cleaned


def validate_simple_skill_layout(
    target: Path,
    repo_root: Path,
    *,
    prefix: str,
    code: str,
    manifest_required: bool,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if not target.exists():
        add(diagnostics, repo_root, target, 1, code, "skillset path does not exist")
        return diagnostics

    skill_dirs = sorted(path for path in target.iterdir() if path.is_dir() and path.name.startswith(prefix))
    if not skill_dirs:
        add(diagnostics, repo_root, target, 1, code, f"no {prefix}* skill folders were found")
    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            add(diagnostics, repo_root, skill_dir, 1, code, "skill folder is missing SKILL.md")
            continue
        frontmatter = parse_frontmatter(read_lines(skill_md))
        if frontmatter.get("name") != skill_name:
            add(diagnostics, repo_root, skill_md, 2, code, "frontmatter name must match the skill folder")
        if not frontmatter.get("description"):
            add(diagnostics, repo_root, skill_md, 3, code, "frontmatter description is required")
        validate_local_references(skill_dir, repo_root, diagnostics, code)
        validate_manifest(skill_dir, repo_root, diagnostics, code, manifest_required=manifest_required)
    return diagnostics


def validate_manifest(
    skill_dir: Path,
    repo_root: Path,
    diagnostics: list[Diagnostic],
    code: str,
    *,
    manifest_required: bool,
) -> None:
    skill_name = skill_dir.name
    manifest = skill_dir / "agents" / "openai.yaml"
    if not manifest.exists():
        if manifest_required:
            add(diagnostics, repo_root, skill_dir, 1, code, "agents/openai.yaml is required")
        return
    fields = parse_interface_fields(read_lines(manifest))
    display_name = fields.get("display_name")
    if display_name is None:
        add(diagnostics, repo_root, manifest, 1, code, "interface.display_name is required")
    elif display_name[0] != skill_name:
        add(diagnostics, repo_root, manifest, display_name[1], code, f"interface.display_name must be '{skill_name}'")
    default_prompt = fields.get("default_prompt")
    if default_prompt is None:
        add(diagnostics, repo_root, manifest, 1, code, "interface.default_prompt is required")
    elif f"${skill_name}" not in default_prompt[0]:
        add(diagnostics, repo_root, manifest, default_prompt[1], code, f"interface.default_prompt must invoke ${skill_name}")


def validate_local_references(skill_dir: Path, repo_root: Path, diagnostics: list[Diagnostic], code: str) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return
    skill_root = skill_dir.resolve()
    for line_number, line in enumerate(read_lines(skill_md), start=1):
        for reference in local_references_from_line(line):
            target = (skill_dir / reference).resolve()
            if not target.is_relative_to(skill_root) or not target.exists():
                add(diagnostics, repo_root, skill_md, line_number, code, f"local reference '{reference}' does not exist inside {skill_dir.name}")


def iter_active_ref_files(repo_root: Path) -> Iterable[Path]:
    for root_name in ACTIVE_REF_ROOTS:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES:
                yield path
    for file_name in ACTIVE_REF_FILES:
        path = repo_root / file_name
        if path.exists():
            yield path


def is_passive_stale_ref_file(path: Path) -> bool:
    return any(part in PASSIVE_STALE_REF_PARTS for part in path.parts)


def validate_migrated_operator_refs(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    pattern = re.compile("|".join(re.escape(name) for name in MIGRATED_OPERATOR_SKILLS))
    validator_path = Path(__file__).resolve()
    for path in sorted(set(iter_active_ref_files(repo_root))):
        if path.resolve() == validator_path:
            continue
        if is_passive_stale_ref_file(path):
            continue
        lines = read_lines(path)
        for line_number, line in enumerate(lines, start=1):
            match = pattern.search(line)
            if match:
                add(
                    diagnostics,
                    repo_root,
                    path,
                    line_number,
                    "OPS002",
                    f"migrated operator skill '{match.group(0)}' must use the new operator or service skill name",
                )
            for old_prefix, new_prefix in STALE_SKILL_NAMESPACE_REPLACEMENTS.items():
                if old_prefix in line:
                    add(
                        diagnostics,
                        repo_root,
                        path,
                        line_number,
                        "OPS002",
                        f"stale skill namespace '{old_prefix}' must use '{new_prefix}' in active guidance",
                    )
            for old_skill, new_skill in STALE_EXACT_SKILL_REPLACEMENTS.items():
                if old_skill in line:
                    add(
                        diagnostics,
                        repo_root,
                        path,
                        line_number,
                        "OPS002",
                        f"stale skill '{old_skill}' must use '{new_skill}' in active guidance",
                    )
    return diagnostics


def validate_topic_team_step_dependency_contract(repo_root: Path, skill_dir: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    references_dir = skill_dir / "references"
    scripts_dir = skill_dir / "scripts"
    manifest_path = references_dir / TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_MANIFEST
    script_path = scripts_dir / TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT

    if not manifest_path.exists():
        add(
            diagnostics,
            repo_root,
            manifest_path,
            1,
            "OPS003",
            f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include references/{TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_MANIFEST}",
        )
    if not script_path.exists():
        add(
            diagnostics,
            repo_root,
            script_path,
            1,
            "OPS003",
            f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include scripts/{TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT}",
        )

    manifest: dict[str, Any] | None = None
    if manifest_path.exists():
        try:
            manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            add(diagnostics, repo_root, manifest_path, exc.lineno, "OPS003", "step dependency manifest must be valid JSON")
        else:
            if isinstance(manifest_data, dict):
                manifest = manifest_data
            else:
                add(diagnostics, repo_root, manifest_path, 1, "OPS003", "step dependency manifest root must be a JSON object")

    if manifest is not None:
        steps = manifest.get("steps")
        canonical_order = manifest.get("canonical_order")
        edges = manifest.get("edges")
        if not isinstance(steps, dict):
            add(diagnostics, repo_root, manifest_path, 1, "OPS003", "step dependency manifest must contain object field 'steps'")
            steps = {}
        if not isinstance(canonical_order, list) or not all(isinstance(step_id, str) for step_id in canonical_order):
            add(diagnostics, repo_root, manifest_path, 1, "OPS003", "step dependency manifest must contain string list field 'canonical_order'")
            canonical_order = []
        if edges is not None and not isinstance(edges, list):
            add(diagnostics, repo_root, manifest_path, 1, "OPS003", "step dependency manifest field 'edges' must be a list when present")

        procedural_step_ids = {
            subcommand.removesuffix(".md") for subcommand in TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS
        }
        manifest_step_ids = {step_id for step_id in steps if isinstance(step_id, str)}
        missing_steps = sorted(procedural_step_ids - manifest_step_ids)
        if missing_steps:
            add(
                diagnostics,
                repo_root,
                manifest_path,
                1,
                "OPS003",
                "step dependency manifest must cover procedural subcommands: " + ", ".join(missing_steps),
            )

        required_step_fields = {
            "id",
            "display_name",
            "kind",
            "predecessors",
            "requires",
            "produces",
            "recovery_conditions",
            "mutation_notes",
            "unrecoverable_blockers",
        }
        for step_id, step in steps.items():
            if not isinstance(step_id, str):
                add(diagnostics, repo_root, manifest_path, 1, "OPS003", "step dependency manifest step ids must be strings")
                continue
            if not isinstance(step, dict):
                add(diagnostics, repo_root, manifest_path, 1, "OPS003", f"step dependency entry '{step_id}' must be an object")
                continue
            missing_fields = sorted(required_step_fields - set(step))
            if missing_fields:
                add(
                    diagnostics,
                    repo_root,
                    manifest_path,
                    1,
                    "OPS003",
                    f"step dependency entry '{step_id}' is missing fields: {', '.join(missing_fields)}",
                )
            if step.get("id") != step_id:
                add(diagnostics, repo_root, manifest_path, 1, "OPS003", f"step dependency entry '{step_id}' must declare matching id")

        unknown_order_steps = sorted(step_id for step_id in canonical_order if step_id not in manifest_step_ids)
        if unknown_order_steps:
            add(
                diagnostics,
                repo_root,
                manifest_path,
                1,
                "OPS003",
                "step dependency canonical_order contains unknown steps: " + ", ".join(unknown_order_steps),
            )

    if script_path.exists():
        result = subprocess.run(
            [sys.executable, str(script_path), "validate"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode != 0:
            output = (result.stderr or result.stdout).strip()
            detail = f": {output}" if output else ""
            add(
                diagnostics,
                repo_root,
                script_path,
                1,
                "OPS003",
                f"{TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT} validate failed{detail}",
            )

    key_docs = (skill_dir / "SKILL.md", references_dir / "help.md", references_dir / "fast-forward.md")
    for doc_path in key_docs:
        if doc_path.exists() and TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT not in doc_path.read_text(encoding="utf-8"):
            add(
                diagnostics,
                repo_root,
                doc_path,
                1,
                "OPS003",
                f"{doc_path.name} must route dependency-path questions through {TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT}",
            )

    for subcommand_file_name in TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS:
        subcommand_path = references_dir / subcommand_file_name
        if not subcommand_path.exists():
            continue
        subcommand_lines = read_lines(subcommand_path)
        subcommand_text = "\n".join(subcommand_lines)
        if "targeted fast-forward recovery" in subcommand_text.lower() and TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT not in subcommand_text:
            add(
                diagnostics,
                repo_root,
                subcommand_path,
                first_line_containing(subcommand_lines, "targeted fast-forward recovery"),
                "OPS003",
                f"references/{subcommand_file_name} must query {TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT} for targeted recovery paths",
            )
        for line_number, line in enumerate(subcommand_lines, start=1):
            lower_line = line.lower()
            if "inclusive default path is" in lower_line and "->" in line:
                add(
                    diagnostics,
                    repo_root,
                    subcommand_path,
                    line_number,
                    "OPS003",
                    f"references/{subcommand_file_name} must not duplicate targeted recovery chains in prose; query {TOPIC_TEAM_SPECIALIZATION_DEPENDENCY_SCRIPT}",
                )

    return diagnostics


def validate_topic_team_specialization_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / TOPIC_TEAM_SPECIALIZATION_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must not contain evals/")
    for removed_skill in REMOVED_OPERATOR_SKILLS:
        removed_path = repo_root / "skillset" / "operator" / removed_skill
        if removed_path.exists():
            add(
                diagnostics,
                repo_root,
                removed_path,
                1,
                "OPS003",
                f"{removed_skill} is no longer part of the active operator skillset and must not be a standalone skill",
            )
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS003", require_contract=True)
    add_forbidden_heavy_operation_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS003")
    for term in TOPIC_TEAM_SPECIALIZATION_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS003",
                f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must document '{term}'",
            )
    skill_workflow_index = line_index_containing(lines, "## Workflow")
    if skill_workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include a ## Workflow section")
    else:
        if skill_workflow_index > 24:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, skill_workflow_index):
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include a freeform fallback")
    references_dir = skill_dir / "references"
    for support_file_name in TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES:
        support_path = references_dir / support_file_name
        if not support_path.exists():
            add(diagnostics, repo_root, support_path, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include references/{support_file_name}")
    diagnostics.extend(validate_topic_team_step_dependency_contract(repo_root, skill_dir))
    allowed_reference_names = set(TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS) | set(TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS003",
                f"{TOPIC_TEAM_SPECIALIZATION_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        skill_file_lines = read_lines(skill_file)
        for line_number, line in enumerate(skill_file_lines, start=1):
            for forbidden_ref in TOPIC_TEAM_SPECIALIZATION_FORBIDDEN_SUPPORT_REFS:
                if forbidden_ref in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS003",
                        f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must keep required support references inside its skill directory; found '{forbidden_ref}'",
                    )
    for subcommand_file_name in TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS:
        subcommand_name = subcommand_file_name.removesuffix(".md")
        subcommand_path = references_dir / subcommand_file_name
        if subcommand_name not in TOPIC_TEAM_SPECIALIZATION_NAMING_EXCEPTIONS and not re.match(r"^[a-z]+(?:-[a-z]+)+$", subcommand_name):
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"subcommand '{subcommand_name}' must be a short verb-object name or an allowed command")
        if len(subcommand_name) > 24 and subcommand_name not in TOPIC_TEAM_SPECIALIZATION_LENGTH_EXCEPTIONS:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"subcommand '{subcommand_name}' must be short")
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS003", f"{TOPIC_TEAM_SPECIALIZATION_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        add_forbidden_heavy_operation_diagnostics(diagnostics, repo_root, subcommand_path, subcommand_lines, code="OPS003")
        workflow_index = line_index_containing(subcommand_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS003", f"references/{subcommand_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subcommand_lines, workflow_index):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS003", f"references/{subcommand_file_name} workflow must use numbered steps")
        subcommand_text = "\n".join(subcommand_lines)
        if "does not map cleanly" not in subcommand_text:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS003", f"references/{subcommand_file_name} must include a freeform fallback")
        if subcommand_file_name in TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS:
            if "## Prerequisite Artifacts" not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must document predecessor artifacts")
            if "refuse to run" not in subcommand_text.lower():
                add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must refuse to run when predecessor artifacts are missing")
        for required_term in TOPIC_TEAM_SPECIALIZATION_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS003", f"references/{subcommand_file_name} must document '{required_term}'")
    help_path = references_dir / "help.md"
    if help_path.exists():
        help_lines = read_lines(help_path)
        help_text = "\n".join(help_lines)
        for table_term in TOPIC_TEAM_SPECIALIZATION_HELP_TABLE_TERMS:
            if table_term not in help_text:
                add(
                    diagnostics,
                    repo_root,
                    help_path,
                    first_line_containing(help_lines, "## Public Subcommands"),
                    "OPS003",
                    f"references/help.md must print public subcommands as a three-column table including '{table_term}'",
                )
        for helper_subcommand in TOPIC_TEAM_SPECIALIZATION_HELP_FORBIDDEN_SUBCOMMANDS:
            if helper_subcommand in help_text:
                add(
                    diagnostics,
                    repo_root,
                    help_path,
                    first_line_containing(help_lines, helper_subcommand),
                    "OPS003",
                    f"references/help.md must not list private helper subcommand '{helper_subcommand}'",
                )
    return diagnostics


def validate_project_manager_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / PROJECT_MANAGER_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must not contain evals/")
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS005", require_contract=True)
    for term in PROJECT_MANAGER_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS005",
                f"{PROJECT_MANAGER_SKILL} must document '{term}'",
            )
    skill_workflow_index = line_index_containing(lines, "## Workflow")
    if skill_workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include a ## Workflow section")
    else:
        if skill_workflow_index > 24:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, skill_workflow_index):
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS005", f"{PROJECT_MANAGER_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include a freeform fallback")
    references_dir = skill_dir / "references"
    for support_file_name in PROJECT_MANAGER_SUPPORT_REFERENCES:
        support_path = references_dir / support_file_name
        if not support_path.exists():
            add(diagnostics, repo_root, support_path, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include references/{support_file_name}")
    allowed_reference_names = set(PROJECT_MANAGER_SUBCOMMANDS) | set(PROJECT_MANAGER_SUPPORT_REFERENCES)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS005",
                f"{PROJECT_MANAGER_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        skill_file_lines = read_lines(skill_file)
        for line_number, line in enumerate(skill_file_lines, start=1):
            for forbidden_ref in PROJECT_MANAGER_FORBIDDEN_SUPPORT_REFS:
                if forbidden_ref in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS005",
                        f"{PROJECT_MANAGER_SKILL} must keep required support references inside its skill directory; found '{forbidden_ref}'",
                    )
            for forbidden_cli_term in PROJECT_MANAGER_FORBIDDEN_CLI_TERMS:
                if forbidden_cli_term in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS005",
                        f"{PROJECT_MANAGER_SKILL} must use 'isomer-cli project ...' command shapes instead of '{forbidden_cli_term}'",
                    )
    for subcommand_file_name in PROJECT_MANAGER_SUBCOMMANDS:
        subcommand_name = subcommand_file_name.removesuffix(".md")
        subcommand_path = references_dir / subcommand_file_name
        if subcommand_name not in PROJECT_MANAGER_NAMING_EXCEPTIONS and not re.match(r"^[a-z]+(?:-[a-z]+)+$", subcommand_name):
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"subcommand '{subcommand_name}' must be a short verb-object name or an allowed command")
        if len(subcommand_name) > 24:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"subcommand '{subcommand_name}' must be short")
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"{PROJECT_MANAGER_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS005", f"{PROJECT_MANAGER_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        workflow_index = line_index_containing(subcommand_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS005", f"references/{subcommand_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS005", f"references/{subcommand_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subcommand_lines, workflow_index):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS005", f"references/{subcommand_file_name} workflow must use numbered steps")
        if "does not map cleanly" not in "\n".join(subcommand_lines):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS005", f"references/{subcommand_file_name} must include a freeform fallback")
    return diagnostics


def validate_topic_creator_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / TOPIC_CREATOR_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS008", f"{TOPIC_CREATOR_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS008", f"{TOPIC_CREATOR_SKILL} must not contain evals/")
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS008", require_contract=True)
    add_forbidden_reset_guidance_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS008")
    for term in TOPIC_CREATOR_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS008",
                f"{TOPIC_CREATOR_SKILL} must document '{term}'",
            )
    workflow_index = line_index_containing(lines, "## Workflow")
    if workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS008", f"{TOPIC_CREATOR_SKILL} must include a ## Workflow section")
    else:
        if workflow_index > 24:
            add(diagnostics, repo_root, skill_md, workflow_index + 1, "OPS008", f"{TOPIC_CREATOR_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, workflow_index):
            add(diagnostics, repo_root, skill_md, workflow_index + 1, "OPS008", f"{TOPIC_CREATOR_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, workflow_index + 1, "OPS008", f"{TOPIC_CREATOR_SKILL} must include a freeform fallback")
    references_dir = skill_dir / "references"
    allowed_reference_names = set(TOPIC_CREATOR_COMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS008",
                f"{TOPIC_CREATOR_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for command_file_name in TOPIC_CREATOR_COMMANDS:
        command_path = references_dir / command_file_name
        if not command_path.exists():
            add(diagnostics, repo_root, command_path, 1, "OPS008", f"{TOPIC_CREATOR_SKILL} must include references/{command_file_name}")
            continue
        if f"references/{command_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS008", f"{TOPIC_CREATOR_SKILL} must link references/{command_file_name}")
        command_lines = read_lines(command_path)
        command_text = "\n".join(command_lines)
        add_forbidden_reset_guidance_diagnostics(diagnostics, repo_root, command_path, command_lines, code="OPS008")
        command_workflow_index = line_index_containing(command_lines, "## Workflow")
        if command_workflow_index is None:
            add(diagnostics, repo_root, command_path, 1, "OPS008", f"references/{command_file_name} must include a ## Workflow section")
            continue
        if command_workflow_index > 8:
            add(diagnostics, repo_root, command_path, command_workflow_index + 1, "OPS008", f"references/{command_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(command_lines, command_workflow_index):
            add(diagnostics, repo_root, command_path, command_workflow_index + 1, "OPS008", f"references/{command_file_name} workflow must use numbered steps")
        if "does not map cleanly" not in command_text:
            add(diagnostics, repo_root, command_path, command_workflow_index + 1, "OPS008", f"references/{command_file_name} must include a freeform fallback")
        for required_term in TOPIC_CREATOR_REFERENCE_REQUIRED_TERMS.get(command_file_name, ()):
            if required_term not in command_text:
                add(diagnostics, repo_root, command_path, 1, "OPS008", f"references/{command_file_name} must document '{required_term}'")
    return diagnostics


def validate_topic_manager_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / TOPIC_MANAGER_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS006", f"{TOPIC_MANAGER_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS006", f"{TOPIC_MANAGER_SKILL} must not contain evals/")
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS006", require_contract=True)
    add_forbidden_reset_guidance_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS006")
    add_copied_topic_main_guidance_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS006")
    for term in TOPIC_MANAGER_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS006",
                f"{TOPIC_MANAGER_SKILL} must document '{term}'",
            )
    skill_workflow_index = line_index_containing(lines, "## Workflow")
    if skill_workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS006", f"{TOPIC_MANAGER_SKILL} must include a ## Workflow section")
    else:
        if skill_workflow_index > 24:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS006", f"{TOPIC_MANAGER_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, skill_workflow_index):
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS006", f"{TOPIC_MANAGER_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, skill_workflow_index + 1, "OPS006", f"{TOPIC_MANAGER_SKILL} must include a freeform fallback")
    references_dir = skill_dir / "references"
    allowed_reference_names = set(TOPIC_MANAGER_SUBCOMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS006",
                f"{TOPIC_MANAGER_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        skill_file_lines = read_lines(skill_file)
        add_forbidden_reset_guidance_diagnostics(diagnostics, repo_root, skill_file, skill_file_lines, code="OPS006")
        add_copied_topic_main_guidance_diagnostics(diagnostics, repo_root, skill_file, skill_file_lines, code="OPS006")
        for line_number, line in enumerate(skill_file_lines, start=1):
            for forbidden_term in TOPIC_MANAGER_FORBIDDEN_PUBLIC_TERMS:
                if forbidden_term in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS006",
                        f"{TOPIC_MANAGER_SKILL} must use agent-name public wording instead of stale '{forbidden_term}'",
                    )
            for forbidden_ref in TOPIC_MANAGER_FORBIDDEN_SUPPORT_REFS:
                if forbidden_ref in line:
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS006",
                        f"{TOPIC_MANAGER_SKILL} must keep required support references inside its skill directory; found '{forbidden_ref}'",
                    )
    for subcommand_file_name in TOPIC_MANAGER_SUBCOMMANDS:
        subcommand_name = subcommand_file_name.removesuffix(".md")
        subcommand_path = references_dir / subcommand_file_name
        if subcommand_name not in TOPIC_MANAGER_NAMING_EXCEPTIONS and not re.match(r"^[a-z]+(?:-[a-z]+)+$", subcommand_name):
            add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"subcommand '{subcommand_name}' must be a short verb-object name or an allowed command")
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"{TOPIC_MANAGER_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS006", f"{TOPIC_MANAGER_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        workflow_index = line_index_containing(subcommand_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"references/{subcommand_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS006", f"references/{subcommand_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subcommand_lines, workflow_index):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS006", f"references/{subcommand_file_name} workflow must use numbered steps")
        subcommand_text = "\n".join(subcommand_lines)
        if "does not map cleanly" not in subcommand_text:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS006", f"references/{subcommand_file_name} must include a freeform fallback")
        for required_term in TOPIC_MANAGER_REFERENCE_REQUIRED_TERMS:
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"references/{subcommand_file_name} must document '{required_term}'")
        for required_term in TOPIC_MANAGER_SEMANTIC_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS006", f"references/{subcommand_file_name} must document '{required_term}'")
    help_path = references_dir / "help.md"
    if help_path.exists():
        help_lines = read_lines(help_path)
        help_text = "\n".join(help_lines)
        for table_term in TOPIC_MANAGER_HELP_TABLE_TERMS:
            if table_term not in help_text:
                add(
                    diagnostics,
                    repo_root,
                    help_path,
                    first_line_containing(help_lines, "## Public Subcommands"),
                    "OPS006",
                    f"references/help.md must print public subcommands as a three-column table including '{table_term}'",
                )
    return diagnostics


def validate_welcome_module(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "operator" / WELCOME_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "OPS011", f"{WELCOME_SKILL} is required")
        return diagnostics
    if (skill_dir / "evals").exists():
        add(diagnostics, repo_root, skill_dir / "evals", 1, "OPS011", f"{WELCOME_SKILL} must not contain evals/")

    lines = read_lines(skill_md)
    text = "\n".join(lines)
    frontmatter = parse_frontmatter(lines)
    if frontmatter.get("name") != WELCOME_SKILL:
        add(diagnostics, repo_root, skill_md, 2, "OPS011", f"{WELCOME_SKILL} frontmatter name must match the skill folder")
    if not frontmatter.get("description"):
        add(diagnostics, repo_root, skill_md, 3, "OPS011", f"{WELCOME_SKILL} frontmatter description is required")
    elif "manual invocation only" not in frontmatter["description"].lower():
        add(diagnostics, repo_root, skill_md, 3, "OPS011", f"{WELCOME_SKILL} description must state Manual invocation only")
    validate_manifest(skill_dir, repo_root, diagnostics, "OPS011", manifest_required=True)
    manifest_path = skill_dir / "agents" / "openai.yaml"
    if manifest_path.exists() and "allow_implicit_invocation: false" not in "\n".join(read_lines(manifest_path)):
        add(diagnostics, repo_root, manifest_path, 1, "OPS011", f"{WELCOME_SKILL} agents/openai.yaml must set allow_implicit_invocation: false")
    validate_local_references(skill_dir, repo_root, diagnostics, "OPS011")
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="OPS011", require_contract=True)

    for term in WELCOME_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "OPS011",
                f"{WELCOME_SKILL} must document '{term}'",
            )
    for usage_path in WELCOME_USAGE_PATHS:
        if usage_path not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "## Usage Path Subcommands"),
                "OPS011",
                f"{WELCOME_SKILL} must expose visible usage path '{usage_path}' in SKILL.md",
            )

    workflow_index = line_index_containing(lines, "## Workflow")
    if workflow_index is None:
        add(diagnostics, repo_root, skill_md, 1, "OPS011", f"{WELCOME_SKILL} must include a ## Workflow section")
    else:
        if workflow_index > 24:
            add(diagnostics, repo_root, skill_md, workflow_index + 1, "OPS011", f"{WELCOME_SKILL} must place ## Workflow near the top")
        if not has_numbered_step_after(lines, workflow_index):
            add(diagnostics, repo_root, skill_md, workflow_index + 1, "OPS011", f"{WELCOME_SKILL} workflow must use numbered steps")
        if "does not map cleanly" not in text:
            add(diagnostics, repo_root, skill_md, workflow_index + 1, "OPS011", f"{WELCOME_SKILL} must include a freeform fallback")

    references_dir = skill_dir / "references"
    allowed_reference_names = set(WELCOME_SUBCOMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "OPS011",
                f"{WELCOME_SKILL} has unexpected reference page references/{reference_path.name}",
            )

    reference_texts: list[str] = []
    for subcommand_file_name in WELCOME_SUBCOMMANDS:
        subcommand_path = references_dir / subcommand_file_name
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "OPS011", f"{WELCOME_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "OPS011", f"{WELCOME_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        subcommand_text = "\n".join(subcommand_lines)
        reference_texts.append(subcommand_text)
        workflow_index = line_index_containing(subcommand_lines, "## Workflow")
        if workflow_index is None:
            add(diagnostics, repo_root, subcommand_path, 1, "OPS011", f"references/{subcommand_file_name} must include a ## Workflow section")
            continue
        if workflow_index > 8:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS011", f"references/{subcommand_file_name} must place ## Workflow near the top")
        if not has_numbered_step_after(subcommand_lines, workflow_index):
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS011", f"references/{subcommand_file_name} workflow must use numbered steps")
        if "does not map cleanly" not in subcommand_text:
            add(diagnostics, repo_root, subcommand_path, workflow_index + 1, "OPS011", f"references/{subcommand_file_name} must include a freeform fallback")
        for required_term in WELCOME_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "OPS011", f"references/{subcommand_file_name} must document '{required_term}'")

    combined_text = "\n".join([text, *reference_texts])
    for owner_skill in WELCOME_ACTIVE_OWNER_SKILLS:
        if owner_skill not in combined_text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Guardrails"), "OPS011", f"{WELCOME_SKILL} must route to active owner skill '{owner_skill}'")
        if f"${owner_skill}" not in combined_text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "## Usage Path Subcommands"),
                "OPS011",
                f"{WELCOME_SKILL} must include direct invocation language for ${owner_skill}",
            )

    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        for line_number, line in enumerate(read_lines(skill_file), start=1):
            lower_line = line.lower()
            for retired_skill in WELCOME_RETIRED_ROUTE_SKILLS:
                if retired_skill in line and not any(marker in lower_line for marker in WELCOME_ALLOWED_RETIRED_ROUTE_MARKERS):
                    add(
                        diagnostics,
                        repo_root,
                        skill_file,
                        line_number,
                        "OPS011",
                        f"{WELCOME_SKILL} must not present retired skill '{retired_skill}' as an active route",
                    )
            if "isomer-misc-tool-packs" in line and not any(marker in lower_line for marker in WELCOME_TOOL_PACK_ALLOWED_MARKERS):
                add(
                    diagnostics,
                    repo_root,
                    skill_file,
                    line_number,
                    "OPS011",
                    f"{WELCOME_SKILL} must mention isomer-misc-tool-packs only as manual explicit routing, not an automatic welcome path",
                )

    return diagnostics


def validate_operator_manifest_inventory(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    manifest_path = repo_root / "skillset" / "manifest.toml"
    if not manifest_path.exists():
        return diagnostics
    try:
        manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        add(diagnostics, repo_root, manifest_path, exc.lineno, "OPS011", "skillset manifest must be valid TOML")
        return diagnostics
    core = manifest.get("groups", {}).get("core", {})
    skills = core.get("skills")
    if not isinstance(skills, list) or not all(isinstance(skill, str) for skill in skills):
        add(diagnostics, repo_root, manifest_path, 1, "OPS011", "skillset manifest groups.core.skills must be a string list")
        return diagnostics
    if f"operator/{WELCOME_SKILL}" not in skills:
        add(diagnostics, repo_root, manifest_path, 1, "OPS011", f"skillset manifest must include operator/{WELCOME_SKILL}")
    for retired_skill in WELCOME_RETIRED_ROUTE_SKILLS:
        retired_entry = f"operator/{retired_skill}"
        if retired_entry in skills:
            add(diagnostics, repo_root, manifest_path, 1, "OPS011", f"skillset manifest must not include retired {retired_entry}")
    return diagnostics


def validate_deepsci_mini_specialization_guide(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    guide = repo_root / "teams" / "deepsci-mini" / "execplan" / "team-specialization-guide.md"
    if not guide.exists():
        add(diagnostics, repo_root, guide, 1, "OPS004", "deepsci-mini must include team-specialization-guide.md")
        return diagnostics
    lines = read_lines(guide)
    text = "\n".join(lines).lower()
    for term in DEEPSCI_MINI_GUIDE_REQUIRED_TERMS:
        if term.lower() not in text:
            add(
                diagnostics,
                repo_root,
                guide,
                first_line_containing(lines, "# deepsci-mini"),
                "OPS004",
                f"deepsci-mini specialization guide must describe '{term}'",
            )
    return diagnostics


def validate_operator_skillset(repo_root: Path) -> list[Diagnostic]:
    diagnostics = validate_simple_skill_layout(
        repo_root / "skillset" / "operator",
        repo_root,
        prefix="isomer-op-",
        code="OPS001",
        manifest_required=True,
    )
    diagnostics.extend(validate_migrated_operator_refs(repo_root))
    diagnostics.extend(validate_topic_team_specialization_module(repo_root))
    diagnostics.extend(validate_project_manager_module(repo_root))
    diagnostics.extend(validate_topic_creator_module(repo_root))
    diagnostics.extend(validate_topic_manager_module(repo_root))
    diagnostics.extend(validate_welcome_module(repo_root))
    diagnostics.extend(validate_operator_manifest_inventory(repo_root))
    diagnostics.extend(validate_deepsci_mini_specialization_guide(repo_root))
    diagnostics.extend(validate_split_output_contract_docs(repo_root, (repo_root / "skillset" / "operator",), code="OPS007"))
    diagnostics.extend(validate_global_isomer_cli_invocation(repo_root, (repo_root / "skillset" / "operator",), code="OPS010"))
    return sorted(set(diagnostics))


def validate_topic_env_setup_service(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    old_skill_dir = repo_root / "skillset" / "service" / "isomer-srv-env-setup"
    if old_skill_dir.exists():
        add(diagnostics, repo_root, old_skill_dir, 1, "SVS002", "legacy isomer-srv-env-setup skill folder must be renamed to isomer-srv-topic-env-setup")
    skill_dir = repo_root / "skillset" / "service" / TOPIC_ENV_SETUP_SERVICE_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "SVS002", f"{TOPIC_ENV_SETUP_SERVICE_SKILL} is required")
        return diagnostics
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="SVS002", require_contract=True)
    add_forbidden_heavy_operation_diagnostics(diagnostics, repo_root, skill_md, lines, code="SVS002")
    add_copied_topic_main_guidance_diagnostics(diagnostics, repo_root, skill_md, lines, code="SVS002")
    for term in TOPIC_ENV_SETUP_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "SVS002",
                f"{TOPIC_ENV_SETUP_SERVICE_SKILL} must document '{term}'",
            )
    references_dir = skill_dir / "references"
    for removed_subcommand in TOPIC_ENV_SETUP_REMOVED_SUBCOMMANDS:
        removed_path = references_dir / removed_subcommand
        if removed_path.exists():
            add(diagnostics, repo_root, removed_path, 1, "SVS002", f"legacy subcommand references/{removed_subcommand} must be renamed")
    allowed_reference_names = set(TOPIC_ENV_SETUP_SUBCOMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "SVS002",
                f"{TOPIC_ENV_SETUP_SERVICE_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for subcommand_file_name in TOPIC_ENV_SETUP_SUBCOMMANDS:
        subcommand_path = references_dir / subcommand_file_name
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "SVS002", f"{TOPIC_ENV_SETUP_SERVICE_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "SVS002", f"{TOPIC_ENV_SETUP_SERVICE_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        add_forbidden_heavy_operation_diagnostics(diagnostics, repo_root, subcommand_path, subcommand_lines, code="SVS002")
        add_copied_topic_main_guidance_diagnostics(diagnostics, repo_root, subcommand_path, subcommand_lines, code="SVS002")
        subcommand_text = "\n".join(subcommand_lines)
        for required_term in TOPIC_ENV_SETUP_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "SVS002", f"references/{subcommand_file_name} must document '{required_term}'")
    for file_name, term in zip(
        ("resolve-topic-workspace.md", "resolve-topic-workspace.md", "read-env-gate.md", "setup-topic-env.md", "verify-env-gate.md"),
        TOPIC_ENV_SETUP_INDEPENDENCE_TERMS,
        strict=True,
    ):
        subcommand_path = references_dir / file_name
        if subcommand_path.exists():
            subcommand_lines = read_lines(subcommand_path)
            subcommand_text = "\n".join(subcommand_lines)
            if term not in subcommand_text:
                add(
                    diagnostics,
                    repo_root,
                    subcommand_path,
                    first_line_containing(subcommand_lines, "#"),
                    "SVS002",
                    f"references/{file_name} must document team-independent environment setup term '{term}'",
                )
    return diagnostics


def validate_agent_env_setup_service(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "service" / AGENT_ENV_SETUP_SERVICE_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "SVS003", f"{AGENT_ENV_SETUP_SERVICE_SKILL} is required")
        return diagnostics
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="SVS003", require_contract=True)
    add_forbidden_heavy_operation_diagnostics(diagnostics, repo_root, skill_md, lines, code="SVS003")
    for term in AGENT_ENV_SETUP_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "SVS003",
                f"{AGENT_ENV_SETUP_SERVICE_SKILL} must document '{term}'",
            )
    references_dir = skill_dir / "references"
    allowed_reference_names = set(AGENT_ENV_SETUP_SUBCOMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "SVS003",
                f"{AGENT_ENV_SETUP_SERVICE_SKILL} has unexpected reference page references/{reference_path.name}",
            )
    for subcommand_file_name in AGENT_ENV_SETUP_SUBCOMMANDS:
        subcommand_path = references_dir / subcommand_file_name
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "SVS003", f"{AGENT_ENV_SETUP_SERVICE_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "SVS003", f"{AGENT_ENV_SETUP_SERVICE_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        add_forbidden_heavy_operation_diagnostics(diagnostics, repo_root, subcommand_path, subcommand_lines, code="SVS003")
        subcommand_text = "\n".join(subcommand_lines)
        for required_term in AGENT_ENV_SETUP_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "SVS003", f"references/{subcommand_file_name} must document '{required_term}'")
    return diagnostics


def validate_houmao_interop_service(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    old_operator_dir = repo_root / "skillset" / "operator" / "isomer-op-houmao-interop"
    old_service_dir = repo_root / "skillset" / "service" / "isomer-op-houmao-interop"
    if old_operator_dir.exists():
        add(diagnostics, repo_root, old_operator_dir, 1, "SVS006", "legacy isomer-op-houmao-interop operator skill folder must be moved to service/isomer-srv-houmao-interop")
    if old_service_dir.exists():
        add(diagnostics, repo_root, old_service_dir, 1, "SVS006", "legacy isomer-op-houmao-interop service folder must be renamed to isomer-srv-houmao-interop")

    skill_dir = repo_root / "skillset" / "service" / HOUMAO_INTEROP_SERVICE_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "SVS006", f"{HOUMAO_INTEROP_SERVICE_SKILL} is required")
        return diagnostics

    lines = read_lines(skill_md)
    text = "\n".join(lines)
    add_split_output_contract_diagnostics(diagnostics, repo_root, skill_md, lines, code="SVS006", require_contract=True)
    for term in HOUMAO_INTEROP_SERVICE_REQUIRED_SKILL_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "SVS006",
                f"{HOUMAO_INTEROP_SERVICE_SKILL} must document '{term}'",
            )

    references_dir = skill_dir / "references"
    allowed_reference_names = set(HOUMAO_INTEROP_SERVICE_SUBCOMMANDS)
    for reference_path in sorted(references_dir.glob("*.md")):
        if reference_path.name not in allowed_reference_names:
            add(
                diagnostics,
                repo_root,
                reference_path,
                1,
                "SVS006",
                f"{HOUMAO_INTEROP_SERVICE_SKILL} has unexpected reference page references/{reference_path.name}",
            )

    for subcommand_file_name in HOUMAO_INTEROP_SERVICE_SUBCOMMANDS:
        subcommand_path = references_dir / subcommand_file_name
        if not subcommand_path.exists():
            add(diagnostics, repo_root, subcommand_path, 1, "SVS006", f"{HOUMAO_INTEROP_SERVICE_SKILL} must include references/{subcommand_file_name}")
            continue
        if f"references/{subcommand_file_name}" not in text:
            add(diagnostics, repo_root, skill_md, first_line_containing(lines, "## Subcommands"), "SVS006", f"{HOUMAO_INTEROP_SERVICE_SKILL} must link references/{subcommand_file_name}")
        subcommand_lines = read_lines(subcommand_path)
        subcommand_text = "\n".join(subcommand_lines)
        for required_term in HOUMAO_INTEROP_SERVICE_REFERENCE_REQUIRED_TERMS.get(subcommand_file_name, ()):
            if required_term not in subcommand_text:
                add(diagnostics, repo_root, subcommand_path, 1, "SVS006", f"references/{subcommand_file_name} must document '{required_term}'")

    for skill_file in sorted(path for path in skill_dir.rglob("*") if path.is_file() and path.suffix in ACTIVE_REF_SUFFIXES):
        for line_number, line in enumerate(read_lines(skill_file), start=1):
            if "isomer-op-houmao-interop" in line:
                add(
                    diagnostics,
                    repo_root,
                    skill_file,
                    line_number,
                    "SVS006",
                    "service Houmao interop guidance must use isomer-srv-houmao-interop",
                )
    return diagnostics


def validate_service_skillset(repo_root: Path) -> list[Diagnostic]:
    diagnostics = validate_simple_skill_layout(
        repo_root / "skillset" / "service",
        repo_root,
        prefix="isomer-srv-",
        code="SVS001",
        manifest_required=False,
    )
    diagnostics.extend(validate_agent_env_setup_service(repo_root))
    diagnostics.extend(validate_houmao_interop_service(repo_root))
    diagnostics.extend(validate_topic_env_setup_service(repo_root))
    diagnostics.extend(
        validate_split_output_contract_docs(
            repo_root,
            (repo_root / "skillset" / "service", repo_root / "skillset" / "misc"),
            code="SVS004",
        )
    )
    diagnostics.extend(validate_global_isomer_cli_invocation(repo_root, (repo_root / "skillset" / "service",), code="SVS005"))
    return sorted(set(diagnostics))


def validate_package_specifics_skill(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    skill_dir = repo_root / "skillset" / "misc" / PACKAGE_SPECIFICS_SKILL
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        add(diagnostics, repo_root, skill_md, 1, "SKL005", f"{PACKAGE_SPECIFICS_SKILL} is required")
        return diagnostics
    lines = read_lines(skill_md)
    text = "\n".join(lines)
    for term in PACKAGE_SPECIFICS_REQUIRED_TERMS:
        if term not in text:
            add(
                diagnostics,
                repo_root,
                skill_md,
                first_line_containing(lines, "# Isomer"),
                "SKL005",
                f"{PACKAGE_SPECIFICS_SKILL} must document '{term}'",
            )
    references_dir = skill_dir / "references"
    if not references_dir.exists():
        add(diagnostics, repo_root, references_dir, 1, "SKL005", f"{PACKAGE_SPECIFICS_SKILL} must include references/")
    else:
        for reference_path in sorted(references_dir.glob("*.md")):
            reference_lines = read_lines(reference_path)
            reference_text = "\n".join(reference_lines)
            for term in ("package source", "variant", "verification", "blocker"):
                if term not in reference_text.lower():
                    add(
                        diagnostics,
                        repo_root,
                        reference_path,
                        first_line_containing(reference_lines, "#"),
                        "SKL005",
                        f"references/{reference_path.name} must document package-specific {term} evidence",
                    )
    return diagnostics


def validate_all(repo_root: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    diagnostics.extend(
        Diagnostic(item.path, item.line, item.code, item.message)
        for item in research_validator.validate_skillset(repo_root / "skillset" / "research-paradigm", repo_root)
    )
    diagnostics.extend(validate_operator_skillset(repo_root))
    diagnostics.extend(validate_service_skillset(repo_root))
    diagnostics.extend(validate_package_specifics_skill(repo_root))
    diagnostics.extend(validate_global_isomer_cli_invocation(repo_root, (repo_root / "skillset" / "misc",), code="SKL004"))
    return sorted(set(diagnostics))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate Isomer skillset namespaces.")
    parser.add_argument(
        "--scope",
        choices=("all", "research", "operator", "service"),
        default="all",
        help="Skillset validation scope.",
    )
    parser.add_argument("--repo-root", type=Path, default=None, help="Repository root for diagnostic paths.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve() if args.repo_root else find_repo_root(Path.cwd())
    if args.scope == "research":
        diagnostics = [
            Diagnostic(item.path, item.line, item.code, item.message)
            for item in research_validator.validate_skillset(repo_root / "skillset" / "research-paradigm", repo_root)
        ]
    elif args.scope == "operator":
        diagnostics = validate_operator_skillset(repo_root)
    elif args.scope == "service":
        diagnostics = validate_service_skillset(repo_root)
    else:
        diagnostics = validate_all(repo_root)
    for diagnostic in diagnostics:
        print(diagnostic.render())
    return 1 if diagnostics else 0


if __name__ == "__main__":
    sys.exit(main())
