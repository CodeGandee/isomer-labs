"""Content locators and checksummed directory manifests for Kaoju Artifacts."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any, Mapping

from isomer_labs.kaoju.repository_evidence import redact_repository_evidence, repository_evidence_diagnostics
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.path_resolution import resolve_semantic_path


DIRECTORY_MANIFEST_NAME = ".isomer-artifact-manifest.json"
DIRECTORY_MANIFEST_VERSION = "isomer-artifact-directory-manifest.v1"


@dataclass(frozen=True)
class ArtifactContent:
    """Validated content locator metadata recorded with an Artifact."""

    content_path: Path
    locator_kind: str
    media_type: str
    checksum: str
    size_bytes: int
    managed: bool
    manifest: dict[str, Any] | None = None

    def metadata(self) -> dict[str, object]:
        value: dict[str, object] = {
            "locator_kind": self.locator_kind,
            "media_type": self.media_type,
            "checksum": self.checksum,
            "size_bytes": self.size_bytes,
            "managed": self.managed,
        }
        if self.manifest is not None:
            value["manifest_schema_version"] = self.manifest["schema_version"]
            if self.locator_kind == "canonical_repository":
                value["locator"] = self.manifest
        return value


def register_ordinary_file(path: Path, *, managed: bool = True) -> ArtifactContent:
    """Validate an ordinary file before the record store copies or registers it."""

    selected = path.resolve(strict=False)
    if not selected.is_file():
        raise ValueError(f"Artifact content file does not exist: {selected}")
    media_type = mimetypes.guess_type(selected.name)[0] or "application/octet-stream"
    return ArtifactContent(
        content_path=selected,
        locator_kind="managed_file" if managed else "external_file",
        media_type=media_type,
        checksum=checksum_file(selected),
        size_bytes=selected.stat().st_size,
        managed=managed,
    )


def register_structured_file(path: Path) -> ArtifactContent:
    """Describe the canonical JSON snapshot that the record store will persist."""

    selected = path.resolve(strict=False)
    if not selected.is_file():
        raise ValueError(f"Artifact content file does not exist: {selected}")
    try:
        value = json.loads(selected.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Structured Artifact content is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("Structured Artifact content must be a JSON object.")
    canonical = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    return ArtifactContent(
        content_path=selected,
        locator_kind="managed_file",
        media_type="application/json",
        checksum=f"sha256:{hashlib.sha256(canonical).hexdigest()}",
        size_bytes=len(canonical),
        managed=True,
    )


def register_external_path(path: Path) -> ArtifactContent:
    """Register an authorized external path without copying or mutating it."""

    selected = path.resolve(strict=False)
    if not selected.exists():
        raise ValueError(f"External Artifact path does not exist: {selected}")
    if selected.is_file():
        return register_ordinary_file(selected, managed=False)
    manifest = directory_manifest(selected, locator_posture="external")
    return ArtifactContent(
        content_path=selected,
        locator_kind="external_directory",
        media_type="application/vnd.isomer.artifact-directory+json",
        checksum=manifest_checksum(manifest),
        size_bytes=sum(int(member["size_bytes"]) for member in manifest["members"]),
        managed=False,
        manifest=manifest,
    )


def register_canonical_repository(path: Path, *, evidence: Mapping[str, Any]) -> ArtifactContent:
    """Register caller-observed repository identity without executing source-control commands."""

    selected = path.resolve(strict=False)
    if not selected.is_dir():
        raise ValueError(f"Canonical repository path is not an existing directory: {selected}")
    sanitized = redact_repository_evidence(evidence)
    if not isinstance(sanitized, dict):
        raise ValueError("Canonical repository evidence must be an object.")
    diagnostics = repository_evidence_diagnostics(sanitized, location="repository_evidence")
    if diagnostics:
        detail = "; ".join(f"{location}: {message}" for _code, message, location in diagnostics)
        raise ValueError(f"Canonical repository evidence is invalid: {detail}")
    identity = {"schema_version": "isomer-canonical-repository-locator.v2", **sanitized}
    encoded = json.dumps(identity, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return ArtifactContent(
        content_path=selected,
        locator_kind="canonical_repository",
        media_type="application/vnd.isomer.canonical-repository+json",
        checksum=f"sha256:{hashlib.sha256(encoded).hexdigest()}",
        size_bytes=0,
        managed=False,
        manifest=identity,
    )


def create_managed_directory_artifact(
    context: EffectiveTopicContext,
    source: Path,
    *,
    semantic_label: str,
    record_kind: str,
    record_id: str,
    env: Mapping[str, str],
    cwd: Path,
) -> ArtifactContent:
    """Copy a directory through a staging path and register its manifest atomically."""

    selected = source.resolve(strict=False)
    if not selected.is_dir():
        raise ValueError(f"Artifact directory does not exist: {selected}")
    resolution, diagnostics = resolve_semantic_path(context, semantic_label, env=env, cwd=cwd)
    if resolution is None:
        messages = "; ".join(diagnostic.message for diagnostic in diagnostics)
        raise ValueError(f"Artifact semantic label could not be resolved: {messages}")
    owner = resolution.path / "research-records" / record_kind / _slug(record_id)
    target = owner / "content"
    owner.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix=".content.", dir=owner))
    try:
        _copy_directory(selected, staged)
        manifest = directory_manifest(staged, locator_posture="managed")
        manifest_path = staged / DIRECTORY_MANIFEST_NAME
        _write_json(manifest_path, manifest)
        if target.exists():
            raise ValueError(f"Managed Artifact content target already exists: {target}")
        os.replace(staged, target)
    finally:
        if staged.exists():
            shutil.rmtree(staged)
    final_manifest = target / DIRECTORY_MANIFEST_NAME
    return ArtifactContent(
        content_path=final_manifest,
        locator_kind="managed_directory_manifest",
        media_type="application/vnd.isomer.artifact-directory+json",
        checksum=manifest_checksum(manifest),
        size_bytes=sum(int(member["size_bytes"]) for member in manifest["members"]),
        managed=True,
        manifest=manifest,
    )


def directory_manifest(root: Path, *, locator_posture: str) -> dict[str, Any]:
    """Build a deterministic manifest without following symlinks."""

    members: list[dict[str, object]] = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix()
        if relative == DIRECTORY_MANIFEST_NAME:
            continue
        if path.is_symlink():
            raise ValueError(f"Directory Artifacts cannot contain symbolic links: {relative}")
        if not path.is_file():
            continue
        members.append(
            {
                "path": relative,
                "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "size_bytes": path.stat().st_size,
                "checksum": checksum_file(path),
            }
        )
    return {
        "schema_version": DIRECTORY_MANIFEST_VERSION,
        "locator_posture": locator_posture,
        "member_count": len(members),
        "members": members,
    }


def validate_directory_manifest(manifest_path: Path) -> list[dict[str, object]]:
    """Report missing, unexpected, or checksum-mismatched directory members."""

    diagnostics: list[dict[str, object]] = []
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [{"code": "artifact_manifest_unreadable", "severity": "error", "message": str(exc), "path": str(manifest_path)}]
    if not isinstance(raw, dict) or raw.get("schema_version") != DIRECTORY_MANIFEST_VERSION or not isinstance(raw.get("members"), list):
        return [{"code": "artifact_manifest_invalid", "severity": "error", "message": "Directory manifest has an unsupported shape.", "path": str(manifest_path)}]
    root = manifest_path.parent
    for member in raw["members"]:
        if not isinstance(member, dict) or not isinstance(member.get("path"), str):
            diagnostics.append({"code": "artifact_manifest_member_invalid", "severity": "error", "message": "Directory manifest member is invalid."})
            continue
        member_path = root / member["path"]
        if not member_path.is_file():
            diagnostics.append({"code": "artifact_content_missing", "severity": "error", "message": "Directory member is missing.", "path": str(member_path)})
        elif checksum_file(member_path) != member.get("checksum"):
            diagnostics.append({"code": "artifact_content_corrupt", "severity": "error", "message": "Directory member checksum does not match.", "path": str(member_path)})
    return diagnostics


def checksum_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def manifest_checksum(manifest: dict[str, Any]) -> str:
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def _copy_directory(source: Path, target: Path) -> None:
    for path in sorted(source.rglob("*"), key=lambda item: item.relative_to(source).as_posix()):
        relative = path.relative_to(source)
        destination = target / relative
        if path.is_symlink():
            raise ValueError(f"Directory Artifacts cannot contain symbolic links: {relative.as_posix()}")
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _slug(value: str) -> str:
    return "".join(character if character.isalnum() or character in "._-" else "-" for character in value).strip("-") or "artifact"
