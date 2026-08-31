---
name: commit-msg
description: Generate one concise Conventional Commit message from staged changes in the Git repository containing the current working directory. Run without asking by default; use another repository only when the user explicitly requests a switch.
---

# Commit Message

Generate exactly one candidate commit message from the current repository's staged changes.

## Guardrails

- Never run `git add`, `git commit`, or any command that changes files or repository state.
- Inspect staged changes only. Ignore unstaged changes and untracked files.
- Do not scan for repositories, maintain a repository index, remember a previous selection, or read, display, or store branch names.

## 1. Resolve the repository

Use the current working directory unless the user explicitly asks to switch repositories:

```sh
git -C <current-working-directory> rev-parse --show-toplevel
```

- When this succeeds, use the returned repository root immediately without asking a question.
- When it fails, reply exactly `目前的資料夾不在 Git repository 中，無法產生 commit msg。` and end. Do not search elsewhere or ask the user to choose a repository.

### Explicit repository switch

Only switch when the user explicitly requests another repository or supplies a repository path.

- Resolve a supplied path with `git -C <supplied-path> rev-parse --show-toplevel` and use the returned root.
- Resolve relative paths from the current working directory.
- If the user supplies only a repository name and it cannot be resolved unambiguously without searching, ask one short question for its path.
- If the supplied path is not a Git repository, report that fact and end.
- The switch applies only to the current request. Do not save it for later invocations.

## 2. Read staged changes

Run every Git command with `git -C <repository-root>`.

1. Check whether staged changes exist with `git -C <repository-root> diff --cached --quiet`.
2. If there are no staged changes, reply exactly `目前的 repository 沒有 staged changes，無法產生 commit msg。` and end.
3. Read repository-specific commit rules when present, such as `.githooks/commit-msg`, `commitlint.config.*`, or the relevant `package.json`.
4. Start with:

   ```sh
   git -C <repository-root> diff --cached --shortstat
   git -C <repository-root> diff --cached --stat
   git -C <repository-root> diff --cached --name-status
   ```

5. For a small change set (at most 20 files and 500 changed lines), read the full `git -C <repository-root> diff --cached`.
6. For a larger change set, do not load the full patch. Use the summary and inspect at most three representative files with a no-color diff excerpt capped at 20 KB.

## 3. Produce the message

Output one candidate message only, unless the user asks for explanation or alternatives.

- Use `<type>(<scope>): <subject>`; omit `scope` when no stable scope is clear.
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Follow repository-specific rules when they exist.
- Write in English, imperative mood, with a subject of 72 characters or fewer and no trailing period.
- Describe the outcome rather than implementation trivia.
- Use `!` before `:` for a breaking change only when warranted.

Example:

```text
feat(auth): add login form validation
```
