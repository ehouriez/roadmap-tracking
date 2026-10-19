#!/usr/bin/env python3
"""Generate the roadmap views from plan front matter — the single source of truth.

Scans every plan file under the roadmap directory (root + ``done/``) and emits
three generated artifacts:

- ``.index.json``  — a compact machine index read by the skill at session start
  instead of the full ``roadmap.md`` narrative (one entry per plan:
  ``{id, status, priority, complexity, title, deps, path}``).
- ``roadmap.md``   — the human-readable active backlog (status ``active`` /
  ``blocked``), sorted by priority then id.
- ``done/INDEX.md``— a compact table of closed plans (status ``done``).

The front-matter parser is reused from ``migrate_plan_ids.py`` (same directory)
so there is a single parsing implementation.

Usage:
    python build_roadmap.py [--roadmap-dir DIR] [--dry-run] [--write] [--check]

Modes (mutually exclusive, --dry-run is the default):
    --dry-run  Print what would be written; change nothing. Default.
    --write    Write .index.json, roadmap.md and done/INDEX.md.
    --check    Compare the generated index with the on-disk .index.json and
               exit non-zero on any drift (for CI / staleness detection).
    --self-check  Run the built-in assertions on an in-memory fixture and exit.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# scripts/ is on sys.path[0] when run as a script, so the sibling import works.
from migrate_plan_ids import (
    MigrationError,
    get_nested_value,
    get_top_value,
    plan_files,
    read_front_matter,
)

INDEX_FILENAME = ".index.json"

# Status vocabulary — mirrors references/roadmap-file.md § Vocabulaire de statut.
CANONICAL_STATUSES = ("active", "blocked", "done", "archived")
STATUS_MAPPING = {"in-progress": "active", "cancelled": "archived"}
STATUS_ICONS = {"active": "🟢", "blocked": "🔴", "done": "🔵", "archived": "⚪"}
BACKLOG_STATUSES = ("active", "blocked")

# Priority ordering for the backlog (highest first); FR labels for roadmap.md.
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
PRIORITY_LABELS_FR = {
    "critical": "CRITIQUE",
    "high": "HAUTE",
    "medium": "MOYENNE",
    "low": "BASSE",
}


def map_status(raw: str | None) -> str | None:
    """Return the canonical status, applying the historical mapping.

    A value already canonical is returned unchanged; a mapped variant is
    translated; any other value is returned as-is (so --check / doctor can flag
    it rather than this generator silently swallowing it).
    """
    if raw is None:
        return None
    return STATUS_MAPPING.get(raw, raw)


def get_top_list(front_matter: list[str], key: str) -> list[str]:
    """Extract a top-level YAML list ``key:`` with ``- item`` entries.

    Returns the item values (quotes stripped). Empty list if the key is absent
    or carries no list items — the only list field a plan uses is ``depends_on``.
    """
    items: list[str] = []
    in_key = False
    for line in front_matter:
        if not line.startswith((" ", "\t")):
            in_key = line.strip() == f"{key}:"
            continue
        if in_key:
            match = re.match(r"\s+-\s*(.+)$", line)
            if match:
                items.append(match.group(1).strip().strip("'\""))
            elif line.strip():  # a non-list indented line ends the block
                break
    return items


def first_h1(content: str) -> str | None:
    """Return the first level-1 Markdown heading text, without the leading '#'."""
    match = re.search(r"(?m)^#\s+(.+?)\s*$", content)
    return match.group(1).strip() if match else None


def load_plan(path: Path, roadmap_dir: Path) -> dict | None:
    """Build one index entry from a plan file, or None if it is not a plan.

    A file without parseable front matter or without ``plan.id`` is not a plan
    (roadmap.md, INDEX.md, CONTEXT.md…) and is skipped.
    """
    content = path.read_text(encoding="utf-8")
    try:
        front_matter = read_front_matter(content)
    except MigrationError:
        return None
    plan_id = get_nested_value(front_matter, "plan", "id")
    if not plan_id:
        return None
    return {
        "id": plan_id,
        "status": map_status(get_top_value(front_matter, "status")),
        "priority": get_top_value(front_matter, "priority"),
        "complexity": get_top_value(front_matter, "complexity"),
        "title": first_h1(content),
        "deps": get_top_list(front_matter, "depends_on"),
        "path": path.relative_to(roadmap_dir).as_posix(),
    }


def build_index(roadmap_dir: Path) -> list[dict]:
    """Scan every plan file and return the index entries, sorted by numeric id."""
    entries = [
        entry
        for path in plan_files(roadmap_dir)
        if (entry := load_plan(path, roadmap_dir)) is not None
    ]
    return sorted(entries, key=lambda e: _id_sort_key(e["id"]))


def _id_sort_key(plan_id: str) -> tuple[int, str]:
    """Sort ids numerically when possible, lexically otherwise (stable)."""
    return (int(plan_id), "") if plan_id.isdigit() else (sys.maxsize, plan_id)


def _backlog_sort_key(entry: dict) -> tuple[int, tuple[int, str]]:
    """Order the backlog by priority (critical→low) then by id."""
    priority_rank = PRIORITY_ORDER.get(entry["priority"], len(PRIORITY_ORDER))
    return (priority_rank, _id_sort_key(entry["id"]))


def _entry_label(entry: dict, mode: str) -> str:
    """Return the '[Issue: #NN]' or '[Plan: NN]' label per issue mode."""
    if mode == "github":
        return f"[Issue: #{entry['id']}]"
    return f"[Plan: {entry['id']}]"


def render_roadmap(index: list[dict], project_name: str, mode: str, today: str) -> str:
    """Render the active backlog (status active/blocked) as roadmap.md."""
    backlog = sorted(
        (e for e in index if e["status"] in BACKLOG_STATUSES), key=_backlog_sort_key
    )
    lines = [
        f"# Roadmap {project_name}",
        "",
        "> Backlog actif généré depuis le front matter des plans (source de vérité).",
        "> Ne pas éditer à la main : régénéré par `scripts/build_roadmap.py`.",
        f"> Dernière génération : {today}.",
        "",
        "## À faire",
        "",
    ]
    if not backlog:
        lines.append("_Aucun plan actif._")
        lines.append("")
    for entry in backlog:
        priority = PRIORITY_LABELS_FR.get(entry["priority"], (entry["priority"] or "?").upper())
        icon = STATUS_ICONS.get(entry["status"], "")
        title = entry["title"] or entry["path"]
        label = _entry_label(entry, mode)
        lines.append(
            f"### {label} {title} [PRIORITÉ: {priority}] "
            f"[Complexité: {entry['complexity'] or '?'}] {icon}".rstrip()
        )
        lines.append("")
        lines.append(f"Plan : [`{entry['path']}`]({entry['path']})")
        if entry["deps"]:
            lines.append("")
            lines.append("Dépend de : " + ", ".join(f"#{dep}" for dep in entry["deps"]))
        lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_done_index(index: list[dict], mode: str, today: str) -> str:
    """Render the compact table of closed plans as done/INDEX.md."""
    done = sorted((e for e in index if e["status"] == "done"), key=_id_sort_key_entry)
    id_header = "Issue" if mode == "github" else "Plan"
    lines = [
        "# Historique des plans clôturés",
        "",
        f"> Index généré par `scripts/build_roadmap.py` — dernière génération : {today}.",
        "> Non lu au démarrage de session ; consultable sur demande.",
        "",
        f"| {id_header} | Titre | Priorité | Complexité | Fichier |",
        "|---|---|---|---|---|",
    ]
    for entry in done:
        ref = f"#{entry['id']}" if mode == "github" else entry["id"]
        title = entry["title"] or entry["path"]
        name = Path(entry["path"]).name
        lines.append(
            f"| {ref} | {title} | {entry['priority'] or '?'} | "
            f"{entry['complexity'] or '?'} | [`{name}`]({name}) |"
        )
    if not done:
        lines.append("| — | _Aucun plan clôturé._ | — | — | — |")
    return "\n".join(lines) + "\n"


def _id_sort_key_entry(entry: dict) -> tuple[int, str]:
    """Numeric id sort for a whole index entry (done index ordering)."""
    return _id_sort_key(entry["id"])


def derive_project_name(roadmap_dir: Path) -> str:
    """Reuse the current roadmap.md H1 project name, else fall back to the dir.

    Keeps '# Roadmap <name>' stable across regenerations instead of inventing a
    new name each time.
    """
    roadmap = roadmap_dir / "roadmap.md"
    if roadmap.exists():
        h1 = first_h1(roadmap.read_text(encoding="utf-8"))
        if h1 and h1.lower().startswith("roadmap "):
            return h1[len("roadmap ") :].strip()
    return roadmap_dir.resolve().parent.parent.name


def _today() -> str:
    """Return today's date as YYYY-MM-DD (local)."""
    from datetime import date

    return date.today().isoformat()


def generate(roadmap_dir: Path, mode: str) -> dict[str, str]:
    """Return the three generated artifacts keyed by their relative path."""
    index = build_index(roadmap_dir)
    today = _today()
    project_name = derive_project_name(roadmap_dir)
    return {
        INDEX_FILENAME: json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        "roadmap.md": render_roadmap(index, project_name, mode, today),
        "done/INDEX.md": render_done_index(index, mode, today),
    }


def run_check(roadmap_dir: Path, mode: str) -> int:
    """Compare the freshly built index with the on-disk one; report drift."""
    index = build_index(roadmap_dir)
    index_path = roadmap_dir / INDEX_FILENAME
    if not index_path.exists():
        print(f"⚠️  no {INDEX_FILENAME} on disk — run with --write to create it", file=sys.stderr)
        return 1
    try:
        on_disk = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        print(f"❌ {INDEX_FILENAME} is not valid JSON: {error}", file=sys.stderr)
        return 1
    if on_disk == index:
        print(f"✅ {INDEX_FILENAME} is up to date ({len(index)} plans)")
        return 0
    print(f"⚠️  {INDEX_FILENAME} is stale — regenerate with --write", file=sys.stderr)
    on_disk_ids = {e.get("id") for e in on_disk if isinstance(e, dict)}
    fresh_ids = {e["id"] for e in index}
    for added in sorted(fresh_ids - on_disk_ids):
        print(f"   + plan {added} missing from index", file=sys.stderr)
    for removed in sorted(on_disk_ids - fresh_ids):
        print(f"   - plan {removed} in index but no longer a plan", file=sys.stderr)
    return 1


def emit(roadmap_dir: Path, mode: str, write: bool) -> int:
    """Generate the artifacts and either write them or print a dry-run summary."""
    artifacts = generate(roadmap_dir, mode)
    index_count = len(json.loads(artifacts[INDEX_FILENAME]))
    for rel_path, content in artifacts.items():
        target = roadmap_dir / rel_path
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            print(f"✅ wrote {rel_path} ({len(content)} bytes)")
        else:
            print(f"📋 would write {rel_path} ({len(content)} bytes)")
    verb = "Wrote" if write else "Would write"
    print(f"\n{verb} index for {index_count} plans (mode: {mode}).")
    if not write:
        print("   (dry-run — nothing changed; pass --write to apply)")
    return 0


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap-dir", type=Path, default=Path("doc/roadmap"))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", help="Default: change nothing.")
    group.add_argument("--write", action="store_true", help="Write the generated files.")
    group.add_argument("--check", action="store_true", help="Fail on index drift.")
    group.add_argument("--self-check", action="store_true", help="Run built-in tests and exit.")
    parser.add_argument("--mode", choices=["github", "local"], help="Override the issue mode.")
    return parser.parse_args()


def self_check() -> int:
    """Assert-based self-check on an in-memory fixture (no disk writes)."""
    assert map_status("in-progress") == "active"
    assert map_status("cancelled") == "archived"
    assert map_status("active") == "active"
    assert map_status("weird") == "weird"  # unknown is passed through, not swallowed
    assert get_top_list(["depends_on:", "  - '16'", "  - '17'", "other: x"], "depends_on") == ["16", "17"]
    assert get_top_list(["status: active"], "depends_on") == []
    assert first_h1("---\nx: 1\n---\n\n# [🔧] Plan #5 - Foo\n") == "[🔧] Plan #5 - Foo"
    assert _id_sort_key("27") < _id_sort_key("100")

    index = [
        {"id": "3", "status": "active", "priority": "low", "complexity": "S", "title": "Low one", "deps": [], "path": "3-low.md"},
        {"id": "1", "status": "blocked", "priority": "high", "complexity": "M", "title": "High one", "deps": ["3"], "path": "1-high.md"},
        {"id": "9", "status": "done", "priority": "medium", "complexity": "L", "title": "Done one", "deps": [], "path": "done/9-done.md"},
    ]
    roadmap = render_roadmap(index, "Test", "github", "2026-10-19")
    # Priority sort: high (#1) must appear before low (#3); done (#9) excluded.
    assert roadmap.index("#1") < roadmap.index("#3"), "backlog not sorted by priority"
    assert "9-done.md" not in roadmap, "done plan leaked into backlog"
    assert "Dépend de : #3" in roadmap, "deps not rendered"
    done_index = render_done_index(index, "github", "2026-10-19")
    assert "9-done.md" in done_index and "1-high.md" not in done_index, "done index wrong set"
    print("✅ self-check passed")
    return 0


def main() -> int:
    """Entry point: dispatch to the selected mode."""
    args = parse_args()
    if args.self_check:
        return self_check()
    if not args.roadmap_dir.is_dir():
        print(f"❌ not a directory: {args.roadmap_dir}", file=sys.stderr)
        return 1
    # Reuse migrate_plan_ids' issue-mode resolution (reads .skill-config.yml).
    from migrate_plan_ids import load_issue_mode

    mode = load_issue_mode(args.roadmap_dir, args.mode)
    if args.check:
        return run_check(args.roadmap_dir, mode)
    return emit(args.roadmap_dir, mode, write=args.write)


if __name__ == "__main__":
    raise SystemExit(main())
