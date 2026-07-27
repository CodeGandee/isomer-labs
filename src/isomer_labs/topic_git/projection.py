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
from isomer_labs.topic_git.models import (
    ComponentBinding,
    PrivacyDisposition,
    PublicationConflict,
    PublicationContentClass,
    PublicationSelectionSettings,
    ReferenceRepositoryBinding,
)


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
_CREDENTIAL_URL_RE = re.compile(rb"(?i)https?://[^/\s@]+@")
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
    content_class: PublicationContentClass = PublicationContentClass.OTHER
    media_type: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "source_relative_path": self.source_relative_path,
            "disposition": self.disposition.value,
            "content_class": self.content_class.value,
        }
        for key, value in (
            ("output_relative_path", self.output_relative_path),
            ("source_fingerprint", self.source_fingerprint),
            ("output_fingerprint", self.output_fingerprint),
            ("transformation", self.transformation),
            ("reason", self.reason),
            ("component_id", self.component_id),
            ("media_type", self.media_type),
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
    selection: PublicationSelectionSettings = PublicationSelectionSettings()
    reference_repositories: tuple[ReferenceRepositoryBinding, ...] = ()
    research_index_fingerprint: str | None = None
    readme_fingerprint: str | None = None
    reproduction_limitations: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "schema_version": "isomer-topic-git-projection-manifest.v2",
            "binding_id": self.binding_id,
            "plan_id": self.plan_id,
            "created_at": self.created_at,
            "entries": [entry.to_json() for entry in self.entries],
            "components": [component.to_json() for component in self.components],
            "selection": self.selection.to_json(),
            "reference_repositories": [
                reference.to_json()
                for reference in sorted(self.reference_repositories, key=lambda item: item.reference_id)
            ],
            "reproduction_limitations": list(self.reproduction_limitations),
        }
        if self.research_index_fingerprint is not None:
            data["research_index_fingerprint"] = self.research_index_fingerprint
        if self.readme_fingerprint is not None:
            data["readme_fingerprint"] = self.readme_fingerprint
        return data


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
    content_class: PublicationContentClass = PublicationContentClass.OTHER,
    selection: PublicationSelectionSettings = PublicationSelectionSettings(),
    approved_media_type: str | None = None,
) -> tuple[PrivacyDisposition, tuple[ProjectionFinding, ...]]:
    """Classify one file without returning sensitive excerpts."""

    normalized = _relative_path(relative_path)
    parts = tuple(part.lower() for part in PurePosixPath(normalized).parts)
    suffix = PurePosixPath(normalized).suffix.lower()
    findings: list[ProjectionFinding] = []

    if content_class is PublicationContentClass.PRIVATE_RUNTIME:
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding("private-runtime", "warning", normalized, "Workspace Runtime content is excluded."),
        )
    if content_class is PublicationContentClass.RAW_MATERIAL and not selection.include_raw_material_bytes:
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding(
                "raw-material-opt-in",
                "warning",
                normalized,
                "Downloaded raw-material bytes require explicit current-plan selection.",
            ),
        )
    if (
        content_class is PublicationContentClass.RAW_EXPERIMENT_OUTPUT
        and not selection.include_raw_experiment_output_bytes
    ):
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding(
                "raw-experiment-output-opt-in",
                "warning",
                normalized,
                "Raw experiment-output bytes require explicit current-plan selection.",
            ),
        )
    if ".git" in parts:
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding("git-metadata", "error", normalized, "Git control material is excluded."),
        )
    if _is_noncontent_private_surface(parts) and not _raw_bytes_selected(content_class, selection):
        return PrivacyDisposition.EXCLUDE, (
            ProjectionFinding("private-surface", "warning", normalized, "Known private or runtime surface is excluded."),
        )
    if len(content) > max_bytes:
        findings.append(ProjectionFinding("size", "error", normalized, "File exceeds the approved publication size limit."))
    if suffix in _ARCHIVE_SUFFIXES:
        findings.append(ProjectionFinding("archive", "error", normalized, "Archives cannot be sanitized automatically."))
    typed_pdf = approved_media_type == "application/pdf"
    if typed_pdf and (suffix != ".pdf" or not content.startswith(b"%PDF-")):
        findings.append(
            ProjectionFinding(
                "pdf-signature",
                "error",
                normalized,
                "Approved paper PDF does not have the required extension and PDF signature.",
            )
        )
    if (suffix in _BINARY_SUFFIXES or b"\x00" in content[:8192]) and not typed_pdf:
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
    reference_roots: Mapping[str, Path] | None = None,
    semantic_classes: Mapping[str, PublicationContentClass] | None = None,
    path_content_classes: Mapping[str, PublicationContentClass] | None = None,
    selection: PublicationSelectionSettings = PublicationSelectionSettings(),
    approved_pdf_paths: Iterable[str] = (),
    max_bytes: int = MAX_DEFAULT_PUBLICATION_BYTES,
) -> tuple[tuple[ProjectionEntry, ...], tuple[ProjectionFinding, ...]]:
    """Inventory Isomer-resolved semantic roots without consulting a Git index."""

    source_root = canonicalize(source_topic_workspace)
    components = {
        canonicalize(path): component_id
        for component_id, path in (component_roots or {}).items()
    }
    references = {
        canonicalize(path): reference_id
        for reference_id, path in (reference_roots or {}).items()
    }
    configured_classes = dict(semantic_classes or {})
    class_surfaces = tuple(
        (
            canonicalize(root),
            configured_classes.get(label, infer_publication_content_class(label)),
        )
        for label, root in semantic_roots.items()
    )
    path_classes = {
        _relative_path(relative): content_class
        for relative, content_class in (path_content_classes or {}).items()
    }
    approved_pdfs = {_relative_path(path) for path in approved_pdf_paths}
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
                    content_class=PublicationContentClass.TOPIC_COMPONENT,
                )
            )
            seen.add(relative)
            continue
        reference_id = references.get(resolved_root)
        if reference_id is not None:
            relative = _relative_to(resolved_root, source_root)
            entries.append(
                ProjectionEntry(
                    source_relative_path=relative,
                    output_relative_path=relative,
                    disposition=PrivacyDisposition.COMPONENT,
                    source_fingerprint=None,
                    component_id=reference_id,
                    content_class=PublicationContentClass.REFERENCE_REPOSITORY,
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
                                    content_class=PublicationContentClass.TOPIC_COMPONENT,
                                )
                            )
                            seen.add(relative)
                        continue
                    nested_reference_id = references.get(directory)
                    if nested_reference_id is not None:
                        if relative not in seen:
                            entries.append(
                                ProjectionEntry(
                                    source_relative_path=relative,
                                    output_relative_path=relative,
                                    disposition=PrivacyDisposition.COMPONENT,
                                    source_fingerprint=None,
                                    component_id=nested_reference_id,
                                    content_class=PublicationContentClass.REFERENCE_REPOSITORY,
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
                content_class = _content_class_for_path(
                    resolved,
                    source_root=source_root,
                    class_surfaces=class_surfaces,
                    path_classes=path_classes,
                )
                findings.append(
                    ProjectionFinding("symlink", "error", relative, "Symlink publication requires an explicit reviewed mapping.")
                )
                entries.append(
                    ProjectionEntry(
                        relative,
                        relative,
                        PrivacyDisposition.BLOCK,
                        None,
                        reason="unreviewed symlink",
                        content_class=content_class,
                    )
                )
                continue
            relative_parts = tuple(part.lower() for part in PurePosixPath(relative).parts)
            content_class = _content_class_for_path(
                resolved,
                source_root=source_root,
                class_surfaces=class_surfaces,
                path_classes=path_classes,
            )
            if (
                ".git" in relative_parts
                or content_class is PublicationContentClass.PRIVATE_RUNTIME
                or (
                    _is_noncontent_private_surface(relative_parts)
                    and not _raw_bytes_selected(content_class, selection)
                )
            ):
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
                        content_class=content_class,
                    )
                )
                continue
            content = resolved.read_bytes()
            approved_media_type = "application/pdf" if relative in approved_pdfs else None
            disposition, path_findings = classify_projection_file(
                relative,
                content,
                max_bytes=max_bytes,
                content_class=content_class,
                selection=selection,
                approved_media_type=approved_media_type,
            )
            findings.extend(path_findings)
            entries.append(
                ProjectionEntry(
                    source_relative_path=relative,
                    output_relative_path=relative if disposition in {PrivacyDisposition.TRACK, PrivacyDisposition.BLOCK} else None,
                    disposition=disposition,
                    source_fingerprint=fingerprint_bytes(content),
                    reason=path_findings[0].message if path_findings else None,
                    content_class=content_class,
                    media_type=approved_media_type,
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
                content_class=entry.content_class,
                media_type=entry.media_type,
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
        disposition, findings = classify_projection_file(
            entry.output_relative_path,
            output.read_bytes(),
            content_class=entry.content_class,
            selection=PublicationSelectionSettings(
                include_raw_material_bytes=entry.content_class is PublicationContentClass.RAW_MATERIAL,
                include_raw_experiment_output_bytes=(
                    entry.content_class is PublicationContentClass.RAW_EXPERIMENT_OUTPUT
                ),
            ),
            approved_media_type=entry.media_type,
        )
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


def infer_publication_content_class(semantic_label: str) -> PublicationContentClass:
    """Infer a safe default class from one resolved semantic label."""

    normalized = semantic_label.strip().lower()
    if normalized.startswith("topic.intent."):
        return PublicationContentClass.INTENT
    if normalized.startswith(("topic.env.", "topic.environment.")) or normalized in {
        "topic.workspace.manifest",
        "topic.pixi.manifest",
        "topic.pixi.lock",
    }:
        return PublicationContentClass.ENVIRONMENT
    if normalized == "topic.records" or normalized.startswith("topic.records."):
        return PublicationContentClass.RESEARCH_RECORD
    if normalized in {"topic.runtime", "topic.runtime.db"} or normalized.startswith("topic.runtime."):
        return PublicationContentClass.PRIVATE_RUNTIME
    if normalized == "topic.repos.main" or normalized.startswith(("topic.actors.", "agent.workspace")):
        return PublicationContentClass.TOPIC_COMPONENT
    if normalized.startswith("topic.repos."):
        return PublicationContentClass.REFERENCE_REPOSITORY
    return PublicationContentClass.OTHER


def _content_class_for_path(
    path: Path,
    *,
    source_root: Path,
    class_surfaces: tuple[tuple[Path, PublicationContentClass], ...],
    path_classes: Mapping[str, PublicationContentClass],
) -> PublicationContentClass:
    relative = _relative_to(path, source_root)
    explicit = [
        (len(PurePosixPath(prefix).parts), content_class)
        for prefix, content_class in path_classes.items()
        if relative == prefix or relative.startswith(f"{prefix}/")
    ]
    if explicit:
        return max(explicit, key=lambda item: item[0])[1]
    resolved = canonicalize(path)
    semantic = [
        (len(root.parts), content_class)
        for root, content_class in class_surfaces
        if resolved == root or is_within(resolved, root)
    ]
    if semantic:
        return max(semantic, key=lambda item: item[0])[1]
    return PublicationContentClass.OTHER


def _raw_bytes_selected(
    content_class: PublicationContentClass,
    selection: PublicationSelectionSettings,
) -> bool:
    if content_class is PublicationContentClass.RAW_MATERIAL:
        return selection.include_raw_material_bytes
    if content_class is PublicationContentClass.RAW_EXPERIMENT_OUTPUT:
        return selection.include_raw_experiment_output_bytes
    return False


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
