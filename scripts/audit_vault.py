#!/usr/bin/env python3
"""Audit repo-level Obsidian vault hygiene.

Obsidian remains authoritative for link resolution. This script catches
convention drift and repo hygiene issues that the Obsidian CLI does not report.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FRONTMATTER = ("title", "aliases", "tags", "updated")
SHORT_WORD_LIMIT = 75


def run_git(args: list[str], *, nul: bool = False) -> list[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        return []
    text = proc.stdout.decode("utf-8", errors="replace")
    if nul:
        return [part for part in text.split("\0") if part]
    return [line for line in text.splitlines() if line]


def markdown_files() -> list[Path]:
    tracked = run_git(["ls-files", "-z", "*.md"], nul=True)
    return sorted(path for name in tracked if (path := ROOT / name).exists())


def is_doc(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return rel == "README.md" or rel == "CLAUDE.md" or rel.startswith("_validation/")


def is_moc(path: Path) -> bool:
    return "(MOC)" in path.name


def is_content(path: Path) -> bool:
    return path.suffix == ".md" and not is_doc(path) and not is_moc(path)


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    current = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if not line.startswith(" ") and ":" in line:
            key, value = line.split(":", 1)
            current = key.strip()
            data[current] = value.strip()
        elif current:
            data[current] += "\n" + line
    return data, body


def parse_aliases(value: str) -> list[str]:
    value = value.strip()
    aliases: list[str] = []
    if not value:
        return aliases
    if value.startswith("[") and value.endswith("]"):
        for item in value[1:-1].split(","):
            item = item.strip().strip("'\"")
            if item:
                aliases.append(item)
        return aliases
    for line in value.splitlines():
        line = line.strip()
        if line.startswith("- "):
            item = line[2:].strip().strip("'\"")
            if item:
                aliases.append(item)
    return aliases


def words_without_boilerplate(text: str) -> int:
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


def check_tracked_ignored() -> list[str]:
    return run_git(["ls-files", "-ci", "--exclude-standard"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--show-short",
        action="store_true",
        help="print short-note inventory in addition to required failures",
    )
    parser.add_argument(
        "--show-uncovered",
        action="store_true",
        help="print content notes without a direct incoming link from a MOC",
    )
    args = parser.parse_args()

    failures: list[str] = []
    warnings: list[str] = []
    aliases: dict[str, set[str]] = defaultdict(set)
    link_owner: dict[str, str] = {}
    linked_from_moc: set[str] = set()

    tracked_ignored = check_tracked_ignored()
    if tracked_ignored:
        failures.append("tracked ignored files: " + ", ".join(tracked_ignored))

    md_extension_links: list[str] = []
    empty_links: list[str] = []
    blank_alias_links: list[str] = []
    missing_related: list[str] = []
    missing_frontmatter: list[str] = []
    missing_summary: list[str] = []
    short_notes: list[tuple[int, str]] = []

    link_pattern = re.compile(r"\[\[([^\]]+)\]\]")

    files = markdown_files()
    frontmatters: dict[Path, dict[str, str]] = {}
    bodies: dict[Path, str] = {}
    texts: dict[Path, str] = {}

    for path in files:
        text = path.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        texts[path] = text
        frontmatters[path] = fm
        bodies[path] = body
        if is_doc(path):
            continue
        names = [path.stem, fm.get("title", "")]
        names.extend(parse_aliases(fm.get("aliases", "")))
        for name in names:
            key = name.strip().lower()
            if key:
                aliases[key].add(path.relative_to(ROOT).as_posix())

    collisions = {
        alias: sorted(paths) for alias, paths in aliases.items() if len(paths) > 1
    }
    if not collisions:
        for alias, paths in aliases.items():
            link_owner[alias] = next(iter(paths))

    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        text = texts[path]
        fm = frontmatters[path]
        body = bodies[path]

        for lineno, line in enumerate(text.splitlines(), 1):
            for match in link_pattern.finditer(line):
                target = match.group(1)
                if not target.strip():
                    empty_links.append(f"{rel}:{lineno}")
                if ".md" in target:
                    md_extension_links.append(f"{rel}:{lineno}: {target}")
                if "|" in target and not target.split("|", 1)[1].strip():
                    blank_alias_links.append(f"{rel}:{lineno}: {target}")
                if is_moc(path):
                    target_key = target.split("|", 1)[0].lower()
                    linked_from_moc.add(link_owner.get(target_key, target_key))

        if is_doc(path):
            continue

        if not fm:
            missing_frontmatter.append(rel)
        else:
            missing = [key for key in REQUIRED_FRONTMATTER if key not in fm]
            if missing:
                missing_frontmatter.append(f"{rel} missing {', '.join(missing)}")
        if "> [!summary]" not in body:
            missing_summary.append(rel)

        if is_content(path):
            if "## Related notes" not in body:
                missing_related.append(rel)
            count = words_without_boilerplate(text)
            if count < SHORT_WORD_LIMIT:
                short_notes.append((count, rel))

    if missing_frontmatter:
        failures.append("missing/incomplete frontmatter:\n  " + "\n  ".join(missing_frontmatter))
    if missing_summary:
        failures.append("missing summary callout:\n  " + "\n  ".join(missing_summary))
    if missing_related:
        failures.append("content notes missing ## Related notes:\n  " + "\n  ".join(missing_related))
    if md_extension_links:
        failures.append(".md wikilinks:\n  " + "\n  ".join(md_extension_links))
    if empty_links:
        failures.append("empty wikilinks:\n  " + "\n  ".join(empty_links))
    if blank_alias_links:
        failures.append("blank alias wikilinks:\n  " + "\n  ".join(blank_alias_links))
    if collisions:
        lines = [f"{alias}: {', '.join(paths)}" for alias, paths in sorted(collisions.items())]
        failures.append("alias collisions:\n  " + "\n  ".join(lines))

    uncovered = []
    for path in markdown_files():
        rel = path.relative_to(ROOT).as_posix()
        if is_content(path) and rel not in linked_from_moc:
            # Reading notes and low-level glossary anchors may be linked from source notes
            # rather than hubs, so keep this informational.
            uncovered.append(rel)
    if uncovered:
        warnings.append(f"content notes without direct MOC link: {len(uncovered)}")
        if args.show_uncovered:
            warnings.extend(f"  {rel}" for rel in uncovered)

    if short_notes:
        warnings.append(
            f"short content notes under {SHORT_WORD_LIMIT} words: {len(short_notes)}"
        )
        if args.show_short:
            warnings.extend(f"  {count:3} {rel}" for count, rel in short_notes)

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"\n{failure}")
    else:
        print("PASS")

    if warnings:
        print("\nWARN")
        for warning in warnings:
            print(warning)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
