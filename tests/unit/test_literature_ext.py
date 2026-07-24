from __future__ import annotations

import contextlib
from copy import deepcopy
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import sqlite3
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    register_builtin_artifact_format_providers,
    validate_payload,
)
from isomer_labs.artifact_formats.research_record_formats import (
    LITERATURE_OBSERVATION_PROFILE_REF,
)
from isomer_labs.records.literature import (
    LITERATURE_OBSERVATION_SCHEMA_VERSION,
    LITERATURE_QUERY_INDEX_SCHEMA_VERSION,
    normalized_paper_key,
)


FIXTURE_ROOT = Path(__file__).parents[1] / "fixtures" / "literature"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def fixture_payload(patch_name: str | None = None) -> dict[str, object]:
    payload = json.loads((FIXTURE_ROOT / "complete-observation.json").read_text(encoding="utf-8"))
    if patch_name is not None:
        changes = json.loads((FIXTURE_ROOT / patch_name).read_text(encoding="utf-8"))
        payload.update(changes)
    observation_id = payload["observation_id"]
    for edge in payload["citation_edges"]:
        edge["source_observation_ref"] = observation_id
    return payload


class LiteratureExtensionTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def make_project(self) -> Path:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "alpha"
            topic_workspace_id = "alpha"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            topic_workspace_id = "alpha"
            status = "active"

            [[topic_workspaces]]
            id = "alpha"
            research_topic_id = "alpha"
            path = "topic-workspaces/alpha"
            status = "active"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Alpha topic"
            """,
        )
        (root / "topic-workspaces" / "alpha").mkdir(parents=True)
        status, output = self.run_main(
            ["--print-json", "project", "--root", str(root), "runtime", "init", "--topic", "alpha"],
            cwd=root,
        )
        self.assertEqual(0, status, output)
        return root

    def run_main(self, args: list[str], *, cwd: Path) -> tuple[int, str]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(cwd),
            patch.dict(os.environ, {"HOME": str(cwd), "PATH": os.environ.get("PATH", "")}, clear=True),
            patch.object(socket.socket, "connect", side_effect=AssertionError("literature CLI attempted network I/O")),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(args)
        return status, stdout.getvalue()

    def run_literature(self, root: Path, args: list[str]) -> tuple[int, dict[str, object]]:
        status, output = self.run_main(
            [
                "--print-json",
                "ext",
                "research",
                "literature",
                *args,
                "--project",
                str(root),
                "--topic",
                "alpha",
            ],
            cwd=root,
        )
        return status, json.loads(output)

    def payload_file(
        self,
        root: Path,
        *,
        patch_name: str | None = None,
        duplicate_first_paper: bool = False,
    ) -> Path:
        payload = fixture_payload(patch_name)
        if duplicate_first_paper:
            papers = payload["papers"]
            assert isinstance(papers, list)
            papers.append(deepcopy(papers[0]))
        attachments = payload.get("raw_attachments")
        if isinstance(attachments, list):
            raw_copy = root / "raw-provider-response.redacted.json"
            raw_copy.write_bytes((FIXTURE_ROOT / "raw-provider-response.redacted.json").read_bytes())
            for attachment in attachments:
                if isinstance(attachment, dict):
                    attachment["path"] = str(raw_copy)
        path = root / f"{payload['observation_id']}.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return path

    def state_db(self, root: Path) -> Path:
        return root / "topic-workspaces" / "alpha" / "state.sqlite"

    def test_profile_accepts_provider_neutral_completeness_fixtures(self) -> None:
        registry = ArtifactFormatRegistry()
        register_builtin_artifact_format_providers(registry)
        for patch_name in (
            None,
            "truncated-observation.patch.json",
            "partial-observation.patch.json",
            "missing-field-observation.patch.json",
            "unresolved-record-observation.patch.json",
            "optional-raw-attachment.patch.json",
        ):
            with self.subTest(patch_name=patch_name):
                result = validate_payload(
                    fixture_payload(patch_name),
                    registry=registry,
                    format_profile_ref=LITERATURE_OBSERVATION_PROFILE_REF,
                )
                self.assertTrue(result.ok, [item.render() for item in result.diagnostics])
                self.assertEqual(LITERATURE_OBSERVATION_SCHEMA_VERSION, result.schema_version)

        for patch_name in (
            "secret-bearing-observation.patch.json",
            "provider-specific-invalid-observation.patch.json",
        ):
            with self.subTest(patch_name=patch_name):
                result = validate_payload(
                    fixture_payload(patch_name),
                    registry=registry,
                    format_profile_ref=LITERATURE_OBSERVATION_PROFILE_REF,
                )
                self.assertFalse(result.ok)

    def test_normalized_paper_key_priority_and_title_fallback_are_deterministic(self) -> None:
        self.assertEqual(
            "doi:10.1000/example",
            normalized_paper_key(
                {
                    "doi": "https://doi.org/10.1000/EXAMPLE",
                    "arxiv_id": "2401.01234v2",
                    "provider_qualified_id": {"provider": "s2", "id": "ABC"},
                    "title": "Example",
                }
            ),
        )
        self.assertEqual("arxiv:2401.01234", normalized_paper_key({"arxiv_id": "arXiv:2401.01234v2"}))
        self.assertEqual(
            "provider:semantic-scholar:ABC",
            normalized_paper_key(
                {"provider_qualified_id": {"provider": "semantic-scholar", "id": "ABC"}}
            ),
        )
        self.assertEqual(
            normalized_paper_key({"title": "A  Normalized Title"}),
            normalized_paper_key({"title": "a normalized title"}),
        )

    def test_recording_is_canonical_first_and_local_queries_are_explicit(self) -> None:
        root = self.make_project()
        db_path = self.state_db(root)
        before = hashlib.sha256(db_path.read_bytes()).hexdigest()
        status, missing = self.run_literature(root, ["papers", "query", "--doi", "10.1000/alpha"])
        self.assertEqual(1, status, missing)
        self.assertEqual("literature_projection_rebuild_required", missing["error"]["code"])
        self.assertEqual(
            "isomer-cli --print-json ext research literature index rebuild --topic alpha",
            missing["rebuild_command"],
        )
        self.assertEqual(before, hashlib.sha256(db_path.read_bytes()).hexdigest())

        payload_file = self.payload_file(root, duplicate_first_paper=True)
        status, recorded = self.run_literature(root, ["record", "--payload-file", str(payload_file)])
        self.assertEqual(0, status, recorded)
        self.assertEqual("committed", recorded["canonical_commit"]["status"])
        self.assertEqual(3, recorded["canonical_commit"]["member_counts"]["papers"])
        self.assertEqual("missing", recorded["projection"]["status"])
        self.assertFalse(recorded["projection"]["refreshed"])
        self.assertTrue(recorded["projection"]["canonical_commit_preserved"])

        with sqlite3.connect(db_path) as connection:
            lifecycle_count = connection.execute("SELECT COUNT(*) FROM lifecycle_records").fetchone()[0]
            observation_count = connection.execute(
                "SELECT COUNT(*) FROM lifecycle_records WHERE id = ?",
                ("literature-observation-complete",),
            ).fetchone()[0]
            structured_count = connection.execute(
                "SELECT COUNT(*) FROM structured_research_payloads"
            ).fetchone()[0]
            literature_tables = connection.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name LIKE 'literature_%'"
            ).fetchone()[0]
        self.assertEqual(3, lifecycle_count)
        self.assertEqual(1, observation_count)
        self.assertEqual(1, structured_count)
        self.assertEqual(0, literature_tables)

        status, listed = self.run_literature(root, ["observations", "list"])
        self.assertEqual(0, status, listed)
        self.assertEqual(1, listed["count"])
        self.assertEqual("valid", listed["observations"][0]["validation"]["status"])
        self.assertEqual("complete", listed["observations"][0]["completeness"]["status"])
        status, shown = self.run_literature(
            root,
            ["observations", "show", "literature-observation-complete"],
        )
        self.assertEqual(0, status, shown)
        self.assertEqual(
            "provider-observation:semantic-scholar:alpha-citations",
            shown["observation"]["provenance_refs"][0],
        )

        status, rebuilt = self.run_literature(root, ["index", "rebuild"])
        self.assertEqual(0, status, rebuilt)
        self.assertEqual(LITERATURE_QUERY_INDEX_SCHEMA_VERSION, rebuilt["schema_version"])
        self.assertEqual(
            {"observations": 1, "paper_occurrences": 2, "citation_edges": 1},
            rebuilt["counts"],
        )
        self.assertEqual(0, rebuilt["canonical_records_mutated"])

        status, doi_result = self.run_literature(
            root,
            ["papers", "query", "--doi", "https://doi.org/10.1000/ALPHA"],
        )
        self.assertEqual(0, status, doi_result)
        self.assertEqual(1, doi_result["count"])
        doi_id = doi_result["occurrences"][0]["occurrence_id"]
        self.assertFalse(doi_result["occurrences"][0]["canonical_record"])
        for selector in (
            ["--arxiv", "2401.01234v2"],
            ["--provider-id", "semantic-scholar:S2-BETA"],
            ["--title", "beta systems"],
            ["--year", "2024"],
            ["--observation-ref", "literature-observation-complete"],
        ):
            status, result = self.run_literature(root, ["papers", "query", *selector])
            self.assertEqual(0, status, result)
            self.assertGreaterEqual(result["count"], 1)

        status, citations = self.run_literature(
            root,
            [
                "citations",
                "query",
                "--paper-key",
                "doi:10.1000/alpha",
                "--direction",
                "forward",
            ],
        )
        self.assertEqual(0, status, citations)
        self.assertEqual(1, citations["count"])
        self.assertTrue(citations["edges"][0]["provider_reported"])
        self.assertEqual("provider-reported-not-full-text-verified", citations["edges"][0]["evidence_posture"])

        status, rebuilt_again = self.run_literature(root, ["index", "rebuild"])
        self.assertEqual(0, status, rebuilt_again)
        status, doi_result_again = self.run_literature(root, ["papers", "query", "--doi", "10.1000/alpha"])
        self.assertEqual(0, status, doi_result_again)
        self.assertEqual(doi_id, doi_result_again["occurrences"][0]["occurrence_id"])
        with sqlite3.connect(db_path) as connection:
            self.assertEqual(
                1,
                connection.execute(
                    "SELECT COUNT(*) FROM lifecycle_records WHERE id = ?",
                    ("literature-observation-complete",),
                ).fetchone()[0],
            )

        status, validated = self.run_literature(root, ["index", "validate"])
        self.assertEqual(0, status, validated)
        self.assertEqual("valid", validated["status"])

    def test_secret_and_provider_specific_payloads_are_rejected_before_commit(self) -> None:
        for patch_name, expected_code in (
            ("secret-bearing-observation.patch.json", "literature_secret_rejected"),
            ("provider-specific-invalid-observation.patch.json", "literature_observation_invalid"),
        ):
            with self.subTest(patch_name=patch_name):
                root = self.make_project()
                payload_file = self.payload_file(root, patch_name=patch_name)
                status, result = self.run_literature(
                    root,
                    ["record", "--payload-file", str(payload_file)],
                )
                self.assertEqual(1, status, result)
                self.assertEqual(expected_code, result["error"]["code"])
                with sqlite3.connect(self.state_db(root)) as connection:
                    self.assertEqual(
                        0,
                        connection.execute(
                            "SELECT COUNT(*) FROM lifecycle_records WHERE id = ?",
                            (
                                "literature-observation-secret-bearing"
                                if patch_name.startswith("secret")
                                else "literature-observation-provider-specific",
                            ),
                        ).fetchone()[0],
                    )

    def test_raw_attachment_is_checked_and_ignored_by_projection(self) -> None:
        root = self.make_project()
        payload_file = self.payload_file(root, patch_name="optional-raw-attachment.patch.json")
        status, recorded = self.run_literature(root, ["record", "--payload-file", str(payload_file)])
        self.assertEqual(0, status, recorded)
        status, rebuilt = self.run_literature(root, ["index", "rebuild"])
        self.assertEqual(0, status, rebuilt)
        self.assertEqual(2, rebuilt["counts"]["paper_occurrences"])

        raw_path = root / "raw-provider-response.redacted.json"
        raw_path.write_text('{"authorization":"Bearer forbidden-secret"}', encoding="utf-8")
        status, rebuilt_again = self.run_literature(root, ["index", "rebuild"])
        self.assertEqual(0, status, rebuilt_again)
        self.assertEqual(2, rebuilt_again["counts"]["paper_occurrences"])

    def test_projection_validation_reports_incompatible_orphan_and_digest_drift_without_repair(self) -> None:
        root = self.make_project()
        payload_file = self.payload_file(root)
        status, recorded = self.run_literature(root, ["record", "--payload-file", str(payload_file)])
        self.assertEqual(0, status, recorded)
        status, rebuilt = self.run_literature(root, ["index", "rebuild"])
        self.assertEqual(0, status, rebuilt)
        db_path = self.state_db(root)

        with sqlite3.connect(db_path) as connection:
            connection.execute(
                """
                INSERT INTO literature_observation_index
                    (
                        source_record_id, payload_digest, observation_time, action,
                        provider_name, completeness_status, payload_file_path
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "orphan-observation",
                    "sha256:orphan",
                    "2026-07-23T08:00:00Z",
                    "search-papers",
                    "example",
                    "complete",
                    None,
                ),
            )
        status, orphaned = self.run_literature(root, ["index", "validate"])
        self.assertEqual(1, status, orphaned)
        self.assertIn("orphan-observation-row", {item["code"] for item in orphaned["issues"]})

        with sqlite3.connect(db_path) as connection:
            connection.execute(
                "DELETE FROM literature_observation_index WHERE source_record_id = ?",
                ("orphan-observation",),
            )
            connection.execute(
                "UPDATE literature_projection_metadata SET schema_version = ?",
                ("isomer-literature-query-index.v999",),
            )
        before = hashlib.sha256(db_path.read_bytes()).hexdigest()
        status, incompatible = self.run_literature(root, ["papers", "query", "--year", "2024"])
        self.assertEqual(1, status, incompatible)
        self.assertEqual("incompatible", incompatible["projection"]["status"])
        self.assertEqual(before, hashlib.sha256(db_path.read_bytes()).hexdigest())

        status, rebuilt = self.run_literature(root, ["index", "rebuild"])
        self.assertEqual(0, status, rebuilt)
        with sqlite3.connect(db_path) as connection:
            stored_payload_path = Path(
                connection.execute(
                    "SELECT payload_file_path FROM structured_research_payloads WHERE record_id = ?",
                    ("literature-observation-complete",),
                ).fetchone()[0]
            )
        drifted = json.loads(stored_payload_path.read_text(encoding="utf-8"))
        drifted["summary"] = "The canonical payload file changed after its digest was committed."
        stored_payload_path.write_text(json.dumps(drifted), encoding="utf-8")
        status, drift = self.run_literature(root, ["index", "validate"])
        self.assertEqual(1, status, drift)
        issue_codes = {item["code"] for item in drift["issues"]}
        self.assertIn("source-observation-invalid", issue_codes)
        self.assertIn("projection-stale", issue_codes)
        with sqlite3.connect(db_path) as connection:
            self.assertEqual(
                1,
                connection.execute(
                    "SELECT COUNT(*) FROM lifecycle_records WHERE id = ?",
                    ("literature-observation-complete",),
                ).fetchone()[0],
            )


if __name__ == "__main__":
    unittest.main()
