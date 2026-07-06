"""Semantic Project Explorer read helpers for the local web API."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext, Project, ProjectState, SelectionRequest
from isomer_labs.project.context import resolve_effective_topic_context


GRAPH_SCOPES = ("idea-lineage", "artifact-overview", "experiment-records", "paper-revisions")


class ProjectExplorerHost(Protocol):
    """Minimal host interface used by Project Explorer helpers."""

    @property
    def project_root(self) -> Path: ...

    @property
    def selected_env(self) -> Mapping[str, str]: ...

    def project_state(self) -> tuple[Project | None, ProjectState | None, list[Diagnostic]]: ...

    def record_viewer_descriptor(self, topic_id: str, record_id: str) -> dict[str, Any]: ...

    def record_file_content(self, topic_id: str, record_id: str, file_id: str) -> dict[str, Any]: ...


def project_explorer_payload(
    host: ProjectExplorerHost,
    *,
    expanded_topic_ids: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Return the semantic Project Explorer tree without reading heavy content."""

    return _ProjectExplorerReadModel(host).project_explorer(expanded_topic_ids=expanded_topic_ids)


def openable_item_descriptor_payload(host: ProjectExplorerHost, openable_item_id: str) -> dict[str, Any]:
    """Resolve a lightweight descriptor for an Explorer item."""

    return _ProjectExplorerReadModel(host).openable_item_descriptor(openable_item_id)


@dataclass(frozen=True)
class _ProjectExplorerReadModel:
    host: ProjectExplorerHost

    def project_explorer(self, *, expanded_topic_ids: tuple[str, ...] = ()) -> dict[str, Any]:
        project, state, diagnostics = self.host.project_state()
        expanded = set(expanded_topic_ids)
        if project is None or state is None:
            return {
                "ok": False,
                "mutated": False,
                "revision": self._explorer_revision(None, (), expanded, diagnostics),
                "root_node_ids": [],
                "nodes": [],
                "descriptors": [],
                "diagnostics": _diagnostics_json(diagnostics),
            }

        nodes: list[dict[str, object]] = []
        root_id = "project"
        topic_group_id = "project:topics"
        diagnostics_count = len(diagnostics)
        self._append_node(
            nodes,
            node_id=root_id,
            parent_id=None,
            label=project.root.name or str(project.root),
            item_kind="project",
            icon_hint="project",
            openable_item_id="project:overview",
            has_children=True,
            children_loaded=True,
            expanded_by_default=True,
            diagnostics_count=diagnostics_count,
            metadata={"root": str(project.root)},
        )
        self._append_node(
            nodes,
            node_id="project:manifest",
            parent_id=root_id,
            label="Project Manifest",
            item_kind="project_manifest",
            icon_hint="manifest",
            openable_item_id="project:manifest",
            metadata={"path": str(project.manifest_path)},
        )
        self._append_node(
            nodes,
            node_id=topic_group_id,
            parent_id=root_id,
            label="Research Topics",
            item_kind="research_topics",
            icon_hint="topics",
            has_children=True,
            children_loaded=True,
            expanded_by_default=True,
            badge_text=str(len(project.manifest.research_topics)),
        )
        if diagnostics_count:
            self._append_node(
                nodes,
                node_id="project:diagnostics",
                parent_id=root_id,
                label="Diagnostics",
                item_kind="diagnostics",
                icon_hint="diagnostics",
                openable_item_id="project:diagnostics",
                diagnostics_count=diagnostics_count,
                badge_text=str(diagnostics_count),
            )

        for topic in project.manifest.research_topics:
            topic_diagnostics: list[Diagnostic] = []
            context, context_diagnostics = resolve_effective_topic_context(
                state,
                SelectionRequest(research_topic_id=topic.id),
                cwd=project.root,
                env=self.host.selected_env,
            )
            topic_diagnostics.extend(context_diagnostics)
            expanded_topic = topic.id in expanded
            topic_statement = None
            if context is not None and context.research_topic_config is not None:
                topic_statement = context.research_topic_config.topic_statement
            topic_node_id = f"topic:{topic.id}"
            self._append_node(
                nodes,
                node_id=topic_node_id,
                parent_id=topic_group_id,
                label=topic.id,
                item_kind="research_topic",
                icon_hint="topic",
                openable_item_id=f"topic:{topic.id}:overview",
                topic_id=topic.id,
                has_children=True,
                children_loaded=expanded_topic,
                expanded_by_default=False,
                badge_text=topic.status,
                diagnostics_count=len(topic_diagnostics),
                metadata={
                    "topic_workspace_id": topic.topic_workspace_id,
                    "topic_workspace_path": str(context.topic_workspace_path) if context is not None else None,
                    "topic_statement": topic_statement,
                    "status": topic.status,
                },
            )
            if expanded_topic and context is not None:
                self._append_topic_children(nodes, context, topic_node_id, len(topic_diagnostics))

        return {
            "ok": not has_errors(diagnostics),
            "mutated": False,
            "revision": self._explorer_revision(project, project.manifest.research_topics, expanded, diagnostics),
            "root_node_ids": [root_id],
            "nodes": nodes,
            "descriptors": [],
            "diagnostics": _diagnostics_json(diagnostics),
        }

    def openable_item_descriptor(self, openable_item_id: str) -> dict[str, Any]:
        project, state, diagnostics = self.host.project_state()
        if project is None or state is None:
            return {
                "ok": False,
                "mutated": False,
                "openable_item_id": openable_item_id,
                "item_kind": "unknown",
                "exists": False,
                "error": {"code": "project_not_found", "message": "The Project could not be discovered."},
                "diagnostics": _diagnostics_json(diagnostics),
            }
        if openable_item_id in {"project:overview", "project:manifest", "project:diagnostics"}:
            return {
                "ok": not has_errors(diagnostics),
                "mutated": False,
                "openable_item_id": openable_item_id,
                "tab_id": openable_item_id.replace(":", "-"),
                "item_kind": openable_item_id.split(":")[1],
                "title": {
                    "project:overview": "Project Overview",
                    "project:manifest": "Project Manifest",
                    "project:diagnostics": "Project Diagnostics",
                }[openable_item_id],
                "preferred_tab_component": {
                    "project:overview": "projectOverview",
                    "project:manifest": "projectOverview",
                    "project:diagnostics": "diagnostics",
                }[openable_item_id],
                "detail_urls": {"project": "/api/project"},
                "exists": True,
                "diagnostics": _diagnostics_json(diagnostics),
            }

        parts = openable_item_id.split(":")
        if len(parts) < 3:
            return self._unknown_openable(openable_item_id, diagnostics)
        if parts[0] == "file" and len(parts) >= 4:
            topic_id = parts[1]
            record_id = parts[2]
            file_id = ":".join(parts[3:])
            return self._file_openable_descriptor(topic_id, record_id, file_id)
        if parts[0] == "record" and len(parts) >= 3:
            topic_id = parts[1]
            record_id = ":".join(parts[2:])
            return self._record_openable_descriptor(topic_id, record_id)
        if parts[0] != "topic":
            return self._unknown_openable(openable_item_id, diagnostics)

        topic_id = parts[1]
        target = parts[2]
        context, context_diagnostics = resolve_effective_topic_context(
            state,
            SelectionRequest(research_topic_id=topic_id),
            cwd=project.root,
            env=self.host.selected_env,
        )
        diagnostics.extend(context_diagnostics)
        if context is None:
            return {
                "ok": False,
                "mutated": False,
                "openable_item_id": openable_item_id,
                "item_kind": target,
                "topic_id": topic_id,
                "exists": False,
                "error": {"code": "topic_not_found", "message": f"Research Topic is not available: {topic_id}"},
                "diagnostics": _diagnostics_json(diagnostics),
            }

        if target == "graph" and len(parts) == 4:
            graph_scope = parts[3]
            if graph_scope not in GRAPH_SCOPES:
                return {
                    "ok": False,
                    "mutated": False,
                    "openable_item_id": openable_item_id,
                    "item_kind": "graph",
                    "topic_id": topic_id,
                    "graph_scope": graph_scope,
                    "exists": False,
                    "error": {"code": "unsupported_graph_scope", "message": f"Unsupported graph scope: {graph_scope}"},
                    "diagnostics": _diagnostics_json(diagnostics),
                }
            return self._openable_descriptor(
                openable_item_id=openable_item_id,
                tab_id=f"topic-{topic_id}-graph-{graph_scope}",
                item_kind="graph",
                title=f"{_graph_scope_label(graph_scope)} Graph",
                preferred_tab_component="ideaGraph" if graph_scope == "idea-lineage" else "denseGraph",
                topic_id=topic_id,
                graph_scope=graph_scope,
                detail_urls={"graph": f"/api/topics/{topic_id}/graphs/{graph_scope}"},
                diagnostics=diagnostics,
            )

        mapping = {
            "overview": ("topic_overview", f"topic-{topic_id}-overview", "topicOverview", "Topic Overview", {"topic": f"/api/topics/{topic_id}"}),
            "records": ("record_collection", f"topic-{topic_id}-records", "records", "Records", {"records": f"/api/topics/{topic_id}/records"}),
            "runtime": ("runtime", f"topic-{topic_id}-runtime", "runtime", "Runtime", {"runtime": f"/api/topics/{topic_id}/runtime"}),
            "actors": ("topic_actors", f"topic-{topic_id}-actors", "actors", "Topic Actors", {"actors": f"/api/topics/{topic_id}/actors"}),
            "repositories": ("repositories", f"topic-{topic_id}-repositories", "repository", "Repositories", {"topic": f"/api/topics/{topic_id}"}),
            "diagnostics": ("diagnostics", f"topic-{topic_id}-diagnostics", "diagnostics", "Diagnostics", {"topic": f"/api/topics/{topic_id}"}),
        }
        selected = mapping.get(target)
        if selected is None:
            return self._unknown_openable(openable_item_id, diagnostics)
        item_kind, tab_id, component, title, detail_urls = selected
        return self._openable_descriptor(
            openable_item_id=openable_item_id,
            tab_id=tab_id,
            item_kind=item_kind,
            title=title,
            preferred_tab_component=component,
            topic_id=topic_id,
            detail_urls=detail_urls,
            diagnostics=diagnostics,
        )

    def _append_topic_children(
        self,
        nodes: list[dict[str, object]],
        context: EffectiveTopicContext,
        parent_id: str,
        diagnostics_count: int,
    ) -> None:
        topic_id = context.research_topic.id
        self._append_node(
            nodes,
            node_id=f"topic:{topic_id}:overview",
            parent_id=parent_id,
            label="Overview",
            item_kind="topic_overview",
            icon_hint="overview",
            openable_item_id=f"topic:{topic_id}:overview",
            topic_id=topic_id,
        )
        graph_group_id = f"topic:{topic_id}:graphs"
        self._append_node(
            nodes,
            node_id=graph_group_id,
            parent_id=parent_id,
            label="Graphs",
            item_kind="graph_collection",
            icon_hint="graph",
            has_children=True,
            children_loaded=True,
        )
        for graph_scope in GRAPH_SCOPES:
            self._append_node(
                nodes,
                node_id=f"topic:{topic_id}:graph:{graph_scope}",
                parent_id=graph_group_id,
                label=_graph_scope_label(graph_scope),
                item_kind="graph",
                icon_hint="graph",
                openable_item_id=f"topic:{topic_id}:graph:{graph_scope}",
                topic_id=topic_id,
                metadata={"graph_scope": graph_scope},
            )
        for target, label, item_kind, icon in (
            ("records", "Records", "record_collection", "records"),
            ("runtime", "Workspace Runtime", "runtime", "runtime"),
            ("actors", "Topic Actors", "topic_actors", "actors"),
            ("repositories", "Repositories", "repositories", "repository"),
        ):
            self._append_node(
                nodes,
                node_id=f"topic:{topic_id}:{target}",
                parent_id=parent_id,
                label=label,
                item_kind=item_kind,
                icon_hint=icon,
                openable_item_id=f"topic:{topic_id}:{target}",
                topic_id=topic_id,
            )
        if diagnostics_count:
            self._append_node(
                nodes,
                node_id=f"topic:{topic_id}:diagnostics",
                parent_id=parent_id,
                label="Diagnostics",
                item_kind="diagnostics",
                icon_hint="diagnostics",
                openable_item_id=f"topic:{topic_id}:diagnostics",
                topic_id=topic_id,
                diagnostics_count=diagnostics_count,
                badge_text=str(diagnostics_count),
            )

    def _append_node(
        self,
        nodes: list[dict[str, object]],
        *,
        node_id: str,
        parent_id: str | None,
        label: str,
        item_kind: str,
        icon_hint: str,
        openable_item_id: str | None = None,
        topic_id: str | None = None,
        badge_text: str | None = None,
        diagnostics_count: int = 0,
        has_children: bool = False,
        children_loaded: bool = False,
        expanded_by_default: bool = False,
        metadata: Mapping[str, object] | None = None,
    ) -> None:
        nodes.append(
            {
                "id": node_id,
                "parent_id": parent_id,
                "label": label,
                "item_kind": item_kind,
                "icon_hint": icon_hint,
                "badge_text": badge_text,
                "diagnostics_count": diagnostics_count,
                "warning": diagnostics_count > 0,
                "openability_state": "openable" if openable_item_id is not None else "group",
                "openable_item_id": openable_item_id,
                "topic_id": topic_id,
                "has_children": has_children,
                "children_loaded": children_loaded,
                "expanded_by_default": expanded_by_default,
                "metadata": dict(metadata or {}),
            }
        )

    def _explorer_revision(
        self,
        project: Project | None,
        topics: Iterable[object],
        expanded_topic_ids: set[str],
        diagnostics: list[Diagnostic],
    ) -> str:
        payload = {
            "project_root": str(project.root) if project is not None else str(self.host.project_root),
            "manifest": project.manifest.to_json() if project is not None else None,
            "topics": [getattr(topic, "id", str(topic)) for topic in topics],
            "expanded_topic_ids": sorted(expanded_topic_ids),
            "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return f"pexp:{hashlib.sha256(encoded.encode('utf-8')).hexdigest()[:20]}"

    def _openable_descriptor(
        self,
        *,
        openable_item_id: str,
        tab_id: str,
        item_kind: str,
        title: str,
        preferred_tab_component: str,
        diagnostics: list[Diagnostic],
        topic_id: str | None = None,
        graph_scope: str | None = None,
        record_id: str | None = None,
        content_url: str | None = None,
        detail_urls: Mapping[str, str] | None = None,
        media_type: str | None = None,
    ) -> dict[str, Any]:
        return {
            "ok": not has_errors(diagnostics),
            "mutated": False,
            "openable_item_id": openable_item_id,
            "tab_id": tab_id,
            "item_kind": item_kind,
            "title": title,
            "preferred_tab_component": preferred_tab_component,
            "topic_id": topic_id,
            "record_id": record_id,
            "graph_scope": graph_scope,
            "content_url": content_url,
            "detail_urls": dict(detail_urls or {}),
            "media_type": media_type,
            "exists": True,
            "diagnostics": _diagnostics_json(diagnostics),
        }

    def _record_openable_descriptor(self, topic_id: str, record_id: str) -> dict[str, Any]:
        descriptor = self.host.record_viewer_descriptor(topic_id, record_id)
        if not descriptor.get("ok"):
            return {
                **descriptor,
                "openable_item_id": f"record:{topic_id}:{record_id}",
                "tab_id": f"topic-{topic_id}-record-{record_id}",
                "item_kind": "record",
                "preferred_tab_component": "recordDetail",
                "content_url": descriptor.get("primary_content_url"),
                "detail_urls": {
                    "detail": str(descriptor.get("detail_url") or ""),
                    "render": str(descriptor.get("render_url") or ""),
                    "files": str(descriptor.get("files_url") or ""),
                    "facets": str(descriptor.get("facets_url") or ""),
                },
            }
        return {
            "ok": True,
            "mutated": False,
            "openable_item_id": f"record:{topic_id}:{record_id}",
            "tab_id": f"topic-{topic_id}-record-{record_id}",
            "item_kind": "record",
            "title": descriptor.get("title") or record_id,
            "preferred_tab_component": "recordDetail",
            "topic_id": topic_id,
            "record_id": record_id,
            "content_url": descriptor.get("primary_content_url"),
            "detail_urls": {
                "detail": str(descriptor.get("detail_url") or ""),
                "render": str(descriptor.get("render_url") or ""),
                "files": str(descriptor.get("files_url") or ""),
                "facets": str(descriptor.get("facets_url") or ""),
            },
            "media_type": descriptor.get("media_type"),
            "viewer_kind": descriptor.get("viewer_kind"),
            "exists": True,
            "diagnostics": descriptor.get("diagnostics", []),
        }

    def _file_openable_descriptor(self, topic_id: str, record_id: str, file_id: str) -> dict[str, Any]:
        content = self.host.record_file_content(topic_id, record_id, file_id)
        if not content.get("ok"):
            return {
                **content,
                "openable_item_id": f"file:{topic_id}:{record_id}:{file_id}",
                "tab_id": f"topic-{topic_id}-record-{record_id}-file-{file_id}",
                "item_kind": "referenced_artifact",
                "preferred_tab_component": "fileArtifact",
                "content_url": None,
                "detail_urls": {"files": f"/api/topics/{topic_id}/records/{record_id}/files"},
            }
        content_url = f"/api/topics/{topic_id}/records/{record_id}/files/{file_id}/content"
        return {
            "ok": True,
            "mutated": False,
            "openable_item_id": f"file:{topic_id}:{record_id}:{file_id}",
            "tab_id": f"topic-{topic_id}-record-{record_id}-file-{file_id}",
            "item_kind": "referenced_artifact",
            "title": file_id,
            "preferred_tab_component": "fileArtifact",
            "topic_id": topic_id,
            "record_id": record_id,
            "content_url": content_url,
            "detail_urls": {"content": content_url, "files": f"/api/topics/{topic_id}/records/{record_id}/files"},
            "media_type": content.get("media_type"),
            "exists": True,
            "diagnostics": content.get("diagnostics", []),
        }

    def _unknown_openable(self, openable_item_id: str, diagnostics: list[Diagnostic]) -> dict[str, Any]:
        return {
            "ok": False,
            "mutated": False,
            "openable_item_id": openable_item_id,
            "item_kind": "unknown",
            "exists": False,
            "error": {"code": "openable_item_not_found", "message": f"Openable item is not known: {openable_item_id}"},
            "diagnostics": _diagnostics_json(diagnostics),
        }


def _diagnostics_json(diagnostics: list[Diagnostic]) -> list[dict[str, object]]:
    return [diagnostic.to_json() for diagnostic in diagnostics]


def _graph_scope_label(scope: str) -> str:
    return {
        "idea-lineage": "Idea Lineage",
        "artifact-overview": "Artifact Overview",
        "experiment-records": "Experiment Records",
        "paper-revisions": "Paper Revisions",
    }.get(scope, scope)
