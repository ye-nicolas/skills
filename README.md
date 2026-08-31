# Skills

Personal collection of reusable Agent Skills for engineering workflows.

## Repository structure

Each skill lives in its own directory under `skills/` and contains a required
`SKILL.md` file. Scripts, references, assets, and agent metadata are optional.

```text
skills/
└── example-skill/
    ├── SKILL.md
    ├── agents/
    │   └── openai.yaml
    ├── scripts/
    ├── references/
    └── assets/
```

## Inventory

See the [skill inventory](docs/skill-inventory.md) for the version-controlled
skills in this repository and a dated snapshot of bundled and plugin-provided
skills found in the local Codex installation. The inventory also records the
version-controlled global Codex guidance under `config/`.

## Quick Setup

Run `make` from the repository root to automatically link all skills and global guidance files to your environment (`~/.agents/skills` and `~/.codex`):

```bash
make
```

Available `make` targets:

```bash
make setup        # (Default) Link both skills and AGENTS.md guidance
make skills       # Link ONLY skills to ~/.agents/skills
make agents       # Link ONLY AGENTS.md and SOP files to ~/.codex
make status       # Inspect current symlink status
make clean        # Remove symlinks created from this repository
make help         # Show available targets
```



## Global Codex guidance

The `config/` directory contains the global `AGENTS.md` working agreements and
their conditional workflow documents. The live files under `~/.codex` are
symlinked to these version-controlled copies.

The guidance is intentionally stored below `config/` instead of as a repository
root `AGENTS.md`. This preserves its global role without also applying it as a
second repository-scoped instruction file when working in this repository.

## Conventions

- Keep each skill focused on one reusable workflow.
- Name skill directories with lowercase letters, digits, and hyphens.
- Keep instructions in `SKILL.md`; add supporting files only when needed.
- Do not commit credentials, tokens, private data, or machine-specific state.
