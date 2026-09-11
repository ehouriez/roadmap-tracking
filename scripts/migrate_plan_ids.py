#!/usr/bin/env python3
"""Migrate roadmap plan files from sequential NNN ids to GitHub-issue ids.

Renames every ``NNN-slug.md`` (or ``draft-slug.md``) plan file to
``{issue}-slug.md``, then rewrites the plan's own metadata, the consolidated
``roadmap.md`` links and, optionally, the referencing GitHub issues.

The target issue number is resolved for each plan in this order:

1. ``issue.id`` in the plan's YAML front matter (the nominal case).
2. A user-supplied mapping ``old-id -> issue`` passed with ``--map`` or
   ``--map-file`` — the only way to migrate a legacy plan whose front matter
   is absent or carries no ``issue.id`` (the number is never guessed).

A plan that resolves to no issue number is left untouched and listed in a final
report so the user knows exactly which mappings to provide. Plans that are
explicitly local (``plan.source: local`` or ``issue.id: null``) are reported as
local and never migrated. When the whole project is in ``local`` issue mode,
migration does not apply and nothing is touched.

Usage:
    python migrate_plan_ids.py [--roadmap-dir DIR] [--dry-run] [--patch-issues]
                               [--map OLD=ISSUE,...] [--map-file FILE]
                               [--mode github|local]
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


@dataclass
class Outcome:
    """The classification of one plan file after resolving its issue number.

    ``kind`` is one of:
    - ``migrate``: an issue number was resolved; ``rename`` and ``source`` set.
    - ``local``: an explicitly local plan; never migrated.
    - ``pending``: a GitHub plan with no resolvable issue number; ``reason``
      explains why and the report tells the user to supply a mapping.
    - ``noop``: already named after its issue number; nothing to do.
    """

    path: Path
    kind: str
    rename: Rename | None = None
    source: str = ""
    reason: str = ""


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
    """Return the slug: the stem without any leading ``NNN-`` / ``draft-``.

    A stem that carries no such prefix is returned unchanged, so a plan mapped
    explicitly (via ``--map``) can still be renamed to ``{issue}-{stem}.md``.
    """
    match = LEADING_ID_PATTERN.match(stem)
    return match.group("slug") if match else stem


def mapping_keys(stem: str) -> list[str]:
    """Return the keys under which a plan may be looked up in a mapping.

    A user may key a mapping entry by the file-name prefix ('010' or its
    zero-stripped form '10'), by the slug, or by the full stem — all are
    accepted so the mapping stays forgiving.
    """
    keys = {stem, derive_slug(stem)}
    prefix = stem.split("-", 1)[0]
    keys.add(prefix)
    if prefix.isdigit():
        keys.add(str(int(prefix)))
    return [key for key in keys if key]


def rewrite_plan_id(content: str, issue_id: str) -> str:
    """Rewrite ``plan.id`` to ``issue_id`` regardless of key order.

    The ``id`` key may not be the first entry under ``plan:`` (a plan that does
    not follow the template ordering), so the whole ``plan:`` block is isolated
    first and only its ``id`` line is rewritten — the ``issue.id`` block, which
    also carries an ``id`` key, is left untouched.
    """

    def fix_block(match: re.Match) -> str:
        return re.sub(
            r"(?m)^(\s+id:\s*)'?[^'\"\n]*'?[ \t]*$",
            rf"\g<1>'{issue_id}'",
            match.group(0),
            count=1,
        )

    return re.sub(
        r"(?ms)^plan:[ \t]*\n(?:[ \t]+\S.*\n?)*",
        fix_block,
        content,
        count=1,
    )


def rewrite_plan_label(text: str, old_ids: list[str], issue_id: str) -> str:
    """Rewrite ``Plan NNN`` / ``Plan #NNN`` references to ``Plan #{issue_id}``.

    Matches both the legacy ``Plan 10`` form and the current template form
    ``Plan #10`` (see ``references/templates.md``), and anchors on word
    boundaries so ``Plan 10`` never rewrites the start of ``Plan 100``.
    """
    for old_id in old_ids:
        text = re.sub(
            rf"\bPlan\s+#?{re.escape(old_id)}\b",
            f"Plan #{issue_id}",
            text,
        )
    return text


def rewrite_plan_content(content: str, rename: Rename) -> str:
    """Update id, name, link and H1 title inside a plan file."""
    updated = content.replace(rename.old_basename, rename.new_basename)
    updated = rewrite_plan_id(updated, rename.issue_id)
    updated = rewrite_plan_label(updated, rename.old_ids(), rename.issue_id)
    return updated


def plan_files(roadmap_dir: Path) -> list[Path]:
    """Return every markdown plan file, excluding roadmap.md itself."""
    return sorted(
        path
        for path in roadmap_dir.rglob("*.md")
        if path.name != "roadmap.md"
    )


def parse_mapping(inline: str | None, map_file: Path | None) -> dict[str, str]:
    """Parse ``OLD=ISSUE`` pairs from ``--map`` and/or ``--map-file``.

    Inline pairs are comma-separated (``10=42,8=51``); a file holds one pair per
    line (``10 = 42``), ignoring blank lines and ``#`` comments. Raises on a
    malformed pair so a typo never silently drops a plan.
    """
    mapping: dict[str, str] = {}
    tokens: list[str] = []
    if inline:
        tokens.extend(inline.split(","))
    if map_file:
        for raw in map_file.read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0].strip()
            if line:
                tokens.append(line)
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        if "=" not in token:
            raise MigrationError(f"invalid mapping entry (expected OLD=ISSUE): {token!r}")
        old, issue = (part.strip() for part in token.split("=", 1))
        if not old or not issue:
            raise MigrationError(f"invalid mapping entry (expected OLD=ISSUE): {token!r}")
        mapping[old] = issue
    return mapping


def load_issue_mode(roadmap_dir: Path, override: str | None) -> str:
    """Return the effective issue mode: ``github`` or ``local``.

    An explicit ``--mode`` wins; otherwise ``issues.mode`` from
    ``.skill-config.yml`` is honoured; anything else (absent, ``auto``) defaults
    to ``github`` for backward compatibility.
    """
    if override:
        return override
    config = roadmap_dir / ".skill-config.yml"
    if config.exists():
        mode = get_nested_value(config.read_text(encoding="utf-8").splitlines(), "issues", "mode")
        if mode == "local":
            return "local"
    return "github"


def resolve_issue_id(
    path: Path, front_matter: list[str], mapping: dict[str, str]
) -> tuple[str | None, str]:
    """Resolve the target issue number and its source for one plan file.

    Front matter ``issue.id`` takes precedence; failing that, the mapping is
    consulted. Returns ``(None, "")`` when the number cannot be resolved.
    """
    issue_id = get_nested_value(front_matter, "issue", "id")
    if issue_id and issue_id.lower() != "null":
        return issue_id, "front matter"
    for key in mapping_keys(path.stem):
        if key in mapping:
            return mapping[key], "--map"
    return None, ""


def classify_plan(path: Path, mapping: dict[str, str]) -> Outcome:
    """Classify one plan file: migrate, local, pending or noop."""
    content = path.read_text(encoding="utf-8")
    try:
        front_matter = read_front_matter(content)
        has_front_matter = True
    except MigrationError:
        front_matter = []
        has_front_matter = False

    source = get_nested_value(front_matter, "plan", "source")
    raw_issue = get_nested_value(front_matter, "issue", "id")
    is_local = source == "local" or (raw_issue is not None and raw_issue.lower() == "null")
    if is_local:
        return Outcome(path, "local", reason="local plan (no GitHub issue)")

    issue_id, id_source = resolve_issue_id(path, front_matter, mapping)
    if not issue_id:
        reason = (
            "no front matter and no --map entry"
            if not has_front_matter
            else "no issue.id and no --map entry"
        )
        return Outcome(path, "pending", reason=reason)

    slug = derive_slug(path.stem)
    new_basename = f"{issue_id}-{slug}.md"
    if new_basename == path.name:
        return Outcome(path, "noop")
    old_prefix = path.stem.split("-", 1)[0]
    old_plan_id = get_nested_value(front_matter, "plan", "id")
    rename = Rename(path, path.name, new_basename, old_prefix, issue_id, old_plan_id)
    return Outcome(path, "migrate", rename=rename, source=id_source)


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
    if not renames or not roadmap.exists():
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
    fixed = rewrite_plan_label(fixed, rename.old_ids(), rename.issue_id)
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
    parser.add_argument(
        "--map",
        dest="mapping",
        metavar="OLD=ISSUE,...",
        help="Comma-separated old-id to issue-number pairs (e.g. 10=42,8=51).",
    )
    parser.add_argument(
        "--map-file",
        type=Path,
        help="File with one OLD=ISSUE pair per line ('#' comments allowed).",
    )
    parser.add_argument(
        "--mode",
        choices=["github", "local"],
        help="Override the issue mode (default: read .skill-config.yml, else github).",
    )
    return parser.parse_args()


def print_report(outcomes: list[Outcome], dry_run: bool) -> None:
    """Print a grouped summary so the user knows exactly what to do next."""
    migrated = [o for o in outcomes if o.kind == "migrate"]
    pending = [o for o in outcomes if o.kind == "pending"]
    local = [o for o in outcomes if o.kind == "local"]
    suffix = " (dry-run)" if dry_run else ""

    print(f"\n━━━ Summary{suffix} ━━━")
    print(f"✅ Migrated: {len(migrated)}")
    for outcome in migrated:
        rename = outcome.rename
        print(f"   {rename.old_basename} → {rename.new_basename}  (id from {outcome.source})")

    if local:
        print(f"\nℹ️  Local plans, no migration needed: {len(local)}")
        for outcome in local:
            print(f"   {outcome.path.name}")

    if pending:
        print(f"\n⚠️  Not migrated — no issue number found: {len(pending)}")
        for outcome in pending:
            print(f"   {outcome.path.name}  ({outcome.reason})")
        hint = ",".join(f"{o.path.stem.split('-', 1)[0]}=<issue>" for o in pending)
        print(
            "\n   To migrate these, provide the plan-to-issue mapping and re-run, e.g.:\n"
            f"     --map {hint}\n"
            "   (replace each <issue> with the real GitHub issue number)."
        )


def main() -> int:
    """Entry point: migrate every plan file under the roadmap directory."""
    args = parse_args()
    if not args.roadmap_dir.is_dir():
        print(f"❌ not a directory: {args.roadmap_dir}", file=sys.stderr)
        return 1

    if load_issue_mode(args.roadmap_dir, args.mode) == "local":
        print("ℹ️  Local issue mode — NNN→issue migration does not apply. Nothing to do.")
        return 0

    try:
        mapping = parse_mapping(args.mapping, args.map_file)
    except MigrationError as error:
        print(f"❌ {error}", file=sys.stderr)
        return 1

    outcomes = [classify_plan(path, mapping) for path in plan_files(args.roadmap_dir)]
    renames = [outcome.rename for outcome in outcomes if outcome.kind == "migrate"]
    for rename in renames:
        apply_rename(rename, args.dry_run)
        if args.patch_issues:
            patch_issue(rename, args.dry_run)
    rewrite_roadmap(args.roadmap_dir, renames, args.dry_run)
    print_report(outcomes, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
