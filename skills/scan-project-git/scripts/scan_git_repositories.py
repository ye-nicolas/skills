#!/usr/bin/env python3
"""Find Git repositories below a project root and prune each Git root."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


SKIP_DIRS = {"node_modules", "vendor", ".venv", "target", "dist", "build"}
DEFAULT_CONFIG = Path("~/.codex/commit-msg-repositories.json").expanduser()


def branch_from_marker(repository: Path) -> str:
    marker = repository / ".git"
    git_directory = marker

    if marker.is_file():
        try:
            line = marker.read_text(encoding="utf-8").splitlines()[0]
        except (OSError, IndexError, UnicodeDecodeError):
            return "(detached HEAD)"
        if not line.startswith("gitdir:"):
            return "(detached HEAD)"
        git_directory = Path(line.split(":", 1)[1].strip())
        if not git_directory.is_absolute():
            git_directory = repository / git_directory

    try:
        head = (git_directory / "HEAD").read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return "(detached HEAD)"

    prefix = "ref: refs/heads/"
    return head[len(prefix) :] if head.startswith(prefix) else "(detached HEAD)"


def scan(root: Path) -> list[dict[str, str]]:
    root = root.resolve()
    repositories: list[dict[str, str]] = []

    pending = [root]
    while pending:
        current_path = pending.pop()
        try:
            entries = list(os.scandir(current_path))
        except OSError:
            continue

        marker = next((entry for entry in entries if entry.name == ".git"), None)
        if marker is not None:
            # A .git marker identifies the repository root. Never descend into it.
            repositories.append(
                {
                    "name": current_path.name,
                    "branch": branch_from_marker(current_path),
                    "path": str(current_path),
                }
            )
            continue

        children = [
            Path(entry.path)
            for entry in entries
            if entry.is_dir(follow_symlinks=False) and entry.name not in SKIP_DIRS
        ]
        pending.extend(sorted(children, reverse=True))

    return sorted(repositories, key=lambda item: item["path"])


def load_cached(config_path: Path, project_root: Path) -> list[dict[str, str]] | None:
    if not config_path.is_file():
        return None

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    projects = data.get("projects") if isinstance(data, dict) else None
    entry = projects.get(str(project_root)) if isinstance(projects, dict) else None
    repositories = entry.get("repositories") if isinstance(entry, dict) else None
    return repositories if isinstance(repositories, list) else None


def save_cached(
    config_path: Path,
    project_root: Path,
    repositories: list[dict[str, str]],
) -> None:
    data: dict[str, object] = {"version": 1, "projects": {}}
    if config_path.is_file():
        try:
            existing = json.loads(config_path.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                data = existing
        except (OSError, json.JSONDecodeError):
            pass

    projects = data.setdefault("projects", {})
    if not isinstance(projects, dict):
        projects = {}
        data["projects"] = projects
    project_key = str(project_root)
    previous_entry = projects.get(project_key)
    next_entry: dict[str, object] = {"repositories": repositories}
    if isinstance(previous_entry, dict):
        previous_last_selected = previous_entry.get("last_selected")
        if isinstance(previous_last_selected, dict):
            selected_path = previous_last_selected.get("path")
            matching_repository = next(
                (
                    repository
                    for repository in repositories
                    if repository.get("path") == selected_path
                ),
                None,
            )
            if matching_repository is not None:
                next_entry["last_selected"] = matching_repository
    projects[project_key] = next_entry

    config_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = config_path.with_suffix(config_path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(config_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="project workspace root; defaults to the current directory",
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="repository index config path",
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="ignore the cached entry and rescan the project",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: project root is not a directory: {root}", file=sys.stderr)
        return 2

    config_path = Path(args.config).expanduser()
    repositories = None if args.refresh else load_cached(config_path, root)
    if repositories is None:
        repositories = scan(root)
        try:
            save_cached(config_path, root, repositories)
        except OSError as error:
            print(f"warning: could not write repository index: {error}", file=sys.stderr)

    print(json.dumps(repositories, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
