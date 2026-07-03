# Isomer History

This directory is the Project-local archive for Isomer Topic Workspaces that have been moved out of active development.

Each subdirectory under `topic-ws/<topic-id>/` is a frozen snapshot of a Topic Workspace at the time it was archived. These workspaces are preserved for reference, audit, and potential future reuse, but they are no longer part of the active project manifest.

**Do not modify archived Topic Workspaces unless explicitly instructed to do so.** Treat this directory as read-only. If you need to resume work on an archived topic, copy or re-import it into `isomer-content/topic-ws/` rather than editing files in place.

Fresh Projects ignore archived content under this root by default. The generated `.gitignore` keeps this `README.md` and the `.gitignore` policy file trackable, while archived Topic Workspaces stay local unless you intentionally track selected files.
