"""Individual-identity sanitization and publication-only reproduction views."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Iterable

from isomer_labs.topic_git.models import ResearchRecordIndexEntry


_PRIVATE_KEY_RE = re.compile(rb"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")
_CREDENTIAL_RE = re.compile(
    rb"(?i)(?:api[_-]?key|client[_-]?secret|password|access[_-]?token|auth[_-]?token)\s*[:=]\s*[\"']?[^\s\"']{8,}"
)
_CREDENTIAL_URL_RE = re.compile(rb"(?i)https?://[^/\s@]+@")
_SIGNED_URL_RE = re.compile(rb"(?i)https?://[^\s?]+\?[^\s]*(?:signature|sig|token|x-amz-credential)=")
_GITHUB_REPOSITORY_RE = re.compile(
    r"(?<![A-Za-z0-9_.-])(?:"
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
    r"|ssh://git@github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
    r"|git@github\.com:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
    r")(?![A-Za-z0-9_.-])"
)
_PERSONAL_GITHUB_SSH_RE = re.compile(
    rb"(?i)(?:ssh://(?!git@)[a-z0-9._-]+@github\.com/|(?!git@)[a-z0-9._-]+@github\.com:)"
)


@dataclass(frozen=True)
class IdentitySanitizationResult:
    content: str
    applied_fields: tuple[str, ...]


def sanitize_individual_identity(
    content: str,
    *,
    local_usernames: Iterable[str] = (),
    local_home_paths: Iterable[str] = (),
    local_hostnames: Iterable[str] = (),
    local_ip_addresses: Iterable[str] = (),
    local_git_authors: Iterable[str] = (),
    local_emails: Iterable[str] = (),
    identity_labels: Iterable[str] = (),
) -> IdentitySanitizationResult:
    """Replace supplied local identity while retaining credential-free GitHub repository provenance."""

    encoded = content.encode("utf-8")
    if (
        _PRIVATE_KEY_RE.search(encoded)
        or _CREDENTIAL_RE.search(encoded)
        or _CREDENTIAL_URL_RE.search(encoded)
        or _SIGNED_URL_RE.search(encoded)
        or _PERSONAL_GITHUB_SSH_RE.search(encoded)
    ):
        raise ValueError("Credential-like or authenticated locator content cannot be sanitized automatically.")

    protected: list[str] = []

    def protect_repository(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"\x00ISOMER_GITHUB_REPOSITORY_{len(protected) - 1}\x00"

    rendered = _GITHUB_REPOSITORY_RE.sub(protect_repository, content)
    categories = (
        ("home-path", "${RESEARCHER_HOME}", local_home_paths),
        ("git-author", "${RESEARCHER_NAME}", local_git_authors),
        ("email", "${RESEARCHER_EMAIL}", local_emails),
        ("hostname", "${LOCAL_HOST}", local_hostnames),
        ("ip-address", "${LOCAL_IP}", local_ip_addresses),
        ("username", "${RESEARCHER_USER}", local_usernames),
        ("identity-label", "${RESEARCHER_IDENTITY}", identity_labels),
    )
    applied: set[str] = set()
    substitutions = sorted(
        (
            (value, placeholder, field)
            for field, placeholder, values in categories
            for value in values
            if value
        ),
        key=lambda item: len(item[0]),
        reverse=True,
    )
    for value, placeholder, field in substitutions:
        if value in rendered:
            rendered = rendered.replace(value, placeholder)
            applied.add(field)
    for index, repository in enumerate(protected):
        rendered = rendered.replace(f"\x00ISOMER_GITHUB_REPOSITORY_{index}\x00", repository)
    return IdentitySanitizationResult(rendered, tuple(sorted(applied)))


def render_publication_readme(
    *,
    research_topic_id: str,
    title: str | None = None,
    latest_paper_path: str | None = None,
    intent_paths: Iterable[str] = (),
    environment_paths: Iterable[str] = (),
    research_index_path: str = "research-record-index.json",
    reproduction_limitations: Iterable[str] = (),
) -> str:
    """Render deterministic publication-only navigation."""

    heading = title.strip() if title and title.strip() else research_topic_id
    _assert_generated_text_safe(heading)
    index_path = _relative_path(research_index_path)
    paper_line = "Latest paper: not yet available."
    if latest_paper_path is not None:
        paper_path = _relative_path(latest_paper_path)
        paper_line = f"Latest paper: [PDF]({paper_path})"
    lines = [
        f"# {heading}",
        "",
        f"Research topic: `{research_topic_id}`",
        "",
        paper_line,
        "",
        "## Reproduction",
        "",
        f"- Research record index: [{index_path}]({index_path})",
    ]
    normalized_intent = tuple(sorted({_relative_path(path) for path in intent_paths}))
    normalized_environment = tuple(sorted({_relative_path(path) for path in environment_paths}))
    if normalized_intent:
        lines.append("- Intent: " + ", ".join(f"[{path}]({path})" for path in normalized_intent))
    if normalized_environment:
        lines.append("- Environment: " + ", ".join(f"[{path}]({path})" for path in normalized_environment))
    limitations = tuple(sorted({item.strip() for item in reproduction_limitations if item.strip()}))
    if limitations:
        lines.extend(("", "## Reproduction Limitations", ""))
        for limitation in limitations:
            _assert_generated_text_safe(limitation)
            lines.append(f"- {limitation}")
    return "\n".join(lines) + "\n"


def render_research_record_index(
    entries: Iterable[ResearchRecordIndexEntry],
    *,
    created_at: str,
    reproduction_limitations: Iterable[str] = (),
) -> str:
    """Render a sanitized portable lineage view without runtime-only state."""

    ordered = tuple(
        sorted(
            entries,
            key=lambda item: (item.semantic_id, item.record_ref, item.revision or ""),
        )
    )
    for entry in ordered:
        if re.fullmatch(r"[0-9a-f]{64}", entry.fingerprint) is None:
            raise ValueError(f"Research record fingerprint is invalid: {entry.record_ref}")
        for value in (
            entry.record_ref,
            entry.semantic_id,
            entry.state,
            entry.revision or "",
            *entry.relationships,
        ):
            _assert_generated_text_safe(value)
            if _looks_like_absolute_local_path(value):
                raise ValueError("Research record index cannot contain absolute local paths.")
    limitations = tuple(sorted({item.strip() for item in reproduction_limitations if item.strip()}))
    for limitation in limitations:
        _assert_generated_text_safe(limitation)
    payload = {
        "schema_version": "isomer-topic-git-research-record-index.v1",
        "created_at": created_at,
        "records": [entry.to_json() for entry in ordered],
        "reproduction_limitations": list(limitations),
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def _assert_generated_text_safe(value: str) -> None:
    encoded = value.encode("utf-8")
    if (
        _PRIVATE_KEY_RE.search(encoded)
        or _CREDENTIAL_RE.search(encoded)
        or _CREDENTIAL_URL_RE.search(encoded)
        or _SIGNED_URL_RE.search(encoded)
        or _PERSONAL_GITHUB_SSH_RE.search(encoded)
    ):
        raise ValueError("Generated publication text contains credential-like material.")


def _looks_like_absolute_local_path(value: str) -> bool:
    return value.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", value) is not None


def _relative_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    parts = tuple(part for part in normalized.split("/") if part)
    if (
        normalized in {"", ".", ".."}
        or normalized.startswith(("/", "../"))
        or any(part in {".", ".."} for part in parts)
    ):
        raise ValueError(f"Publication path must be a non-root relative path: {value!r}")
    return normalized
