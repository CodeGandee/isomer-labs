from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from isomer_labs.topic_git import (
    PrivacyDisposition,
    ProjectionEntry,
    ProjectionManifest,
    compare_projection,
    fingerprint_bytes,
    inventory_projection_sources,
    materialize_projection,
    render_projection_manifest,
    render_structured_template,
    render_topic_workspace_version,
)
from isomer_labs.topic_git.projection import classify_projection_file


class TopicGitProjectionTests(unittest.TestCase):
    def test_classification_blocks_credentials_keys_signed_urls_binary_archives_and_license_ambiguity(self) -> None:
        cases = {
            "credential.txt": b"api_key=abcdefghijk",
            "private.pem": b"-----BEGIN PRIVATE KEY-----\nvalue",
            "signed.txt": b"https://example.test/object?signature=value",
            "binary.bin": b"\x00\x01\x02",
            "archive.zip": b"not-really-an-archive",
        }
        for path, content in cases.items():
            with self.subTest(path=path):
                disposition, findings = classify_projection_file(path, content)
                self.assertEqual(PrivacyDisposition.BLOCK, disposition)
                self.assertTrue(findings)
                self.assertNotIn("abcdefghijk", " ".join(finding.message for finding in findings))
        disposition, _ = classify_projection_file("source.py", b"print('safe')\n", approved_license=False)
        self.assertEqual(PrivacyDisposition.BLOCK, disposition)

    def test_git_metadata_runtime_and_pre_runtime_support_are_excluded(self) -> None:
        for path in (".git/config", "runtime/state.sqlite", ".isomer/topic-git/publication-plan.json"):
            with self.subTest(path=path):
                disposition, _ = classify_projection_file(path, b"content")
                self.assertEqual(PrivacyDisposition.EXCLUDE, disposition)

    def test_inventory_uses_explicit_semantic_roots_and_selects_components(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "topic"
            source.mkdir()
            (source / "README.md").write_text("current untracked content\n", encoding="utf-8")
            runtime = source / "runtime"
            runtime.mkdir()
            (runtime / "state.sqlite").write_bytes(b"private")
            component = source / "repos" / "topic-main"
            component.mkdir(parents=True)
            (component / "source.py").write_text("print('component')\n", encoding="utf-8")
            entries, _ = inventory_projection_sources(
                source,
                semantic_roots={
                    "topic-root": source,
                    "topic.runtime": runtime,
                    "topic.repos.main": component,
                },
                component_roots={"topic-main": component},
            )
            by_path = {entry.source_relative_path: entry for entry in entries}
            self.assertEqual(PrivacyDisposition.TRACK, by_path["README.md"].disposition)
            self.assertEqual(PrivacyDisposition.EXCLUDE, by_path["runtime/state.sqlite"].disposition)
            self.assertEqual(PrivacyDisposition.COMPONENT, by_path["repos/topic-main"].disposition)
            self.assertNotIn("repos/topic-main/source.py", by_path)

    def test_structured_placeholder_and_materialization_preserve_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "topic"
            copy = root / "copy"
            source.mkdir()
            config = source / "config.json"
            original = '{"api_key": "real-value", "endpoint": "https://example.test"}\n'
            config.write_text(original, encoding="utf-8")
            rendered = render_structured_template(original, format_name="json")
            self.assertIn("${API_KEY}", rendered)
            self.assertNotIn("real-value", rendered)
            entries = materialize_projection(
                source,
                copy,
                (
                    ProjectionEntry(
                        source_relative_path="config.json",
                        output_relative_path="config.json",
                        disposition=PrivacyDisposition.TEMPLATE,
                        source_fingerprint=fingerprint_bytes(original.encode()),
                        transformation="structured-placeholder",
                    ),
                ),
                template_outputs={"config.json": rendered.encode()},
            )
            self.assertEqual(original, config.read_text(encoding="utf-8"))
            self.assertEqual(rendered, (copy / "config.json").read_text(encoding="utf-8"))
            self.assertIsNotNone(entries[0].output_fingerprint)

    def test_copier_never_materializes_excluded_git_or_runtime_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "topic"
            copy = root / "copy"
            (source / ".git").mkdir(parents=True)
            (source / ".git" / "config").write_text("private remote", encoding="utf-8")
            (source / "runtime").mkdir()
            (source / "runtime" / "state.sqlite").write_bytes(b"private state")
            (source / "README.md").write_text("safe\n", encoding="utf-8")
            materialize_projection(
                source,
                copy,
                (
                    ProjectionEntry(".git/config", None, PrivacyDisposition.EXCLUDE, None),
                    ProjectionEntry("runtime/state.sqlite", None, PrivacyDisposition.EXCLUDE, None),
                    ProjectionEntry(
                        "README.md",
                        "README.md",
                        PrivacyDisposition.TRACK,
                        fingerprint_bytes(b"safe\n"),
                    ),
                ),
            )
            self.assertTrue((copy / "README.md").is_file())
            self.assertFalse((copy / ".git" / "config").exists())
            self.assertFalse((copy / "runtime" / "state.sqlite").exists())

    def test_four_way_comparison_handles_updates_deletions_and_conflicts(self) -> None:
        comparison = compare_projection(
            expected={
                "safe-update.txt": "new-a",
                "simultaneous.txt": "new-b",
                "new.txt": "new-c",
            },
            prior_generated={
                "safe-update.txt": "old-a",
                "simultaneous.txt": "old-b",
                "safe-delete.txt": "old-c",
                "delete-conflict.txt": "old-d",
            },
            current_copy={
                "safe-update.txt": "old-a",
                "simultaneous.txt": "manual-b",
                "safe-delete.txt": "old-c",
                "delete-conflict.txt": "manual-d",
            },
        )
        self.assertEqual(("new.txt", "safe-update.txt"), comparison.updates)
        self.assertEqual(("safe-delete.txt",), comparison.removals)
        self.assertEqual(
            {"delete-conflict.txt", "simultaneous.txt"},
            {conflict.relative_path for conflict in comparison.conflicts},
        )

    def test_sanitized_manifests_contain_no_absolute_source_paths_or_sensitive_content(self) -> None:
        manifest = ProjectionManifest(
            binding_id="binding",
            plan_id="plan",
            created_at="2026-07-23T00:00:00Z",
            entries=(
                ProjectionEntry(
                    "README.md",
                    "README.md",
                    PrivacyDisposition.TRACK,
                    "a" * 64,
                    "b" * 64,
                ),
            ),
            components=(),
        )
        rendered = render_projection_manifest(manifest)
        payload = json.loads(rendered)
        self.assertEqual("isomer-topic-git-projection-manifest.v1", payload["schema_version"])
        self.assertNotIn("/project/", rendered)
        self.assertNotIn("remote_url", rendered)
        version = render_topic_workspace_version(
            binding_id="binding",
            plan_id="plan",
            created_at="2026-07-23T00:00:00Z",
            branch_commits={"topic-owner/main": "abcdef1", "topic-workspace/main": "abcdef2"},
        )
        self.assertIn('name = "topic-owner/main"', version)
        self.assertNotIn("/project/", version)


if __name__ == "__main__":
    unittest.main()
