"""Shared validation and serialization helpers for named Kaoju templates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import tempfile
from typing import Mapping, Sequence
import uuid

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.content import DIRECTORY_MANIFEST_NAME
from isomer_labs.runtime.records import RuntimeLifecycleRecord


TEMPLATE_SEMANTIC_ID = "KAOJU:PAPER-TEMPLATE-MYST"
TEMPLATE_AUDIT_SEMANTIC_ID = "KAOJU:PAPER-TEMPLATE-MUTATION-AUDIT"
TEMPLATE_EXPORT_SEMANTIC_ID = "KAOJU:PAPER-TEMPLATE-EXPORT"
TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID = "KAOJU:PAPER-TEMPLATE-MANIFEST"
TEMPLATE_PRODUCER = "isomer-kaoju-write"
TEMPLATE_EXCHANGE_LABEL = "topic.paper.template_exchange_root"
DEFAULT_TEMPLATE_NAME = "main"
EXPORT_METADATA_NAME = ".isomer-template-export.json"
EXPORT_METADATA_VERSION = "isomer-kaoju-template-export.v1"
AUDIT_VERSION = "isomer-kaoju-template-mutation-audit.v1"
_TEMPLATE_NAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9._-]{0,126}[A-Za-z0-9])?$")
_AUTHORED_METADATA_KEYS = frozenset(("entrypoint", "use_guidance", "extensions"))
_SERVICE_METADATA_KEYS = frozenset(
    (
        "artifact_type",
        "binding_schema_version",
        "content_mode",
        "artifact_content",
        "semantic_id",
        "semantic_label",
        "scope_key",
        "template_name",
        "state_token",
        "tree_digest",
        "last_audit_ref",
        "mutation_audit",
        "producer",
        "consumer",
        "skill",
        "relationships",
        "query_index",
    )
)


@dataclass(frozen=True)
class TemplateState:
    """Resolved current state for one mutable template name."""

    record: RuntimeLifecycleRecord
    name: str
    state_token: str
    tree_digest: str
    authored_metadata: dict[str, object]
    root: Path


def validate_template_name(name: str) -> str:
    """Return an exact single-segment template name or raise a stable error."""

    if name in {"", ".", ".."} or "/" in name or "\\" in name or _TEMPLATE_NAME_RE.fullmatch(name) is None:
        raise KaojuServiceError(
            "template_name_invalid",
            "Template name must be one path-safe segment of 1-128 letters, digits, dots, underscores, or hyphens and must start and end with a letter or digit.",
        )
    return name


def validate_template_relative_path(value: str) -> PurePosixPath:
    """Validate a safe relative file path within a template tree."""

    if not value or "\\" in value or value.startswith("/") or "//" in value:
        raise KaojuServiceError("template_path_invalid", f"Template file path is not a safe relative path: {value!r}")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise KaojuServiceError("template_path_invalid", f"Template file path is not a safe relative path: {value!r}")
    if any(part in {EXPORT_METADATA_NAME, DIRECTORY_MANIFEST_NAME} for part in path.parts):
        raise KaojuServiceError("template_reserved_file", f"Template file path uses a service-reserved name: {value!r}")
    return path


def template_tree_digest(
    root: Path,
    *,
    allow_internal_manifest: bool = False,
    exclude_exchange_metadata: bool = False,
) -> str:
    """Hash safe relative paths and file bytes, excluding exchange metadata."""

    selected = root.resolve(strict=False)
    if not selected.is_dir():
        raise KaojuServiceError("template_tree_missing", f"Template tree is not an existing directory: {selected}")
    digest = hashlib.sha256()
    member_count = 0
    for path in sorted(selected.rglob("*"), key=lambda item: item.relative_to(selected).as_posix()):
        relative = path.relative_to(selected).as_posix()
        if path.is_symlink():
            raise KaojuServiceError("template_symlink_forbidden", f"Template trees cannot contain symbolic links: {relative}")
        if not path.is_file():
            continue
        if relative == EXPORT_METADATA_NAME and exclude_exchange_metadata:
            continue
        if relative == DIRECTORY_MANIFEST_NAME and allow_internal_manifest:
            continue
        if path.name in {EXPORT_METADATA_NAME, DIRECTORY_MANIFEST_NAME}:
            raise KaojuServiceError("template_reserved_file", f"Template tree contains a service-reserved file: {relative}")
        encoded_path = relative.encode("utf-8")
        digest.update(len(encoded_path).to_bytes(8, "big"))
        digest.update(encoded_path)
        size = path.stat().st_size
        digest.update(size.to_bytes(8, "big"))
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        member_count += 1
    if member_count == 0:
        raise KaojuServiceError("template_tree_empty", "Template tree must contain at least one non-reserved file.")
    return f"sha256:{digest.hexdigest()}"


def _new_state_token() -> str:
    return f"template-state-{uuid.uuid4().hex}"


def _required_actor(actor: str) -> str:
    selected = actor.strip()
    if not selected:
        raise KaojuServiceError("template_actor_required", "Template mutations and export observations require a non-empty actor ref.")
    return selected


def _unique_strings(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


def _contains_exact(value: object, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, list):
        return any(_contains_exact(item, expected) for item in value)
    if isinstance(value, dict):
        return any(_contains_exact(item, expected) for item in value.values())
    return False


def _nested_string(value: Mapping[str, object], first: str, second: str) -> str | None:
    nested = value.get(first)
    result = nested.get(second) if isinstance(nested, dict) else None
    return result if isinstance(result, str) else None


def _prune_empty_parents(path: Path, root: Path) -> None:
    current = path
    while current != root and current.is_dir() and not any(current.iterdir()):
        current.rmdir()
        current = current.parent


def _atomic_write_json(path: Path, payload: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(raw)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _replace_directory(staged: Path, target: Path) -> None:
    if not target.exists():
        os.replace(staged, target)
        return
    backup = target.parent / f".{target.name}.backup-{uuid.uuid4().hex[:12]}"
    os.replace(target, backup)
    try:
        os.replace(staged, target)
    except Exception:
        os.replace(backup, target)
        raise
    shutil.rmtree(backup)


def _load_export_metadata(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise KaojuServiceError("template_export_metadata_invalid", f"Template export metadata is unreadable: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != EXPORT_METADATA_VERSION:
        raise KaojuServiceError("template_export_metadata_invalid", "Template export metadata has an unsupported shape or schema version.")
    required = ("template_name", "canonical_ref", "state_token", "canonical_tree_digest", "exported_tree_digest", "observed_path", "observed_at", "actor")
    missing = [field for field in required if not isinstance(value.get(field), str) or not value.get(field)]
    if missing:
        raise KaojuServiceError("template_export_metadata_invalid", f"Template export metadata is missing fields: {', '.join(missing)}")
    return value


def _result_ref(payload: Mapping[str, object]) -> str:
    record = payload.get("record")
    if isinstance(record, dict) and isinstance(record.get("id"), str):
        return str(record["id"])
    affected = payload.get("affected_refs")
    if isinstance(affected, list) and affected:
        return str(affected[0])
    raise KaojuServiceError("template_observation_ref_missing", "Template export observation did not return a stable ref.")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
