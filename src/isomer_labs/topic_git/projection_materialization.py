"""Projection rendering, materialization, rescanning, and comparison."""

from __future__ import annotations

import json
import os
from pathlib import Path, PurePosixPath
import re
from typing import Iterable, Mapping, cast

import tomlkit
import yaml  # type: ignore[import-untyped]

from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.topic_git.models import (
    PrivacyDisposition,
    ProjectionEntryOrigin,
    PublicationConflict,
    PublicationContentClass,
    PublicationSelectionSettings,
)
from isomer_labs.topic_git.projection import (
    ProjectionComparison,
    ProjectionEntry,
    ProjectionFinding,
    ProjectionManifest,
    _relative_path,
    classify_projection_file,
    fingerprint_bytes,
    fingerprint_file,
    validate_projection_entries,
)


_SECRET_FIELD_RE = re.compile(
    r"(?i)(?:api[_-]?key|client[_-]?secret|password|private[_-]?key|access[_-]?token)"
)


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
    generated_outputs: Mapping[str, bytes] | None = None,
) -> tuple[ProjectionEntry, ...]:
    """Copy only approved files into the publication copy and preserve source bytes."""

    source_root = canonicalize(source_topic_workspace)
    copy_root = canonicalize(publication_copy)
    templates = dict(template_outputs or {})
    generated = dict(generated_outputs or {})
    materialized: list[ProjectionEntry] = []
    source_before: dict[str, str] = {}
    entry_list = tuple(entries)
    diagnostics = validate_projection_entries(entry_list)
    if diagnostics:
        raise ValueError("Invalid projection entries: " + "; ".join(item.message for item in diagnostics))

    for entry in entry_list:
        if entry.disposition in {PrivacyDisposition.EXCLUDE, PrivacyDisposition.COMPONENT}:
            materialized.append(entry)
            continue
        if entry.disposition is PrivacyDisposition.BLOCK:
            raise ValueError(
                "Blocked projection entry cannot be materialized: "
                f"{entry.source_relative_path or '<generated>'}"
            )
        if entry.output_relative_path is None:
            raise ValueError(
                f"Projection entry has no output path: {entry.source_relative_path or '<generated>'}"
            )
        destination = canonicalize(copy_root / entry.output_relative_path)
        if not is_within(destination, copy_root):
            raise ValueError("Projection paths must remain inside their approved roots.")
        if entry.origin is ProjectionEntryOrigin.GENERATED:
            try:
                output = generated[entry.output_relative_path]
            except KeyError as error:
                raise ValueError(
                    f"Missing approved generated output: {entry.output_relative_path}"
                ) from error
            source_content = None
        else:
            if entry.source_relative_path is None:
                raise ValueError("Source-backed projection entry has no source path.")
            source_path = canonicalize(source_root / entry.source_relative_path)
            if not is_within(source_path, source_root):
                raise ValueError("Projection paths must remain inside their approved roots.")
            if ".git" in PurePosixPath(entry.source_relative_path).parts:
                raise ValueError("Projection cannot copy Git control paths.")
            source_content = source_path.read_bytes()
            source_before[entry.source_relative_path] = fingerprint_bytes(source_content)
            if entry.disposition is PrivacyDisposition.TEMPLATE:
                try:
                    output = templates[entry.source_relative_path]
                except KeyError as error:
                    raise ValueError(
                        f"Missing approved template output: {entry.source_relative_path}"
                    ) from error
            else:
                output = source_content
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(output)
        materialized.append(
            ProjectionEntry(
                source_relative_path=entry.source_relative_path,
                output_relative_path=entry.output_relative_path,
                disposition=entry.disposition,
                source_fingerprint=(
                    fingerprint_bytes(source_content)
                    if source_content is not None
                    else None
                ),
                output_fingerprint=fingerprint_bytes(output),
                transformation=entry.transformation,
                reason=entry.reason,
                component_id=entry.component_id,
                content_class=entry.content_class,
                media_type=entry.media_type,
                origin=entry.origin,
            )
        )

    for relative, before in source_before.items():
        if fingerprint_file(source_root / relative) != before:
            raise RuntimeError(f"Source changed during publication materialization: {relative}")
    blockers = rescan_projection(copy_root, materialized)
    if blockers:
        raise ValueError(
            "Materialized projection failed privacy rescan: "
            + "; ".join(item.message for item in blockers)
        )
    return tuple(materialized)


def prune_unapproved_publication_paths(
    publication_copy: Path,
    *,
    approved_paths: Iterable[str],
    preserved_roots: Iterable[str] = (".git", ".isomer"),
) -> tuple[str, ...]:
    """Remove unapproved projected paths while preserving Git and ignored support state."""

    copy_root = canonicalize(publication_copy)
    approved = {_relative_path(path) for path in approved_paths}
    preserved = {_relative_path(path) for path in preserved_roots}

    def is_preserved(relative: str) -> bool:
        return any(
            relative == root or relative.startswith(f"{root}/")
            for root in preserved
        )

    removed: list[str] = []
    if not copy_root.exists():
        return ()
    for directory, directory_names, file_names in os.walk(
        copy_root,
        topdown=False,
        followlinks=False,
    ):
        current = Path(directory)
        for name in file_names:
            path = current / name
            relative = path.relative_to(copy_root).as_posix()
            if relative not in approved and not is_preserved(relative):
                path.unlink()
                removed.append(relative)
        for name in directory_names:
            path = current / name
            relative = path.relative_to(copy_root).as_posix()
            if is_preserved(relative):
                continue
            if path.is_symlink():
                if relative not in approved:
                    path.unlink()
                    removed.append(relative)
                continue
            if not any(
                approved_path == relative
                or approved_path.startswith(f"{relative}/")
                for approved_path in approved
            ):
                try:
                    path.rmdir()
                except OSError:
                    pass
    return tuple(sorted(removed))


def materialize_exact_projection(
    source_topic_workspace: Path,
    publication_copy: Path,
    entries: Iterable[ProjectionEntry],
    *,
    template_outputs: Mapping[str, bytes] | None = None,
    generated_outputs: Mapping[str, bytes] | None = None,
    preserved_roots: Iterable[str] = (".git", ".isomer"),
) -> tuple[tuple[ProjectionEntry, ...], tuple[str, ...]]:
    """Materialize the approved tree and remove stale unapproved projected paths."""

    materialized = materialize_projection(
        source_topic_workspace,
        publication_copy,
        entries,
        template_outputs=template_outputs,
        generated_outputs=generated_outputs,
    )
    approved = tuple(
        entry.output_relative_path
        for entry in materialized
        if entry.output_relative_path is not None
        and entry.disposition in {PrivacyDisposition.TRACK, PrivacyDisposition.TEMPLATE}
    )
    removed = prune_unapproved_publication_paths(
        publication_copy,
        approved_paths=approved,
        preserved_roots=preserved_roots,
    )
    return materialized, removed


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
                ProjectionFinding(
                    "path",
                    "error",
                    entry.source_relative_path or entry.output_relative_path,
                    "Projection output escapes the publication copy.",
                )
            )
            continue
        disposition, findings = classify_projection_file(
            entry.output_relative_path,
            output.read_bytes(),
            content_class=entry.content_class,
            selection=PublicationSelectionSettings(
                include_raw_material_bytes=(
                    entry.content_class is PublicationContentClass.RAW_MATERIAL
                ),
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
    return ProjectionComparison(
        tuple(updates),
        tuple(removals),
        tuple(unchanged),
        tuple(conflicts),
    )


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

    del plan_id, created_at
    lines = [
        'schema_version = "isomer-topic-workspace-version.v2"',
        f"binding_id = {json.dumps(binding_id)}",
        'canonical_branch = "main"',
        'history_format = "sanitized-linear.v1"',
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
        return {
            str(child_key): _template_value(child, str(child_key))
            for child_key, child in value.items()
        }
    if isinstance(value, list):
        return [_template_value(child) for child in value]
    return value
