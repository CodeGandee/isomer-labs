"""Canonical uppercase extension artifact identities."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import PurePosixPath
import re
from typing import Iterable

from isomer_labs.skills.system_assets import iter_system_skill_extensions


ARTIFACT_IDENTITY_PATTERN = r"^[A-Z0-9]+(?:-[A-Z0-9]+)*:[A-Z0-9]+(?:-[A-Z0-9]+)*$"
ARTIFACT_IDENTITY_RE = re.compile(
    r"^(?P<namespace>[A-Z0-9]+(?:-[A-Z0-9]+)*):(?P<what>[A-Z0-9]+(?:-[A-Z0-9]+)*)$"
)


class ArtifactIdentityError(ValueError):
    """Raised when an extension artifact identity violates its contract."""

    def __init__(
        self,
        message: str,
        *,
        code: str,
        value: str,
        expected_extension: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.value = value
        self.expected_extension = expected_extension
        self.expected_namespace = expected_extension.upper() if expected_extension is not None else None


@dataclass(frozen=True)
class ArtifactIdentity:
    """Parsed canonical extension artifact identity."""

    namespace: str
    what: str

    @property
    def extension_id(self) -> str:
        """Return the lowercase catalog id that owns this namespace."""

        return self.namespace.lower()

    @property
    def value(self) -> str:
        """Return the exact canonical serialized identity."""

        return f"{self.namespace}:{self.what}"


def parse_artifact_identity(
    value: str,
    *,
    expected_extension: str | None = None,
    known_extensions: Iterable[str] | None = None,
) -> ArtifactIdentity:
    """Parse one canonical identity and optionally enforce catalog ownership."""

    match = ARTIFACT_IDENTITY_RE.fullmatch(value)
    if match is None:
        raise ArtifactIdentityError(
            "Artifact identity must use exact uppercase EXTENSION-NAME:WHAT syntax.",
            code="invalid_artifact_identity",
            value=value,
            expected_extension=expected_extension,
        )
    identity = ArtifactIdentity(match.group("namespace"), match.group("what"))
    if expected_extension is not None and identity.namespace != expected_extension.upper():
        raise ArtifactIdentityError(
            f"Artifact identity {value!r} belongs to namespace {identity.namespace!r}, expected {expected_extension.upper()!r}.",
            code="artifact_identity_extension_mismatch",
            value=value,
            expected_extension=expected_extension,
        )
    if known_extensions is not None and identity.extension_id not in frozenset(known_extensions):
        raise ArtifactIdentityError(
            f"Artifact identity {value!r} uses unknown packaged namespace {identity.namespace!r}.",
            code="unknown_artifact_identity_extension",
            value=value,
            expected_extension=expected_extension,
        )
    return identity


def valid_artifact_identity(value: str) -> bool:
    """Return whether a value uses canonical uppercase artifact identity syntax."""

    return ARTIFACT_IDENTITY_RE.fullmatch(value) is not None


@lru_cache(maxsize=1)
def packaged_extension_ids() -> frozenset[str]:
    """Return lowercase manifest-owned packaged extension identifiers."""

    return frozenset(extension.extension_id for extension in iter_system_skill_extensions())


@lru_cache(maxsize=1)
def packaged_extension_namespaces() -> frozenset[str]:
    """Return uppercase artifact namespaces projected from the manifest."""

    return frozenset(extension_id.upper() for extension_id in packaged_extension_ids())


@lru_cache(maxsize=1)
def packaged_extension_skill_owners() -> dict[str, str]:
    """Return packaged skill names mapped to lowercase extension ids."""

    owners: dict[str, str] = {}
    for extension in iter_system_skill_extensions():
        skill_names = {
            extension.entry_skill,
            *extension.protected_members,
            *extension.legacy_aliases,
            *(PurePosixPath(skill_path).name for skill_path in extension.skills),
        }
        for skill_name in skill_names:
            prior = owners.setdefault(skill_name, extension.extension_id)
            if prior != extension.extension_id:
                raise ArtifactIdentityError(
                    f"Packaged skill {skill_name!r} is owned by both {prior!r} and {extension.extension_id!r}.",
                    code="duplicate_artifact_identity_skill_owner",
                    value=skill_name,
                )
    return owners


def extension_id_for_skill(skill_name: str | None) -> str | None:
    """Return the lowercase manifest extension that owns a packaged skill."""

    if not skill_name:
        return None
    return packaged_extension_skill_owners().get(skill_name)


def extension_namespace_for_skill(skill_name: str | None) -> str | None:
    """Return the uppercase artifact namespace that owns a packaged skill."""

    extension_id = extension_id_for_skill(skill_name)
    return extension_id.upper() if extension_id is not None else None
