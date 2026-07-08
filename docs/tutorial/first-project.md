# Create a Project

An Isomer Project is a normal directory with project metadata, content storage, and topic workspaces. Start with an empty directory unless you are intentionally adopting an existing project.

```bash
mkdir my-isomer-project
cd my-isomer-project
isomer-cli project init
isomer-cli --print-json project validate
```

The validation command reports missing configuration, invalid topic bindings, and runtime issues. Fix those before launching agents or writing records.

The project root is the path you pass to Isomer CLI commands and automation. Keep generated caches and temporary work out of version control.
