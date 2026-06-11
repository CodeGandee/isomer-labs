# DeepScientist Work Area

This directory is reserved for local DeepScientist testing.

## Layout

- `app/`: local source install of DeepScientist from `extern/orphan/DeepScientist`.
  The current install places the CLI tree in `app/cli` and launcher wrappers in
  `app/bin`.
- `workspace/`: local runtime workspace for DeepScientist quests, experiments,
  generated files, and daemon state.

Both directories are tracked with `.gitkeep` placeholders, but their generated
contents are ignored by `dswork/.gitignore`.

## Install Command

Install or refresh DeepScientist from the local source checkout:

```bash
bash extern/orphan/DeepScientist/install.sh --dir dswork/app --bin-dir dswork/app/bin
```

Verify the installed launcher:

```bash
dswork/app/bin/ds --help
```

Start DeepScientist from this repository with:

```bash
dswork/app/bin/ds --home dswork/workspace
```
