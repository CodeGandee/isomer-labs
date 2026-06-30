# Package Check Playbook

Package knowledge and solver availability are separate. Check the current environment before treating any scientific package, executable, module, license, dataset, GPU backend, or queue as usable.

## Check Order

1. Identify the package, solver, workflow tool, dataset, or service needed.
2. Check import, executable existence, module state, license state, credential availability, queue access, data path, or network requirement as applicable.
3. Capture version and important backend details.
4. Run a minimal smoke test when the package supports it and Gate Policy preflight clears any cost, safety, credential, private-data, external-upload, or long-compute concern.
5. Save the diagnostic output as an Artifact or Evidence Item.
6. Record the route as passed, failed, or blocked.

## Python Package Pattern

Use an approved Execution Adapter Command Request to run a short check that writes durable JSON or text evidence. The check should capture import status, version, backend, and smoke-test result without relying on conversation recall.

```python
result = {"package_id": "pyscf", "import": "failed", "version": None, "smoke": "not_run"}
try:
    import pyscf
    result["import"] = "passed"
    result["version"] = getattr(pyscf, "__version__", None)
    result["smoke"] = "passed"
except Exception as exc:
    result["error"] = repr(exc)
```

## CLI Solver Pattern

Check executable path, version output, module or environment state, minimal input handling, and output write permissions. Record failed checks when they explain a blocker.

## Interpretation

- `passed` means the current environment can run at least the checked smoke path.
- `failed` means the package or solver was attempted and did not work.
- `blocked` means the agent could not check because credentials, data, modules, licenses, network access, queue access, or a required Gate Policy decision is missing.
