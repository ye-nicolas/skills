---
name: conventional-commits-zh
description: Explain Conventional Commits 1.0.0 or draft an English message from user-provided intent without inspecting a repository. Prefer commit-msg when staged changes in an active project should be inspected.
---

# Conventional Commits（中文參考）— 英文提交信息生成

Use this skill when explicitly invoked for the Conventional Commits format or
when no repository inspection is requested. For a message derived from staged
changes, use `$commit-msg` instead.

## Hard requirement: output language

- ALWAYS output the final commit message in **English**.
- If the user writes Chinese, translate the intent to English for the commit subject/body.

## Format used by the referenced repository

Apply these constraints only when the user confirms they belong to the target
repository; a global skill must not assume every repository has the same hook:

- Format: `<type>(<scope>)?!?: <subject>`
- Allowed `type`: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- `scope` (optional): `([a-zA-Z0-9_/-]+)`
- `!` (optional) before `:` indicates breaking change

If the user provides a diff / file list, infer `type/scope/subject` from it.

## Output checklist

1) Pick `type`
- `feat`: new feature
- `fix`: bug fix
- `refactor`: restructure without behavior change
- `perf`: performance improvement
- `test`: tests only
- `docs`: docs only
- `chore`: misc / non-product changes
- `build`: build/deps
- `ci`: CI workflow
- `style`: formatting only
- `revert`: revert

2) Pick `scope` (recommended)
- Use a small, stable area name (e.g. `batch`, `pull`, `delta-config`, `config`, `util`, `scheduler`, `test`, `docs`).
- Prefer the most user-facing module affected.

3) Write `subject` (ENGLISH)
- Imperative tone; <= 72 chars preferred.
- No trailing period.
- Describe outcome, not implementation details.

4) Breaking changes
- If API/behavior is breaking, use `!` before `:`.
- Optionally add a footer line starting with `BREAKING CHANGE: ...`.

## Templates

- `feat(scope): <what changed>`
- `fix(scope): <bug fixed>`
- `refactor(scope): <what refactored>`
- `test(scope): <what tests updated>`
- `docs(scope): <what docs updated>`

## Examples

- `feat(batch): cap catch-up windows per tick`
- `fix(pull): avoid processing incomplete current window`
- `refactor(util): simplify safe time limit calculation`
- `test(pull): cover catch-up cap behavior`

## Reference

If the user needs the full 1.0.0 spec text (Chinese), read:
- `references/conventional-commits-1.0.0-zh.md`
