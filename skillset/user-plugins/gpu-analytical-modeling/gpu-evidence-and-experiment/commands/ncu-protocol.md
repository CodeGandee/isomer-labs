# NCU Protocol

## Workflow

When NCU evidence is planned, collected, or reported, execute the following steps in order.

1. **Record the command shape**. In Pixi-managed projects, prefer `pixi run ncu ...` over `ncu pixi run ...` unless local evidence proves another wrapper is required.
2. **Name target and kernel selection**. Record GPU device, host or remote node when relevant, kernel selector, input shape, precision, and run count.
3. **List metrics before interpreting them**. Include raw metric names, section choices, and derived counter-to-component mapping.
4. **Preserve failures**. Record permission issues, section flag errors, empty package installs, timing bugs, timeouts, and harness fixes.
5. **Separate raw and derived evidence**. Keep raw counters distinct from derived dominant component, trend agreement, or path label.
6. **Link results to claims**. State which model output each counter supports, contradicts, or leaves unresolved.

If NCU cannot run, record the concrete blocker and route to repair, alternate measurement, or limitation.

## Counter Mapping

Map counters to components conservatively. A good mapping names the raw metric, normalized value, intended component, and reason the mapping is valid for the target GPU and kernel.

## Common Mistakes

- Quoting the whole NCU section list as one shell argument.
- Reporting only a profiler summary screenshot without raw metric names.
- Treating unavailable counters as zero activity.
- Forgetting that profiler labels can be coarser than the analytical bottleneck claim.
