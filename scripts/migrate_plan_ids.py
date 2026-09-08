#!/usr/bin/env python3
"""Migrate roadmap plan files from sequential NNN ids to GitHub-issue ids.

Renames every ``NNN-slug.md`` (or ``draft-slug.md``) plan file to
``{issue}-slug.md`` where ``{issue}`` is the ``issue.id`` declared in the plan's
YAML front matter, then rewrites the plan's own metadata, the consolidated
``roadmap.md`` links and, optionally, the referencing GitHub issues.

The identifier is derived from the front matter only: no directory scan, no
counter. Files without an ``issue.id`` are reported and skipped.

Usage:
    python migrate_plan_ids.py [--roadmap-dir DIR] [--dry-run] [--patch-issues]
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

FRONT_MATTER_DELIMITER = "---"
LEADING_ID_PATTERN = re.compile(r"^(?:\d+|draft)-(?P<slug>.+)$")


class MigrationError(Exception):
    """Raised when a plan file cannot be migrated safely."""


@dataclass
class Rename:
    """A single plan file rename, from old to new basename."""

    path: Path
    old_basename: str
    new_basename: str
    old_prefix: str
    issue_id: str
    old_plan_id: str | None = None

    def old_ids(self) -> list[str]:
        """Return every legacy id form to rewrite (file prefix and plan.id).

        Textual references may use the file-name prefix ('010') or the logical
        plan.id ('10'); both must be migrated to the issue id.
        """
        ids = [self.old_prefix]
        if self.old_plan_id and self.old_plan_id not in ids:
            ids.append(self.old_plan_id)
        return ids


def read_front_matter(content: str) -> list[str]:
    """Return the raw front matter lines, or raise if none is present."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != FRONT_MATTER_DELIMITER:
        raise MigrationError("missing YAML front matter")
    for index in range(1, len(lines)):
        if lines[index].strip() == FRONT_MATTER_DELIMITER:
            return lines[1:index]
    raise MigrationError("unterminated YAML front matter")


def get_nested_value(front_matter: list[str], section: str, key: str) -> str | None:
    """Extract ``section.key`` from indented front matter lines."""
    in_section = False
    for line in front_matter:
        if not line.startswith(" ") and line.rstrip().endswith(":"):
            in_section = line.strip() == f"{section}:"
            continue
        if in_section:
            match = re.match(rf"\s+{re.escape(key)}:\s*(.+)$", line)
            if match:
                return match.group(1).strip().strip("'\"")
    return None


def derive_slug(stem: str) -> str:
    """Strip a leading ``NNN-`` or ``draft-`` prefix, returning the slug."""
    match = LEADING_ID_PATTERN.match(stem)
    if not match:
        raise MigrationError(f"unexpected file name: {stem}")
    return match.group("slug")


def rewrite_plan_content(content: str, rename: Rename) -> str:
    """Update id, name, link and H1 title inside a plan file."""
    updated = content.replace(rename.old_basename, rename.new_basename)
    # Replace the current plan.id value whatever it is: the front matter id may
    # differ from the file-name prefix (e.g. file '010-...' with id '10').
    updated = re.sub(
        r"(\bplan:\s*\n\s+id:\s*)'?[^'\"\n]+'?",
        rf"\g<1>'{rename.issue_id}'",
        updated,
        count=1,
    )
    for old_id in rename.old_ids():
        updated = updated.replace(f"Plan {old_id}", f"Plan #{rename.issue_id}")
    return updated


def plan_files(roadmap_dir: Path) -> list[Path]:
    """Return every markdown plan file, excluding roadmap.md itself."""
    return sorted(
        path
        for path in roadmap_dir.rglob("*.md")
        if path.name != "roadmap.md"
    )


def build_rename(path: Path) -> Rename | None:
    """Compute the rename for one plan file, or ``None`` if not applicable."""
    content = path.read_text(encoding="utf-8")
    front_matter = read_front_matter(content)
    issue_id = get_nested_value(front_matter, "issue", "id")
    if not issue_id or issue_id.lower() == "null":
        print(f"⏭️  {path.name}: no issue.id, skipped", file=sys.stderr)
        return None
    slug = derive_slug(path.stem)
    new_basename = f"{issue_id}-{slug}.md"
    if new_basename == path.name:
        return None
    old_prefix = path.stem.split("-", 1)[0]
    old_plan_id = get_nested_value(front_matter, "plan", "id")
    return Rename(path, path.name, new_basename, old_prefix, issue_id, old_plan_id)


def apply_rename(rename: Rename, dry_run: bool) -> None:
    """Rewrite the plan content and ``git mv`` it to its new name."""
    new_content = rewrite_plan_content(
        rename.path.read_text(encoding="utf-8"), rename
    )
    target = rename.path.with_name(rename.new_basename)
    print(f"✅ {rename.old_basename} → {rename.new_basename}")
    if dry_run:
        return
    rename.path.write_text(new_content, encoding="utf-8")
    subprocess.run(
        ["git", "mv", rename.old_basename, target.name],
        check=True,
        cwd=rename.path.parent,
    )


def rewrite_roadmap(roadmap_dir: Path, renames: list[Rename], dry_run: bool) -> None:
    """Replace old basenames and ``NNN`` references inside roadmap.md."""
    roadmap = roadmap_dir / "roadmap.md"
    if not roadmap.exists():
        return
    content = roadmap.read_text(encoding="utf-8")
    for rename in renames:
        content = content.replace(rename.old_basename, rename.new_basename)
        for old_id in rename.old_ids():
            content = content.replace(f"`{old_id}`", f"`#{rename.issue_id}`")
    print("📋 roadmap.md updated")
    if not dry_run:
        roadmap.write_text(content, encoding="utf-8")


def patch_issue(rename: Rename, dry_run: bool) -> None:
    """Fix plan references in the GitHub issue body and add a trace comment."""
    body = subprocess.run(
        ["gh", "issue", "view", rename.issue_id, "--json", "body", "-q", ".body"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    fixed = body.replace(rename.old_basename, rename.new_basename)
    for old_id in rename.old_ids():
        fixed = fixed.replace(f"Plan {old_id}", f"Plan #{rename.issue_id}")
    print(f"🔗 issue #{rename.issue_id} patched")
    if dry_run:
        return
    if fixed != body:
        subprocess.run(
            ["gh", "issue", "edit", rename.issue_id, "--body", fixed], check=True
        )
    subprocess.run(
        [
            "gh",
            "issue",
            "comment",
            rename.issue_id,
            "--body",
            f"📝 Plan file renamed: `{rename.old_basename}` → "
            f"`{rename.new_basename}` (id aligned with issue number).",
        ],
        check=True,
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap-dir", type=Path, default=Path("doc/roadmap"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--patch-issues", action="store_true")
    return parser.parse_args()


def main() -> int:
    """Entry point: migrate every plan file under the roadmap directory."""
    args = parse_args()
    if not args.roadmap_dir.is_dir():
        print(f"❌ not a directory: {args.roadmap_dir}", file=sys.stderr)
        return 1
    renames: list[Rename] = []
    for path in plan_files(args.roadmap_dir):
        try:
            rename = build_rename(path)
        except MigrationError as error:
            print(f"⚠️  {path.name}: {error}", file=sys.stderr)
            continue
        if rename is not None:
            renames.append(rename)
    for rename in renames:
        apply_rename(rename, args.dry_run)
        if args.patch_issues:
            patch_issue(rename, args.dry_run)
    rewrite_roadmap(args.roadmap_dir, renames, args.dry_run)
    print(f"\nDone: {len(renames)} plan(s) migrated{' (dry-run)' if args.dry_run else ''}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
