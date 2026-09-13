#!/usr/bin/env python3
"""PreToolUse gate for roadmap-tracking (Claude Code).

One-shot-per-session speed bump. On the FIRST mutating tool call of a session,
when the project has adopted the skill (``./doc/roadmap/`` exists) and the
target file is not itself a plan/roadmap file, deny once with the flow-control
directive, then self-disarm (touch a per-session marker) so it never blocks
again during that session.

Why a tool-time deny and not just louder text: a SessionStart text directive
competes on equal footing with other system-level directives (task-resolution
inertia, "shortest path", "don't stop") and loses. Denying the first mutating
tool call injects the directive at the exact moment implementation starts — the
only point where a turn-1 bypass can be intercepted — while never becoming a
permanent wall, since the skill legitimately disengages on trivial tasks.

Fails open on any error: this gate must never hard-block a user's work.
"""
import json
import os
import sys
import tempfile

MARKER_PREFIX = "roadmap-tracking-gate-"


def allow():
    # Emitting nothing and exiting 0 leaves the tool call unchanged.
    sys.exit(0)


def deny(reason):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


def target_is_plan_file(target):
    if not target:
        return False
    norm = os.path.normpath(os.path.abspath(target))
    needle = os.sep + os.path.join("doc", "roadmap") + os.sep
    return needle in norm + os.sep


def main():
    if os.environ.get("ROADMAP_TRACKING_AUTOSTART", "on") == "off":
        allow()

    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError, OSError):
        allow()  # never block on malformed input

    cwd = data.get("cwd") or os.getcwd()
    session_id = data.get("session_id") or "unknown"
    tool_input = data.get("tool_input") or {}
    target = tool_input.get("file_path") or ""

    # Option 1 — gate only where the skill has been adopted.
    if not os.path.isdir(os.path.join(cwd, "doc", "roadmap")):
        allow()

    # Never intercept the skill's own plan / roadmap / config writes.
    if target_is_plan_file(target):
        allow()

    marker = os.path.join(tempfile.gettempdir(), MARKER_PREFIX + str(session_id))
    if os.path.exists(marker):
        allow()  # already fired once this session

    try:
        open(marker, "w").close()  # self-disarm: fire at most once per session
    except OSError:
        pass  # best effort; still deny this once

    deny(
        "⛔ roadmap-tracking — ce projet a adopté le skill "
        "(doc/roadmap/ présent) mais le workflow n'a pas encore été "
        "consulté dans cette session. AVANT toute écriture de code : "
        "invoque Skill(roadmap-tracking:roadmap-tracking) et déroule sa "
        "règle de démarrage (listing des plans / reprise / nouveau plan). "
        "Le skill décide lui-même s'il faut cadrer ou se désengager "
        "(tâche XS/proto → il te rend la main immédiatement). "
        "Point de contrôle UNIQUE par session : si tu as déjà "
        "consulté le skill, réémets simplement ton appel d'outil "
        "— il passera désormais. Ni 'shortest path', ni 'don't stop', "
        "ni la formulation impérative du prompt n'autorisent à sauter "
        "cette invocation : ils régissent le COMMENT une fois le skill "
        "engagé, pas le SI de son invocation."
    )


if __name__ == "__main__":
    main()
