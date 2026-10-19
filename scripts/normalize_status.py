#!/usr/bin/env python3
"""Normalise plan statuses and move misplaced plans in bulk.

Two operations (always idempotent):
1. Status rewrite  — maps legacy status values to canonical ones in front matter
   (in-progress→active, cancelled→archived).  Uses the same STATUS_MAPPING as
   ``build_roadmap.py``.
2. Location move   — moves a plan whose canonical status implies a subdirectory
   to the right place:
   - ``status: done``     → ``done/``
   - ``status: archived`` → ``archived/``
   - ``status: active/blocked`` found inside ``done/`` or ``archived/``
     → moved back to root.
   Creates the target directory when it does not exist yet.

Usage:
    python normalize_status.py [--roadmap-dir DIR] [--dry-run] [--write]
                               [--self-check]

``--dry-run`` is the default: prints what would change, touches nothing.
``--write`` applies both rewrites and moves and prints a git rollback hint.
Exit code: 0 (nothing to do or all changes applied), 1 (error).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from build_roadmap import (
    CANONICAL_STATUSES,
    STATUS_MAPPING,
    build_index,
)
from migrate_plan_ids import (
    MigrationError,
    get_top_value,
    plan_files,
    read_front_matter,
)

DONE_DIR = "done"
ARCHIVES_DIR = "archived"

LOCATION_FOR_STATUS: dict[str, str] = {
    "done": DONE_DIR,
    "archived": ARCHIVES_DIR,
}


def location_of(rel_path: str) -> str:
    """Return the top-level folder a plan lives in."""
    head = Path(rel_path).parts[0] if Path(rel_path).parts else ""
    if head in (DONE_DIR, ARCHIVES_DIR):
        return head
    return "root"


# ---------------------------------------------------------------------------
# Status rewrite
# ---------------------------------------------------------------------------

def _rewrite_status_in_text(text: str, new_status: str) -> str:
    """Replace the ``status: <value>`` line inside the front-matter block."""
    return re.sub(
        r'^(status:\s*)(.+)$',
        lambda m: m.group(1) + new_status,
        text,
        count=1,
        flags=re.MULTILINE,
    )


def collect_status_rewrites(
    roadmap_dir: Path,
) -> list[tuple[Path, str, str]]:
    """Return (path, old_status, new_status) for every plan needing a rewrite."""
    results = []
    for path in plan_files(roadmap_dir):
        try:
            text = path.read_text(encoding="utf-8")
            front_matter = read_front_matter(text)
        except (MigrationError, OSError):
            continue
        raw = get_top_value(front_matter, "status")
        if raw is None or raw not in STATUS_MAPPING:
            continue
        results.append((path, raw, STATUS_MAPPING[raw]))
    return results


# ---------------------------------------------------------------------------
# Location moves
# ---------------------------------------------------------------------------

def collect_moves(roadmap_dir: Path) -> list[tuple[Path, Path]]:
    """Return (src, dst) for every plan that lives in the wrong subdirectory."""
    try:
        index = build_index(roadmap_dir)
    except Exception:
        return []
    moves = []
    for entry in index:
        canon = entry["status"]
        if canon not in CANONICAL_STATUSES:
            continue
        rel = entry["path"]
        loc = location_of(rel)
        expected = LOCATION_FOR_STATUS.get(canon)
        src = roadmap_dir / rel

        if expected is not None and loc != expected:
            dst = roadmap_dir / expected / Path(rel).name
            moves.append((src, dst))
        elif expected is None and loc != "root":
            dst = roadmap_dir / Path(rel).name
            moves.append((src, dst))
    return moves


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------

def apply_rewrites(rewrites: list[tuple[Path, str, str]]) -> None:
    for path, _old, new in rewrites:
        text = path.read_text(encoding="utf-8")
        path.write_text(_rewrite_status_in_text(text, new), encoding="utf-8")


def apply_moves(roadmap_dir: Path, moves: list[tuple[Path, Path]]) -> None:
    for src, dst in moves:
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def _report_rewrites(
    rewrites: list[tuple[Path, str, str]], roadmap_dir: Path
) -> None:
    if not rewrites:
        return
    print(f"\n📝 Status rewrites ({len(rewrites)}):")
    print("| Plan | Avant | Après |")
    print("|---|---|---|")
    for path, old, new in rewrites:
        rel = path.relative_to(roadmap_dir).as_posix()
        print(f"| `{rel}` | `{old}` | `{new}` |")


def _report_moves(
    moves: list[tuple[Path, Path]], roadmap_dir: Path
) -> None:
    if not moves:
        return
    print(f"\n📁 Déplacements ({len(moves)}):")
    print("| Source | Destination |")
    print("|---|---|")
    for src, dst in moves:
        rel_src = src.relative_to(roadmap_dir).as_posix()
        rel_dst = dst.relative_to(roadmap_dir).as_posix()
        print(f"| `{rel_src}` | `{rel_dst}` |")


# ---------------------------------------------------------------------------
# Self-check
# ---------------------------------------------------------------------------

def self_check() -> int:
    """Assert-based self-check on in-memory fixtures (no disk writes)."""
    sample = "---\nstatus: in-progress\npriority: high\n---\n# Plan\n"
    result = _rewrite_status_in_text(sample, "active")
    assert "status: active" in result, "rewrite failed"
    assert "status: in-progress" not in result, "old value still present"

    sample2 = "---\nstatus: active\n---\n"
    result2 = _rewrite_status_in_text(sample2, "active")
    assert "status: active" in result2

    assert location_of("27-x.md") == "root"
    assert location_of("done/9-x.md") == DONE_DIR
    assert location_of("archived/3-x.md") == ARCHIVES_DIR

    print("✅ self-check passed")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap-dir", type=Path, default=Path("doc/roadmap"))
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print proposed changes without touching any file (default).",
    )
    parser.add_argument(
        "--write", action="store_true",
        help="Apply status rewrites and plan moves.",
    )
    parser.add_argument(
        "--self-check", action="store_true",
        help="Run built-in assertions and exit.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_check:
        return self_check()

    roadmap_dir = args.roadmap_dir
    if not roadmap_dir.is_dir():
        print(f"❌ not a directory: {roadmap_dir}", file=sys.stderr)
        return 1

    rewrites = collect_status_rewrites(roadmap_dir)
    moves = collect_moves(roadmap_dir)

    if not rewrites and not moves:
        print("✅ normalize — rien à faire (statuts canoniques, plans bien placés).")
        return 0

    _report_rewrites(rewrites, roadmap_dir)
    _report_moves(moves, roadmap_dir)

    if args.write:
        apply_rewrites(rewrites)
        apply_moves(roadmap_dir, moves)
        print("\n✅ normalize — modifications appliquées.")
        print(f"💡 Rollback : git checkout -- {roadmap_dir} && git stash")
        print(f"   Régénérer les vues : python3 scripts/build_roadmap.py --roadmap-dir {roadmap_dir} --write")
    else:
        print("\n(dry-run — aucun fichier modifié. Passe --write pour appliquer.)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
