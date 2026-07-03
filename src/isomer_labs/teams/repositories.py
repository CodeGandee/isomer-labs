"""Team Repository manifest loading."""

from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import Any, Mapping

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import (
    DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION,
    TEAM_REPOSITORY_MANIFEST_SCHEMA_VERSION,
    DomainAgentTeamTemplateRegistration,
    Project,
    TeamRepositoryRegistration,
)
from isomer_labs.core.path_utils import canonicalize, is_within, resolve_project_path
from isomer_labs.core.toml_loader import load_toml


TEAM_REPOSITORY_MANIFEST_NAME = "isomer-team-repo.toml"
TEAM_REPOSITORIES_ENV = "ISOMER_TEAM_REPOSITORIES"


@dataclass(frozen=True)
class TeamRepository:
    id: str
    root: Path
    manifest_path: Path
    schema_version: str
    status: str
    templates: list[DomainAgentTeamTemplateRegistration] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(diagnostic.severity == "error" for diagnostic in self.diagnostics)

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "root": str(self.root),
            "manifest_path": str(self.manifest_path),
            "schema_version": self.schema_version,
            "status": self.status,
            "ok": self.ok,
            "templates": [template.to_json() for template in self.templates],
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


def discover_team_repositories(project: Project | None = None, env: Mapping[str, str] | None = None) -> list[TeamRepository]:
    env = env or os.environ
    repositories: list[TeamRepository] = []
    seen_roots: set[Path] = set()
    for registration in _team_repository_registrations(project, env):
        if registration.status == "archived":
            continue
        root = _resolve_team_repository_root(project, registration)
        if root in seen_roots:
            continue
        seen_roots.add(root)
        repositories.append(load_team_repository(root, configured_id=registration.id))
    return repositories


def discover_team_repository_templates(project: Project | None = None, env: Mapping[str, str] | None = None) -> list[DomainAgentTeamTemplateRegistration]:
    templates: list[DomainAgentTeamTemplateRegistration] = []
    seen: set[str] = set()
    for repository in discover_team_repositories(project, env):
        for template in repository.templates:
            if template.status == "archived" or template.id in seen:
                continue
            seen.add(template.id)
            templates.append(template)
    return templates


def load_team_repository(root: Path, *, configured_id: str | None = None) -> TeamRepository:
    repo_root = canonicalize(root)
    manifest_path = repo_root / TEAM_REPOSITORY_MANIFEST_NAME
    raw, diagnostics = load_toml(manifest_path, "Team Repository manifest")
    if raw is None:
        return TeamRepository(
            id=configured_id or repo_root.name,
            root=repo_root,
            manifest_path=manifest_path,
            schema_version=TEAM_REPOSITORY_MANIFEST_SCHEMA_VERSION,
            status="invalid",
            diagnostics=diagnostics,
        )
    repository_id = _first_string(raw, ("id", "team_repository_id", "repository_id")) or configured_id or repo_root.name
    schema_version = _first_string(raw, ("schema_version", "manifest_schema_version")) or TEAM_REPOSITORY_MANIFEST_SCHEMA_VERSION
    status = _first_string(raw, ("status",)) or "active"
    templates = _parse_repository_templates(repository_id, repo_root, manifest_path, raw, diagnostics)
    return TeamRepository(
        id=repository_id,
        root=repo_root,
        manifest_path=manifest_path,
        schema_version=schema_version,
        status=status,
        templates=templates,
        diagnostics=diagnostics,
    )


def _team_repository_registrations(project: Project | None, env: Mapping[str, str]) -> list[TeamRepositoryRegistration]:
    registrations: list[TeamRepositoryRegistration] = []
    if project is not None:
        registrations.extend(project.manifest.team_repositories)
    for index, root in enumerate(_env_repository_roots(env)):
        registrations.append(
            TeamRepositoryRegistration(
                id=f"env:{index}",
                path_input=root,
                schema_version=TEAM_REPOSITORY_MANIFEST_SCHEMA_VERSION,
                status="active",
                source_path=Path.cwd(),
            )
        )
    return registrations


def _resolve_team_repository_root(project: Project | None, registration: TeamRepositoryRegistration) -> Path:
    if project is None:
        return canonicalize(Path(registration.path_input))
    return resolve_project_path(project.root, registration.path_input)


def _env_repository_roots(env: Mapping[str, str]) -> list[str]:
    value = env.get(TEAM_REPOSITORIES_ENV, "")
    return [item for item in value.split(os.pathsep) if item]


def _parse_repository_templates(
    repository_id: str,
    repo_root: Path,
    manifest_path: Path,
    raw: dict[str, Any],
    diagnostics: list[Diagnostic],
) -> list[DomainAgentTeamTemplateRegistration]:
    templates: list[DomainAgentTeamTemplateRegistration] = []
    for index, item in enumerate(_table_items(raw.get("domain_agent_team_templates"))):
        field = f"domain_agent_team_templates[{index}]"
        template_id = _first_string(item, ("id", "domain_agent_team_template_id", "template_id", "ref"))
        source_path_input = _first_string(item, ("path", "source_path", "template_path", "execplan_path", "source"))
        if template_id is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Team Repository manifest",
                    path=manifest_path,
                    field=f"{field}.id",
                    message="Team Repository template entry must include an id.",
                )
            )
            continue
        if source_path_input is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO003",
                    severity="error",
                    concept="Team Repository manifest",
                    path=manifest_path,
                    field=f"{field}.path",
                    message="Team Repository template entry must include a path.",
                )
            )
            continue
        template_path = canonicalize(repo_root / source_path_input)
        if not is_within(template_path, repo_root):
            diagnostics.append(
                Diagnostic(
                    code="ISO016",
                    severity="error",
                    concept="Team Repository manifest",
                    path=manifest_path,
                    field=f"{field}.path",
                    message="Team Repository template path resolves outside the Team Repository root.",
                )
            )
            continue
        templates.append(
            DomainAgentTeamTemplateRegistration(
                id=template_id,
                source_path_input=str(template_path),
                source_kind="team-repository",
                schema_version=_first_string(item, ("schema_version",)) or DOMAIN_AGENT_TEAM_TEMPLATE_REF_SCHEMA_VERSION,
                status=_first_string(item, ("status",)) or "active",
                source_path=manifest_path,
                team_repository_id=repository_id,
                team_repository_source_path=repo_root,
            )
        )
    return templates


def _table_items(value: object) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        if all(isinstance(item, dict) for item in value.values()):
            items: list[dict[str, Any]] = []
            for key, item in value.items():
                copied = dict(item)
                copied.setdefault("id", key)
                items.append(copied)
            return items
        return [value]
    return []


def _first_string(data: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return None
