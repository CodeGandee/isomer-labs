"""Self-contained Kaoju wiki export, viewer deployment, and governed launch."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from importlib import resources
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import socket
import sys
import tempfile
from typing import Mapping, Sequence
import uuid

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from isomer_labs.kaoju.artifacts import KaojuArtifactService, KaojuServiceError
from isomer_labs.kaoju.execution import ExecutionAdapterCommandRequest, command_environment, execute_command_request
from isomer_labs.kaoju.runs import KaojuRunService
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.index import query_index_list
from isomer_labs.records.store import ResearchRecordRequest, create_record, show_record


WIKI_SCHEMA_VERSION = "isomer-kaoju-wiki-export-manifest.v1"
VIEWER_SCHEMA_VERSION = "isomer-kaoju-wiki-viewer-manifest.v1"
WIKI_MARKER = ".kaoju-wiki-managed.json"
VIEWER_MARKER = ".kaoju-viewer-managed.json"
VIEWER_ASSETS = ("index.html", "styles.css", "app.js")
WIKI_SEMANTICS = {
    "kaoju:llm-wiki-export",
    "kaoju:llm-wiki-metadata",
    "kaoju:llm-wiki-viewer",
    "kaoju:llm-wiki-viewer-manifest",
}
WIKI_ACCEPTED_STATUSES = {"active", "complete", "ready", "supported"}


@dataclass(frozen=True)
class ManagedUpdate:
    """One deterministic in-place managed-file update result."""

    created: tuple[str, ...]
    changed: tuple[str, ...]
    unchanged: tuple[str, ...]
    stale: tuple[str, ...]
    removed: tuple[str, ...]

    @property
    def mutated(self) -> bool:
        return bool(self.created or self.changed or self.removed)

    def to_json(self) -> dict[str, list[str]]:
        return {
            "created": list(self.created),
            "changed": list(self.changed),
            "unchanged": list(self.unchanged),
            "stale": list(self.stale),
            "removed": list(self.removed),
        }


class KaojuWikiService:
    """Export accepted records without external skill or viewer dependencies."""

    def __init__(self, context: EffectiveTopicContext, *, env: Mapping[str, str], cwd: Path) -> None:
        self.context = context
        self.env = env
        self.cwd = cwd
        self.artifacts = KaojuArtifactService(context, env=env, cwd=cwd)
        self.runs = KaojuRunService(context, env=env, cwd=cwd)

    def export(
        self,
        *,
        artifact_refs: Sequence[str],
        direction_scope: str | None,
        paper_scope: str | None,
        target: Path | None,
        target_policy: str,
    ) -> dict[str, object]:
        if target_policy not in {"create", "update"}:
            raise KaojuServiceError("wiki_target_policy_invalid", "Wiki target policy must be create or update.")
        records, selection = self._select_records(artifact_refs, direction_scope=direction_scope, paper_scope=paper_scope)
        if not records:
            raise KaojuServiceError("wiki_selection_empty", "No accepted Kaoju Artifacts matched the selected state-DB scope.")
        scope_name = direction_scope or paper_scope or "topic"
        selected_target = target.resolve(strict=False) if target is not None else self.context.topic_workspace_path / "exports" / "kaoju-wiki" / _slug(scope_name)
        prior = _load_managed_state(selected_target, WIKI_MARKER, expected_schema="isomer-kaoju-wiki-managed.v1")
        if selected_target.exists() and any(selected_target.iterdir()) and prior is None:
            raise KaojuServiceError("wiki_target_unrecognized", f"Non-empty wiki target is not recognized: {selected_target}", ("Choose another target or explicitly clear it outside this command.",))
        if selected_target.exists() and target_policy == "create":
            raise KaojuServiceError("wiki_target_exists", f"Wiki target already exists: {selected_target}", ("Use update or choose another target.",))

        source_fingerprint = _fingerprint_records(records)
        prior_manifest = _try_json(selected_target / "wiki.json") if prior is not None else None
        if prior_manifest is not None and prior_manifest.get("source_fingerprint") == source_fingerprint:
            prior_files = prior.get("files") if prior is not None else None
            paths = tuple(sorted(str(path) for path in prior_files)) if isinstance(prior_files, dict) else ()
            update = ManagedUpdate((), (), paths, (), ())
            export_ref = self._latest_ref("kaoju:llm-wiki-export", _target_scope(selected_target))
            metadata_ref = self._latest_ref("kaoju:llm-wiki-metadata", _target_scope(selected_target))
            return {"ok": True, "mutated": False, "operation": "wiki.export", "target": str(selected_target), "source_fingerprint": source_fingerprint, "export_ref": export_ref, "metadata_ref": metadata_ref, "changelog": update.to_json(), "affected_refs": []}

        page_files: dict[str, bytes] = {}
        artifact_entries: list[dict[str, object]] = []
        page_entries: list[dict[str, object]] = []
        relationships: list[dict[str, object]] = []
        for record in records:
            record_id = str(record["id"])
            semantic_id = _semantic_id(record)
            scope_key = _metadata(record).get("scope_key")
            page_path = f"pages/{_slug(semantic_id.removeprefix('kaoju:'))}/{_slug(str(scope_key or record_id))}.md"
            page_text, page_title = self._render_record(record)
            encoded = page_text.encode("utf-8")
            page_files[page_path] = encoded
            page_checksum = _checksum_bytes(encoded)
            artifact_content = _metadata(record).get("artifact_content")
            artifact_checksum = str(artifact_content.get("checksum") or "") if isinstance(artifact_content, dict) else ""
            artifact_entries.append({"record_id": record_id, "semantic_id": semantic_id, "scope_key": scope_key, "revision": record.get("updated_at"), "checksum": artifact_checksum, "page": page_path, "status": record.get("status")})
            page_entries.append({"path": page_path, "title": page_title, "checksum": page_checksum, "artifact_refs": [record_id]})
            relationships.extend(_record_relationships(record_id, _metadata(record).get("relationships")))

        preliminary = {**page_files, "wiki.json": b""}
        predicted = _predict_update(selected_target, preliminary, prior)
        manifest = {
            "schema_version": WIKI_SCHEMA_VERSION,
            "title": "Kaoju survey wiki metadata",
            "summary": "Canonical mapping from accepted Topic Workspace records to self-contained wiki pages.",
            "artifact_family": "kaoju",
            "semantic_id": "kaoju:llm-wiki-metadata",
            "artifact_type": "llm-wiki-metadata",
            "version": "v1",
            "source_fingerprint": source_fingerprint,
            "sections": {
                "topic": {"research_topic_id": self.context.research_topic.id, "topic_workspace_id": self.context.topic_workspace_id},
                "artifacts": artifact_entries,
                "pages": page_entries,
                "relationships": relationships,
                "provenance": {"selection": selection, "exporter": "isomer-labs.kaoju.wiki.v1", "state_discovery": "workspace-runtime-query-index"},
                "target": {"path": str(selected_target), "policy": target_policy},
                "changelog": predicted.to_json(),
            },
        }
        _validate_schema(manifest, "schemas/wiki-export.v1.schema.json", "wiki_manifest_invalid")
        files = {**page_files, "wiki.json": _json_bytes(manifest)}
        update = _apply_managed_update(selected_target, files, marker=WIKI_MARKER, marker_schema="isomer-kaoju-wiki-managed.v1", prior=prior)

        target_scope = _target_scope(selected_target)
        accepted_ref = str(records[0]["id"])
        export_result = self._upsert("kaoju:llm-wiki-export", selected_target, target_scope, relationships=_relationships(accepted_artifact=accepted_ref))
        metadata_result = self._upsert("kaoju:llm-wiki-metadata", selected_target / "wiki.json", target_scope, relationships=_relationships(wiki_export=_record_id(export_result), accepted_artifact=accepted_ref))
        return {"ok": True, "mutated": update.mutated, "operation": "wiki.export", "target": str(selected_target), "source_fingerprint": source_fingerprint, "export_ref": _record_id(export_result), "metadata_ref": _record_id(metadata_result), "changelog": update.to_json(), "affected_refs": [_record_id(export_result), _record_id(metadata_result)]}

    def deploy(self, *, wiki_target: Path, target: Path | None, target_policy: str) -> dict[str, object]:
        source = wiki_target.resolve(strict=True)
        wiki_manifest = _load_json(source / "wiki.json", "wiki_manifest_unreadable")
        _validate_schema(wiki_manifest, "schemas/wiki-export.v1.schema.json", "wiki_manifest_invalid")
        source_fingerprint = str(wiki_manifest["source_fingerprint"])
        selected_target = target.resolve(strict=False) if target is not None else self.context.topic_workspace_path / "exports" / "kaoju-wiki-viewer" / _slug(source.name)
        prior = _load_managed_state(selected_target, VIEWER_MARKER, expected_schema="isomer-kaoju-viewer-managed.v1")
        if selected_target.exists() and any(selected_target.iterdir()) and prior is None:
            raise KaojuServiceError("viewer_target_unrecognized", f"Non-empty viewer target is not recognized: {selected_target}", ("Clarify another target or explicitly clear it outside this command.",))
        if target_policy not in {"create", "update"}:
            raise KaojuServiceError("viewer_target_policy_invalid", "Viewer target policy must be create or update.")
        if selected_target.exists() and target_policy == "create":
            raise KaojuServiceError("viewer_target_exists", f"Viewer target already exists: {selected_target}")

        files = _viewer_files()
        data_paths = ["wiki.json", *[str(page["path"]) for page in _object_list(_sections(wiki_manifest).get("pages"))]]
        for relative in data_paths:
            source_file = _safe_join(source, relative)
            if not source_file.is_file():
                raise KaojuServiceError("viewer_wiki_target_stale", f"Wiki target member is missing: {relative}")
            files[f"data/{relative}"] = source_file.read_bytes()
        viewer_checksums = {path: _checksum_bytes(content) for path, content in sorted(files.items())}
        manifest = {
            "schema_version": VIEWER_SCHEMA_VERSION,
            "title": "Kaoju wiki viewer manifest",
            "summary": "Independent package-owned static viewer deployment for one checked Kaoju wiki export.",
            "artifact_family": "kaoju",
            "semantic_id": "kaoju:llm-wiki-viewer-manifest",
            "artifact_type": "llm-wiki-viewer-manifest",
            "version": "v1",
            "sections": {
                "viewer": {"implementation": "isomer-independent-static-viewer", "version": "v1", "files": sorted(files), "checksums": viewer_checksums},
                "wiki_target": {"source_path": str(source), "source_fingerprint": source_fingerprint, "snapshot_path": "data/wiki.json"},
                "launch": {"default_host": "127.0.0.1", "default_port": 8000, "network_exposure_gate": "required-for-non-loopback"},
            },
        }
        _validate_schema(manifest, "schemas/wiki-viewer.v1.schema.json", "viewer_manifest_invalid")
        files["viewer-manifest.json"] = _json_bytes(manifest)
        update = _apply_managed_update(selected_target, files, marker=VIEWER_MARKER, marker_schema="isomer-kaoju-viewer-managed.v1", prior=prior)
        target_scope = _target_scope(selected_target)
        wiki_export_ref = self._latest_ref("kaoju:llm-wiki-export", _target_scope(source)) or f"wiki-target:{source_fingerprint}"
        viewer_result = self._upsert("kaoju:llm-wiki-viewer", selected_target, target_scope, relationships=_relationships(wiki_export=wiki_export_ref))
        manifest_result = self._upsert("kaoju:llm-wiki-viewer-manifest", selected_target / "viewer-manifest.json", target_scope, relationships=_relationships(wiki_viewer=_record_id(viewer_result), wiki_export=wiki_export_ref))
        return {"ok": True, "mutated": update.mutated, "operation": "wiki.deploy", "target": str(selected_target), "viewer_ref": _record_id(viewer_result), "viewer_manifest_ref": _record_id(manifest_result), "source_fingerprint": source_fingerprint, "changelog": update.to_json(), "affected_refs": [_record_id(viewer_result), _record_id(manifest_result)]}

    def start(
        self,
        *,
        viewer_target: Path,
        host: str,
        port: int,
        network_exposure_approved: bool,
        timeout_seconds: float,
        dry_run: bool = False,
    ) -> dict[str, object]:
        target = viewer_target.resolve(strict=True)
        manifest = _load_json(target / "viewer-manifest.json", "viewer_manifest_unreadable")
        _validate_schema(manifest, "schemas/wiki-viewer.v1.schema.json", "viewer_manifest_invalid")
        if not _loopback(host) and not network_exposure_approved:
            raise KaojuServiceError("viewer_network_gate_required", f"Host {host} requires an approved network-exposure Gate.")
        selected_port = _available_port(host, port)
        if selected_port is None:
            raise KaojuServiceError("viewer_port_conflict", f"Viewer port is already in use: {host}:{port}", ("Choose another port or pass 0 for automatic selection.",))
        url_host = "127.0.0.1" if host in {"0.0.0.0", "::"} else host
        url = f"http://{url_host}:{selected_port}/"
        command_preview = [sys.executable, "-m", "isomer_labs.kaoju.viewer_server", "--root", str(target), "--host", host, "--port", str(selected_port)]
        if dry_run:
            return {"ok": True, "mutated": False, "operation": "wiki.start", "dry_run": True, "url": url, "command": command_preview, "network_exposure_gate": "approved" if not _loopback(host) else "not-required", "affected_refs": []}
        run_id = f"run-wiki-viewer-{uuid.uuid4().hex[:12]}"
        begun = self.runs.begin(procedure_id="export-survey-wiki", control_mode="adapter", input_refs=[str(target)], expected_output_refs=[url], stage_id="viewer-launch", run_id=run_id)
        runtime_dir = self.context.topic_workspace_path / "runtime" / "kaoju-viewer"
        runtime_dir.mkdir(parents=True, exist_ok=True)
        pid_file = runtime_dir / f"{run_id}.pid"
        log_file = runtime_dir / f"{run_id}.log"
        request = ExecutionAdapterCommandRequest.create(extension_point="viewer_launch", argv=(*command_preview, "--pid-file", str(pid_file), "--log-file", str(log_file)), cwd=target, timeout_seconds=timeout_seconds, recording_refs=(run_id, str(target)))
        observation = execute_command_request(request, env=command_environment(self.env))
        terminal = "complete" if observation.get("status") == "succeeded" else "failed"
        completed = self.runs.complete(run_id, terminal_status=terminal, completed_refs=[url] if terminal == "complete" else [], blocker_refs=[] if terminal == "complete" else [str(observation.get("request"))], resume_hint=None if terminal == "complete" else "Resolve viewer launch observation and retry.")
        log_ref = self._record_log(run_id, log_file, observation)
        request_value = observation.get("request")
        request_ref = str(request_value.get("id")) if isinstance(request_value, dict) and request_value.get("id") else None
        affected_refs = [run_id, log_ref, *([request_ref] if request_ref is not None else [])]
        return {"ok": terminal == "complete", "mutated": True, "operation": "wiki.start", "url": url, "run_ref": run_id, "research_task_ref": begun.get("research_task_ref"), "log_ref": log_ref, "pid_file": str(pid_file), "observation": observation, "terminal_status": completed.get("terminal_status"), "network_exposure_gate": "approved" if not _loopback(host) else "not-required", "affected_refs": affected_refs}

    def _select_records(self, artifact_refs: Sequence[str], *, direction_scope: str | None, paper_scope: str | None) -> tuple[list[dict[str, object]], dict[str, object]]:
        selected: dict[str, dict[str, object]] = {}
        if artifact_refs:
            for record_id in artifact_refs:
                record = self._accepted_record(record_id)
                selected[record_id] = record
            return [selected[key] for key in sorted(selected)], {"mode": "explicit", "artifact_refs": list(artifact_refs)}
        scopes: list[str] = [scope for scope in (direction_scope, paper_scope) if scope is not None]
        queries: list[str | None] = list(scopes)
        if not queries:
            queries.append(None)
        for scope in queries:
            payload, _diagnostics = query_index_list(self.context, env=self.env, artifact_family="kaoju", scope_key=scope, latest_only=True)
            ambiguous = [diagnostic for diagnostic in _object_list(payload.get("diagnostics")) if diagnostic.get("code") == "query_index_latest_ambiguous"]
            if ambiguous:
                raise KaojuServiceError("wiki_selection_ambiguous", f"Accepted Artifact selection is ambiguous for scope {scope or '<topic>'}.", ("Supply explicit Artifact refs or resolve competing current candidates.",))
            for row in _object_list(payload.get("records")):
                record_id_value = row.get("record_id")
                if isinstance(record_id_value, str) and row.get("status") in WIKI_ACCEPTED_STATUSES:
                    record = self._accepted_record(record_id_value)
                    if _semantic_id(record) not in WIKI_SEMANTICS:
                        selected[record_id_value] = record
        return [selected[key] for key in sorted(selected)], {"mode": "scoped", "direction_scope": direction_scope, "paper_scope": paper_scope}

    def _accepted_record(self, record_id: str) -> dict[str, object]:
        payload, _diagnostics = show_record(self.context, record_id, env=self.env, include_body=True, include_payload=True)
        record = payload.get("record")
        if not isinstance(record, dict):
            raise KaojuServiceError("wiki_artifact_missing", f"Selected Artifact is missing: {record_id}")
        if record.get("status") not in WIKI_ACCEPTED_STATUSES:
            raise KaojuServiceError("wiki_artifact_not_accepted", f"Selected Artifact is not accepted: {record_id}")
        if not _semantic_id(record).startswith("kaoju:"):
            raise KaojuServiceError("wiki_artifact_family_invalid", f"Selected record is not a Kaoju Artifact: {record_id}")
        diagnostics = self.artifacts.content_diagnostics({"record": record})
        if diagnostics:
            raise KaojuServiceError("wiki_artifact_content_stale", f"Selected Artifact content is missing, stale, or corrupt: {record_id}", tuple(str(item.get("message")) for item in diagnostics))
        if not isinstance(record.get("content_path"), str):
            raise KaojuServiceError("wiki_artifact_content_missing", f"Selected Artifact has no authoritative file content: {record_id}")
        return record

    def _render_record(self, record: dict[str, object]) -> tuple[str, str]:
        path = Path(str(record["content_path"]))
        semantic_id = _semantic_id(record)
        title = semantic_id
        body = ""
        if path.name == ".isomer-artifact-manifest.json":
            body = "Directory-backed Artifact. Inspect the registered directory manifest for members and checksums."
        elif path.suffix.casefold() == ".json":
            value = _try_json(path)
            if isinstance(value, dict):
                title = str(value.get("title") or semantic_id)
                summary = str(value.get("summary") or "")
                body = (summary + "\n\n```json\n" + json.dumps(value.get("sections", value), indent=2, sort_keys=True, ensure_ascii=False) + "\n```").strip()
            else:
                body = path.read_text(encoding="utf-8", errors="replace")
        elif path.suffix.casefold() in {".md", ".myst", ".txt", ".log", ".tex"}:
            body = path.read_text(encoding="utf-8", errors="replace")
            first_heading = next(iter(re.finditer(r"(?m)^#\s+(.+)$", body)), None)
            if first_heading is not None:
                title = first_heading.group(1).strip()
        else:
            body = f"Binary Artifact `{path.name}` with checksum `{_artifact_checksum(record)}`."
        provenance = f"> Artifact `{record['id']}` · `{semantic_id}` · revision `{record.get('updated_at')}` · checksum `{_artifact_checksum(record)}`\n\n"
        if body.lstrip().startswith("# "):
            rendered = provenance + body.rstrip() + "\n"
        else:
            rendered = f"# {title}\n\n{provenance}{body.rstrip()}\n"
        return rendered, title

    def _upsert(self, semantic_id: str, content: Path, scope_key: str, *, relationships: list[dict[str, object]]) -> dict[str, object]:
        current = self._latest_ref(semantic_id, scope_key)
        if current is None:
            return self.artifacts.put(semantic_id, content, producer="isomer-kaoju-export", scope_key=scope_key, relationships=relationships)
        return self.artifacts.revise(current, content, producer="isomer-kaoju-export", scope_key=scope_key, relationships=relationships)

    def _latest_ref(self, semantic_id: str, scope_key: str) -> str | None:
        payload = self.artifacts.latest(semantic_id, scope_key=scope_key)
        rows = payload.get("records")
        if not isinstance(rows, list) or not rows or not isinstance(rows[0], dict):
            return None
        value = rows[0].get("record_id")
        return str(value) if value else None

    def _record_log(self, run_id: str, log_file: Path, observation: Mapping[str, object]) -> str:
        if not log_file.is_file():
            log_file.write_text(json.dumps(observation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        log_ref = f"log-wiki-viewer-{uuid.uuid4().hex[:12]}"
        payload, _diagnostics = create_record(self.context, ResearchRecordRequest(record_kind="artifact", record_id=log_ref, status="ready", body_file=log_file, content_name=log_file.name, semantic_label="topic.records.logs", metadata={"artifact_type": "wiki-viewer-launch-log", "run_ref": run_id, "producer": "isomer-kaoju-export"}), env=self.env, cwd=self.cwd)
        if payload.get("ok") is False:
            raise KaojuServiceError("viewer_log_record_failed", "Viewer launch log could not be registered.")
        return log_ref


def _viewer_files() -> dict[str, bytes]:
    root = resources.files("isomer_labs.kaoju").joinpath("viewer_assets")
    result: dict[str, bytes] = {}
    for name in VIEWER_ASSETS:
        item = root.joinpath(name)
        if not item.is_file():
            raise KaojuServiceError("viewer_package_asset_missing", f"Packaged viewer asset is missing: {name}")
        result[name] = item.read_bytes()
    return result


def _validate_schema(value: object, resource: str, code: str) -> None:
    schema_item = resources.files("isomer_labs.kaoju").joinpath(resource)
    schema = json.loads(schema_item.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda error: tuple(str(part) for part in error.path))
    if errors:
        details = tuple(f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}" for error in errors)
        raise KaojuServiceError(code, "Versioned wiki contract validation failed.", details)


def _apply_managed_update(target: Path, files: Mapping[str, bytes], *, marker: str, marker_schema: str, prior: dict[str, object] | None) -> ManagedUpdate:
    update = _predict_update(target, files, prior)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix=f".{target.name}.update-", dir=target.parent))
    try:
        for relative, content in files.items():
            destination = _safe_join(staged, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        for relative in (*update.created, *update.changed):
            destination = _safe_join(target, relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(_safe_join(staged, relative), destination)
        for relative in update.removed:
            _safe_join(target, relative).unlink(missing_ok=True)
        marker_payload = {"schema_version": marker_schema, "files": {path: _checksum_bytes(content) for path, content in sorted(files.items())}}
        marker_staged = staged / marker
        marker_staged.write_bytes(_json_bytes(marker_payload))
        os.replace(marker_staged, target / marker)
        _remove_empty_managed_dirs(target)
    finally:
        if staged.exists():
            shutil.rmtree(staged)
    return update


def _predict_update(target: Path, files: Mapping[str, bytes], prior: dict[str, object] | None) -> ManagedUpdate:
    raw_old = prior.get("files") if isinstance(prior, dict) else None
    old: dict[str, str] = {str(path): str(checksum) for path, checksum in raw_old.items()} if isinstance(raw_old, dict) else {}
    new = {path: _checksum_bytes(content) for path, content in files.items()}
    created = sorted(path for path in new if path not in old)
    changed = sorted(path for path in new if path in old and new[path] != old[path])
    unchanged = sorted(path for path in new if path in old and new[path] == old[path])
    stale = sorted(path for path in old if path not in new)
    return ManagedUpdate(tuple(created), tuple(changed), tuple(unchanged), tuple(stale), tuple(stale))


def _load_managed_state(target: Path, marker: str, *, expected_schema: str) -> dict[str, object] | None:
    marker_path = target / marker
    value = _try_json(marker_path)
    if not isinstance(value, dict) or value.get("schema_version") != expected_schema or not isinstance(value.get("files"), dict):
        return None
    return value


def _record_relationships(record_id: str, value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [{"source_record_id": record_id, **item} for item in value if isinstance(item, dict)]


def _fingerprint_records(records: Sequence[Mapping[str, object]]) -> str:
    values = [{"record_id": record.get("id"), "semantic_id": _semantic_id(record), "revision": record.get("updated_at"), "checksum": _artifact_checksum(record), "scope_key": _metadata(record).get("scope_key")} for record in records]
    return _checksum_bytes(json.dumps(values, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def _artifact_checksum(record: Mapping[str, object]) -> str:
    content = _metadata(record).get("artifact_content")
    return str(content.get("checksum") or "") if isinstance(content, dict) else ""


def _metadata(record: Mapping[str, object]) -> dict[str, object]:
    value = record.get("transition_metadata")
    return value if isinstance(value, dict) else {}


def _semantic_id(record: Mapping[str, object]) -> str:
    return str(_metadata(record).get("semantic_id") or "")


def _sections(manifest: Mapping[str, object]) -> dict[str, object]:
    value = manifest.get("sections")
    return value if isinstance(value, dict) else {}


def _relationships(**values: str) -> list[dict[str, object]]:
    return [{"role": role, "target_ref": target} for role, target in values.items()]


def _record_id(payload: Mapping[str, object]) -> str:
    record = payload.get("record")
    if isinstance(record, dict) and isinstance(record.get("id"), str):
        return record["id"]
    refs = payload.get("affected_refs")
    if isinstance(refs, list) and refs:
        return str(refs[0])
    raise KaojuServiceError("wiki_record_ref_missing", "Artifact service did not return a stable record ref.")


def _target_scope(target: Path) -> str:
    return "export-target:" + hashlib.sha256(str(target.resolve(strict=False)).encode("utf-8")).hexdigest()[:20]


def _available_port(host: str, requested: int) -> int | None:
    if requested < 0 or requested > 65535:
        raise KaojuServiceError("viewer_port_invalid", "Viewer port must be between 0 and 65535.")
    try:
        with socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM) as candidate:
            candidate.bind((host, requested))
            return int(candidate.getsockname()[1])
    except OSError:
        return None


def _loopback(host: str) -> bool:
    return host in {"127.0.0.1", "localhost", "::1"}


def _safe_join(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts:
        raise KaojuServiceError("wiki_path_invalid", f"Managed wiki path is unsafe: {relative}")
    return root.joinpath(*path.parts)


def _remove_empty_managed_dirs(target: Path) -> None:
    for path in sorted((item for item in target.rglob("*") if item.is_dir()), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def _load_json(path: Path, code: str) -> dict[str, object]:
    value = _try_json(path)
    if not isinstance(value, dict):
        raise KaojuServiceError(code, f"JSON manifest is missing or unreadable: {path}")
    return value


def _try_json(path: Path) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _object_list(value: object) -> list[dict[str, object]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _json_bytes(value: Mapping[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def _checksum_bytes(value: bytes) -> str:
    return f"sha256:{hashlib.sha256(value).hexdigest()}"


def _slug(value: str) -> str:
    selected = "".join(character if character.isalnum() or character in "._-" else "-" for character in value).strip("-")
    return selected or "topic"
