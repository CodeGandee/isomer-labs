from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.content import DIRECTORY_MANIFEST_NAME
from isomer_labs.kaoju.template_support import _replace_directory
from isomer_labs.models import SelectionRequest
from isomer_labs.project import discover_project
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.project.validation import build_project_state
from isomer_labs.runtime.store import WorkspaceRuntimeStore


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class KaojuNamedTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = os.environ.get("PATH", "")
        _write(
            self.root / ".isomer-labs/manifest.toml",
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
        _write(
            self.root / ".isomer-labs/research-topics/alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Alpha survey"
            """,
        )
        _write(self.root / "topic-workspaces/alpha/isomer-topic-workspace-summary.md", "# Alpha\n")
        status, payload = self.run_cli("project", "--root", str(self.root), "runtime", "init", "--topic", "alpha")
        self.assertEqual(0, status, payload)

    def run_cli(self, *arguments: str) -> tuple[int, dict[str, object]]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(self.root),
            patch.dict(os.environ, {"HOME": str(self.root), "PATH": self.path}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(["--print-json", *arguments])
        return status, json.loads(stdout.getvalue())

    def template(self, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli(
            "ext",
            "kaoju",
            "paper",
            "template",
            *arguments,
            "--project",
            str(self.root),
            "--topic",
            "alpha",
        )

    def prepared_tree(self, name: str, body: str = "# Paper\n") -> Path:
        root = self.root / "prepared" / name
        _write(root / "paper/index.md", body)
        _write(root / "myst.yml", "project:\n  title: Fixture\n")
        _write(root / "guidance/README.md", "Use the selected entrypoint.\n")
        return root

    def context(self):
        project, diagnostics = discover_project(cwd=self.root, env={}, project_selector=str(self.root))
        self.assertIsNotNone(project, [item.message for item in diagnostics])
        assert project is not None
        context, diagnostics = resolve_effective_topic_context(
            build_project_state(project),
            SelectionRequest(research_topic_id="alpha"),
            cwd=self.root,
            env={},
        )
        self.assertIsNotNone(context, [item.message for item in diagnostics])
        return context

    def create_generic_record(
        self,
        record_id: str,
        semantic_id: str,
        *,
        body_file: Path | None = None,
        status: str = "ready",
        metadata: dict[str, object] | None = None,
        scope_key: str | None = None,
    ) -> dict[str, object]:
        arguments = [
            "ext",
            "research",
            "records",
            "create",
            "--id",
            record_id,
            "--record-kind",
            "artifact",
            "--semantic-id",
            semantic_id,
            "--status",
            status,
        ]
        if body_file is None:
            arguments.extend(("--body", f"fixture {record_id}"))
        else:
            arguments.extend(("--body-file", str(body_file), "--content-name", body_file.name))
        if metadata is not None:
            arguments.extend(("--metadata-json", json.dumps(metadata)))
        if scope_key is not None:
            arguments.extend(("--scope-key", scope_key))
        arguments.extend(("--project", str(self.root), "--topic", "alpha"))
        status_code, payload = self.run_cli(*arguments)
        self.assertEqual(0, status_code, payload)
        return payload

    def create_main(self) -> dict[str, object]:
        tree = self.prepared_tree("main-v1")
        metadata = self.root / "prepared/main-metadata.json"
        _write(metadata, json.dumps({"entrypoint": "paper/index.md", "use_guidance": "Use the paper entrypoint.", "extensions": {"fixture": {"mode": "survey"}}}) + "\n")
        status, payload = self.template("create", "--name", "main", "--from", str(tree), "--metadata-file", str(metadata), "--actor", "agent:test")
        self.assertEqual(0, status, payload)
        return payload

    def test_mutable_update_keeps_one_stable_record_and_rejects_stale_state(self) -> None:
        created = self.create_main()
        stable_ref = created["stable_ref"]
        token = str(created["state_token"])
        replacement = self.prepared_tree("main-v2", "# Revised paper\n")

        status, stale = self.template("update", "--name", "main", "--from", str(replacement), "--expected-state", "wrong", "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_state_stale", stale["error"]["code"])

        status, updated = self.template("update", "--name", "main", "--from", str(replacement), "--expected-state", token, "--actor", "agent:test", "--change-summary", "Adopt revised tree.")
        self.assertEqual(0, status, updated)
        self.assertEqual(stable_ref, updated["stable_ref"])
        self.assertNotEqual(token, updated["state_token"])
        self.assertNotEqual(created["tree_digest"], updated["tree_digest"])

        status, listed = self.template("list")
        self.assertEqual(0, status, listed)
        self.assertEqual(1, listed["count"])
        self.assertEqual(stable_ref, listed["templates"][0]["stable_ref"])

        status, records = self.run_cli("project", "--root", str(self.root), "artifacts", "list", "--semantic-id", "KAOJU:PAPER-TEMPLATE-MYST", "--topic", "alpha")
        self.assertEqual(0, status, records)
        self.assertEqual(1, records["count"])
        record = records["records"][0]
        self.assertNotIn("revision_of_record_id", record["transition_metadata"])
        self.assertNotIn("supersedes_record_id", record["transition_metadata"])

    def test_named_copy_and_exact_replacement_remain_independent(self) -> None:
        created = self.create_main()
        status, copied = self.template("create", "--name", "main-before-change", "--from-template", "main", "--actor", "agent:test")
        self.assertEqual(0, status, copied)
        self.assertNotEqual(created["stable_ref"], copied["stable_ref"])
        self.assertEqual(created["tree_digest"], copied["tree_digest"])

        changed = self.prepared_tree("main-changed", "# Changed main\n")
        status, updated = self.template("update", "--name", "main", "--from", str(changed), "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(0, status, updated)
        status, copy_state = self.template("show", "--name", "main-before-change")
        self.assertEqual(0, status, copy_state)
        self.assertEqual(copied["tree_digest"], copy_state["template"]["tree_digest"])

        status, restored = self.template("update", "--name", "main", "--from-template", "main-before-change", "--expected-state", str(updated["state_token"]), "--actor", "agent:test")
        self.assertEqual(0, status, restored)
        self.assertEqual(copied["tree_digest"], restored["tree_digest"])
        status, copy_after = self.template("show", "--name", "main-before-change")
        self.assertEqual(0, status, copy_after)
        self.assertEqual(copy_state["template"]["state_token"], copy_after["template"]["state_token"])

    def test_file_metadata_and_export_exchange(self) -> None:
        created = self.create_main()
        token = str(created["state_token"])
        extra = self.root / "prepared/extra.md"
        _write(extra, "Additional guidance.\n")
        status, put = self.template("file", "put", "--name", "main", "--path", "guidance/extra.md", "--from", str(extra), "--expected-state", token, "--actor", "agent:test")
        self.assertEqual(0, status, put)

        patch_file = self.root / "prepared/patch.json"
        _write(patch_file, json.dumps({"use_guidance": "Updated guidance."}) + "\n")
        status, patched = self.template("metadata", "patch", "--name", "main", "--patch-file", str(patch_file), "--expected-state", str(put["state_token"]), "--actor", "agent:test")
        self.assertEqual(0, status, patched)
        self.assertEqual("Updated guidance.", patched["authored_metadata"]["use_guidance"])

        status, exported = self.template("export", "--actor", "agent:test")
        self.assertEqual(0, status, exported)
        target = self.root / "topic-workspaces/alpha/intent/derived/writing-template/main"
        self.assertEqual(str(target), exported["target"])
        self.assertTrue((target / ".isomer-template-export.json").is_file())
        self.assertTrue((target / "paper/index.md").is_file())

        status, exports = self.template("exports")
        self.assertEqual(0, status, exports)
        self.assertEqual("unchanged", exports["exports"][0]["posture"])
        _write(target / "paper/index.md", "# Locally edited paper\n")
        status, edited = self.template("exports")
        self.assertEqual(0, status, edited)
        self.assertEqual("edited", edited["exports"][0]["posture"])
        status, refused = self.template("export", "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_export_edited", refused["error"]["code"])

        status, observed = self.template("export", "--name", "main", "--target", str(target), "--observe", "--actor", "agent:test")
        self.assertEqual(0, status, observed)
        self.assertFalse(observed["canonical"])
        status, canonical = self.template("show", "--name", "main")
        self.assertEqual(0, status, canonical)
        self.assertEqual(patched["state_token"], canonical["template"]["state_token"])

    def test_file_remove_metadata_guards_and_audit_evidence(self) -> None:
        created = self.create_main()
        status, removed = self.template(
            "file",
            "remove",
            "--name",
            "main",
            "--path",
            "guidance/README.md",
            "--expected-state",
            str(created["state_token"]),
            "--actor",
            "agent:test",
            "--source-ref",
            "artifact:user-edit",
        )
        self.assertEqual(0, status, removed)

        protected_patch = self.root / "prepared/protected-patch.json"
        _write(protected_patch, json.dumps({"state_token": "forged"}) + "\n")
        status, protected = self.template("metadata", "patch", "--name", "main", "--patch-file", str(protected_patch), "--expected-state", str(removed["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_metadata_protected", protected["error"]["code"])

        invalid_entrypoint = self.root / "prepared/invalid-entrypoint.json"
        _write(invalid_entrypoint, json.dumps({"entrypoint": "missing.md"}) + "\n")
        status, invalid = self.template("metadata", "patch", "--name", "main", "--patch-file", str(invalid_entrypoint), "--expected-state", str(removed["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_entrypoint_missing", invalid["error"]["code"])

        valid_patch = self.root / "prepared/valid-patch.json"
        _write(valid_patch, json.dumps({"entrypoint": "paper/index.md", "extensions": {"fixture": {"enabled": True}}}) + "\n")
        status, patched = self.template("metadata", "patch", "--name", "main", "--patch-file", str(valid_patch), "--expected-state", str(removed["state_token"]), "--actor", "agent:test", "--change-summary", "Select the paper entrypoint.")
        self.assertEqual(0, status, patched)
        self.assertEqual("paper/index.md", patched["authored_metadata"]["entrypoint"])

        status, stale = self.template("file", "remove", "--name", "main", "--path", "myst.yml", "--expected-state", str(removed["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_state_stale", stale["error"]["code"])

        status, audits = self.run_cli("project", "--root", str(self.root), "artifacts", "list", "--semantic-id", "KAOJU:PAPER-TEMPLATE-MUTATION-AUDIT", "--topic", "alpha")
        self.assertEqual(0, status, audits)
        self.assertEqual(3, audits["count"])
        patched_audit = next(item for item in audits["records"] if item["transition_metadata"]["mutation"]["operation"] == "metadata-patch")
        event = json.loads(Path(str(patched_audit["content_path"])).read_text(encoding="utf-8"))
        self.assertEqual("main", event["template_name"])
        self.assertEqual("agent:test", event["actor"])
        self.assertEqual("metadata-patch", event["operation"])
        self.assertEqual(removed["state_token"], event["prior_state_token"])
        self.assertEqual(patched["state_token"], event["state_token"])
        self.assertEqual(removed["tree_digest"], event["prior_tree_digest"])
        self.assertEqual(patched["tree_digest"], event["tree_digest"])
        self.assertNotIn("prior_content", event)
        self.assertNotIn("prior_bytes", event)

    def test_reference_safe_archive_and_delete(self) -> None:
        created = self.create_main()
        stable_ref = str(created["stable_ref"])
        self.create_generic_record(
            "artifact-paper-draft-fixture",
            "KAOJU:PAPER-DRAFT-MYST",
            metadata={"template_ref": stable_ref, "template_name": "main", "observed_template_digest": created["tree_digest"]},
        )

        status, referenced = self.template("archive", "--name", "main", "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_referenced", referenced["error"]["code"])
        self.assertIn("artifact-paper-draft-fixture", referenced["error"]["message"])

        status, archived_draft = self.run_cli("ext", "research", "records", "delete", "artifact-paper-draft-fixture", "--reason", "fixture complete", "--project", str(self.root), "--topic", "alpha")
        self.assertEqual(0, status, archived_draft)
        status, archived = self.template("archive", "--name", "main", "--expected-state", str(created["state_token"]), "--actor", "agent:test", "--reason", "No longer active.")
        self.assertEqual(0, status, archived)
        self.assertEqual("archived", archived["status"])

        status, stale = self.template("delete", "--name", "main", "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_state_stale", stale["error"]["code"])
        status, deleted = self.template("delete", "--name", "main", "--expected-state", str(archived["state_token"]), "--actor", "agent:test")
        self.assertEqual(0, status, deleted)
        self.assertEqual("deleted", deleted["status"])
        status, missing = self.template("show", "--name", "main")
        self.assertEqual(1, status)
        self.assertEqual("template_not_found", missing["error"]["code"])

        status, audits = self.run_cli("project", "--root", str(self.root), "artifacts", "list", "--semantic-id", "KAOJU:PAPER-TEMPLATE-MUTATION-AUDIT", "--topic", "alpha")
        self.assertEqual(0, status, audits)
        operations = {record["transition_metadata"]["mutation"]["operation"] for record in audits["records"]}
        self.assertEqual({"create", "archive", "delete"}, operations)

    def test_precommit_failure_rolls_back_and_postcommit_index_failure_is_diagnostic(self) -> None:
        created = self.create_main()
        replacement = self.prepared_tree("atomic-v2", "# Atomic replacement\n")
        manifests_before = {path.resolve() for path in self.root.rglob(DIRECTORY_MANIFEST_NAME)}
        original_upsert = WorkspaceRuntimeStore.upsert_lifecycle_record

        def fail_audit(store: WorkspaceRuntimeStore, record) -> None:
            if record.transition_metadata.get("semantic_id") == "KAOJU:PAPER-TEMPLATE-MUTATION-AUDIT":
                raise KaojuServiceError("injected_partial_write", "Injected audit write failure.")
            original_upsert(store, record)

        with patch.object(WorkspaceRuntimeStore, "upsert_lifecycle_record", new=fail_audit):
            status, failed = self.template("update", "--name", "main", "--from", str(replacement), "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("injected_partial_write", failed["error"]["code"])
        status, unchanged = self.template("show", "--name", "main")
        self.assertEqual(0, status, unchanged)
        self.assertEqual(created["state_token"], unchanged["template"]["state_token"])
        self.assertEqual(manifests_before, {path.resolve() for path in self.root.rglob(DIRECTORY_MANIFEST_NAME)})

        with patch("isomer_labs.kaoju.template_state.refresh_query_index_for_record", side_effect=RuntimeError("injected index outage")):
            status, committed = self.template("update", "--name", "main", "--from", str(replacement), "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(0, status, committed)
        self.assertTrue(committed["diagnostics"])
        self.assertTrue(all(item["code"] == "query_index_refresh_failed" for item in committed["diagnostics"]))
        status, current = self.template("show", "--name", "main")
        self.assertEqual(0, status, current)
        self.assertEqual(committed["state_token"], current["template"]["state_token"])
        self.assertEqual(committed["tree_digest"], current["template"]["tree_digest"])

    def test_export_postures_digest_exclusion_refresh_and_unrecognized_refusal(self) -> None:
        created = self.create_main()
        status, exported = self.template("export", "--actor", "agent:test")
        self.assertEqual(0, status, exported)
        target = Path(str(exported["target"]))
        metadata_path = target / ".isomer-template-export.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["actor"] = "agent:metadata-only-edit"
        _write(metadata_path, json.dumps(metadata, indent=2, sort_keys=True) + "\n")
        status, unchanged = self.template("exports")
        self.assertEqual(0, status, unchanged)
        self.assertEqual("unchanged", unchanged["exports"][0]["posture"])

        replacement = self.prepared_tree("canonical-changed", "# Canonical v2\n")
        status, updated = self.template("update", "--name", "main", "--from", str(replacement), "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(0, status, updated)
        status, changed = self.template("exports")
        self.assertEqual(0, status, changed)
        self.assertEqual("canonical-changed", changed["exports"][0]["posture"])

        status, refreshed = self.template("export", "--actor", "agent:test")
        self.assertEqual(0, status, refreshed)
        self.assertEqual("# Canonical v2\n", (target / "paper/index.md").read_text(encoding="utf-8"))
        self.assertFalse(any(path.name.startswith("v000") for path in target.parent.iterdir()))
        status, clean = self.template("exports")
        self.assertEqual(0, status, clean)
        self.assertEqual("unchanged", clean["exports"][0]["posture"])

        shutil.rmtree(target)
        status, missing = self.template("exports")
        self.assertEqual(0, status, missing)
        self.assertEqual("missing", missing["exports"][0]["posture"])
        status, restored = self.template("export", "--actor", "agent:test")
        self.assertEqual(0, status, restored)

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["canonical_ref"] = "artifact:wrong-template"
        _write(metadata_path, json.dumps(metadata) + "\n")
        status, invalid = self.template("exports")
        self.assertEqual(0, status, invalid)
        self.assertEqual("identity-invalid", invalid["exports"][0]["posture"])
        status, refused = self.template("export", "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_export_identity_invalid", refused["error"]["code"])

        unrecognized = self.root / "prepared/unrecognized-export"
        _write(unrecognized / "notes.md", "unrecognized\n")
        status, refused = self.template("export", "--name", "main", "--target", str(unrecognized), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_export_target_unrecognized", refused["error"]["code"])

    def test_multiple_edited_exports_remain_explicit_ambiguity_candidates(self) -> None:
        created = self.create_main()
        status, copied = self.template("create", "--name", "alternate", "--from-template", "main", "--actor", "agent:test")
        self.assertEqual(0, status, copied)
        status, main_export = self.template("export", "--name", "main", "--actor", "agent:test")
        self.assertEqual(0, status, main_export)
        status, alternate_export = self.template("export", "--name", "alternate", "--actor", "agent:test")
        self.assertEqual(0, status, alternate_export)
        _write(Path(str(main_export["target"])) / "paper/index.md", "# Edited main\n")
        _write(Path(str(alternate_export["target"])) / "paper/index.md", "# Edited alternate\n")

        status, exports = self.template("exports")
        self.assertEqual(0, status, exports)
        edited = [item for item in exports["exports"] if item["posture"] == "edited"]
        self.assertEqual(2, len(edited))
        self.assertEqual({"main", "alternate"}, {item["name"] for item in edited})
        status, canonical = self.template("show", "--name", "main")
        self.assertEqual(0, status, canonical)
        self.assertEqual(created["state_token"], canonical["template"]["state_token"])

    def test_migration_wraps_one_current_file_and_preserves_legacy_state(self) -> None:
        source = self.root / "prepared/legacy-template.md"
        _write(source, "# Legacy template\n")
        current = self.create_generic_record(
            "artifact-legacy-paper-template-current",
            "KAOJU:PAPER-TEMPLATE-MYST",
            body_file=source,
            scope_key="paper-main",
            metadata={"paper_line": "paper-main"},
        )
        historical_source = self.root / "prepared/legacy-template-old.md"
        _write(historical_source, "# Historical template\n")
        self.create_generic_record(
            "artifact-legacy-paper-template-old",
            "KAOJU:PAPER-TEMPLATE-MYST",
            body_file=historical_source,
            status="archived",
            scope_key="paper-main",
            metadata={"revision_of_record_id": "artifact-legacy-paper-template-current"},
        )
        versioned_export = self.root / "topic-workspaces/alpha/exports/kaoju-paper/main/v0001"
        _write(versioned_export / "template.md", "historical export\n")
        legacy_latex = self.root / "topic-workspaces/alpha/intent/derived/writing-template/latex-old"
        _write(legacy_latex / "main.tex", "legacy latex\n")

        status, inspection = self.template("migrate")
        self.assertEqual(0, status, inspection)
        self.assertEqual(1, len(inspection["active_candidates"]))
        candidate = inspection["active_candidates"][0]
        self.assertEqual(current["record"]["id"], candidate["record_id"])
        self.assertRegex(str(candidate["digest"]), r"^sha256:[0-9a-f]{64}$")
        self.assertEqual(["artifact-legacy-paper-template-old"], inspection["historical_record_ids"])
        self.assertEqual([str(versioned_export)], inspection["versioned_export_paths"])
        self.assertEqual([str(legacy_latex)], inspection["legacy_latex_paths"])

        status, migrated = self.template("migrate", "--apply", "--actor", "agent:test")
        self.assertEqual(0, status, migrated)
        self.assertEqual("main", migrated["name"])
        self.assertEqual("artifact-legacy-paper-template-current", migrated["legacy_record_id"])
        status, shown = self.template("show", "--name", "main")
        self.assertEqual(0, status, shown)
        canonical_root = Path(str(shown["template"]["content_path"])).parent
        self.assertEqual("# Legacy template\n", (canonical_root / source.name).read_text(encoding="utf-8"))
        self.assertTrue(versioned_export.is_dir())
        self.assertTrue((legacy_latex / "main.tex").is_file())
        status, legacy = self.run_cli("ext", "research", "records", "show", "artifact-legacy-paper-template-current", "--include-body", "--project", str(self.root), "--topic", "alpha")
        self.assertEqual(0, status, legacy)
        self.assertEqual("# Legacy template\n", legacy["body"])

    def test_migration_requires_explicit_choices_for_multiple_or_ambiguous_candidates(self) -> None:
        first_source = self.root / "prepared/legacy-a.md"
        second_source = self.root / "prepared/legacy-b.md"
        _write(first_source, "# Legacy A\n")
        _write(second_source, "# Legacy B\n")
        self.create_generic_record("artifact-legacy-a", "KAOJU:PAPER-TEMPLATE-MYST", body_file=first_source, scope_key="paper-a")
        self.create_generic_record("artifact-legacy-b", "KAOJU:PAPER-TEMPLATE-MYST", body_file=second_source, scope_key="paper-b")

        status, ambiguous = self.template("migrate", "--apply", "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_migration_ambiguous", ambiguous["error"]["code"])
        status, first = self.template("migrate", "--apply", "--record", "artifact-legacy-a", "--name", "venue-a", "--actor", "agent:test")
        self.assertEqual(0, status, first)
        status, second = self.template("migrate", "--apply", "--record", "artifact-legacy-b", "--name", "venue-b", "--actor", "agent:test")
        self.assertEqual(0, status, second)
        status, listed = self.template("list")
        self.assertEqual(0, status, listed)
        self.assertEqual({"venue-a", "venue-b"}, {item["name"] for item in listed["templates"]})

        manifest_source = self.root / "prepared" / DIRECTORY_MANIFEST_NAME
        _write(manifest_source, "{}\n")
        ambiguous_record = self.create_generic_record("artifact-legacy-ambiguous", "KAOJU:PAPER-TEMPLATE-MYST", body_file=manifest_source, scope_key="paper-ambiguous")
        content_path = Path(str(ambiguous_record["record"]["content_path"]))
        _write(content_path.parent / "first.md", "# First\n")
        _write(content_path.parent / "second.md", "# Second\n")
        status, blocked = self.template("migrate", "--apply", "--record", "artifact-legacy-ambiguous", "--name", "ambiguous", "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_migration_entrypoint_ambiguous", blocked["error"]["code"])

    def test_path_safety_reserved_files_and_symlinks_are_rejected(self) -> None:
        tree = self.prepared_tree("unsafe")
        _write(tree / ".isomer-template-export.json", "{}\n")
        status, reserved = self.template("create", "--name", "main", "--from", str(tree), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_reserved_file", reserved["error"]["code"])

        (tree / ".isomer-template-export.json").unlink()
        (tree / "linked.md").symlink_to(tree / "paper/index.md")
        status, linked = self.template("create", "--name", "main", "--from", str(tree), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_symlink_forbidden", linked["error"]["code"])

        (tree / "linked.md").unlink()
        status, invalid_name = self.template("create", "--name", "../main", "--from", str(tree), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_name_invalid", invalid_name["error"]["code"])

        safe_tree = self.prepared_tree("safe-main")
        status, created = self.template("create", "--name", "main", "--from", str(safe_tree), "--actor", "agent:test")
        self.assertEqual(0, status, created)
        source = self.root / "prepared/path-source.md"
        _write(source, "path source\n")
        status, traversal = self.template("file", "put", "--name", "main", "--path", "../escape.md", "--from", str(source), "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_path_invalid", traversal["error"]["code"])
        status, reserved_file = self.template("file", "put", "--name", "main", "--path", ".isomer-template-export.json", "--from", str(source), "--expected-state", str(created["state_token"]), "--actor", "agent:test")
        self.assertEqual(1, status)
        self.assertEqual("template_reserved_file", reserved_file["error"]["code"])

    def test_working_directory_swap_restores_target_after_partial_failure(self) -> None:
        parent = self.root / "atomic-export"
        staged = parent / "staged"
        target = parent / "target"
        _write(staged / "paper.md", "new\n")
        _write(target / "paper.md", "old\n")
        original_replace = os.replace

        def fail_staged_swap(source, destination) -> None:
            if Path(source) == staged and Path(destination) == target:
                raise OSError("injected working-copy swap failure")
            original_replace(source, destination)

        with patch("isomer_labs.kaoju.template_support.os.replace", side_effect=fail_staged_swap):
            with self.assertRaises(OSError):
                _replace_directory(staged, target)
        self.assertEqual("old\n", (target / "paper.md").read_text(encoding="utf-8"))
        self.assertEqual("new\n", (staged / "paper.md").read_text(encoding="utf-8"))
        self.assertFalse(any(path.name.startswith(".target.backup-") for path in parent.iterdir()))

    def test_generic_artifact_mutation_is_rejected_for_named_template_binding(self) -> None:
        tree = self.prepared_tree("generic-put")
        status, rejected = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "artifacts",
            "put",
            "KAOJU:PAPER-TEMPLATE-MYST",
            str(tree),
            "--producer",
            "isomer-kaoju-write",
            "--scope-key",
            "main",
            "--topic",
            "alpha",
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_mutable_service_required", rejected["error"]["code"])
        self.assertTrue(any("ext kaoju paper template" in action for action in rejected["recovery_actions"]))

    def test_unknown_template_command_returns_named_template_examples(self) -> None:
        status, payload = self.run_cli("ext", "kaoju", "paper", "template", "not-a-command")
        self.assertEqual(2, status, payload)
        examples = payload["diagnostics"][0]["examples"]
        self.assertTrue(any("template list" in example for example in examples))
        self.assertTrue(any("template show" in example for example in examples))
        self.assertTrue(any("template export" in example for example in examples))


if __name__ == "__main__":
    unittest.main()
