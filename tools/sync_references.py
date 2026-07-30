#!/usr/bin/env python3
"""Sync shared references into each skill so every skill folder is self-contained.

The files under ``references/`` are the source of truth. Each skill gets its own
copy of only the references it links to, so a skill folder keeps working when it
is installed on its own -- which is how both Codex skill collections and Claude
Code plugins load skills.

Usage:
    python tools/sync_references.py            # regenerate skill copies
    python tools/sync_references.py --check    # fail if copies are out of date
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REFERENCES_DIR = REPO_ROOT / "references"
SKILLS_DIR = REPO_ROOT / "skills"

# Which references each skill links to, as paths under references/.
# Keep this in sync with the "References" section of each SKILL.md.
SKILL_REFERENCES: dict[str, list[str]] = {
    "bitbake-debug": [
        "shared/yocto-field-guide.md",
        "yocto/qa-errors.md",
        "bitbake/variables-core.md",
    ],
    "yocto-doc-router": [
        "shared/official-doc-map.md",
        "yocto/migration.md",
        "yocto/qa-errors.md",
        "bitbake/variables-core.md",
        "bitbake/classes-core.md",
    ],
    "yocto-recipe-review": [
        "shared/official-doc-map.md",
        "yocto/qa-errors.md",
        "bitbake/variables-core.md",
        "bitbake/classes-core.md",
    ],
    "yocto-layer-review": [
        "shared/official-doc-map.md",
        "shared/yocto-field-guide.md",
        "yocto/migration.md",
    ],
    "yocto-image-rootfs": [
        "yocto/image-rootfs.md",
        "bitbake/variables-core.md",
        "bitbake/tasks-reference.md",
    ],
    "yocto-bsp-kernel": [
        "yocto/bsp-kernel.md",
        "yocto/migration.md",
        "bitbake/classes-core.md",
    ],
    "yocto-security-sbom": [
        "yocto/security-sbom.md",
        "yocto/migration.md",
        "bitbake/classes-core.md",
    ],
}

HEADER = (
    "<!-- Generated from references/{source} by tools/sync_references.py. "
    "Edit the source file, not this copy. -->"
)


def render(source: str) -> str:
    """Return the generated content for one skill-local reference copy."""
    body = (REFERENCES_DIR / source).read_text(encoding="utf-8")
    return HEADER.format(source=source) + "\n\n" + body


def target_path(skill: str, source: str) -> Path:
    """Skill-local copies are flattened; reference basenames are unique."""
    return SKILLS_DIR / skill / "references" / Path(source).name


def expected_files() -> dict[Path, str]:
    return {
        target_path(skill, source): render(source)
        for skill, sources in SKILL_REFERENCES.items()
        for source in sources
    }


def existing_files() -> set[Path]:
    return {
        path
        for skill in SKILL_REFERENCES
        for path in (SKILLS_DIR / skill / "references").glob("*.md")
    }


def normalized(text: str) -> str:
    """Compare content without tripping over platform line endings."""
    return "\n".join(text.splitlines())


def check() -> list[str]:
    """Return a list of drift problems; empty means the copies are current."""
    problems = []
    expected = expected_files()

    for path, content in expected.items():
        rel = path.relative_to(REPO_ROOT).as_posix()
        if not path.exists():
            problems.append(f"missing generated reference: {rel}")
        elif normalized(path.read_text(encoding="utf-8")) != normalized(content):
            problems.append(f"out of date, regenerate: {rel}")

    for path in sorted(existing_files() - set(expected)):
        rel = path.relative_to(REPO_ROOT).as_posix()
        problems.append(f"stale generated reference, no longer linked: {rel}")

    return problems


def sync() -> int:
    """Write the skill-local copies and drop ones no longer linked."""
    expected = expected_files()
    written = 0

    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current is None or normalized(current) != normalized(content):
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
            print(f"wrote {path.relative_to(REPO_ROOT).as_posix()}")
            written += 1

    for path in sorted(existing_files() - set(expected)):
        path.unlink()
        print(f"removed {path.relative_to(REPO_ROOT).as_posix()}")
        written += 1

    print(f"{written} file(s) changed, {len(expected)} generated reference(s) total")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report drift instead of writing files",
    )
    args = parser.parse_args()

    missing = [
        source
        for sources in SKILL_REFERENCES.values()
        for source in sources
        if not (REFERENCES_DIR / source).is_file()
    ]
    if missing:
        for source in sorted(set(missing)):
            print(f"error: mapped source does not exist: references/{source}")
        return 1

    if not args.check:
        return sync()

    problems = check()
    for problem in problems:
        print(f"error: {problem}")
    if problems:
        print(f"{len(problems)} problem(s); run: python tools/sync_references.py")
        return 1
    print("generated references are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
