"""Privacy classification, sanitized projection, and four-way comparison."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path, PurePosixPath
import re
from typing import Iterable, Mapping, cast

import tomlkit
import yaml  # type: ignore[import-untyped]

from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.topic_git.models import ComponentBinding, PrivacyDisposition, PublicationConflict


MAX_DEFAULT_PUBLICATION_BYTES = 10 * 1024 * 1024
_ARCHIVE_SUFFIXES = {
    ".7z",
    ".bz2",
    ".gz",
    ".rar",
    ".tar",
    ".tgz",
    ".xz",
    ".zip",
}
_BINARY_SUFFIXES = {
    ".a",
    ".bin",
    ".class",
    ".dll",
    ".dylib",
    ".exe",
    ".o",
    ".pdf",
    ".pyc",
    ".so",
}
_PRIVATE_KEY_RE = re.compile(rb"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")
_CREDENTIAL_RE = re.compile(
    rb"(?i)(?:api[_-]?key|client[_-]?secret|password|access[_-]?token|auth[_-]?token)\s*[:=]\s*[\"']?[^\s\"']{8,}"
)
_CREDENTIAL_URL_RE = re.compile(rb"(?i)https?://[^/\s:@]+:[^/\s@]+@")
_SIGNED_URL_RE = re.compile(rb"(?i)https?://[^\s?]+\?[^\s]*(?:signature|sig|token|x-amz-credential)=")
_SECRET_FIELD_RE = re.compile(r"(?i)(?:api[_-]?key|client[_-]?secret|password|private[_-]?key|access[_-]?token)")


@dataclass(frozen=True)
class ProjectionFinding:
    code: str
    severity: str
    relative_path: str
    message: str


@dataclass(frozen=True)
class ProjectionEntry:
    source_relative_path: str
    output_relative_path: str | None
    disposition: PrivacyDisposition
    source_fingerprint: str | None
    output_fingerprint: str | None = None
    transformation: str | None = None
    reason: str | None = None
    component_id: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "source_relative_path": self.source_relative_path,
            "disposition": self.disposition.value,
        }
        for key, value in (
            ("output_relative_path", self.output_relative_path),
            ("source_fingerprint", self.source_fingerprint),
            ("output_fingerprint", self.output_fingerprint),
            ("transformation", self.transformation),
            ("reason", self.reason),
            ("component_id", self.component_id),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class ProjectionManifest:
    binding_id: str
    plan_id: str
    created_at: str
    entries: tuple[ProjectionEntry, ...]
    components: tuple[ComponentBinding, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": "isomer-topic-git-projection-manifest.v1",
            "binding_id": self.binding_id,
            "plan_id": self.plan_id,
            "created_at": self.created_at,
            "entries": [entry.to_json() for entry in self.entries],
            "components": [component.to_json() for component in self.components],
        }


@dataclass(frozen=True)
class ProjectionComparison:
    updates: tuple[str, ...]
    removals: tuple[str, ...]
    unchanged: tuple[str, ...]
    conflicts: tuple[PublicationConflict, ...]


def fingerprint_bytes(content: bytes) -> str:
    return sha256(content).hexdigest()


def fingerprint_file(path: Path) -> str:
    return fingerprint_bytes(path.read_bytes())


def classify_projection_file(
    relative_path: str,
    content: bytes,
    *,
    max_bytes: int = MAX_DEFAULT_PUBLICATION_BYTES,
    approved_license: bool = True,
) -> tuple[PrivacyDisposition, tuple[ProjectionFinding, ...]]:
    """Classify one file without returning sensitive excerpts."""

    normalized = _relative_path(relative_path)
    parts = tuple(part.lower() for part in PurePosixPath(normalized).parts)
    suffix = PurePosixPath(normalized).suffix.lower()
    findings: list[ProjectionFinding] = []

    if ".git" in parts:
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding("git-metadata", "error", normalized, "Git control material is excluded."),
        )
    if _is_noncontent_private_surface(parts):
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding("private-surface", "warning", normalized, "Known private or runtime surface is excluded."),
        )
    if len(content) > max_bytes:
        findings.append(ProjectionFinding("size", "error", normalized, "File exceeds the approved publication size limit."))
    if suffix in _ARCHIVE_SUFFIXES:
        findings.append(ProjectionFinding("archive", "error", normalized, "Archives cannot be sanitized automatically."))
    if suffix in _BINARY_SUFFIXES or b"\x00" in content[:8192]:
        findings.append(ProjectionFinding("binary", "error", normalized, "Binary content cannot be masked automatically."))
    if _PRIVATE_KEY_RE.search(content):
        findings.append(ProjectionFinding("private-key", "error", normalized, "Private-key material blocks publication."))
    if _CREDENTIAL_RE.search(content) or _CREDENTIAL_URL_RE.search(content):
        findings.append(ProjectionFinding("credential", "error", normalized, "Credential-like material blocks publication."))
    if _SIGNED_URL_RE.search(content):
        findings.append(ProjectionFinding("signed-url", "error", normalized, "Signed URL material blocks publication."))
    if not approved_license:
        findings.append(ProjectionFinding("license", "error", normalized, "Publication license is unresolved."))
    if any(finding.severity == "error" for finding in findings):
        return PrivacyDisposition.BLOCK, tuple(findings)
    if _is_sensitive_file_surface(parts):
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding("private-surface", "warning", normalized, "Known private file surface is excluded."),
        )
    return PrivacyDisposition.TRACK, tuple(findings)


def inventory_projection_sources(
    source_topic_workspace: Path,
    *,
    semantic_roots: Mapping[str, Path],
    component_roots: Mapping[str, Path] | None = None,
    max_bytes: int = MAX_DEFAULT_PUBLICATION_BYTES,
) -> tuple[tuple[ProjectionEntry, ...], tuple[ProjectionFinding, ...]]:
    """Inventory Isomer-resolved semantic roots without consulting a Git index."""

    source_root = canonicalize(source_topic_workspace)
    components = {
        canonicalize(path): component_id
        for component_id, path in (component_roots or {}).items()
    }
    entries: list[ProjectionEntry] = []
    findings: list[ProjectionFinding] = []
    seen: set[str] = set()

    for label, root in sorted(semantic_roots.items()):
        resolved_root = canonicalize(root)
        if resolved_root != source_root and not is_within(resolved_root, source_root):
            raise ValueError(f"Semantic root {label!r} escapes the Source Topic Workspace.")
        component_id = components.get(resolved_root)
        if component_id is not None:
            relative = _relative_to(resolved_root, source_root)
            entries.append(
                ProjectionEntry(
                    source_relative_path=relative,
                    output_relative_path=relative,
                    disposition=PrivacyDisposition.COMPONENT,
                    source_fingerprint=None,
                    component_id=component_id,
                )
            )
            seen.add(relative)
            continue
        if not resolved_root.exists():
            continue
        candidates: tuple[Path, ...]
        if resolved_root.is_file():
            candidates = (resolved_root,)
        else:
            discovered: list[Path] = []
            for current_root, directory_names, file_names in os.walk(resolved_root):
                current = canonicalize(Path(current_root))
                retained_directories: list[str] = []
                for directory_name in sorted(directory_names):
                    directory = canonicalize(current / directory_name)
                    relative = _relative_to(directory, source_root)
                    if directory_name == ".git":
                        if relative not in seen:
                            entries.append(
                                ProjectionEntry(
                                    source_relative_path=relative,
                                    output_relative_path=None,
                                    disposition=PrivacyDisposition.EXCLUDE,
                                    source_fingerprint=None,
                                    reason="Git control material is excluded without inspection.",
                                )
                            )
                            seen.add(relative)
                        continue
                    nested_component_id = components.get(directory)
                    if nested_component_id is not None:
                        if relative not in seen:
                            entries.append(
                                ProjectionEntry(
                                    source_relative_path=relative,
                                    output_relative_path=relative,
                                    disposition=PrivacyDisposition.COMPONENT,
                                    source_fingerprint=None,
                                    component_id=nested_component_id,
                                )
                            )
                            seen.add(relative)
                        continue
                    retained_directories.append(directory_name)
                directory_names[:] = retained_directories
                discovered.extend(current / file_name for file_name in sorted(file_names))
            candidates = tuple(discovered)
        for path in candidates:
            resolved = canonicalize(path)
            relative = _relative_to(resolved, source_root)
            if relative in seen or _under_component(resolved, components):
                continue
            seen.add(relative)
            if resolved.is_symlink():
                findings.append(
                    ProjectionFinding("symlink", "error", relative, "Symlink publication requires an explicit reviewed mapping.")
                )
                entries.append(
                    ProjectionEntry(relative, relative, PrivacyDisposition.BLOCK, None, reason="unreviewed symlink")
                )
                continue
            relative_parts = tuple(part.lower() for part in PurePosixPath(relative).parts)
            if ".git" in relative_parts or _is_noncontent_private_surface(relative_parts):
                findings.append(
                    ProjectionFinding(
                        "private-surface",
                        "warning",
                        relative,
                        "Known Git, private, or runtime surface is excluded without reading content.",
                    )
                )
                entries.append(
                    ProjectionEntry(
                        source_relative_path=relative,
                        output_relative_path=None,
                        disposition=PrivacyDisposition.EXCLUDE,
                        source_fingerprint=None,
                        reason="known private surface",
                    )
                )
                continue
            content = resolved.read_bytes()
            disposition, path_findings = classify_projection_file(relative, content, max_bytes=max_bytes)
            findings.extend(path_findings)
            entries.append(
                ProjectionEntry(
                    source_relative_path=relative,
                    output_relative_path=relative if disposition in {PrivacyDisposition.TRACK, PrivacyDisposition.BLOCK} else None,
                    disposition=disposition,
                    source_fingerprint=fingerprint_bytes(content),
                    reason=path_findings[0].message if path_findings else None,
                )
            )
    return tuple(sorted(entries, key=lambda item: item.source_relative_path)), tuple(findings)


def render_structured_template(content: str, *, format_name: str) -> str:
    """Replace sensitive structured values with descriptive placeholders."""

    normalized = format_name.lower().lstrip(".")
    if normalized == "json":
        value = json.loads(content)
        rendered = _template_value(value)
        return json.dumps(rendered, indent=2, sort_keys=True) + "\n"
    if normalized in {"toml", "tml"}:
        value = tomlkit.parse(content).unwrap()
        rendered = _template_value(value)
        return tomlkit.dumps(cast(Mapping[str, object], rendered))
    if normalized in {"yaml", "yml"}:
        value = yaml.safe_load(content)
        rendered = _template_value(value)
        return yaml.safe_dump(rendered, sort_keys=True)
    raise ValueError(f"Unsupported structured template format: {format_name}")


def materialize_projection(
    source_topic_workspace: Path,
    publication_copy: Path,
    entries: Iterable[ProjectionEntry],
    *,
    template_outputs: Mapping[str, bytes] | None = None,
) -> tuple[ProjectionEntry, ...]:
    """Copy only approved files into the publication copy and preserve source bytes."""

    source_root = canonicalize(source_topic_workspace)
    copy_root = canonicalize(publication_copy)
    templates = dict(template_outputs or {})
    materialized: list[ProjectionEntry] = []
    source_before: dict[str, str] = {}

    for entry in entries:
        if entry.disposition in {PrivacyDisposition.EXCLUDE, PrivacyDisposition.COMPONENT}:
            materialized.append(entry)
            continue
        if entry.disposition is PrivacyDisposition.BLOCK:
            raise ValueError(f"Blocked projection entry cannot be materialized: {entry.source_relative_path}")
        if entry.output_relative_path is None:
            raise ValueError(f"Projection entry has no output path: {entry.source_relative_path}")
        source_path = canonicalize(source_root / entry.source_relative_path)
        destination = canonicalize(copy_root / entry.output_relative_path)
        if not is_within(source_path, source_root) or not is_within(destination, copy_root):
            raise ValueError("Projection paths must remain inside their approved roots.")
        if ".git" in PurePosixPath(entry.source_relative_path).parts:
            raise ValueError("Projection cannot copy Git control paths.")
        source_content = source_path.read_bytes()
        source_before[entry.source_relative_path] = fingerprint_bytes(source_content)
        if entry.disposition is PrivacyDisposition.TEMPLATE:
            try:
                output = templates[entry.source_relative_path]
            except KeyError as error:
                raise ValueError(f"Missing approved template output: {entry.source_relative_path}") from error
        else:
            output = source_content
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(output)
        materialized.append(
            ProjectionEntry(
                source_relative_path=entry.source_relative_path,
                output_relative_path=entry.output_relative_path,
                disposition=entry.disposition,
                source_fingerprint=fingerprint_bytes(source_content),
                output_fingerprint=fingerprint_bytes(output),
                transformation=entry.transformation,
                reason=entry.reason,
                component_id=entry.component_id,
            )
        )

    for relative, before in source_before.items():
        if fingerprint_file(source_root / relative) != before:
            raise RuntimeError(f"Source changed during publication materialization: {relative}")
    blockers = rescan_projection(copy_root, materialized)
    if blockers:
        raise ValueError("Materialized projection failed privacy rescan: " + "; ".join(item.message for item in blockers))
    return tuple(materialized)


def rescan_projection(
    publication_copy: Path,
    entries: Iterable[ProjectionEntry],
) -> tuple[ProjectionFinding, ...]:
    """Scan every ordinary file eligible for a publication commit."""

    copy_root = canonicalize(publication_copy)
    blockers: list[ProjectionFinding] = []
    for entry in entries:
        if entry.disposition not in {PrivacyDisposition.TRACK, PrivacyDisposition.TEMPLATE}:
            continue
        if entry.output_relative_path is None:
            continue
        output = canonicalize(copy_root / entry.output_relative_path)
        if not is_within(output, copy_root):
            blockers.append(
                ProjectionFinding("path", "error", entry.source_relative_path, "Projection output escapes the publication copy.")
            )
            continue
        disposition, findings = classify_projection_file(entry.output_relative_path, output.read_bytes())
        if disposition is PrivacyDisposition.BLOCK:
            blockers.extend(findings)
    return tuple(blockers)


def compare_projection(
    *,
    expected: Mapping[str, str],
    prior_generated: Mapping[str, str],
    current_copy: Mapping[str, str],
    approved_conflicts: Iterable[str] = (),
) -> ProjectionComparison:
    """Compare expected, prior, and current output fingerprints without mutating files."""

    approved = {_relative_path(path) for path in approved_conflicts}
    updates: list[str] = []
    removals: list[str] = []
    unchanged: list[str] = []
    conflicts: list[PublicationConflict] = []
    for path in sorted(set(expected) | set(prior_generated) | set(current_copy)):
        expected_value = expected.get(path)
        prior_value = prior_generated.get(path)
        current_value = current_copy.get(path)
        if expected_value == current_value:
            unchanged.append(path)
            continue
        if expected_value is None:
            if current_value is None:
                unchanged.append(path)
            elif current_value == prior_value or path in approved:
                removals.append(path)
            else:
                conflicts.append(
                    PublicationConflict(
                        relative_path=path,
                        reason="source removed but destination changed",
                        prior_output_fingerprint=prior_value,
                        current_output_fingerprint=current_value,
                    )
                )
            continue
        if current_value is None or current_value == prior_value or path in approved:
            updates.append(path)
            continue
        conflicts.append(
            PublicationConflict(
                relative_path=path,
                reason="source and destination both changed",
                source_fingerprint=expected_value,
                prior_output_fingerprint=prior_value,
                current_output_fingerprint=current_value,
            )
        )
    return ProjectionComparison(tuple(updates), tuple(removals), tuple(unchanged), tuple(conflicts))


def render_projection_manifest(manifest: ProjectionManifest) -> str:
    return json.dumps(manifest.to_json(), indent=2, sort_keys=True) + "\n"


def render_topic_workspace_version(
    *,
    binding_id: str,
    plan_id: str,
    created_at: str,
    branch_commits: Mapping[str, str],
) -> str:
    """Render sanitized branch-to-commit publication metadata."""

    lines = [
        'schema_version = "isomer-topic-workspace-version.v1"',
        f"binding_id = {json.dumps(binding_id)}",
        f"plan_id = {json.dumps(plan_id)}",
        f"created_at = {json.dumps(created_at)}",
    ]
    for branch, commit in sorted(branch_commits.items()):
        lines.extend(
            (
                "",
                "[[branches]]",
                f"name = {json.dumps(branch)}",
                f"commit_sha = {json.dumps(commit)}",
            )
        )
    return "\n".join(lines) + "\n"


def _template_value(value: object, key: str | None = None) -> object:
    if key is not None and _SECRET_FIELD_RE.fullmatch(key):
        placeholder = re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_").upper()
        return f"${{{placeholder}}}"
    if isinstance(value, Mapping):
        return {str(child_key): _template_value(child, str(child_key)) for child_key, child in value.items()}
    if isinstance(value, list):
        return [_template_value(child) for child in value]
    return value


def _is_noncontent_private_surface(parts: tuple[str, ...]) -> bool:
    name = parts[-1] if parts else ""
    return (
        any(part in {"runtime", "tmp", "temp", ".pixi", ".venv", "__pycache__", ".isomer"} for part in parts)
        or name == "state.sqlite"
        or name.startswith(".env")
        or name.endswith((".log", ".pyc"))
    )


def _is_sensitive_file_surface(parts: tuple[str, ...]) -> bool:
    name = parts[-1] if parts else ""
    return name.endswith((".pem", ".key"))


def _relative_path(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    normalized = path.as_posix()
    if normalized in {"", ".", ".."} or normalized.startswith("../") or normalized.startswith("/"):
        raise ValueError(f"Projection path must be a non-root relative path: {value!r}")
    return normalized


def _relative_to(path: Path, root: Path) -> str:
    return _relative_path(canonicalize(path).relative_to(canonicalize(root)).as_posix())


def _under_component(path: Path, components: Mapping[Path, str]) -> bool:
    for component_root in components:
        if path != component_root and is_within(path, component_root):
            return True
    return False
