#!/usr/bin/env python3
"""Generate the Agent-Flow product walkthrough as a landscape PDF presentation."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "presentations" / "agent-flow-walkthrough.pdf"
PAGE = landscape((540, 960))
W, H = PAGE

INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#5E6975")
LINE = colors.HexColor("#D9DEE5")
PANEL = colors.HexColor("#FFFFFF")
BG = colors.HexColor("#F6F8FA")
TEAL = colors.HexColor("#1C9BB0")
GREEN = colors.HexColor("#2E9D68")
VIOLET = colors.HexColor("#6556D9")
AMBER = colors.HexColor("#B6791E")


def wrap(text: str, font: str, size: int, max_width: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        line = ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if stringWidth(candidate, font, size) <= max_width:
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def draw_text(c: canvas.Canvas, text: str, x: float, y: float, width: float, size: int = 14,
              font: str = "Helvetica", fill=INK, leading: float | None = None) -> float:
    c.setFillColor(fill)
    c.setFont(font, size)
    lead = leading or size * 1.35
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= lead
    return y


def header(c: canvas.Canvas) -> None:
    c.setFillColor(BG)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColor(INK)
    c.roundRect(38, H - 58, 22, 22, 5, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(43, H - 44, "AF")
    c.setFillColor(MUTED)
    c.setFont("Helvetica-Bold", 6)
    c.drawString(66, H - 43, "AGENT-FLOW")
    c.setStrokeColor(colors.HexColor("#E5E9EF"))
    c.line(38, 38, W - 38, 38)


def title(c: canvas.Canvas, text: str, y: float = 430, width: float = 520) -> float:
    return draw_text(c, text, 38, y, width, size=24, font="Helvetica-Bold", leading=29)


def subtitle(c: canvas.Canvas, text: str, y: float, width: float = 520) -> float:
    return draw_text(c, text, 38, y, width, size=10, fill=MUTED, leading=15)


def pill(c: canvas.Canvas, x: float, y: float, label: str, accent) -> None:
    c.setFillColor(PANEL)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, 96, 18, 8, stroke=1, fill=1)
    c.setFillColor(accent)
    c.circle(x + 13, y + 9, 3, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(x + 22, y + 6, label)


def card(c: canvas.Canvas, x: float, y: float, w: float, h: float, heading: str,
         body: str, accent=TEAL) -> None:
    c.setFillColor(PANEL)
    c.setStrokeColor(LINE)
    c.roundRect(x, y, w, h, 5, stroke=1, fill=1)
    c.setFillColor(accent)
    c.rect(x, y, 3, h, stroke=0, fill=1)
    draw_text(c, heading, x + 14, y + h - 22, w - 24, size=8, font="Helvetica-Bold", leading=10)
    draw_text(c, body, x + 14, y + h - 39, w - 24, size=6, fill=MUTED, leading=8)


def command_box(c: canvas.Canvas, x: float, y: float, w: float, text: str) -> None:
    c.setFillColor(colors.HexColor("#EFF3F6"))
    c.setStrokeColor(colors.HexColor("#DDE4EA"))
    c.roundRect(x, y, w, 20, 3, stroke=1, fill=1)
    c.setFillColor(MUTED)
    c.setFont("Courier", 7)
    c.drawCentredString(x + w / 2, y + 7, text)


def numbered(c: canvas.Canvas, x: float, y: float, n: int, heading: str, body: str, accent) -> None:
    c.setFillColor(accent)
    c.circle(x, y + 4, 9, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(x, y + 1, str(n))
    draw_text(c, heading, x + 20, y + 10, 190, size=9, font="Helvetica-Bold", leading=11)
    draw_text(c, body, x + 20, y - 8, 190, size=6, fill=MUTED, leading=8)


def slide_1(c: canvas.Canvas) -> None:
    header(c)
    c.setFillColor(INK)
    c.roundRect(40, 330, 52, 52, 11, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(52, 346, "AF")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(112, 364, "Agent-Flow")
    c.setFont("Helvetica", 10)
    c.setFillColor(MUTED)
    c.drawString(112, 346, "Structured workflow rules for AI coding agents.")
    subtitle(c, "A practical walkthrough for turning AI coding chats into reviewable development sessions.", 292, 560)
    pill(c, 40, 246, "worktrees", TEAL)
    pill(c, 150, 246, "devlogs", GREEN)
    pill(c, 260, 246, "reviews", VIOLET)
    pill(c, 370, 246, "guarded merge", AMBER)
    c.setFont("Helvetica", 6)
    c.setFillColor(MUTED)
    c.drawString(40, 86, "Structured workflow rules for AI coding agents")


def slide_2(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Agent work gets hard to trust when the workflow only exists in chat.", width=500)
    subtitle(c, "Agent-Flow exists because capable agents still need local operating rules around Git, docs, review, and release.", 345, 440)
    y = 292
    for heading, body, accent in [
        ("Branch drift", "A session can edit the wrong branch or collide with parallel work.", AMBER),
        ("Weak handoff", "A finished chat may leave no durable record of decisions or validation.", VIOLET),
        ("Hidden release risk", "Open child worktrees can be bypassed when a parent branch is pushed.", TEAL),
        ("Docs lag behind code", "Behavior changes faster than maintainers can reconstruct it.", GREEN),
    ]:
        card(c, 555, y, 250, 42, heading, body, accent)
        y -= 55


def slide_3(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Agent-Flow is a local workflow kit, not another task database.")
    subtitle(c, "It installs shared rules, adapters, skills, scripts, and templates that make agent-assisted work repeatable across repos.", 344, 560)
    x = 58
    for heading, body, accent in [
        ("Codex instructions", "AGENT-FLOW.md is canonical. AGENTS.md points Codex to the same repo rules.", TEAL),
        ("Session scripts", "Start, finish, reconcile, status, and release helpers manage worktrees with repo-local helpers.", GREEN),
        ("Durable history", "Every file-changing session leaves a devlog entry, decisions, and validation.", VIOLET),
        ("Release discipline", "Review gates and push-readiness checks protect parent branches.", AMBER),
    ]:
        card(c, x, 194, 190, 92, heading, body, accent)
        x += 208


def slide_4(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Install once, then Codex gets the same operating model in every repo.", width=560)
    subtitle(c, "Agent-Flow copies the shared setup into home-directory surfaces that Codex and repo init can reuse.", 344, 520)
    command_box(c, 58, 260, 220, "./scripts/install.sh")
    c.setStrokeColor(TEAL)
    c.line(300, 270, 360, 270)
    for i, (path, body) in enumerate([
        ("~/.agent-flow", "Shared rules, skills, scripts, docs, and templates."),
        ("~/.codex", "Codex adapter, AF skills, profiles, and AGENTS.md."),
        ("Claude CLI", "Optional external review through af-claude-review only."),
    ]):
        card(c, 380, 305 - i * 72, 230, 58, path, body, [TEAL, GREEN, VIOLET][i])


def slide_5(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Every repo makes one choice: use Agent-Flow or opt out.", width=540)
    subtitle(c, "When a repo has no AF setup, file-changing work waits until init runs or the repo is marked disabled.", 345, 540)
    numbered(c, 58, 278, 1, "Run init in the repo", "agent-flow/scripts/init-repo.sh creates config, adapters, docs, devlog, and helper scripts.", TEAL)
    numbered(c, 58, 214, 2, "Choose branch rules", "Pick integration branch, production target, optional staging, and push-readiness hook.", GREEN)
    numbered(c, 470, 278, 3, "Opt out when needed", "af-disable writes a local disabled config; af-enable reverses it or runs init.", AMBER)
    command_box(c, 470, 205, 210, "af-disable | af-enable")


def slide_6(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Daily work stays fluid because the worktree is the durable session.", width=580)
    subtitle(c, "A Codex flow can continue across prompts while Git metadata, files, and the devlog keep the session grounded.", 342, 590)
    steps = [("af-flow", TEAL), ("implement", GREEN), ("validate", VIOLET), ("devlog", AMBER), ("af-finish", INK)]
    x = 90
    for label, accent in steps:
        c.setFillColor(PANEL)
        c.setStrokeColor(accent)
        c.roundRect(x, 236, 96, 32, 4, stroke=1, fill=1)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + 48, 249, label)
        if label != "af-finish":
            c.setStrokeColor(LINE)
            c.line(x + 96, 252, x + 126, 252)
        x += 126
    draw_text(c, "Do not finish after every prompt. Finish when you want to wrap, review, reconcile, merge, or switch direction.", 210, 190, 540, size=8, fill=MUTED)


def slide_7(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Finish turns an open session into a merge-ready unit.", width=560)
    subtitle(c, "af-finish validates the work, checks docs and devlog, commits the session, and asks before merging.", 342, 590)
    x = 58
    for heading, body, accent in [
        ("Validation", "Run the tests, builds, checks, or manual proof that fit the change.", TEAL),
        ("Devlog", "Record what changed, why, validation, proof, and risks.", GREEN),
        ("Commit", "Create a session commit from the isolated worktree.", VIOLET),
        ("Ask", "Merge only after explicit approval.", AMBER),
    ]:
        card(c, x, 220, 190, 82, heading, body, accent)
        x += 208
    command_box(c, 300, 150, 270, "scripts/finish-session.sh --merge")


def slide_8(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Release work uses a separate gate.", width=520)
    subtitle(c, "The daily loop stays light; release adds reconciliation, full review, optional security review, and PR preparation.", 346, 560)
    numbered(c, 80, 276, 1, "Reconcile open work", "af-reconcile finds dirty, merged, unmanaged, and cleanup-ready worktrees.", TEAL)
    numbered(c, 80, 204, 2, "Review the release diff", "af-full-review runs the broad gate once, before protected branches.", VIOLET)
    numbered(c, 500, 276, 3, "Prepare the release path", "af-release moves development through staging and main when configured.", GREEN)
    numbered(c, 500, 204, 4, "Escalate security when needed", "af-security-review is used for sensitive or configured release scopes.", AMBER)


def slide_9(c: canvas.Canvas) -> None:
    header(c)
    title(c, "Most days only need five concepts.", width=520)
    subtitle(c, "Specialist skills stay available for package, docs, audit, UI, and release work.", 345, 540)
    x = 54
    for label, accent in [("af-flow", TEAL), ("af-status", GREEN), ("af-review", VIOLET), ("af-reconcile", AMBER), ("af-finish", INK)]:
        pill(c, x, 282, label, accent)
        x += 146
    card(c, 92, 178, 180, 64, "Repo setup", "af-enable, af-disable, af-pnpm", TEAL)
    card(c, 350, 178, 180, 64, "Documentation", "af-docs, af-devlog, af-show", GREEN)
    card(c, 608, 178, 180, 64, "Campaigns", "af-feature-audit, af-ui-audit, af-release", VIOLET)


def slide_10(c: canvas.Canvas) -> None:
    header(c)
    title(c, "The payoff is trust you can inspect later.", width=520)
    subtitle(c, "Agent-Flow makes agent-assisted work safer to continue, review, merge, and explain because every session leaves a repo-local trail.", 330, 560)
    command_box(c, 58, 248, 280, "Use agent-flow/scripts/init-repo.sh")
    command_box(c, 58, 215, 280, "Use af-flow for this file-changing request.")
    command_box(c, 58, 182, 280, "Use af-finish when I am ready to wrap up.")
    draw_text(c, "One related working session. One isolated worktree. One devlog. Explicit review before merge.", 420, 250, 320, size=14, font="Helvetica-Bold", leading=18)


SLIDES = [slide_1, slide_2, slide_3, slide_4, slide_5, slide_6, slide_7, slide_8, slide_9, slide_10]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=PAGE)
    c.setTitle("Agent-Flow Walkthrough")
    c.setAuthor("Agent-Flow")
    for draw in SLIDES:
        draw(c)
        c.showPage()
    c.save()
    print(OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
