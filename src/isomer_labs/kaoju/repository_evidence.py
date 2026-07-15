"""Validation and redaction for externally acquired repository evidence."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import re
from typing import Any
from urllib.parse import SplitResult, urlsplit, urlunsplit

from isomer_labs.workspace.path_resolution import is_grouped_topic_repo_label


REDACTED = "[redacted]"
_GIT_COMMIT_IDENTITY = re.compile(r"(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})\Z")
_CONTENT_DIGEST_IDENTITY = re.compile(r"(?:sha256:)?[0-9a-fA-F]{64}\Z")
_SENSITIVE_KEY_PARTS = (
    "authorization",
    "cookie",
    "credential",
    "env",
    "environment",
    "header",
    "password",
    "secret",
    "stderr",
    "stdout",
    "token",
)
_SENSITIVE_EXACT_KEYS = {"argv", "command", "command_line", "raw_command", "shell"}
_REDACTED_VALUES = {REDACTED, "<redacted>", "redacted", "omitted"}
_OBSERVED_AT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})\Z")


def redact_repository_evidence(value: object) -> object:
    """Return evidence with credential-bearing fields and URL secrets removed."""

    return _redact_value(value, key=None)


def repository_evidence_diagnostics(evidence: Mapping[str, Any], *, location: str) -> list[tuple[str, str, str]]:
    """Validate durable evidence for one externally verified repository."""

    diagnostics: list[tuple[str, str, str]] = []
    required_strings = (
        "semantic_label",
        "requested_locator",
        "resolved_locator",
        "observed_at",
        "relationship_basis",
    )
    for field in required_strings:
        if not _nonempty_string(evidence.get(field)):
            diagnostics.append(("repository_evidence_field_missing", f"Repository evidence requires {field}.", f"{location}.{field}"))
    observed_at = evidence.get("observed_at")
    if isinstance(observed_at, str) and _OBSERVED_AT.fullmatch(observed_at) is None:
        diagnostics.append(("repository_observation_time_invalid", "observed_at must be an ISO 8601 timestamp with a timezone.", f"{location}.observed_at"))

    semantic_label = evidence.get("semantic_label")
    if isinstance(semantic_label, str) and (semantic_label == "topic.repos.main" or not is_grouped_topic_repo_label(semantic_label)):
        diagnostics.append(
            (
                "repository_semantic_label_invalid",
                "Repository evidence requires a non-main grouped topic.repos.* semantic label.",
                f"{location}.semantic_label",
            )
        )

    for field in ("requested_locator", "resolved_locator"):
        locator = evidence.get(field)
        if isinstance(locator, str) and not _locator_is_sanitized(locator):
            diagnostics.append(
                (
                    "repository_locator_secret",
                    f"{field} must omit URL credentials, signed query parameters, and fragments.",
                    f"{location}.{field}",
                )
            )

    identity = evidence.get("immutable_identity")
    identity_value: str | None = None
    if not isinstance(identity, Mapping):
        diagnostics.append(("repository_identity_missing", "Repository evidence requires immutable_identity.", f"{location}.immutable_identity"))
    else:
        kind = identity.get("kind")
        identity_value = identity.get("value") if isinstance(identity.get("value"), str) else None
        if kind not in {"git_commit", "content_digest"}:
            diagnostics.append(
                (
                    "repository_identity_kind_invalid",
                    "immutable_identity.kind must be git_commit or content_digest.",
                    f"{location}.immutable_identity.kind",
                )
            )
        identity_pattern = _GIT_COMMIT_IDENTITY if kind == "git_commit" else _CONTENT_DIGEST_IDENTITY
        if identity_value is None or identity_pattern.fullmatch(identity_value) is None:
            diagnostics.append(
                (
                    "repository_identity_invalid",
                    "immutable_identity.value must match its kind: a full 40- or 64-character Git commit, or a 64-character SHA-256 content digest.",
                    f"{location}.immutable_identity.value",
                )
            )

    method = evidence.get("acquisition_method")
    if not isinstance(method, Mapping):
        diagnostics.append(("repository_method_missing", "Repository evidence requires acquisition_method.", f"{location}.acquisition_method"))
    else:
        for field in ("tool_class", "operation", "description"):
            if not _nonempty_string(method.get(field)):
                diagnostics.append(("repository_method_field_missing", f"acquisition_method requires {field}.", f"{location}.acquisition_method.{field}"))
        if not isinstance(method.get("options"), list):
            diagnostics.append(
                (
                    "repository_method_options_missing",
                    "acquisition_method requires an explicit list of non-secret options.",
                    f"{location}.acquisition_method.options",
                )
            )

    commands = evidence.get("command_evidence")
    if not isinstance(commands, list) or not commands:
        diagnostics.append(("repository_command_evidence_missing", "Repository evidence requires sanitized external command evidence.", f"{location}.command_evidence"))
    else:
        for index, command in enumerate(commands):
            command_location = f"{location}.command_evidence/{index}"
            if not isinstance(command, Mapping):
                diagnostics.append(("repository_command_evidence_invalid", "Command evidence entries must be objects.", command_location))
                continue
            for field in ("tool_class", "operation", "description", "status", "observed_identity"):
                if not _nonempty_string(command.get(field)):
                    diagnostics.append(("repository_command_field_missing", f"Command evidence requires {field}.", f"{command_location}.{field}"))
            if command.get("status") != "succeeded":
                diagnostics.append(("repository_verification_incomplete", "Accepted repository command evidence must report succeeded.", f"{command_location}.status"))
            observed = command.get("observed_identity")
            if identity_value is not None and isinstance(observed, str) and observed.lower() != identity_value.lower():
                diagnostics.append(
                    (
                        "repository_identity_mismatch",
                        "Command evidence observed identity does not match immutable_identity.",
                        f"{command_location}.observed_identity",
                    )
                )

    verification = evidence.get("verification")
    if not isinstance(verification, Mapping) or verification.get("status") != "verified" or not _nonempty_string(verification.get("method")):
        diagnostics.append(
            (
                "repository_verification_incomplete",
                "Accepted repository evidence requires verification.status = verified and a non-secret method description.",
                f"{location}.verification",
            )
        )

    for field in ("access", "license"):
        posture = evidence.get(field)
        if not isinstance(posture, Mapping) or not _nonempty_string(posture.get("status")) or not _nonempty_string(posture.get("basis")):
            diagnostics.append(
                (
                    "repository_posture_missing",
                    f"Repository evidence requires {field}.status and {field}.basis.",
                    f"{location}.{field}",
                )
            )

    for field in ("limitations", "blockers"):
        if not isinstance(evidence.get(field), list):
            diagnostics.append(("repository_evidence_list_missing", f"Repository evidence requires an explicit {field} list.", f"{location}.{field}"))
    if isinstance(evidence.get("blockers"), list) and evidence["blockers"]:
        diagnostics.append(("repository_evidence_blocked", "Accepted repository evidence cannot contain unresolved blockers.", f"{location}.blockers"))

    diagnostics.extend(_secret_diagnostics(evidence, location=location))
    return _deduplicate(diagnostics)


def repository_blocker_diagnostics(blocker: Mapping[str, Any], *, location: str) -> list[tuple[str, str, str]]:
    """Validate resumable evidence for an unsuccessful external repository attempt."""

    diagnostics: list[tuple[str, str, str]] = []
    for field in ("requested_locator", "acquisition_method", "command_evidence", "observed_at", "filesystem_posture", "impact", "resume_condition"):
        if blocker.get(field) in (None, "", [], {}):
            diagnostics.append(("repository_blocker_field_missing", f"Repository blocker requires {field}.", f"{location}.{field}"))
    locator = blocker.get("requested_locator")
    if isinstance(locator, str) and not _locator_is_sanitized(locator):
        diagnostics.append(("repository_locator_secret", "requested_locator must omit URL credentials, signed query parameters, and fragments.", f"{location}.requested_locator"))
    diagnostics.extend(_secret_diagnostics(blocker, location=location))
    return _deduplicate(diagnostics)


def _redact_value(value: object, *, key: str | None) -> object:
    if key is not None and _is_sensitive_key(key):
        return REDACTED
    if isinstance(value, Mapping):
        return {str(item_key): _redact_value(item_value, key=str(item_key)) for item_key, item_value in value.items()}
    if isinstance(value, list):
        return [_redact_value(item, key=key) for item in value]
    if isinstance(value, tuple):
        return [_redact_value(item, key=key) for item in value]
    if isinstance(value, str):
        return _sanitize_text(value)
    return value


def _sanitize_text(value: str) -> str:
    words = value.split()
    if not words:
        return value
    return " ".join(_sanitize_url_token(word) for word in words)


def _sanitize_url_token(value: str) -> str:
    prefix = ""
    suffix = ""
    core = value
    while core and core[0] in "(['\"":
        prefix += core[0]
        core = core[1:]
    while core and core[-1] in ").,;]'\"":
        suffix = core[-1] + suffix
        core = core[:-1]
    try:
        parsed = urlsplit(core)
    except ValueError:
        return value
    if not parsed.scheme or not parsed.netloc:
        return value
    host = parsed.hostname or ""
    if parsed.port is not None:
        host = f"{host}:{parsed.port}"
    sanitized = urlunsplit(SplitResult(parsed.scheme, host, parsed.path, "", ""))
    return f"{prefix}{sanitized}{suffix}"


def _locator_is_sanitized(value: str) -> bool:
    try:
        parsed = urlsplit(value)
    except ValueError:
        return False
    if not parsed.scheme or not parsed.netloc:
        return True
    return parsed.username is None and parsed.password is None and not parsed.query and not parsed.fragment


def _secret_diagnostics(value: object, *, location: str) -> list[tuple[str, str, str]]:
    diagnostics: list[tuple[str, str, str]] = []
    if isinstance(value, Mapping):
        for key, item in value.items():
            child_location = f"{location}.{key}"
            if _is_sensitive_key(str(key)) and not _is_redacted(item):
                diagnostics.append(
                    (
                        "repository_evidence_secret",
                        f"Sensitive repository evidence field {key!r} must be omitted or redacted.",
                        child_location,
                    )
                )
            else:
                diagnostics.extend(_secret_diagnostics(item, location=child_location))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, item in enumerate(value):
            diagnostics.extend(_secret_diagnostics(item, location=f"{location}/{index}"))
    elif isinstance(value, str) and _text_contains_secret_url(value):
        diagnostics.append(("repository_evidence_secret", "Repository evidence contains a credential-bearing or signed URL.", location))
    return diagnostics


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    return normalized in _SENSITIVE_EXACT_KEYS or any(part in normalized for part in _SENSITIVE_KEY_PARTS)


def _text_contains_secret_url(value: str) -> bool:
    for token in value.split():
        core = token.strip("()[]{}<>,;'\"")
        try:
            parsed = urlsplit(core)
        except ValueError:
            return True
        if parsed.scheme and parsed.netloc and (parsed.username is not None or parsed.password is not None or parsed.query or parsed.fragment):
            return True
    return False


def _is_redacted(value: object) -> bool:
    return isinstance(value, str) and value.strip().lower() in _REDACTED_VALUES


def _nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _deduplicate(values: list[tuple[str, str, str]]) -> list[tuple[str, str, str]]:
    return list(dict.fromkeys(values))
