"""Topic Service Master identity and binding helpers."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import resolve_project_path
from isomer_labs.models import EffectiveTopicContext, Project


TOPIC_SERVICE_MASTER_NAME_PREFIX = "isomer-tsm-"
TOPIC_SERVICE_MASTER_NAME_MAX_LENGTH = 63
_SLUG_RE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class TopicServiceMasterNames:
    topic_workspace_id: str
    topic_workspace_slug: str | None
    stem: str | None
    specialist_name: str | None
    launch_profile_name: str | None
    managed_agent_name: str | None
    diagnostics: tuple[Diagnostic, ...] = ()

    @property
    def ok(self) -> bool:
        return not any(diagnostic.is_error for diagnostic in self.diagnostics)

    def to_json(self) -> dict[str, object]:
        return {
            "topic_workspace_id": self.topic_workspace_id,
            "topic_workspace_slug": self.topic_workspace_slug,
            "stem": self.stem,
            "specialist_name": self.specialist_name,
            "launch_profile_name": self.launch_profile_name,
            "managed_agent_name": self.managed_agent_name,
            "max_name_length": TOPIC_SERVICE_MASTER_NAME_MAX_LENGTH,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


@dataclass(frozen=True)
class TopicServiceMasterNamesResult:
    ok: bool
    mutated: bool
    project_root: Path
    names: TopicServiceMasterNames
    diagnostics: tuple[Diagnostic, ...]
    research_topic_id: str | None = None
    topic_workspace_path: Path | None = None

    def to_json(self) -> dict[str, object]:
        data = {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            **self.names.to_json(),
        }
        if self.research_topic_id is not None:
            data["research_topic_id"] = self.research_topic_id
        if self.topic_workspace_path is not None:
            data["topic_workspace_path"] = str(self.topic_workspace_path)
        data["suggested_names"] = self.names.to_json()
        data["diagnostics"] = [diagnostic.to_json() for diagnostic in self.diagnostics]
        return data


@dataclass(frozen=True)
class TopicServiceMasterBindingResult:
    ok: bool
    mutated: bool
    project_root: Path
    topic_service_master: dict[str, object]
    diagnostics: tuple[Diagnostic, ...]
    integration_status: str | None = None
    skip_reason: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            "topic_service_master": self.topic_service_master,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }
        if self.integration_status is not None:
            data["integration_status"] = self.integration_status
        if self.skip_reason is not None:
            data["skip_reason"] = self.skip_reason
        return data


def derive_topic_service_master_names(topic_workspace_id: str) -> TopicServiceMasterNames:
    slug = _slug_topic_workspace_id(topic_workspace_id)
    if not slug:
        diagnostic = Diagnostic(
            code="ISO103",
            severity="error",
            concept="Topic Service Master identity",
            field="topic_workspace_id",
            message="Topic Workspace id does not produce a non-empty Topic Service Master name slug.",
        )
        return TopicServiceMasterNames(
            topic_workspace_id=topic_workspace_id,
            topic_workspace_slug=None,
            stem=None,
            specialist_name=None,
            launch_profile_name=None,
            managed_agent_name=None,
            diagnostics=(diagnostic,),
        )
    slug = _bounded_slug(topic_workspace_id, slug)
    stem = f"{TOPIC_SERVICE_MASTER_NAME_PREFIX}{slug}"
    return TopicServiceMasterNames(
        topic_workspace_id=topic_workspace_id,
        topic_workspace_slug=slug,
        stem=stem,
        specialist_name=f"{stem}-specialist",
        launch_profile_name=f"{stem}-profile",
        managed_agent_name=f"{stem}-agent",
    )


def topic_service_master_name_drift(
    *,
    specialist_name: str | None,
    launch_profile_name: str | None,
    managed_agent_name: str | None,
    suggested_names: TopicServiceMasterNames,
) -> dict[str, dict[str, str | None]]:
    if not suggested_names.ok:
        return {}
    expected = {
        "specialist_name": suggested_names.specialist_name,
        "launch_profile_name": suggested_names.launch_profile_name,
        "managed_agent_name": suggested_names.managed_agent_name,
    }
    actual = {
        "specialist_name": specialist_name,
        "launch_profile_name": launch_profile_name,
        "managed_agent_name": managed_agent_name,
    }
    return {
        field: {"expected": expected_value, "actual": actual[field]}
        for field, expected_value in expected.items()
        if actual[field] is not None and actual[field] != expected_value
    }


def resolve_topic_service_master_names(
    project: Project,
    topic_workspace_id: str,
) -> TopicServiceMasterNamesResult:
    diagnostics: list[Diagnostic] = []
    names = derive_topic_service_master_names(topic_workspace_id)
    diagnostics.extend(names.diagnostics)
    workspace = project.manifest.first_workspace(topic_workspace_id)
    topic_id = None
    workspace_path = None
    if workspace is None:
        diagnostics.append(
            Diagnostic(
                code="ISO014",
                severity="error",
                concept="Topic Workspace",
                field="topic_workspace_id",
                message=f"Topic Workspace is not registered by the Project Manifest: {topic_workspace_id}.",
            )
        )
    else:
        topic_id = workspace.research_topic_id
        if workspace.path_input is not None:
            workspace_path = resolve_project_path(project.root, workspace.path_input)
    return TopicServiceMasterNamesResult(
        not has_errors(diagnostics),
        False,
        project.root,
        names,
        tuple(diagnostics),
        research_topic_id=topic_id,
        topic_workspace_path=workspace_path,
    )


def topic_service_master_identity_for_context(
    context: EffectiveTopicContext,
) -> tuple[dict[str, object], list[Diagnostic]]:
    from isomer_labs.workspace.manifest import load_topic_workspace_manifest

    diagnostics: list[Diagnostic] = []
    suggested = derive_topic_service_master_names(context.topic_workspace_id)
    diagnostics.extend(suggested.diagnostics)
    manifest, manifest_diagnostics = load_topic_workspace_manifest(context)
    diagnostics.extend(manifest_diagnostics)
    binding = manifest.topic_service_master
    data: dict[str, object] = {
        "suggested_names": suggested.to_json(),
        "binding": binding.to_json() if binding is not None else None,
        "binding_status": binding.status if binding is not None else "absent",
    }
    if binding is not None and binding.houmao is not None:
        drift = topic_service_master_name_drift(
            specialist_name=binding.houmao.specialist_name,
            launch_profile_name=binding.houmao.launch_profile_name,
            managed_agent_name=binding.houmao.managed_agent_name,
            suggested_names=suggested,
        )
        if drift:
            data["drift"] = drift
    return data, diagnostics


def show_topic_service_master_binding(context: EffectiveTopicContext) -> TopicServiceMasterBindingResult:
    identity, diagnostics = topic_service_master_identity_for_context(context)
    return TopicServiceMasterBindingResult(
        not has_errors(diagnostics),
        False,
        context.project.root,
        identity,
        tuple(diagnostics),
    )


def record_topic_service_master_binding(
    context: EffectiveTopicContext,
    *,
    status: str,
    specialist_name: str | None = None,
    launch_profile_name: str | None = None,
    managed_agent_name: str | None = None,
    specialist_ref: str | None = None,
    launch_profile_ref: str | None = None,
    managed_agent_ref: str | None = None,
    updated_by: str | None = None,
    updated_at: str | None = None,
) -> TopicServiceMasterBindingResult:
    from isomer_labs.workspace.manifest import record_topic_service_master_binding as write_binding

    diagnostics: list[Diagnostic] = []
    if status in {"blocked", "skipped"}:
        skipped_identity, identity_diagnostics = topic_service_master_identity_for_context(context)
        diagnostics.extend(identity_diagnostics)
        skipped_identity["record_status"] = status
        skipped_identity["binding_write"] = "skipped"
        return TopicServiceMasterBindingResult(
            not has_errors(diagnostics),
            False,
            context.project.root,
            skipped_identity,
            tuple(diagnostics),
        )
    suggested = derive_topic_service_master_names(context.topic_workspace_id)
    diagnostics.extend(suggested.diagnostics)
    specialist_name = specialist_name or suggested.specialist_name
    launch_profile_name = launch_profile_name or suggested.launch_profile_name
    managed_agent_name = managed_agent_name or suggested.managed_agent_name
    if specialist_name is None or launch_profile_name is None or managed_agent_name is None:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Topic Service Master binding",
                field="names",
                message="Topic Service Master binding record requires specialist, launch profile, and managed agent names.",
            )
        )
        return TopicServiceMasterBindingResult(False, False, context.project.root, {"suggested_names": suggested.to_json(), "binding": None}, tuple(diagnostics))
    manifest, binding, write_diagnostics = write_binding(
        context,
        status=status,
        specialist_name=specialist_name,
        launch_profile_name=launch_profile_name,
        managed_agent_name=managed_agent_name,
        specialist_ref=specialist_ref,
        launch_profile_ref=launch_profile_ref,
        managed_agent_ref=managed_agent_ref,
        updated_by=updated_by,
        prepared_at=updated_at if status == "prepared" else None,
        launched_at=updated_at if status == "launched" else None,
        updated_at=updated_at,
    )
    diagnostics.extend(write_diagnostics)
    recorded_identity: dict[str, object] = {
        "suggested_names": suggested.to_json(),
        "binding": binding.to_json() if binding is not None else None,
        "binding_status": binding.status if binding is not None else "absent",
    }
    if manifest is not None:
        recorded_identity["topic_workspace_manifest"] = str(manifest.path)
    return TopicServiceMasterBindingResult(
        not has_errors(diagnostics),
        not has_errors(diagnostics),
        context.project.root,
        recorded_identity,
        tuple(diagnostics),
    )


def _slug_topic_workspace_id(topic_workspace_id: str) -> str:
    slug = _SLUG_RE.sub("-", topic_workspace_id.lower())
    return slug.strip("-")


def _bounded_slug(topic_workspace_id: str, slug: str) -> str:
    longest_suffix = "-specialist"
    max_stem_length = TOPIC_SERVICE_MASTER_NAME_MAX_LENGTH - len(longest_suffix)
    max_slug_length = max_stem_length - len(TOPIC_SERVICE_MASTER_NAME_PREFIX)
    if len(slug) <= max_slug_length:
        return slug
    hash_suffix = sha256(topic_workspace_id.encode("utf-8")).hexdigest()[:8]
    hash_part = f"-{hash_suffix}"
    prefix_length = max(1, max_slug_length - len(hash_part))
    return f"{slug[:prefix_length].rstrip('-')}{hash_part}"
