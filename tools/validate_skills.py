#!/usr/bin/env python3
"""Validate the skill collection.

Covers what ``claude plugin validate`` does not: skill frontmatter conventions,
relative links that actually resolve, generated references that match their
source, and README catalogs that match the skills on disk.

Run ``claude plugin validate . --strict`` alongside this for manifest checks.

Usage:
    python tools/validate_skills.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import sync_references
from sync_references import REPO_ROOT, SKILLS_DIR

# Claude Code truncates description + when_to_use at this length in the skill
# listing, so anything past it is invisible when Claude picks a skill.
DESCRIPTION_LIMIT = 1536

# This is a public repository, so every commit is a publication. These patterns
# catch the disclosures that are easy to paste in from a real build machine.
# Generic placeholders stay allowed so documentation examples still read naturally.
PLACEHOLDER_USERS = {"user", "username", "youruser", "builder", "build", "yocto", "developer"}

DISCLOSURE_PATTERNS = (
    ("email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("Windows user path", re.compile(r"[A-Za-z]:\\Users\\[A-Za-z0-9._-]+")),
    ("credential", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("credential", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("credential", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("credential", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private key", re.compile(r"BEGIN [A-Z ]*PRIVATE KEY")),
)

HOME_PATH = re.compile(r"/(?:home|Users)/([A-Za-z0-9._-]+)")

SCAN_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml"}

FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
FRONTMATTER_FIELD = re.compile(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$")
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
README_SKILL = re.compile(r"^- `skills/([\w-]+)`")

READMES = ("README.md", "README.ko.md")


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Parse the simple single-line ``key: value`` frontmatter these skills use."""
    match = FRONTMATTER.match(text)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        field = FRONTMATTER_FIELD.match(line)
        if field:
            fields[field.group(1)] = field.group(2).strip()
    return fields


def check_frontmatter(problems: list[str]) -> None:
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        rel = skill_md.relative_to(REPO_ROOT).as_posix()
        folder = skill_md.parent.name
        fields = parse_frontmatter(skill_md.read_text(encoding="utf-8"))

        if fields is None:
            problems.append(f"{rel}: missing YAML frontmatter")
            continue

        name = fields.get("name")
        if not name:
            problems.append(f"{rel}: frontmatter is missing 'name'")
        elif name != folder:
            # In a plugin skill the frontmatter name becomes the last segment of
            # the command, so a mismatch silently renames the skill.
            problems.append(f"{rel}: name '{name}' does not match folder '{folder}'")

        description = fields.get("description")
        if not description:
            problems.append(f"{rel}: frontmatter is missing 'description'")
            continue

        listed = len(description) + len(fields.get("when_to_use", ""))
        if listed > DESCRIPTION_LIMIT:
            problems.append(
                f"{rel}: description + when_to_use is {listed} chars, "
                f"over the {DESCRIPTION_LIMIT} char listing limit"
            )


def check_links(problems: list[str]) -> None:
    targets = sorted(SKILLS_DIR.glob("*/**/*.md")) + [REPO_ROOT / "SKILL.md"]
    for markdown in targets:
        rel = markdown.relative_to(REPO_ROOT).as_posix()
        for target in MARKDOWN_LINK.findall(markdown.read_text(encoding="utf-8")):
            target = target.split()[0].strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (markdown.parent / target.split("#")[0]).resolve()
            if not resolved.exists():
                problems.append(f"{rel}: broken link '{target}'")


def check_reference_mapping(problems: list[str]) -> None:
    """The sync mapping must match the references each SKILL.md actually links to."""
    for skill, sources in sync_references.SKILL_REFERENCES.items():
        skill_md = SKILLS_DIR / skill / "SKILL.md"
        rel = skill_md.relative_to(REPO_ROOT).as_posix()
        if not skill_md.exists():
            problems.append(f"sync mapping lists unknown skill '{skill}'")
            continue

        linked = {
            Path(target).name
            for target in MARKDOWN_LINK.findall(skill_md.read_text(encoding="utf-8"))
            if target.startswith("references/")
        }
        mapped = {Path(source).name for source in sources}

        for name in sorted(linked - mapped):
            problems.append(
                f"{rel}: links references/{name} but it is not in the sync mapping"
            )
        for name in sorted(mapped - linked):
            problems.append(
                f"{rel}: sync mapping copies {name} but SKILL.md never links it"
            )


def check_readmes(problems: list[str]) -> None:
    on_disk = {path.parent.name for path in SKILLS_DIR.glob("*/SKILL.md")}
    for readme in READMES:
        path = REPO_ROOT / readme
        if not path.exists():
            problems.append(f"{readme}: missing")
            continue
        listed = {
            match.group(1)
            for line in path.read_text(encoding="utf-8").splitlines()
            if (match := README_SKILL.match(line))
        }
        for name in sorted(on_disk - listed):
            problems.append(f"{readme}: skill '{name}' exists but is not listed")
        for name in sorted(listed - on_disk):
            problems.append(f"{readme}: lists '{name}' but no such skill exists")


def check_manifests(problems: list[str]) -> None:
    """Guard the Claude Code plugin manifests.

    ``claude plugin validate --strict`` is the authority and contributors run it
    locally, but it needs the Claude Code CLI. These checks cover the breakage
    that actually happens -- drifting names, a missing version, and a root
    CLAUDE.md -- so CI catches them without that dependency.
    """
    plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    marketplace_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"

    if (REPO_ROOT / "CLAUDE.md").exists():
        problems.append(
            "CLAUDE.md at the repository root makes `claude plugin validate --strict` "
            "fail; keep project rules in .claude/CLAUDE.md"
        )

    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        problems.append(".claude-plugin/plugin.json: missing")
        return
    except json.JSONDecodeError as error:
        problems.append(f".claude-plugin/plugin.json: invalid JSON ({error})")
        return

    for field in ("name", "description", "version"):
        if not plugin.get(field):
            problems.append(f".claude-plugin/plugin.json: missing '{field}'")

    name = plugin.get("name", "")
    if name and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        problems.append(f".claude-plugin/plugin.json: name '{name}' is not kebab-case")

    version = plugin.get("version", "")
    if version and not re.fullmatch(r"\d+\.\d+\.\d+", version):
        problems.append(
            f".claude-plugin/plugin.json: version '{version}' is not MAJOR.MINOR.PATCH"
        )

    try:
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        problems.append(".claude-plugin/marketplace.json: missing")
        return
    except json.JSONDecodeError as error:
        problems.append(f".claude-plugin/marketplace.json: invalid JSON ({error})")
        return

    for field in ("name", "owner", "plugins"):
        if not marketplace.get(field):
            problems.append(f".claude-plugin/marketplace.json: missing '{field}'")

    entries = marketplace.get("plugins") or []
    if len(entries) != 1:
        problems.append(
            f".claude-plugin/marketplace.json: expected 1 plugin entry, found {len(entries)}"
        )
    for entry in entries:
        if entry.get("name") != name:
            problems.append(
                f".claude-plugin/marketplace.json: entry name '{entry.get('name')}' "
                f"does not match plugin.json name '{name}'"
            )
        if entry.get("source") != "./":
            problems.append(
                ".claude-plugin/marketplace.json: source must be './' for a plugin "
                "hosted in this repository"
            )
        if "version" in entry:
            # plugin.json wins, so a second copy here is a release-time trap.
            problems.append(
                ".claude-plugin/marketplace.json: drop 'version'; plugin.json is the "
                "single place to bump it"
            )


def scannable_files() -> list[Path]:
    return sorted(
        path
        for path in REPO_ROOT.rglob("*")
        if path.is_file()
        and path.suffix in SCAN_SUFFIXES
        and ".git" not in path.parts
    )


def check_disclosure(problems: list[str]) -> None:
    """Keep personal and machine-specific details out of a public repository."""
    for path in scannable_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for label, pattern in DISCLOSURE_PATTERNS:
                match = pattern.search(line)
                if match:
                    problems.append(f"{rel}:{number}: {label} in public repo: {match.group(0)}")

            home = HOME_PATH.search(line)
            if home and home.group(1) not in PLACEHOLDER_USERS:
                problems.append(
                    f"{rel}:{number}: local home path in public repo: {home.group(0)} "
                    f"(use a placeholder such as /home/user)"
                )


def main() -> int:
    problems: list[str] = []

    check_frontmatter(problems)
    check_links(problems)
    check_reference_mapping(problems)
    check_readmes(problems)
    check_manifests(problems)
    check_disclosure(problems)
    problems.extend(sync_references.check())

    for problem in problems:
        print(f"error: {problem}")

    if problems:
        print(f"\n{len(problems)} problem(s) found")
        return 1

    skills = sorted(path.parent.name for path in SKILLS_DIR.glob("*/SKILL.md"))
    print(f"ok: {len(skills)} skills validated ({', '.join(skills)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
