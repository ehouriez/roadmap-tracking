#!/usr/bin/env python3
"""Audit roadmap integrity from plan front matter — report, never auto-destroy.

Reads only the front matter of every plan (root + ``done/`` + ``_archives/``)
plus the generated ``.index.json`` and ``done/INDEX.md``. It reports drift that
accumulates silently (report findings F3/F4/F6 of the 2026-10-17 audit) and
*proposes* a correction for each one — it never moves, deletes or rewrites a
file. Applying a fix is a separate, operator-driven act.

Checks:
- status in enum        — status is one of active/blocked/done/archived
                          (a historical variant in-progress/cancelled is flagged
                          as mappable; anything else as unknown).
- status vs location    — done lives in done/, archived in _archives/, and an
                          active/blocked plan is not buried in either.
- dependency integrity  — every depends_on id resolves to a known plan.
- done index links      — every file linked from done/INDEX.md exists on disk.
- index freshness       — the on-disk .index.json matches a fresh rebuild.

Usage:
    python doctor.py [--roadmap-dir DIR] [--dry-run] [--self-check]

``--dry-run`` is the default and the only on-disk mode: doctor never writes.
Exit code 0 when no finding, 1 when at least one finding is reported.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# scripts/ is on sys.path[0] when run as a script, so the sibling imports work.
from build_roadmap import (
    CANONICAL_STATUSES,
    INDEX_FILENAME,
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
ARCHIVES_DIR = "_archives"
# shortcut: normalize_status.py (plan #27 step 11) is not implemented yet; the
# proposed fixes name it as the command to run once it ships. Until then these
# are manual edits. Upgrade the wording when step 11 lands.
NORMALIZE_SCRIPT = "scripts/normalize_status.py (livré étape 11)"


class Finding:
    """One integrity issue with a non-destructive proposed correction."""

    def __init__(self, category: str, plan: str, issue: str, fix: str) -> None:
        self.category = category
        self.plan = plan
        self.issue = issue
        self.fix = fix


def raw_status(path: Path) -> str | None:
    """Return the status exactly as written in the front matter (no mapping).

    Returns None when the file has no parseable front matter or no status — such
    a file is not a conformant plan and is skipped by the status checks.
    """
    try:
        front_matter = read_front_matter(path.read_text(encoding="utf-8"))
    except MigrationError:
        return None
    return get_top_value(front_matter, "status")


def location_of(rel_path: str) -> str:
    """Return the top-level folder a plan lives in: done/, _archives/ or root."""
    head = Path(rel_path).parts[0] if Path(rel_path).parts else ""
    if head == DONE_DIR:
        return DONE_DIR
    if head == ARCHIVES_DIR:
        return ARCHIVES_DIR
    return "root"


def check_status_enum(roadmap_dir: Path) -> list[Finding]:
    """Flag any plan whose written status is not a canonical value."""
    findings: list[Finding] = []
    for path in plan_files(roadmap_dir):
        status = raw_status(path)
        if status is None or status in CANONICAL_STATUSES:
            continue
        rel = path.relative_to(roadmap_dir).as_posix()
        if status in STATUS_MAPPING:
            target = STATUS_MAPPING[status]
            findings.append(Finding(
                "statut hors-enum (mappable)", rel,
                f"`{status}` → `{target}`",
                f"normaliser via `{NORMALIZE_SCRIPT}` ou éditer `status: {target}`",
            ))
        else:
            findings.append(Finding(
                "statut inconnu", rel,
                f"`{status}` ∉ {{{', '.join(CANONICAL_STATUSES)}}}",
                "corriger manuellement le champ `status` (valeur non reconnue)",
            ))
    return findings


def check_status_location(index: list[dict]) -> list[Finding]:
    """Flag a mismatch between a plan's status and the folder it sits in."""
    findings: list[Finding] = []
    for entry in index:
        status, loc = entry["status"], location_of(entry["path"])
        if status == "done" and loc != DONE_DIR:
            findings.append(Finding(
                "plan mal placé", entry["path"], "`done` hors de `done/`",
                f"déplacer vers `{DONE_DIR}/` (`git mv`)",
            ))
        elif status == "archived" and loc != ARCHIVES_DIR:
            findings.append(Finding(
                "plan mal placé", entry["path"], "`archived` hors de `_archives/`",
                f"déplacer vers `{ARCHIVES_DIR}/` (`git mv`, créer le dossier si absent)",
            ))
        elif status in ("active", "blocked") and loc != "root":
            findings.append(Finding(
                "plan mal placé", entry["path"], f"`{status}` dans `{loc}/`",
                "déplacer à la racine de `doc/roadmap/` (`git mv`)",
            ))
    return findings


def check_dependencies(index: list[dict]) -> list[Finding]:
    """Flag a depends_on id that resolves to no known plan."""
    known = {entry["id"] for entry in index}
    findings: list[Finding] = []
    for entry in index:
        for dep in entry["deps"]:
            if dep not in known:
                findings.append(Finding(
                    "dépendance orpheline", entry["path"],
                    f"`depends_on: {dep}` introuvable",
                    "corriger ou retirer la dépendance (aucun plan avec cet id)",
                ))
    return findings


def check_done_links(roadmap_dir: Path) -> list[Finding]:
    """Flag a done/INDEX.md link whose target file is missing on disk."""
    index_md = roadmap_dir / DONE_DIR / "INDEX.md"
    if not index_md.exists():
        return []
    findings: list[Finding] = []
    for line in index_md.read_text(encoding="utf-8").splitlines():
        # Links are rendered as [`name`](name) by build_roadmap; the target is
        # the parenthesised relative name inside the done/ folder.
        if "](" not in line:
            continue
        target = line.split("](", 1)[1].split(")", 1)[0].strip()
        if not target.endswith(".md"):
            continue
        if not (roadmap_dir / DONE_DIR / target).exists():
            findings.append(Finding(
                "lien done/ orphelin", f"{DONE_DIR}/INDEX.md",
                f"`{target}` introuvable",
                f"régénérer l'index via `python3 scripts/build_roadmap.py --write`",
            ))
    return findings


def check_index_fresh(roadmap_dir: Path, index: list[dict]) -> list[Finding]:
    """Flag a stale or missing .index.json against a fresh rebuild."""
    index_path = roadmap_dir / INDEX_FILENAME
    fix = "régénérer via `python3 scripts/build_roadmap.py --write`"
    if not index_path.exists():
        return [Finding("index absent", INDEX_FILENAME, "fichier manquant", fix)]
    try:
        on_disk = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [Finding("index corrompu", INDEX_FILENAME, f"JSON invalide: {error}", fix)]
    if on_disk != index:
        return [Finding("index périmé", INDEX_FILENAME, "diffère du front matter", fix)]
    return []


def run_doctor(roadmap_dir: Path) -> list[Finding]:
    """Run every check and return the aggregated findings."""
    index = build_index(roadmap_dir)
    return [
        *check_status_enum(roadmap_dir),
        *check_status_location(index),
        *check_dependencies(index),
        *check_done_links(roadmap_dir),
        *check_index_fresh(roadmap_dir, index),
    ]


def render_report(findings: list[Finding]) -> str:
    """Render findings as a markdown table (empty = all clear)."""
    if not findings:
        return "✅ doctor — aucune incohérence détectée."
    lines = [
        f"⚠️  doctor — {len(findings)} incohérence(s) détectée(s) :",
        "",
        "| Catégorie | Plan | Problème | Correction proposée |",
        "|---|---|---|---|",
    ]
    for f in findings:
        lines.append(f"| {f.category} | `{f.plan}` | {f.issue} | {f.fix} |")
    lines.append("")
    lines.append("> Corrections **proposées** — doctor ne modifie jamais de fichier.")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap-dir", type=Path, default=Path("doc/roadmap"))
    parser.add_argument("--dry-run", action="store_true", help="Default: report only, change nothing.")
    parser.add_argument("--self-check", action="store_true", help="Run built-in tests and exit.")
    return parser.parse_args()


def self_check() -> int:
    """Assert-based self-check on in-memory fixtures (no disk writes)."""
    assert location_of("27-x.md") == "root"
    assert location_of("done/9-x.md") == DONE_DIR
    assert location_of("_archives/3-x.md") == ARCHIVES_DIR

    index = [
        {"id": "1", "status": "active", "deps": ["999"], "path": "1-a.md",
         "priority": "high", "complexity": "M", "title": "A"},
        {"id": "2", "status": "done", "deps": [], "path": "2-done.md",
         "priority": "low", "complexity": "S", "title": "B"},
        {"id": "3", "status": "archived", "deps": [], "path": "_archives/3-arch.md",
         "priority": "low", "complexity": "S", "title": "C"},
    ]
    loc = check_status_location(index)
    assert any(f.plan == "2-done.md" for f in loc), "done at root not flagged"
    assert not any(f.plan == "_archives/3-arch.md" for f in loc), "archived in _archives/ wrongly flagged"
    deps = check_dependencies(index)
    assert len(deps) == 1 and deps[0].plan == "1-a.md", "orphan dep not flagged"
    assert render_report([]).startswith("✅"), "clean report wrong"
    assert "| Catégorie |" in render_report(deps), "report not a table"
    print("✅ self-check passed")
    return 0


def main() -> int:
    """Entry point: run the audit and report."""
    args = parse_args()
    if args.self_check:
        return self_check()
    if not args.roadmap_dir.is_dir():
        print(f"❌ not a directory: {args.roadmap_dir}", file=sys.stderr)
        return 1
    findings = run_doctor(args.roadmap_dir)
    print(render_report(findings))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
