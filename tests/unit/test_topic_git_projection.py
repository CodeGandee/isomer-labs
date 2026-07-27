from __future__ import annotations

import json
import tempfile
from pathlib import Path
import unittest

from isomer_labs.topic_git import (
    PrivacyDisposition,
    ProjectionEntryOrigin,
    PUBLICATION_PROJECTION_MANIFEST_PATH,
    PUBLICATION_RESEARCH_RECORD_INDEX_PATH,
    PUBLICATION_TOPIC_WORKSPACE_VERSION_PATH,
    PublicationContentClass,
    PublicationSelectionSettings,
    ProjectionEntry,
    ProjectionManifest,
    ReferenceRepositoryBinding,
    RemoteVisibility,
    ResearchRecordIndexEntry,
    compare_projection,
    fingerprint_bytes,
    inventory_projection_sources,
    materialize_projection,
    render_publication_readme,
    render_projection_manifest,
    render_research_record_index,
    render_structured_template,
    render_topic_workspace_version,
    sanitize_individual_identity,
    validate_projection_entries,
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

    def test_semantic_raw_byte_settings_and_typed_paper_pdf(self) -> None:
        raw_default, findings = classify_projection_file(
            "materials/paper.pdf",
            b"%PDF-1.7\n",
            content_class=PublicationContentClass.RAW_MATERIAL,
        )
        self.assertEqual(PrivacyDisposition.EXCLUDE, raw_default)
        self.assertEqual("raw-material-opt-in", findings[0].code)

        raw_selected, _ = classify_projection_file(
            "records/profiler.ncu-rep",
            b"normalized output\n",
            content_class=PublicationContentClass.RAW_EXPERIMENT_OUTPUT,
            selection=PublicationSelectionSettings(include_raw_experiment_output_bytes=True),
        )
        self.assertEqual(PrivacyDisposition.TRACK, raw_selected)

        paper, _ = classify_projection_file(
            "records/paper.pdf",
            b"%PDF-1.7\n",
            content_class=PublicationContentClass.RESEARCH_RECORD,
            approved_media_type="application/pdf",
        )
        self.assertEqual(PrivacyDisposition.TRACK, paper)
        invalid_paper, invalid_findings = classify_projection_file(
            "records/paper.pdf",
            b"not a pdf",
            content_class=PublicationContentClass.RESEARCH_RECORD,
            approved_media_type="application/pdf",
        )
        self.assertEqual(PrivacyDisposition.BLOCK, invalid_paper)
        self.assertEqual("pdf-signature", invalid_findings[0].code)

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

    def test_inventory_prefers_specific_semantic_classes_and_keeps_raw_bytes_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "topic"
            intent = source / "intent"
            records = source / "records"
            raw = source / "materials"
            reference = source / "repos" / "extern" / "powerinfer"
            for directory in (intent, records, raw, reference):
                directory.mkdir(parents=True)
            (intent / "overview.md").write_text("questions\n", encoding="utf-8")
            (records / "decision.json").write_text('{"decision": "Q4 is P0"}\n', encoding="utf-8")
            (raw / "paper.txt").write_text("downloaded bytes\n", encoding="utf-8")
            (reference / "source.py").write_text("upstream\n", encoding="utf-8")
            entries, _ = inventory_projection_sources(
                source,
                semantic_roots={
                    "topic-root": source,
                    "topic.intent.overview": intent / "overview.md",
                    "topic.records.artifacts": records,
                    "custom.raw-materials": raw,
                    "topic.repos.sources.powerinfer": reference,
                },
                reference_roots={"powerinfer": reference},
                semantic_classes={"custom.raw-materials": PublicationContentClass.RAW_MATERIAL},
            )
            by_path = {entry.source_relative_path: entry for entry in entries}
            self.assertEqual(PublicationContentClass.INTENT, by_path["intent/overview.md"].content_class)
            self.assertEqual(PublicationContentClass.RESEARCH_RECORD, by_path["records/decision.json"].content_class)
            self.assertEqual(PrivacyDisposition.EXCLUDE, by_path["materials/paper.txt"].disposition)
            self.assertEqual(PrivacyDisposition.COMPONENT, by_path["repos/extern/powerinfer"].disposition)
            self.assertEqual(
                PublicationContentClass.REFERENCE_REPOSITORY,
                by_path["repos/extern/powerinfer"].content_class,
            )
            self.assertNotIn("repos/extern/powerinfer/source.py", by_path)

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

    def test_projection_entry_origins_are_explicit_and_legacy_entries_remain_readable(self) -> None:
        generated = ProjectionEntry(
            source_relative_path=None,
            output_relative_path=PUBLICATION_PROJECTION_MANIFEST_PATH,
            disposition=PrivacyDisposition.TRACK,
            source_fingerprint=None,
            origin=ProjectionEntryOrigin.GENERATED,
        )
        self.assertNotIn("source_relative_path", generated.to_json())
        self.assertEqual("generated", generated.to_json()["origin"])

        legacy = ProjectionEntry.from_json(
            {
                "source_relative_path": "pixi.toml",
                "output_relative_path": "pixi.toml",
                "disposition": "track",
                "source_fingerprint": "a" * 64,
            }
        )
        self.assertEqual(ProjectionEntryOrigin.SOURCE, legacy.origin)
        self.assertEqual("pixi.toml", legacy.output_relative_path)

        manifest = ProjectionManifest.from_json(
            {
                "schema_version": "isomer-topic-git-projection-manifest.v1",
                "binding_id": "binding",
                "plan_id": "plan",
                "created_at": "2026-07-27T00:00:00Z",
                "entries": [legacy.to_json()],
                "components": [],
            }
        )
        self.assertEqual(ProjectionEntryOrigin.SOURCE, manifest.entries[0].origin)

    def test_projection_validation_enforces_path_identity_and_reserved_overlay(self) -> None:
        findings = validate_projection_entries(
            (
                ProjectionEntry(
                    "pixi.toml",
                    "environment/pixi.toml",
                    PrivacyDisposition.TRACK,
                    "a" * 64,
                ),
                ProjectionEntry(
                    "runtime/state.sqlite",
                    "runtime/state.sqlite",
                    PrivacyDisposition.EXCLUDE,
                    None,
                ),
                ProjectionEntry(
                    ".isomer-publication/user.json",
                    ".isomer-publication/user.json",
                    PrivacyDisposition.TRACK,
                    "b" * 64,
                ),
                ProjectionEntry(
                    None,
                    "generated/control.json",
                    PrivacyDisposition.TRACK,
                    None,
                    origin=ProjectionEntryOrigin.GENERATED,
                ),
            )
        )
        self.assertEqual(
            {"path-preservation", "pathless-disposition", "reserved-source-path", "generated-path"},
            {finding.code for finding in findings},
        )

    def test_path_preserving_materialization_keeps_root_files_and_reserved_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "topic"
            copy = root / "copy"
            (source / "records").mkdir(parents=True)
            source_files = {
                "pixi.toml": "[workspace]\n",
                "pixi.lock": "version = 6\n",
                "topic-workspace.toml": 'schema_version = "v1"\n',
                ".gitignore": ".pixi/\n",
                ".gitattributes": "*.pdf binary\n",
                "records/readiness.md": "ready\n",
            }
            for relative, content in source_files.items():
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            source_entries = tuple(
                ProjectionEntry(
                    relative,
                    relative,
                    PrivacyDisposition.TRACK,
                    fingerprint_bytes(content.encode()),
                )
                for relative, content in source_files.items()
            )
            generated_entries = (
                ProjectionEntry(
                    None,
                    PUBLICATION_RESEARCH_RECORD_INDEX_PATH,
                    PrivacyDisposition.TRACK,
                    None,
                    origin=ProjectionEntryOrigin.GENERATED,
                ),
                ProjectionEntry(
                    None,
                    PUBLICATION_PROJECTION_MANIFEST_PATH,
                    PrivacyDisposition.TRACK,
                    None,
                    origin=ProjectionEntryOrigin.GENERATED,
                ),
                ProjectionEntry(
                    None,
                    PUBLICATION_TOPIC_WORKSPACE_VERSION_PATH,
                    PrivacyDisposition.TRACK,
                    None,
                    origin=ProjectionEntryOrigin.GENERATED,
                ),
            )
            generated_outputs = {
                PUBLICATION_RESEARCH_RECORD_INDEX_PATH: b"{}\n",
                PUBLICATION_PROJECTION_MANIFEST_PATH: b"{}\n",
                PUBLICATION_TOPIC_WORKSPACE_VERSION_PATH: b'schema_version = "v1"\n',
            }
            materialize_projection(
                source,
                copy,
                (*source_entries, *generated_entries),
                generated_outputs=generated_outputs,
            )
            for relative, content in source_files.items():
                self.assertEqual(content, (copy / relative).read_text(encoding="utf-8"))
                self.assertFalse((copy / "environment" / relative).exists())
            for relative in generated_outputs:
                self.assertTrue((copy / relative).is_file())

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

    def test_individual_identity_sanitization_preserves_github_repository_identity(self) -> None:
        result = sanitize_individual_identity(
            "alice used /home/alice on lab-node at 10.0.0.8; source https://github.com/alice/PowerInfer.git",
            local_usernames=("alice",),
            local_home_paths=("/home/alice",),
            local_hostnames=("lab-node",),
            local_ip_addresses=("10.0.0.8",),
        )
        self.assertNotIn("/home/alice", result.content)
        self.assertNotIn("lab-node", result.content)
        self.assertIn("${RESEARCHER_USER}", result.content)
        self.assertIn("https://github.com/alice/PowerInfer.git", result.content)
        with self.assertRaisesRegex(ValueError, "Credential-like"):
            sanitize_individual_identity("https://alice:secret@github.com/org/private.git")

    def test_publication_readme_and_research_index_are_deterministic_and_path_safe(self) -> None:
        readme = render_publication_readme(
            research_topic_id="pwinfer-analysis",
            latest_paper_path="records/artifacts/paper/pwinfer-analysis.pdf",
            intent_paths=("intent/src/topic-overview.md",),
            environment_paths=("pixi.lock", "pixi.toml"),
            reproduction_limitations=("Private reference requires organization access.",),
        )
        self.assertIn(
            "Latest paper: [PDF](records/artifacts/paper/pwinfer-analysis.pdf)",
            readme,
        )
        self.assertIn(PUBLICATION_RESEARCH_RECORD_INDEX_PATH, readme)
        no_paper = render_publication_readme(research_topic_id="pwinfer-analysis")
        self.assertIn("Latest paper: not yet available.", no_paper)
        composed = render_publication_readme(
            research_topic_id="pwinfer-analysis",
            source_readme="# Existing Topic\n\nSource-authored introduction.\n",
        )
        self.assertTrue(composed.startswith("# Existing Topic\n\nSource-authored introduction."))
        self.assertEqual(
            composed,
            render_publication_readme(
                research_topic_id="pwinfer-analysis",
                source_readme=composed,
            ),
        )

        rendered_index = render_research_record_index(
            (
                ResearchRecordIndexEntry(
                    "artifact:direction:2",
                    "KAOJU:DIRECTION-SET",
                    "accepted",
                    "b" * 64,
                    revision="2",
                ),
                ResearchRecordIndexEntry(
                    "artifact:direction:1",
                    "KAOJU:DIRECTION-SET",
                    "superseded",
                    "a" * 64,
                    revision="1",
                    relationships=("artifact:direction:2",),
                ),
            ),
            created_at="2026-07-27T00:00:00Z",
        )
        payload = json.loads(rendered_index)
        self.assertEqual("isomer-topic-git-research-record-index.v1", payload["schema_version"])
        self.assertEqual("artifact:direction:1", payload["records"][0]["record_ref"])
        with self.assertRaisesRegex(ValueError, "absolute local paths"):
            render_research_record_index(
                (
                    ResearchRecordIndexEntry(
                        "/home/alice/private.json",
                        "KAOJU:DIRECTION-SET",
                        "accepted",
                        "a" * 64,
                    ),
                ),
                created_at="2026-07-27T00:00:00Z",
            )

    def test_sanitized_manifests_contain_no_absolute_source_paths_or_sensitive_content(self) -> None:
        reference = ReferenceRepositoryBinding(
            reference_id="powerinfer",
            semantic_label="topic.repos.sources.powerinfer",
            relative_path="repos/extern/sources/powerinfer",
            remote_url="https://github.com/SJTU-IPADS/PowerInfer.git",
            commit_sha="c" * 40,
            visibility=RemoteVisibility.PUBLIC,
            license_status="Apache-2.0",
        )
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
            selection=PublicationSelectionSettings(),
            reference_repositories=(reference,),
            research_index_fingerprint="c" * 64,
            readme_fingerprint="d" * 64,
            reproduction_limitations=("Private comparison source requires access.",),
        )
        rendered = render_projection_manifest(manifest)
        payload = json.loads(rendered)
        self.assertEqual("isomer-topic-git-projection-manifest.v2", payload["schema_version"])
        self.assertFalse(payload["selection"]["include_raw_material_bytes"])
        self.assertEqual("c" * 40, payload["reference_repositories"][0]["commit_sha"])
        self.assertIn("https://github.com/SJTU-IPADS/PowerInfer.git", rendered)
        self.assertNotIn("/project/", rendered)
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
