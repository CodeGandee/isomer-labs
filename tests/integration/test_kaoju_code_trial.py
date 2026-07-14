from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from isomer_labs import cli


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class KaojuCodeTrialIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = os.environ.get("PATH", "")
        write(
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
        write(
            self.root / ".isomer-labs/research-topics/alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Alpha survey"
            """,
        )
        write(self.workspace / "isomer-topic-workspace-summary.md", "# Alpha\n")
        status, result = self.run_cli("project", "--root", str(self.root), "runtime", "init", "--topic", "alpha")
        self.assertEqual(0, status, result)
        fake_bin = self.root / "fake-bin"
        write(
            fake_bin / "pixi",
            """
            #!/bin/sh
            while [ "$#" -gt 0 ]; do
              if [ "$1" = "--" ]; then
                shift
                exec "$@"
              fi
              shift
            done
            exit 64
            """,
        )
        (fake_bin / "pixi").chmod(0o755)
        self.path = f"{fake_bin}:{self.path}"

    @property
    def workspace(self) -> Path:
        return self.root / "topic-workspaces/alpha"

    def run_cli(self, *arguments: str) -> tuple[int, dict[str, object]]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(self.root),
            patch.dict(os.environ, {"HOME": str(self.root), "PATH": self.path}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(["--print-json", *arguments])
        return status, json.loads(stdout.getvalue())

    def artifact(self, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli("project", "--root", str(self.root), "artifacts", *arguments, "--topic", "alpha")

    def service_request(self, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli("project", "--root", str(self.root), "service-requests", *arguments, "--topic", "alpha")

    def put_structured(
        self,
        semantic_id: str,
        record_id: str,
        producer: str,
        sections: dict[str, object],
        relationships: dict[str, str],
        *,
        scope: str | None = None,
        status: str = "ready",
    ) -> dict[str, object]:
        source = self.root / "inputs" / f"{record_id}.json"
        write(
            source,
            json.dumps(
                {
                    "title": record_id.replace("-", " ").title(),
                    "summary": f"Durable {semantic_id} integration fixture.",
                    "artifact_family": "kaoju",
                    "semantic_id": semantic_id,
                    "artifact_type": semantic_id.removeprefix("kaoju:"),
                    "sections": sections,
                },
                indent=2,
            )
            + "\n",
        )
        arguments = [
            "put",
            semantic_id,
            str(source),
            "--producer",
            producer,
            "--id",
            record_id,
            "--status",
            status,
            "--relationships-json",
            json.dumps([{"role": role, "target_ref": target} for role, target in relationships.items()]),
        ]
        if scope is not None:
            arguments.extend(["--scope-key", scope])
        command_status, result = self.artifact(*arguments)
        self.assertEqual(0, command_status, result)
        return result

    def put_file(
        self,
        semantic_id: str,
        record_id: str,
        producer: str,
        source: Path,
        relationships: dict[str, str],
        *,
        scope: str,
    ) -> dict[str, object]:
        status, result = self.artifact(
            "put",
            semantic_id,
            str(source),
            "--producer",
            producer,
            "--id",
            record_id,
            "--scope-key",
            scope,
            "--relationships-json",
            json.dumps([{"role": role, "target_ref": target} for role, target in relationships.items()]),
        )
        self.assertEqual(0, status, result)
        return result

    def acquire_source(self) -> dict[str, str]:
        upstream = self.root / "upstream"
        upstream.mkdir()
        subprocess.run(["git", "init", "-q", str(upstream)], check=True)
        subprocess.run(["git", "-C", str(upstream), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(upstream), "config", "user.name", "Test User"], check=True)
        write(upstream / "src/method.py", "def score(value: int) -> int:\n    return value * 2\n")
        subprocess.run(["git", "-C", str(upstream), "add", "src/method.py"], check=True)
        subprocess.run(["git", "-C", str(upstream), "commit", "-q", "-m", "method"], check=True)
        status, acquired = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "repos",
            "acquire",
            f"file://{upstream}",
            "--topic",
            "alpha",
            "--semantic-label",
            "topic.repos.sources.method",
        )
        self.assertEqual(0, status, acquired)
        repository = acquired["repository"]
        assert isinstance(repository, dict)
        self.assertEqual(1, repository["depth"])
        self.assertTrue(repository["shallow"])
        self.assertTrue(all(item["request"]["extension_point"] == "repository_acquisition" for item in acquired["command_requests"]))  # type: ignore[index]
        return {"label": "topic.repos.sources.method", "commit": str(repository["commit"]), "path": str(repository["path"]), "remote": f"file://{upstream}"}

    def register_source_evidence(self, repository: dict[str, str]) -> None:
        self.put_structured(
            "kaoju:associated-source-code",
            "associated-code-1",
            "isomer-kaoju-acquire",
            {
                "source": {"paper_ref": "paper-1", "version_family": "paper-v1"},
                "repository": {"semantic_label": repository["label"], "remote_url": repository["remote"], "commit": repository["commit"], "depth": 1},
                "relationship": {"status": "verified", "basis": "author-linked repository", "verified_at": "2026-07-14T12:00:00Z"},
            },
            {"source": "paper-1", "repository": repository["label"]},
            scope="source:paper-1",
        )
        self.put_structured(
            "kaoju:artifact-library",
            "artifact-library-1",
            "isomer-kaoju-acquire",
            {
                "materials": [
                    {
                        "material_id": "method-repository",
                        "source_identity": repository["remote"],
                        "source_class": "repository",
                        "content_ref": repository["label"],
                        "status": "ready",
                        "provenance_refs": ["command-request:repository-acquisition"],
                    }
                ]
            },
            {"material": "associated-code-1"},
        )
        self.put_structured(
            "kaoju:source-digest",
            "source-digest-code-1",
            "isomer-kaoju-examine",
            {
                "source_identity": {"source_class": "repository", "repository_ref": repository["label"], "commit": repository["commit"], "version_family": "git-commit"},
                "findings": [
                    {
                        "claim": "score doubles its input",
                        "source_class": "repository",
                        "repository_ref": repository["label"],
                        "commit": repository["commit"],
                        "file": "src/method.py",
                        "line_start": 1,
                        "line_end": 2,
                        "source_statement": "The return expression multiplies value by two.",
                        "interpretation": "For integer inputs, this function implements a doubling operation.",
                    }
                ],
                "approval": {"status": "approved", "actor_ref": "topic-actor:researcher"},
            },
            {"source": "associated-code-1", "repository": repository["label"]},
            scope="source:repository-method",
            status="supported",
        )

    def prepare_environment(self, repository: dict[str, str]) -> dict[str, str]:
        self.put_structured(
            "kaoju:env-prep-plan",
            "env-plan-1",
            "isomer-kaoju-trial",
            {
                "dependencies": [{"name": "python", "intent_constraint": ">=3.11"}],
                "critical_path": {"source_ref": "associated-code-1", "repository_ref": repository["label"], "task_critical_path": "import and call src.method.score"},
                "candidates": [{"name": "default", "strategy": "reuse", "compatible": True}],
                "risks": [],
                "authorization": {"status": "approved", "actor_ref": "topic-actor:researcher", "allowed_mutations": []},
                "expected_smoke_outputs": ["import succeeded", "score(2) == 4"],
            },
            {"repository": repository["label"], "research_task": "research-task-trial", "run": "run-env-1"},
            scope="environment:method",
        )

        ambient_request = json.dumps({"extension_point": "smoke_run", "argv": ["python", "-c", "print('unsafe')"], "cwd": str(self.workspace)})
        status, ambient = self.service_request(
            "create",
            "--task-description",
            "Run an ambient smoke check",
            "--scope-kind",
            "topic_workspace",
            "--scope-ref",
            "alpha",
            "--authorization",
            "smoke only",
            "--dispatch-form",
            "tool_native_subagent",
            "--command-request-json",
            ambient_request,
            "--actor-ref",
            "project-operator-session:test",
            "--id",
            "service-request-ambient",
        )
        self.assertEqual(1, status)
        self.assertEqual("command_request_ambient_environment", ambient["error"]["code"])  # type: ignore[index]

        failed_request = self.create_execution_request("service-request-smoke-failed", "smoke_run", ["sh", "-c", "exit 7"], expected=["kaoju:smoke-run-result"])
        status, failed = self.service_request("dispatch", failed_request, "--service-actor-ref", "service-agent:environment")
        self.assertEqual(1, status)
        self.assertEqual("failed", failed["terminal_status"])
        self.assertTrue(failed["support_artifact_ref"])

        smoke_request = self.create_execution_request("service-request-smoke-ready", "smoke_run", ["sh", "-c", "printf 'ready\\n'"], expected=["kaoju:smoke-run-result"])
        status, dispatched = self.service_request("dispatch", smoke_request, "--service-actor-ref", "service-agent:environment")
        self.assertEqual(0, status, dispatched)
        self.assertEqual("complete", dispatched["terminal_status"])
        command_request_ref = str(dispatched["command_request_ref"])
        self.put_structured(
            "kaoju:env-gate-revision",
            "env-gate-1",
            "isomer-srv-topic-env-setup",
            {"before": {"environment": "default", "state": "candidate"}, "after": {"environment": "default", "state": "ready"}, "decision": {"status": "approved", "actor_ref": "topic-actor:researcher"}},
            {"env_prep_plan": "env-plan-1", "service_request": smoke_request},
            scope="environment:method",
        )
        self.put_structured(
            "kaoju:pixi-env-ref",
            "pixi-env-1",
            "isomer-srv-topic-env-setup",
            {"intent_constraints": {"python": ">=3.11"}, "resolved_packages": {"python": "3.11.13"}, "lock": {"identity": "sha256:lock-method", "status": "ready"}},
            {"env_gate_revision": "env-gate-1"},
            scope="environment:method",
        )
        smoke_script = self.root / "inputs/smoke-method.sh"
        write(smoke_script, "#!/bin/sh\npython -c 'from src.method import score; assert score(2) == 4'\n")
        script_result = self.put_file(
            "kaoju:smoke-run-script",
            "smoke-script-1",
            "isomer-srv-topic-env-setup",
            smoke_script,
            {"pixi_env": "pixi-env-1", "repository": repository["label"]},
            scope="environment:method",
        )
        canonical_script = Path(str(script_result["record"]["content_path"]))  # type: ignore[index]
        self.assertIn("research-records", canonical_script.parts)
        self.assertFalse(canonical_script.is_relative_to(Path(repository["path"])))
        self.assertFalse(canonical_script.is_relative_to(self.workspace / "tmp"))
        self.put_structured(
            "kaoju:smoke-run-result",
            "smoke-result-1",
            "isomer-srv-topic-env-setup",
            {
                "execution": {"command_request_ref": command_request_ref, "run_ref": "run-env-1", "script_ref": "smoke-script-1", "pixi_env_ref": "pixi-env-1"},
                "observation": {"status": "passed", "task_critical_check": "passed", "logs": [str(dispatched["support_artifact_ref"])], "environment_ready": True, "checks": ["import", "call"]},
            },
            {"smoke_script": "smoke-script-1", "run": "run-env-1", "pixi_env": "pixi-env-1"},
            scope="environment:method",
        )
        return {"pixi": "pixi-env-1", "lock": "sha256:lock-method", "smoke": "smoke-result-1"}

    def create_execution_request(self, request_id: str, extension_point: str, command: list[str], *, expected: list[str]) -> str:
        argv = ["pixi", "run", "--environment", "default", "--", *command]
        command_request = json.dumps({"extension_point": extension_point, "argv": argv, "cwd": str(self.workspace)})
        status, created = self.service_request(
            "create",
            "--task-description",
            f"Execute {extension_point}",
            "--scope-kind",
            "run",
            "--scope-ref",
            request_id,
            "--authorization",
            "execute only the named Pixi command",
            "--dispatch-form",
            "tool_native_subagent",
            *[item for ref in expected for item in ("--expected-output-ref", ref)],
            "--command-request-json",
            command_request,
            "--actor-ref",
            "project-operator-session:test",
            "--id",
            request_id,
        )
        self.assertEqual(0, status, created)
        return request_id

    def test_uc08_repository_ingestion_and_exact_code_evidence(self) -> None:
        repository = self.acquire_source()
        self.register_source_evidence(repository)

        status, duplicate = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "repos",
            "acquire",
            repository["remote"],
            "--topic",
            "alpha",
            "--semantic-label",
            repository["label"],
        )
        self.assertEqual(1, status)
        self.assertEqual("repository_target_exists", duplicate["error"]["code"])  # type: ignore[index]
        status, inaccessible = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "repos",
            "acquire",
            "file:///missing/kaoju-source",
            "--topic",
            "alpha",
            "--semantic-label",
            "topic.repos.sources.missing",
        )
        self.assertEqual(1, status)
        self.assertEqual("repository_remote_unreachable", inaccessible["error"]["code"])  # type: ignore[index]
        topic_manifest = self.workspace / "topic-workspace.toml"
        self.assertNotIn("topic.repos.sources.missing", topic_manifest.read_text(encoding="utf-8"))

        invalid = self.root / "inputs/invalid-code-digest.json"
        payload = json.loads((self.root / "inputs/source-digest-code-1.json").read_text(encoding="utf-8"))
        del payload["sections"]["findings"][0]["line_end"]
        write(invalid, json.dumps(payload, indent=2) + "\n")
        status, rejected = self.artifact(
            "put",
            "kaoju:source-digest",
            str(invalid),
            "--producer",
            "isomer-kaoju-examine",
            "--id",
            "invalid-code-digest",
            "--status",
            "supported",
            "--scope-key",
            "source:invalid",
            "--relationships-json",
            '[{"role":"source","target_ref":"associated-code-1"},{"role":"repository","target_ref":"topic.repos.sources.method"}]',
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_contract_invalid", rejected["error"]["code"])  # type: ignore[index]

    def test_uc09_environment_service_preserves_failed_attempt_and_requires_pixi(self) -> None:
        repository = self.acquire_source()
        self.register_source_evidence(repository)
        prepared = self.prepare_environment(repository)
        self.assertEqual("pixi-env-1", prepared["pixi"])
        status, failed_status = self.service_request("status", "service-request-smoke-failed")
        self.assertEqual(0, status, failed_status)
        self.assertEqual("failed", failed_status["record"]["status"])  # type: ignore[index]
        status, ready = self.artifact("latest", "kaoju:smoke-run-result", "--scope-key", "environment:method")
        self.assertEqual(0, status, ready)
        self.assertEqual(["smoke-result-1"], [record["record_id"] for record in ready["records"]])  # type: ignore[index]

    def test_uc10_gate_generated_data_wrapper_and_immutable_attempts(self) -> None:
        repository = self.acquire_source()
        self.register_source_evidence(repository)
        environment = self.prepare_environment(repository)

        invalid_dataset = self.root / "inputs/generated-invalid"
        write(invalid_dataset / "input.json", "[1, 2, 3]\n")
        status, rejected_dataset = self.artifact(
            "put",
            "kaoju:generated-dataset",
            str(invalid_dataset),
            "--producer",
            "isomer-kaoju-trial",
            "--id",
            "generated-invalid",
            "--scope-key",
            "trial:random",
            "--relationships-json",
            '[{"role":"trial_run","target_ref":"trial-run-success"}]',
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_contract_invalid", rejected_dataset["error"]["code"])  # type: ignore[index]

        generated = self.root / "inputs/generated-valid"
        write(generated / "input.json", "[1, 2, 3]\n")
        write(
            generated / "generated-dataset.json",
            json.dumps(
                {
                    "title": "Generated integer probe",
                    "summary": "Seeded inputs for execution capability only.",
                    "artifact_family": "kaoju",
                    "semantic_id": "kaoju:generated-dataset",
                    "artifact_type": "generated-dataset",
                    "sections": {
                        "purpose": "capability-probe",
                        "verification_depth": "execution-only",
                        "generator": {"source_class": "synthetic", "seed": 7, "schema": "integer-array", "size": 3, "assumptions": ["integer input"]},
                        "outputs": [{"file_ref": "input.json", "records": 3}],
                        "checks": ["three integers", "seed recorded"],
                        "limitations": ["not the paper benchmark dataset"],
                    },
                },
                indent=2,
            )
            + "\n",
        )
        status, generated_result = self.artifact(
            "put",
            "kaoju:generated-dataset",
            str(generated),
            "--producer",
            "isomer-kaoju-trial",
            "--id",
            "generated-data-1",
            "--scope-key",
            "trial:random",
            "--relationships-json",
            '[{"role":"trial_run","target_ref":"trial-run-success"}]',
        )
        self.assertEqual(0, status, generated_result)

        rejected_plan_sections = {
            "trial_id": "trial-random",
            "prerequisites": {"source_ref": "associated-code-1", "repository_ref": repository["label"], "source_commit": repository["commit"], "data_strategy": "random_data", "generated_dataset_ref": "generated-data-1", "pixi_env_ref": environment["pixi"]},
            "wrapper": {"artifact_ref": "trial-wrapper-1", "run_command": "pixi run --environment default -- sh trial-wrapper-1", "fidelity": "smallest-adaptation"},
            "evaluation": {"evaluator": "exact output check", "metrics": ["output-value"], "expected_outputs": ["trial-output.json"], "limitations": ["capability probe only"]},
            "authorization": {"attempt_bound": 3, "resource_limits": {"wall_seconds": 30}, "human_gate": {"status": "rejected", "actor_ref": "topic-actor:researcher"}},
        }
        self.put_structured(
            "kaoju:method-trial-plan",
            "trial-plan-rejected",
            "isomer-kaoju-trial",
            rejected_plan_sections,
            {"repository": repository["label"], "pixi_env": environment["pixi"], "dataset": "generated-data-1"},
            scope="trial:random",
            status="blocked",
        )
        approved_source = self.root / "inputs/trial-plan-approved.json"
        approved_sections = json.loads(json.dumps(rejected_plan_sections))
        approved_sections["authorization"]["human_gate"] = {"status": "approved", "actor_ref": "topic-actor:researcher"}
        write(
            approved_source,
            json.dumps({"title": "Approved random trial", "summary": "Actor-approved bounded capability probe.", "artifact_family": "kaoju", "semantic_id": "kaoju:method-trial-plan", "artifact_type": "method-trial-plan", "sections": approved_sections}, indent=2) + "\n",
        )
        status, approved = self.artifact(
            "revise",
            "trial-plan-rejected",
            str(approved_source),
            "--producer",
            "isomer-kaoju-trial",
            "--id",
            "trial-plan-approved",
            "--scope-key",
            "trial:random",
            "--relationships-json",
            json.dumps([{"role": "repository", "target_ref": repository["label"]}, {"role": "pixi_env", "target_ref": environment["pixi"]}, {"role": "dataset", "target_ref": "generated-data-1"}]),
        )
        self.assertEqual(0, status, approved)

        wrapper_source = self.root / "inputs/trial-wrapper.sh"
        write(wrapper_source, "#!/bin/sh\nprintf '{\"score\": 6}\\n' > trial-output.json\n")
        wrapper = self.put_file(
            "kaoju:method-trial-wrapper",
            "trial-wrapper-1",
            "isomer-kaoju-trial",
            wrapper_source,
            {"trial_plan": "trial-plan-approved", "repository": repository["label"]},
            scope="trial:random",
        )
        wrapper_path = str(wrapper["record"]["content_path"])  # type: ignore[index]

        ambient_trial = json.dumps({"extension_point": "code_trial", "argv": ["sh", wrapper_path], "cwd": str(self.workspace)})
        status, ambient = self.service_request(
            "create",
            "--task-description",
            "Unsafe ambient trial",
            "--scope-kind",
            "run",
            "--scope-ref",
            "trial:random",
            "--authorization",
            "approved trial only",
            "--dispatch-form",
            "tool_native_subagent",
            "--command-request-json",
            ambient_trial,
            "--actor-ref",
            "project-operator-session:test",
            "--id",
            "trial-ambient",
        )
        self.assertEqual(1, status)
        self.assertEqual("command_request_ambient_environment", ambient["error"]["code"])  # type: ignore[index]

        failed_request = self.create_execution_request("trial-exec-failed", "code_trial", ["sh", "-c", "exit 3"], expected=["trial-run-failed"])
        status, failed_dispatch = self.service_request("dispatch", failed_request, "--service-actor-ref", "service-agent:trial")
        self.assertEqual(1, status)
        self.assertEqual("failed", failed_dispatch["terminal_status"])
        self.record_trial_run("trial-run-failed", "failed", failed_dispatch, repository, environment, wrapper_path)

        success_request = self.create_execution_request("trial-exec-success", "code_trial", ["sh", wrapper_path], expected=["trial-run-success", "trial-result-success"])
        status, success_dispatch = self.service_request("dispatch", success_request, "--service-actor-ref", "service-agent:trial")
        self.assertEqual(0, status, success_dispatch)
        self.assertTrue((self.workspace / "trial-output.json").is_file())
        self.record_trial_run("trial-run-success", "complete", success_dispatch, repository, environment, wrapper_path)
        self.put_structured(
            "kaoju:method-trial-result",
            "trial-result-success",
            "isomer-kaoju-trial",
            {
                "execution": {"trial_run_ref": "trial-run-success", "input_basis": "random_data", "run_purpose": "capability-probe", "outputs": ["trial-output.json"]},
                "results": {"checks": ["wrapper exited zero", "output parsed"], "metrics": {"score": 6}},
                "verdict": {"status": "observed", "depth": "execution-only", "fidelity": "smallest-adaptation", "adaptations": ["minimal output wrapper"]},
                "limitations": ["Generated input does not validate the paper benchmark."],
            },
            {"trial_run": "trial-run-success", "trial_plan": "trial-plan-approved"},
            scope="trial:random",
        )
        status, attempts = self.artifact("list", "--semantic-id", "kaoju:method-trial-run", "--scope-key", "trial:random")
        self.assertEqual(0, status, attempts)
        self.assertEqual({"trial-run-failed", "trial-run-success"}, {record["id"] for record in attempts["records"]})  # type: ignore[index]
        status, immutable = self.artifact(
            "revise",
            "trial-run-failed",
            str(self.root / "inputs/trial-run-failed.json"),
            "--producer",
            "isomer-kaoju-trial",
            "--scope-key",
            "trial:random",
            "--relationships-json",
            '[]',
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_revision_forbidden", immutable["error"]["code"])  # type: ignore[index]

        self.put_structured(
            "kaoju:method-trial-plan",
            "trial-plan-path-data",
            "isomer-kaoju-trial",
            {
                **rejected_plan_sections,
                "trial_id": "trial-path",
                "prerequisites": {"source_ref": "associated-code-1", "repository_ref": repository["label"], "source_commit": repository["commit"], "data_strategy": "dataset_path", "dataset_path": str(self.root / "actor-data/sample"), "pixi_env_ref": environment["pixi"]},
                "authorization": {"attempt_bound": 1, "resource_limits": {"wall_seconds": 30}, "human_gate": {"status": "pending"}},
            },
            {"repository": repository["label"], "pixi_env": environment["pixi"], "dataset": "external-dataset:sample"},
            scope="trial:path",
        )

    def record_trial_run(
        self,
        record_id: str,
        terminal_status: str,
        dispatch: dict[str, object],
        repository: dict[str, str],
        environment: dict[str, str],
        wrapper_path: str,
    ) -> None:
        succeeded = terminal_status == "complete"
        self.put_structured(
            "kaoju:method-trial-run",
            record_id,
            "isomer-kaoju-trial",
            {
                "execution": {
                    "command_request_ref": dispatch["command_request_ref"],
                    "source_commit": repository["commit"],
                    "pixi_env_ref": environment["pixi"],
                    "environment_lock": environment["lock"],
                    "data_ref": "generated-data-1",
                    "wrapper_ref": "trial-wrapper-1",
                    "wrapper_path": wrapper_path,
                    "logs": [dispatch["support_artifact_ref"]],
                    "outputs": ["trial-output.json" if succeeded else "no-output"],
                    "timing": {"elapsed_seconds": dispatch["observation"]["elapsed_seconds"]},  # type: ignore[index]
                    "resources": {"wall_seconds_limit": 30},
                    "adaptations": ["minimal output wrapper"],
                    "terminal_status": terminal_status,
                },
                "results": {"checks": ["exit-zero" if succeeded else "exit-nonzero"], "metrics": {"exit_code": 0 if succeeded else 3}},
            },
            {"trial_plan": "trial-plan-approved", "repository": repository["label"], "pixi_env": environment["pixi"], "dataset": "generated-data-1"},
            scope="trial:random",
            status=terminal_status,
        )


if __name__ == "__main__":
    unittest.main()
