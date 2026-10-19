#!/usr/bin/env python3
"""Enforce the CONTEXT.md core budget by offloading surplus sections.

The session-hydration core ``doc/roadmap/CONTEXT.md`` has a hard budget
(200 lines / 15 KiB). When it grows past either limit, this script keeps only
the "RÈGLES ABSOLUES" section(s) in the core and moves every other ``##``
section to its own thematic file under ``doc/roadmap/context/<slug>.md`` — the
files the skill loads on demand rather than at every session start.

The split is idempotent: once the core holds nothing but its preamble and the
"RÈGLES ABSOLUES" section(s), a re-run finds nothing movable and is a no-op.
A move never overwrites an existing thematic file — a collision fails loudly so
no content is lost.

Usage:
    python split_context.py [--roadmap-dir DIR] [--dry-run] [--write] [--self-check]

Modes (mutually exclusive, --dry-run is the default):
    --dry-run     Report what would move, change nothing (default).
    --write       Apply the split.
    --self-check  Run built-in tests and exit.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

MAX_LINES = 200
MAX_BYTES = 15 * 1024  # 15 KiB
CORE_HEADING_PATTERN = re.compile(r"r[eè]gles\s+absolues")
SECTION_HEADING_PATTERN = re.compile(r"^## (?!#)(.+)$")


def slugify(title: str) -> str:
    """Return a kebab-case ASCII slug derived from a ``##`` heading text."""
    folded = unicodedata.normalize("NFKD", title)
    ascii_only = folded.encode("ascii", "ignore").decode("ascii")
    kebab = re.sub(r"[^a-z0-9]+", "-", ascii_only.lower()).strip("-")
    return kebab or "section"


def is_core_heading(title: str) -> bool:
    """A section stays in the core only when its heading names the absolute rules."""
    folded = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    return bool(CORE_HEADING_PATTERN.search(folded.lower()))


def split_sections(content: str) -> tuple[str, list[tuple[str, str]]]:
    """Split ``content`` into its preamble and a list of ``(title, block)`` sections.

    ``block`` keeps the heading line and everything up to the next ``##`` (or EOF).
    The preamble is everything before the first top-level ``##`` heading.
    """
    lines = content.splitlines(keepends=True)
    boundaries = [i for i, line in enumerate(lines) if SECTION_HEADING_PATTERN.match(line.rstrip("\n"))]
    if not boundaries:
        return content, []
    preamble = "".join(lines[: boundaries[0]])
    sections: list[tuple[str, str]] = []
    for start, end in zip(boundaries, boundaries[1:] + [len(lines)]):
        title = SECTION_HEADING_PATTERN.match(lines[start].rstrip("\n")).group(1).strip()
        sections.append((title, "".join(lines[start:end])))
    return preamble, sections


def over_budget(content: str) -> bool:
    """True when the core exceeds the line budget OR the byte budget."""
    return len(content.splitlines()) > MAX_LINES or len(content.encode("utf-8")) > MAX_BYTES


def plan_split(content: str) -> tuple[str, list[tuple[str, str]]]:
    """Return the trimmed core and the ``(slug, block)`` sections to offload.

    Everything that is not a "RÈGLES ABSOLUES" section leaves the core.
    """
    preamble, sections = split_sections(content)
    kept = [block for title, block in sections if is_core_heading(title)]
    moved = [(slugify(title), block) for title, block in sections if not is_core_heading(title)]
    core = preamble + "".join(kept)
    return core, moved


def emit(roadmap_dir: Path, write: bool) -> int:
    """Measure the core and, if over budget, offload its non-core sections."""
    context_file = roadmap_dir / "CONTEXT.md"
    if not context_file.is_file():
        print(f"✅ pas de CONTEXT.md dans {roadmap_dir} — rien à faire")
        return 0
    content = context_file.read_text(encoding="utf-8")
    line_count = len(content.splitlines())
    byte_count = len(content.encode("utf-8"))
    if not over_budget(content):
        print(f"✅ CONTEXT.md dans le budget ({line_count} l. / {byte_count} o. ≤ {MAX_LINES} l. / {MAX_BYTES} o.)")
        return 0

    core, moved = plan_split(content)
    print(f"⚠️ CONTEXT.md hors budget : {line_count} l. / {byte_count} o. (seuil {MAX_LINES} l. / {MAX_BYTES} o.)")
    if not moved:
        print("⚠️ aucune section déplaçable : le noyau « RÈGLES ABSOLUES » dépasse déjà le budget à lui seul.")
        return 1

    context_dir = roadmap_dir / "context"
    targets = [(context_dir / f"{slug}.md", slug, block) for slug, block in moved]

    # Fail before touching anything if a move would clobber an existing file.
    collisions = [str(path) for path, _, _ in targets if path.exists()]
    if collisions:
        print(f"❌ cibles déjà présentes (collision, aucune écriture) : {', '.join(collisions)}", file=sys.stderr)
        return 1

    print(f"\n📦 {len(moved)} section(s) à déporter vers {context_dir}/ :")
    for path, slug, _ in targets:
        print(f"   - ## … → {path.name}")
    new_core_lines = len(core.splitlines())
    print(f"📏 noyau après découpe : {new_core_lines} l. / {len(core.encode('utf-8'))} o.")

    if not write:
        print("\n(dry-run — aucune écriture ; relance avec --write pour appliquer)")
        return 0

    context_dir.mkdir(exist_ok=True)
    for path, _, block in targets:
        path.write_text(block.rstrip("\n") + "\n", encoding="utf-8")
    context_file.write_text(core.rstrip("\n") + "\n", encoding="utf-8")
    print("\n✅ découpe appliquée.")
    print(f"↩️ Rollback git : git checkout -- {context_file} && git clean -fd {context_dir}")
    return 0


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roadmap-dir", type=Path, default=Path("doc/roadmap"))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", help="Default: report only, change nothing.")
    group.add_argument("--write", action="store_true", help="Apply the split.")
    group.add_argument("--self-check", action="store_true", help="Run built-in tests and exit.")
    return parser.parse_args()


def self_check() -> int:
    """Assert-based self-check on in-memory fixtures (no disk writes)."""
    assert slugify("Hydratation du contexte de session") == "hydratation-du-contexte-de-session"
    assert slugify("## RÈGLES ABSOLUES ##") == "regles-absolues"
    assert slugify("🩺 Réconciliation !!!") == "reconciliation"
    assert slugify("") == "section"

    assert is_core_heading("RÈGLES ABSOLUES")
    assert is_core_heading("Règles absolues de session")
    assert not is_core_heading("Hydratation du contexte")

    assert over_budget("x\n" * (MAX_LINES + 1))
    assert over_budget("a" * (MAX_BYTES + 1))
    assert not over_budget("ok\n")

    fixture = (
        "---\nkey: value\n---\n\n"
        "# CONTEXT\n\nIntro line.\n\n"
        "## RÈGLES ABSOLUES\n\nAlways hold.\n\n"
        "### sub-rule\n\nNested stays with its parent.\n\n"
        "## Hydratation du contexte\n\nSome notes.\n\n"
        "## Décisions en cours\n\nMore notes.\n"
    )
    core, moved = plan_split(fixture)
    assert "RÈGLES ABSOLUES" in core, "core lost the absolute rules"
    assert "### sub-rule" in core, "nested ### under a kept section must stay"
    assert "Hydratation" not in core and "Décisions" not in core, "surplus not removed from core"
    assert [slug for slug, _ in moved] == ["hydratation-du-contexte", "decisions-en-cours"]
    assert all("## " in block for _, block in moved), "moved block must keep its heading"

    # Idempotency: re-splitting the trimmed core moves nothing more.
    core_again, moved_again = plan_split(core)
    assert moved_again == [], "second pass must be a no-op"
    assert core_again == core

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
    return emit(args.roadmap_dir, write=args.write)


if __name__ == "__main__":
    raise SystemExit(main())
