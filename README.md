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

## Use with Codex

Codex discovers personal skills from `~/.agents/skills`. Link a skill from this
repository into that directory:

```bash
mkdir -p "$HOME/.agents/skills"
ln -s "$PWD/skills/example-skill" "$HOME/.agents/skills/example-skill"
```

Replace `example-skill` with the skill directory name. Run the commands from
the repository root.

## Conventions

- Keep each skill focused on one reusable workflow.
- Name skill directories with lowercase letters, digits, and hyphens.
- Keep instructions in `SKILL.md`; add supporting files only when needed.
- Do not commit credentials, tokens, private data, or machine-specific state.

