#!/usr/bin/env python3
"""Produce a deterministic candidate index for a Java refactoring audit.

This is a discovery aid, not a semantic clone detector. Its output must be
validated against implementations, callers, tests, and behavior contracts.
"""

from __future__ import annotations

import argparse
import collections
import re
from dataclasses import dataclass
from pathlib import Path


EXCLUDED_PARTS = {
    ".git",
    ".gradle",
    ".idea",
    ".mvn",
    "build",
    "generated",
    "node_modules",
    "out",
    "target",
}

PACKAGE_PATTERN = re.compile(r"^\s*package\s+([\w.]+)\s*;", re.MULTILINE)
IMPORT_PATTERN = re.compile(r"^\s*import\s+(?:static\s+)?([\w.]+)\s*;", re.MULTILINE)
STATIC_MAP_METHOD_PATTERN = re.compile(
    r"\bstatic\s+(?:<[^>{}]+>\s+)?Map\s*<", re.MULTILINE
)
START_CALL_ASSIGNMENT_PATTERN = re.compile(
    r"\b(?P<variable>[A-Za-z_$][\w$]*)\s*=\s*"
    r"(?:[A-Za-z_$][\w$]*\.)+(?:start|begin|open)\s*\([^;]*\)\s*;"
)


@dataclass(frozen=True)
class JavaFile:
    path: Path
    relative_path: Path
    text: str
    line_count: int
    package_name: str | None

    @property
    def class_name(self) -> str:
        return self.path.stem

    @property
    def qualified_name(self) -> str | None:
        if self.package_name is None:
            return None
        return f"{self.package_name}.{self.class_name}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inventory Java refactoring candidates across a repository."
    )
    parser.add_argument("root", nargs="?", default=".", help="Repository or module root")
    parser.add_argument("--top", type=int, default=15, help="Rows per ranked section")
    return parser.parse_args()


def is_included(path: Path) -> bool:
    return not any(part in EXCLUDED_PARTS for part in path.parts)


def load_java_files(root: Path) -> list[JavaFile]:
    files: list[JavaFile] = []
    for path in sorted(root.rglob("*.java")):
        relative_path = path.relative_to(root)
        if not is_included(relative_path):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        package_match = PACKAGE_PATTERN.search(text)
        files.append(
            JavaFile(
                path=path,
                relative_path=relative_path,
                text=text,
                line_count=text.count("\n") + 1,
                package_name=package_match.group(1) if package_match else None,
            )
        )
    return files


def print_ranked(title: str, rows: list[tuple[object, ...]], headers: tuple[str, ...]) -> None:
    print(f"\n## {title}")
    print("\t".join(headers))
    for row in rows:
        print("\t".join(str(value) for value in row))


def start_then_mutate_occurrences(text: str) -> list[tuple[int, str]]:
    """Find lifecycle objects changed shortly after start/begin/open returns them."""
    occurrences: list[tuple[int, str]] = []
    for match in START_CALL_ASSIGNMENT_PATTERN.finditer(text):
        variable = match.group("variable")
        following_text = text[match.end() : match.end() + 4000]
        setter_pattern = re.compile(
            rf"\b{re.escape(variable)}\.set[A-Z][A-Za-z0-9_$]*\s*\("
        )
        if setter_pattern.search(following_text):
            line_number = text.count("\n", 0, match.start()) + 1
            occurrences.append((line_number, variable))
    return occurrences


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    java_files = load_java_files(root)

    if not java_files:
        print(f"No Java files found under {root}")
        return 1

    main_files = [f for f in java_files if "src/main/" in f.relative_path.as_posix()]
    test_files = [f for f in java_files if "src/test/" in f.relative_path.as_posix()]

    print("# Java refactoring candidate index")
    print(f"root\t{root}")
    print(f"java_files\t{len(java_files)}")
    print(f"main_java_files\t{len(main_files)}")
    print(f"test_java_files\t{len(test_files)}")
    print(f"java_lines\t{sum(f.line_count for f in java_files)}")

    largest = sorted(java_files, key=lambda f: (-f.line_count, str(f.relative_path)))
    print_ranked(
        "Largest Java files",
        [(f.line_count, f.relative_path) for f in largest[: args.top]],
        ("lines", "path"),
    )

    by_basename: dict[str, list[Path]] = collections.defaultdict(list)
    for java_file in java_files:
        by_basename[java_file.class_name].append(java_file.relative_path)
    repeated_basenames = sorted(
        (
            (len(paths), name, ", ".join(str(path) for path in paths))
            for name, paths in by_basename.items()
            if len(paths) > 1
        ),
        key=lambda row: (-row[0], row[1]),
    )
    print_ranked(
        "Repeated class basenames",
        repeated_basenames[: args.top],
        ("count", "class", "paths"),
    )

    by_qualified_name = {
        java_file.qualified_name: java_file
        for java_file in java_files
        if java_file.qualified_name is not None
    }
    importers: dict[str, set[Path]] = collections.defaultdict(set)
    static_reference_counts: collections.Counter[str] = collections.Counter()
    for java_file in java_files:
        for imported_name in IMPORT_PATTERN.findall(java_file.text):
            if imported_name in by_qualified_name:
                importers[imported_name].add(java_file.relative_path)
        static_reference_counts.update(
            re.findall(r"\b([A-Z][A-Za-z0-9_]*)\s*\.", java_file.text)
        )

    fan_in_rows: list[tuple[object, ...]] = []
    for qualified_name, importer_paths in importers.items():
        source = by_qualified_name[qualified_name]
        own_references = len(
            re.findall(
                rf"\b{re.escape(source.class_name)}\s*\.",
                source.text,
            )
        )
        static_references = static_reference_counts[source.class_name] - own_references
        fan_in_rows.append(
            (len(importer_paths), static_references, source.class_name, source.relative_path)
        )
    fan_in_rows.sort(key=lambda row: (-row[0], -row[1], str(row[3])))
    print_ranked(
        "High import fan-in classes",
        fan_in_rows[: args.top],
        ("importers", "static_refs", "class", "path"),
    )

    imperative_rows: list[tuple[object, ...]] = []
    for java_file in java_files:
        for_loops = len(re.findall(r"\bfor\s*\(", java_file.text))
        map_puts = len(re.findall(r"\.put\s*\(", java_file.text))
        list_adds = len(re.findall(r"\.add\s*\(", java_file.text))
        static_map_methods = len(STATIC_MAP_METHOD_PATTERN.findall(java_file.text))
        if for_loops and (map_puts or list_adds or static_map_methods):
            imperative_rows.append(
                (
                    static_map_methods,
                    map_puts,
                    list_adds,
                    for_loops,
                    java_file.relative_path,
                )
            )
    imperative_rows.sort(
        key=lambda row: (-row[0], -row[1], -row[2], -row[3], str(row[4]))
    )
    print_ranked(
        "Imperative collection transformation candidates",
        imperative_rows[: args.top],
        ("static_map_methods", "map_puts", "list_adds", "for_loops", "path"),
    )

    lifecycle_rows: list[tuple[object, ...]] = []
    for java_file in java_files:
        occurrences = start_then_mutate_occurrences(java_file.text)
        if occurrences:
            examples = ", ".join(
                f"{variable}@{line_number}"
                for line_number, variable in occurrences[:3]
            )
            lifecycle_rows.append(
                (len(occurrences), examples, java_file.relative_path)
            )
    lifecycle_rows.sort(key=lambda row: (-row[0], str(row[2])))
    print_ranked(
        "Lifecycle objects mutated after start/begin/open",
        lifecycle_rows[: args.top],
        ("occurrences", "examples", "path"),
    )
    print(
        "lifecycle_mutations_total\t"
        f"{sum(row[0] for row in lifecycle_rows)}\t"
        f"{len(lifecycle_rows)} files"
    )

    syntax_patterns = {
        "lambdas": re.compile(r"->"),
        "method_references": re.compile(r"::"),
        "stream_calls": re.compile(r"\.stream\s*\("),
        "collect_calls": re.compile(r"\.collect\s*\("),
        "anonymous_comparators": re.compile(r"new\s+Comparator(?:\s*<[^>]*>)?\s*\("),
        "anonymous_runnables": re.compile(r"new\s+Runnable\s*\("),
        "switches": re.compile(r"\bswitch\s*\("),
        "field_injection": re.compile(r"@Autowired\b"),
        "raw_map_construction": re.compile(r"\bMap\s+\w+\s*=\s*new\s+(?:HashMap|TreeMap)\s*\("),
        "optional_or_else_null": re.compile(r"\.orElse\s*\(\s*null\s*\)"),
        "broad_exception_catches": re.compile(r"catch\s*\(\s*(?:Exception|Throwable)\b"),
        "common_pool_async": re.compile(r"CompletableFuture\.(?:runAsync|supplyAsync)\s*\("),
        "return_null": re.compile(r"\breturn\s+null\s*;"),
        "todo_markers": re.compile(r"\bTODO\b", re.IGNORECASE),
    }
    print("\n## Functional and branching syntax")
    print("signal\tcount\tfiles")
    for name, pattern in syntax_patterns.items():
        matches = [len(pattern.findall(java_file.text)) for java_file in java_files]
        print(f"{name}\t{sum(matches)}\t{sum(1 for count in matches if count)}")

    print("\nReview these rows as leads only; verify contracts and callers before recommending refactors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
