"""Provider-neutral literature observation validation and normalization."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Iterable, Mapping
import unicodedata

from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    register_builtin_artifact_format_providers,
    validate_payload,
)
from isomer_labs.artifact_formats.research_record_formats import (
    LITERATURE_OBSERVATION_PROFILE_REF,
)
from isomer_labs.records.store import ResearchRecordError
from isomer_labs.runtime.records import StructuredResearchPayloadRecord


LITERATURE_OBSERVATION_SCHEMA_VERSION = "isomer-literature-provider-observation.v1"
PAPER_KEY_RE = re.compile(
    r"^(?:doi:[^\s]+|arxiv:[^\s]+|provider:[a-z0-9][a-z0-9._-]*:[^\s]+|title-sha256:[a-f0-9]{64})$"
)
ARXIV_VERSION_RE = re.compile(r"v[0-9]+$", re.IGNORECASE)
SECRET_KEY_NAMES = {
    "api-key",
    "api_key",
    "apikey",
    "authorization",
    "credential",
    "credentials",
    "password",
    "secret",
    "x-api-key",
    "x_api_key",
    "access-token",
    "access_token",
}
SECRET_TEXT_RE = re.compile(
    r"(?i)(?:authorization\s*:|x-api-key\s*:|api[_-]?key\s*[=:]|access[_-]?token\s*[=:]|bearer\s+[A-Za-z0-9._~+/-]{8,})"
)


def normalized_paper_key(paper: Mapping[str, object]) -> str:
    """Return the deterministic DOI, arXiv, provider-id, or title key for a paper."""

    doi = optional_string(paper.get("doi"))
    if doi is not None:
        value = doi.strip()
        for prefix in (
            "https://doi.org/",
            "http://doi.org/",
            "https://dx.doi.org/",
            "http://dx.doi.org/",
            "doi:",
        ):
            if value.lower().startswith(prefix):
                value = value[len(prefix) :]
                break
        if value:
            return f"doi:{value.lower()}"
    arxiv_id = optional_string(paper.get("arxiv_id"))
    if arxiv_id is not None:
        value = arxiv_id.strip()
        for prefix in (
            "https://arxiv.org/abs/",
            "http://arxiv.org/abs/",
            "https://arxiv.org/pdf/",
            "http://arxiv.org/pdf/",
            "arxiv:",
        ):
            if value.lower().startswith(prefix):
                value = value[len(prefix) :]
                break
        value = value.removesuffix(".pdf")
        value = ARXIV_VERSION_RE.sub("", value)
        if value:
            return f"arxiv:{value.lower()}"
    qualified_id = paper.get("provider_qualified_id")
    if isinstance(qualified_id, Mapping):
        provider = optional_string(qualified_id.get("provider"))
        provider_id = optional_string(qualified_id.get("id"))
        if provider is not None and provider_id is not None:
            return f"provider:{provider.lower()}:{provider_id}"
    title = optional_string(paper.get("title"))
    if title is not None:
        normalized_title = " ".join(unicodedata.normalize("NFKC", title).casefold().split())
        if normalized_title:
            return "title-sha256:" + hashlib.sha256(normalized_title.encode("utf-8")).hexdigest()
    raise ResearchRecordError(
        "Each normalized paper requires a DOI, arXiv id, provider-qualified id, or title.",
        code="literature_paper_identity_missing",
    )


def validate_observation_contract(
    payload: Mapping[str, object],
    *,
    attachment_base: Path,
    check_attachments: bool,
) -> None:
    """Validate provider-neutral identities, edges, and attachment safety."""

    if payload.get("schema_version") != LITERATURE_OBSERVATION_SCHEMA_VERSION:
        raise ResearchRecordError(
            f"Literature observation schema_version must be {LITERATURE_OBSERVATION_SCHEMA_VERSION}.",
            code="literature_schema_version_invalid",
        )
    secret_locations = list(_secret_locations(payload))
    if secret_locations:
        raise ResearchRecordError(
            "Literature observations must not contain credentials, authorization headers, or secret values.",
            code="literature_secret_rejected",
            payload={"secret_locations": secret_locations},
        )
    observation_id = optional_string(payload.get("observation_id"))
    if observation_id is None:
        raise ResearchRecordError(
            "Literature observation requires observation_id.",
            code="literature_observation_id_missing",
        )
    papers_raw = payload.get("papers")
    edges_raw = payload.get("citation_edges")
    if not isinstance(papers_raw, list) or not isinstance(edges_raw, list):
        raise ResearchRecordError(
            "Literature observation papers and citation_edges must be arrays.",
            code="literature_normalized_members_invalid",
        )
    paper_by_key: dict[str, Mapping[str, object]] = {}
    for index, value in enumerate(papers_raw):
        if not isinstance(value, Mapping):
            raise ResearchRecordError(
                f"Normalized paper at index {index} must be an object.",
                code="literature_paper_invalid",
            )
        declared = optional_string(value.get("paper_key"))
        expected = normalized_paper_key(value)
        if declared != expected:
            raise ResearchRecordError(
                f"Normalized paper key at papers[{index}] must be {expected!r}.",
                code="literature_paper_key_invalid",
                payload={"field": f"papers[{index}].paper_key", "expected": expected, "actual": declared},
            )
        previous = paper_by_key.get(expected)
        if previous is not None and dict(previous) != dict(value):
            raise ResearchRecordError(
                f"Conflicting normalized papers use the same key: {expected}",
                code="literature_paper_key_conflict",
            )
        paper_by_key[expected] = value
    for index, value in enumerate(edges_raw):
        if not isinstance(value, Mapping):
            raise ResearchRecordError(
                f"Citation edge at index {index} must be an object.",
                code="literature_citation_edge_invalid",
            )
        citing = optional_string(value.get("citing_paper_key"))
        cited = optional_string(value.get("cited_paper_key"))
        source = optional_string(value.get("source_observation_ref"))
        parent = optional_string(value.get("parent_seed_key"))
        missing = [key for key in (citing, cited) if key is None or key not in paper_by_key]
        if missing:
            raise ResearchRecordError(
                f"Citation edge at index {index} references a paper absent from the observation.",
                code="literature_citation_endpoint_missing",
                payload={"field": f"citation_edges[{index}]", "missing_endpoints": missing},
            )
        if source != observation_id:
            raise ResearchRecordError(
                f"Citation edge at index {index} must use source_observation_ref {observation_id!r}.",
                code="literature_citation_source_mismatch",
            )
        if parent is not None and parent not in paper_by_key:
            raise ResearchRecordError(
                f"Citation edge at index {index} has a parent seed absent from the observation: {parent}",
                code="literature_parent_seed_missing",
            )
    attachments = payload.get("raw_attachments", [])
    if not isinstance(attachments, list):
        raise ResearchRecordError(
            "raw_attachments must be an array.",
            code="literature_attachment_invalid",
        )
    if check_attachments:
        for index, attachment in enumerate(attachments):
            _validate_attachment(attachment, attachment_base=attachment_base, index=index)


def validate_observation_schema(payload: Mapping[str, object]) -> None:
    """Validate an observation against its registered Artifact Format Profile."""

    registry = ArtifactFormatRegistry()
    register_builtin_artifact_format_providers(registry)
    validation = validate_payload(
        payload,
        registry=registry,
        format_profile_ref=LITERATURE_OBSERVATION_PROFILE_REF,
    )
    if validation.ok:
        return
    raise ResearchRecordError(
        "Literature observation does not satisfy the provider-neutral schema.",
        code="literature_observation_invalid",
        payload={
            "validation_status": validation.status,
            "diagnostics": [item.to_json() for item in validation.diagnostics],
            "recovery_actions": [
                "Map provider-shaped output into isomer-literature-provider-observation.v1.",
                "Remove provider-specific wrappers, request bodies, headers, and credentials.",
            ],
        },
    )


def attachment_index_entries(raw: object, base: Path) -> list[dict[str, object]]:
    """Convert validated raw attachment declarations into record-store entries."""

    entries: list[dict[str, object]] = []
    if not isinstance(raw, list):
        return entries
    for item in raw:
        if not isinstance(item, Mapping):
            continue
        path = Path(str(item["path"]))
        selected = path if path.is_absolute() else base / path
        entries.append(
            {
                "path": str(selected.resolve(strict=False)),
                "file_role": "raw-provider-response",
                "media_type": str(item["media_type"]),
                "sha256": str(item["sha256"]),
                "redaction_posture": "redacted",
                "provenance_refs": list(string_array(item["provenance_refs"])),
            }
        )
    return entries


def read_payload_path(path: Path) -> dict[str, object]:
    """Read one provider-neutral observation payload from JSON."""

    if not path.exists() or not path.is_file():
        raise ResearchRecordError(
            f"Literature observation payload file does not exist: {path}",
            code="literature_payload_missing",
        )
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ResearchRecordError(
            f"Literature observation payload is not valid JSON: {exc.msg}",
            code="literature_payload_invalid_json",
        ) from exc
    if not isinstance(loaded, dict):
        raise ResearchRecordError(
            "Literature observation payload must be a JSON object.",
            code="literature_payload_invalid",
        )
    return loaded


def read_structured_payload(structured: StructuredResearchPayloadRecord) -> dict[str, object]:
    """Read the immutable payload represented by a structured record row."""

    if structured.payload_file_path is None:
        return dict(structured.payload_json)
    return read_payload_path(Path(structured.payload_file_path))


def mapping(value: object) -> Mapping[str, object]:
    """Require one JSON object."""

    if not isinstance(value, Mapping):
        raise ResearchRecordError(
            "Literature observation contains a malformed object.",
            code="literature_payload_invalid",
        )
    return value


def object_array(value: object) -> list[Mapping[str, object]]:
    """Require one JSON array of objects."""

    if not isinstance(value, list) or any(not isinstance(item, Mapping) for item in value):
        raise ResearchRecordError(
            "Literature observation contains a malformed object array.",
            code="literature_payload_invalid",
        )
    return [item for item in value if isinstance(item, Mapping)]


def string_array(value: object) -> list[str]:
    """Require one JSON array of strings."""

    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ResearchRecordError(
            "Literature observation contains a malformed string array.",
            code="literature_payload_invalid",
        )
    return list(value)


def optional_string(value: object) -> str | None:
    """Return a non-empty string or ``None``."""

    return value if isinstance(value, str) and value.strip() else None


def normalized_doi(value: str) -> str:
    """Normalize a DOI selector without its paper-key prefix."""

    return normalized_paper_key({"doi": value}).removeprefix("doi:")


def normalized_optional_doi(value: object) -> str | None:
    """Normalize an optional DOI value."""

    selected = optional_string(value)
    return normalized_doi(selected) if selected is not None else None


def normalized_arxiv_id(value: str) -> str:
    """Normalize an arXiv selector without its paper-key prefix."""

    return normalized_paper_key({"arxiv_id": value}).removeprefix("arxiv:")


def normalized_optional_arxiv_id(value: object) -> str | None:
    """Normalize an optional arXiv identifier."""

    selected = optional_string(value)
    return normalized_arxiv_id(selected) if selected is not None else None


def _validate_attachment(attachment: object, *, attachment_base: Path, index: int) -> None:
    if not isinstance(attachment, Mapping):
        raise ResearchRecordError(
            f"Raw attachment at index {index} must be an object.",
            code="literature_attachment_invalid",
        )
    raw_path = optional_string(attachment.get("path"))
    expected_digest = optional_string(attachment.get("sha256"))
    if raw_path is None or expected_digest is None:
        raise ResearchRecordError(
            f"Raw attachment at index {index} requires path and sha256.",
            code="literature_attachment_invalid",
        )
    path = Path(raw_path)
    path = path if path.is_absolute() else attachment_base / path
    path = path.resolve(strict=False)
    if not path.exists() or not path.is_file():
        raise ResearchRecordError(
            f"Raw provider attachment does not exist: {path}",
            code="literature_attachment_missing",
        )
    content = path.read_bytes()
    actual_digest = hashlib.sha256(content).hexdigest()
    if actual_digest != expected_digest:
        raise ResearchRecordError(
            f"Raw provider attachment checksum mismatch: {path}",
            code="literature_attachment_checksum_mismatch",
            payload={"expected": expected_digest, "actual": actual_digest},
        )
    if SECRET_TEXT_RE.search(content.decode("utf-8", errors="replace")):
        raise ResearchRecordError(
            f"Raw provider attachment contains a credential or authorization header: {path}",
            code="literature_secret_attachment_rejected",
        )


def _secret_locations(value: object, path: str = "$") -> Iterable[str]:
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}"
            if key_text.casefold() in SECRET_KEY_NAMES:
                yield child_path
            yield from _secret_locations(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _secret_locations(child, f"{path}[{index}]")
    elif isinstance(value, str) and SECRET_TEXT_RE.search(value):
        yield path
