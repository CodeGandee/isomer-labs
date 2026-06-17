# Debug Response

Use debug when a candidate failed but still looks strategically valuable. Debug is bugfix-only; do not use it to smuggle in a new performance idea.

## Template

```md
# Debug Response

## Error

What concrete error or failure occurred?

## Retrieved Context

What similar failure pattern, Finding, Evidence Item, or repair lesson should be reused?

## Root Cause

What is the most likely underlying cause?

## Minimal Fix

What is the smallest plausible fix?

## Keep Unchanged

What parts of the line must remain unchanged for comparability and stability?

## Next Check

What bounded smoke or validation check should confirm the fix?

## Archive Threshold

What outcome would prove this candidate should be archived instead of debugged again?
```

## Archive Rather Than Debug When

- the failure is strategic rather than local
- the candidate no longer beats nearby alternatives
- the fix would effectively turn it into a different candidate
