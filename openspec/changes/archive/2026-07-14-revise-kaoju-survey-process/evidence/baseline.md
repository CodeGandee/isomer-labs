# Pre-Change Focused Test Baseline

Captured on 2026-07-14 before changes to package code, dependencies, manifests, or skill assets.

Command:

```text
pixi run python -m pytest -q tests/unit/test_kaoju_skill_assets.py tests/unit/test_kaoju_artifact_bindings.py tests/unit/test_research_records_ext.py tests/unit/test_research_templates_ext.py tests/unit/test_houmao_cli_adapter.py tests/unit/test_team_repositories.py tests/unit/test_topic_workspace_manifest.py tests/unit/test_toolbox_runtime_params.py tests/integration/test_kaoju_record_lifecycle.py
```

Result: `84 passed in 9.14s` with exit status 0.

The slice covers Kaoju skill assets, artifact bindings, research records, template CLI behavior, the Houmao execution adapter boundary, repository registration, Workspace Runtime topic manifests, runtime parameter handling, and the current Kaoju record lifecycle.
