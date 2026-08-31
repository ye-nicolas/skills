---
name: scan-project-git
description: Scan an active project for Git repositories, report each repository name and current branch, and prune a repository as soon as its .git marker is found so nested contents are not scanned. Use when the user asks to find, list, or select Git repositories under a project.
---

# Scan Project Git

Find the Git repositories that belong to the active project without descending into a repository after its `.git` marker is found.

## Preconditions

- Run only for an active configured project/workspace.
- If no project is configured, reply `沒有設定專案，無法掃描 Git repository。` and end.
- Scan only the configured project workspace. Do not search the user's home directory or other unrelated paths.

## Repository index configuration

- Use `~/.codex/commit-msg-repositories.json` as the user-level repository index.
- Key entries by the absolute path of the active project workspace.
- A project entry may include `last_selected` with the last selected repository's `name`, `branch`, and `path`.
- Before scanning, read the config file. If it contains an entry for the active project, return that entry immediately and do not scan or validate every repository.
- If the config file or project entry is missing, scan once and save the result to the config file.
- Callers that select a repository should validate only the selected path; if it is missing or no longer Git, request a refresh and replace the entry.
- Preserve `last_selected` across refreshes when that repository still exists; discard it when the repository is gone.
- When the user asks to refresh or rescan, ignore the existing entry, scan again, and replace that project's entry.
- Never write this index inside the project workspace.

## Scan behavior

1. Start at the configured project workspace root.
2. Walk directories top-down and skip common dependency/generated directories: `node_modules`, `vendor`, `.venv`, `target`, `dist`, and `build`.
3. When the current directory contains `.git` as either a directory or a file:

   - Treat the current directory as one Git repository.
   - Record its path and current branch.
   - Prune the current directory immediately so no child directory is scanned.

4. Continue scanning sibling directories after pruning a repository. This finds multiple sibling repositories while avoiding nested repositories or unrelated contents inside a discovered repository.
5. Deduplicate repository paths and sort them by path relative to the project root.
6. Read the branch from the repository's `HEAD` marker when possible; display `(detached HEAD)` when it does not point to a local branch.

Prefer the bundled `scripts/scan_git_repositories.py` for the traversal and config handling. It emits JSON containing `name`, `branch`, and `path`; use `path` for later commands but do not display full paths unless the user asks.

## Output

Ask one choice-style question by default instead of printing a table. If the host provides a native choice prompt, use repository names and branches as its options. Otherwise render one option per line and accept a natural-language option reply; do not ask the user to fill in a number.

```text
要選哪個 repository 產生 commit msg？

- api-service（main）
- web-client（feature/login）
```

Use one option per line with the repository name and current branch. Keep the full path hidden. Wait for the user's choice before any further operation. If no repository is found, reply `沒有找到 Git repository。` and end.

Do not inspect diffs, stage files, commit changes, or modify the project. This skill only discovers repositories.
