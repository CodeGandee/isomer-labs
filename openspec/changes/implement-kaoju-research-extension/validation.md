## Validation Evidence

Validated on 2026-07-10 from the repository root.

| Check | Result |
| --- | --- |
| Imsight/OpenAI skill structural validation | All eleven Kaoju skill directories passed `skill-creator/scripts/quick_validate.py`. |
| Research-paradigm validation | The packaged research-paradigm root passed with no Kaoju or DeepSci diagnostics. |
| Focused unit tests | 81 tests passed across Kaoju contracts, system assets, installer lifecycle, Project extension declarations, callback filtering, and research-paradigm validation. |
| DeepSci regression | The complete existing DeepSci validator suite passed as part of the focused run. |
| Lint | `pixi run lint` passed. |
| Type checking | `pixi run typecheck` passed with no issues in 121 source files. |
| Full unit suite | `pixi run test` passed all 487 tests after the final operator-routing update. |
| Installation smoke test | `isomer-cli --print-json system-skills install --target generic --home tmp/kaoju-install-smoke --extension kaoju` installed core plus exactly eleven flat Kaoju skills, preserved pipeline commands and shared references, and installed no DeepSci skill. |
| Guidance review | Active Kaoju files contain no feature-design or OpenSpec runtime dependency, named provider binding, hard-coded local runtime path, retired namespace, standalone maintenance procedure, or per-CRUD public command. |

The implementation remains asset-only. Existing Topic Workspace, provider, environment, execution, Gate, callback, installer, Project declaration, and research-recording owners supply runtime behavior.
