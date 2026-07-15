from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from isomer_labs.kaoju.content import register_canonical_repository
from isomer_labs.kaoju.repository_evidence import REDACTED, redact_repository_evidence, repository_evidence_diagnostics
from isomer_labs.kaoju.survey import validate_structured_artifact


COMMIT = "a" * 40


def repository_evidence() -> dict[str, object]:
    return {
        "semantic_label": "topic.repos.sources.method",
        "requested_locator": "https://example.test/owner/method.git",
        "resolved_locator": "https://example.test/owner/method.git",
        "immutable_identity": {"kind": "git_commit", "value": COMMIT},
        "acquisition_method": {
            "tool_class": "git",
            "operation": "clone-and-checkout",
            "description": "Test-owned external Git commands acquired the selected source.",
            "options": ["selected revision", "full working tree"],
        },
        "command_evidence": [
            {
                "tool_class": "git",
                "operation": "identity-verification",
                "description": "External verification observed the selected revision.",
                "status": "succeeded",
                "observed_identity": COMMIT,
            }
        ],
        "verification": {"status": "verified", "method": "external source and revision checks"},
        "observed_at": "2026-07-15T12:00:00Z",
        "access": {"status": "available", "basis": "authorized public source"},
        "license": {"status": "unknown", "basis": "not established by acquisition"},
        "relationship_basis": "Author-linked project source.",
        "limitations": ["License review remains separate."],
        "blockers": [],
    }


class KaojuRepositoryEvidenceTests(unittest.TestCase):
    def test_valid_evidence_uses_registered_semantic_identity_shape(self) -> None:
        self.assertEqual([], repository_evidence_diagnostics(repository_evidence(), location="repository"))

    def test_identity_mismatch_and_partial_verification_are_rejected(self) -> None:
        evidence = repository_evidence()
        evidence["command_evidence"] = [
            {
                "tool_class": "git",
                "operation": "identity-verification",
                "description": "External verification found another revision.",
                "status": "failed",
                "observed_identity": "b" * 40,
            }
        ]
        evidence["verification"] = {"status": "partial", "method": "external check failed"}
        evidence["blockers"] = ["Identity mismatch"]
        codes = {code for code, _message, _location in repository_evidence_diagnostics(evidence, location="repository")}
        self.assertIn("repository_identity_mismatch", codes)
        self.assertIn("repository_verification_incomplete", codes)
        self.assertIn("repository_evidence_blocked", codes)

    def test_identity_value_must_match_the_declared_kind(self) -> None:
        evidence = repository_evidence()
        evidence["immutable_identity"] = {"kind": "content_digest", "value": COMMIT}
        codes = {code for code, _message, _location in repository_evidence_diagnostics(evidence, location="repository")}
        self.assertIn("repository_identity_invalid", codes)

        evidence["immutable_identity"] = {"kind": "content_digest", "value": "sha256:" + "b" * 64}
        evidence["command_evidence"] = [
            {
                "tool_class": "copy",
                "operation": "digest-verification",
                "description": "External verification observed the selected content digest.",
                "status": "succeeded",
                "observed_identity": "sha256:" + "b" * 64,
            }
        ]
        self.assertEqual([], repository_evidence_diagnostics(evidence, location="repository"))

    def test_redactor_removes_every_credential_bearing_command_surface(self) -> None:
        secret = "do-not-store"
        unsafe = {
            "requested_locator": f"https://user:{secret}@example.test/repo.git?X-Amz-Signature={secret}#fragment",
            "resolved_locator": "https://example.test/repo.git",
            "argv": ["git", "clone", f"https://token:{secret}@example.test/repo.git?sig={secret}"],
            "headers": {"Authorization": f"Bearer {secret}"},
            "environment": {"ACCESS_TOKEN": secret},
            "credential_helper_output": secret,
            "stdout": f"remote included {secret}",
            "stderr": f"helper returned {secret}",
        }
        redacted = redact_repository_evidence(unsafe)
        encoded = json.dumps(redacted)
        self.assertNotIn(secret, encoded)
        self.assertEqual("https://example.test/repo.git", redacted["requested_locator"])  # type: ignore[index]
        for field in ("argv", "headers", "environment", "credential_helper_output", "stdout", "stderr"):
            self.assertEqual(REDACTED, redacted[field])  # type: ignore[index]

    def test_unredacted_urls_headers_environment_and_output_are_rejected(self) -> None:
        evidence = repository_evidence()
        evidence["requested_locator"] = "https://user:password@example.test/repo.git?token=secret"
        evidence["command_evidence"] = [
            {
                "tool_class": "git",
                "operation": "identity-verification",
                "description": "External verification observed the selected revision.",
                "status": "succeeded",
                "observed_identity": COMMIT,
                "headers": {"Authorization": "Bearer secret"},
                "environment": {"TOKEN": "secret"},
                "credential_helper_output": "secret",
                "stdout": "secret",
                "stderr": "secret",
            }
        ]
        diagnostics = repository_evidence_diagnostics(evidence, location="repository")
        locations = {location for _code, _message, location in diagnostics}
        self.assertIn("repository.requested_locator", locations)
        self.assertTrue(any("headers" in location for location in locations))
        self.assertTrue(any("environment" in location for location in locations))
        self.assertTrue(any("credential_helper_output" in location for location in locations))
        self.assertTrue(any("stdout" in location for location in locations))
        self.assertTrue(any("stderr" in location for location in locations))

    def test_canonical_repository_registration_is_filesystem_only(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            repository = Path(temporary) / "provider-checkout"
            repository.mkdir()
            (repository / "README.md").write_text("provider-managed source\n", encoding="utf-8")
            content = register_canonical_repository(repository, evidence=repository_evidence())
        self.assertEqual("canonical_repository", content.locator_kind)
        self.assertEqual("isomer-canonical-repository-locator.v2", content.manifest["schema_version"])  # type: ignore[index]
        self.assertEqual("topic.repos.sources.method", content.metadata()["locator"]["semantic_label"])  # type: ignore[index]

    def test_structured_repository_records_require_complete_safe_evidence(self) -> None:
        associated = {
            "title": "Associated source",
            "summary": "Verified relationship.",
            "artifact_family": "kaoju",
            "semantic_id": "KAOJU:ASSOCIATED-SOURCE-CODE",
            "sections": {
                "source": {"paper_ref": "paper-1"},
                "repository": repository_evidence(),
                "relationship": {"status": "verified", "basis": "Author-linked project source."},
            },
        }
        library = {
            "title": "Artifact library",
            "summary": "Accepted materials.",
            "artifact_family": "kaoju",
            "semantic_id": "KAOJU:ARTIFACT-LIBRARY",
            "sections": {
                "materials": [
                    {
                        "material_id": "method",
                        "source_identity": "https://example.test/owner/method.git",
                        "source_class": "repository",
                        "content_ref": "topic.repos.sources.method",
                        "status": "ready",
                        "provenance_refs": ["associated-source-1"],
                        "repository": repository_evidence(),
                    }
                ]
            },
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name, semantic_id, payload in (
                ("associated.json", "KAOJU:ASSOCIATED-SOURCE-CODE", associated),
                ("library.json", "KAOJU:ARTIFACT-LIBRARY", library),
            ):
                path = root / name
                path.write_text(json.dumps(payload), encoding="utf-8")
                _loaded, diagnostics = validate_structured_artifact(path, semantic_id)
                self.assertEqual([], diagnostics)


if __name__ == "__main__":
    unittest.main()
