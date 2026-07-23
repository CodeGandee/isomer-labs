# extern/orphan

This directory holds local-only external checkouts, clones, and working copies that should never be committed. Keep tracked third-party code under `extern/tracked/`.

Everything here is ignored by `extern/.gitignore` except this `README.md`.

## Current contents

- `data/` — Local data snapshots, such as `deepscientist-run-006-snapshot`. These are produced by local runs and are not versioned.
- `DeepScientist/` — Local clone of the DeepScientist repository (`https://github.com/ResearAI/DeepScientist.git`).
- `houmao` — Symlink to a local Houmao source checkout (`https://github.com/igamenovoer/houmao`).
- `houmao-agents` — Symlink to a local Houmao agents checkout (`https://github.com/igamenovoer/houmao-agents.git`).
- `domain-skills` — Symlink to a local domain-skills checkout (`https://github.com/igamenovoer/domain-skills.git`).

## Recreating this directory

From the repository root:

```bash
# 1. Enter the orphan directory.
cd extern/orphan

# 2. Clone the standalone repository that lives inside this directory.
git clone https://github.com/ResearAI/DeepScientist.git

# 3. Check out the Houmao repositories outside this repo. The project convention
#    is ~/workspace/code/, but any convenient path works.
mkdir -p ~/workspace/code
git clone https://github.com/igamenovoer/houmao.git ~/workspace/code/houmao
git clone https://github.com/igamenovoer/houmao-agents.git ~/workspace/code/houmao-agents

# 4. Recreate the symlinks to those local checkouts.
ln -s ~/workspace/code/houmao houmao
ln -s ~/workspace/code/houmao-agents houmao-agents
ln -s /data/ssd2/huangzhe/code/domain-skills domain-skills
```

The `data/` directory contains local run snapshots and is not reproducible from upstream; restore it from backups or recreate it as needed.
