#!/usr/bin/env python3
"""Generate the Codex fast-path PDF guide."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "agent-flow-codex-fast-path-guide.pdf"

INK = colors.HexColor("#1f2937")
MUTED = colors.HexColor("#6b7280")
LINE = colors.HexColor("#cbd5e1")
SURFACE = colors.HexColor("#f8fafc")
ACCENT = colors.HexColor("#2563eb")
GREEN = colors.HexColor("#16a34a")
AMBER = colors.HexColor("#d97706")


def styles():
    base = getSampleStyleSheet()
    base["Title"].fontName = "Helvetica-Bold"
    base["Title"].fontSize = 24
    base["Title"].leading = 29
    base["Title"].textColor = INK
    base["Heading1"].fontName = "Helvetica-Bold"
    base["Heading1"].fontSize = 15
    base["Heading1"].leading = 19
    base["Heading1"].spaceBefore = 10
    base["Heading1"].spaceAfter = 6
    base["Heading1"].textColor = INK
    base["Heading2"].fontName = "Helvetica-Bold"
    base["Heading2"].fontSize = 12
    base["Heading2"].leading = 15
    base["Heading2"].spaceBefore = 8
    base["Heading2"].spaceAfter = 4
    base["BodyText"].fontName = "Helvetica"
    base["BodyText"].fontSize = 9.5
    base["BodyText"].leading = 13
    base["BodyText"].textColor = INK
    base.add(
        ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontSize=8,
            leading=10,
            textColor=MUTED,
        )
    )
    base.add(
        ParagraphStyle(
            "CodeBlock",
            parent=base["BodyText"],
            fontName="Courier",
            fontSize=8,
            leading=10,
            backColor=colors.HexColor("#eef2ff"),
            borderColor=colors.HexColor("#dbeafe"),
            borderWidth=0.5,
            borderPadding=6,
        )
    )
    return base


def draw_box(drawing: Drawing, x: float, y: float, w: float, h: float, label: str, fill=SURFACE, stroke=LINE):
    drawing.add(Rect(x, y, w, h, rx=6, ry=6, fillColor=fill, strokeColor=stroke, strokeWidth=1))
    words = label.split()
    if len(label) > 24 and len(words) > 2:
        mid = len(words) // 2
        lines = [" ".join(words[:mid]), " ".join(words[mid:])]
    else:
        lines = [label]
    for i, line in enumerate(lines):
        drawing.add(
            String(
                x + w / 2,
                y + h / 2 + (len(lines) - 1) * 5 - i * 10 - 3,
                line,
                textAnchor="middle",
                fontName="Helvetica-Bold",
                fontSize=8,
                fillColor=INK,
            )
        )


def arrow(drawing: Drawing, x1: float, y1: float, x2: float, y2: float, color=ACCENT):
    drawing.add(Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=1.4))
    if abs(x2 - x1) >= abs(y2 - y1):
        direction = 1 if x2 >= x1 else -1
        points = [x2, y2, x2 - 7 * direction, y2 + 4, x2 - 7 * direction, y2 - 4]
    else:
        direction = 1 if y2 >= y1 else -1
        points = [x2, y2, x2 - 4, y2 - 7 * direction, x2 + 4, y2 - 7 * direction]
    drawing.add(Polygon(points, fillColor=color, strokeColor=color))


def daily_flow() -> Drawing:
    d = Drawing(500, 175)
    y = 110
    boxes = [
        (15, y, 84, 42, "Prompt"),
        (118, y, 92, 42, "Active session?"),
        (230, y, 96, 42, "Targeted context"),
        (346, y, 96, 42, "Scoped change"),
        (200, 32, 96, 42, "Focused validation"),
        (320, 32, 92, 42, "af-finish"),
    ]
    for b in boxes:
        fill = colors.HexColor("#eff6ff") if b[4] in {"Prompt", "af-finish"} else SURFACE
        draw_box(d, *b, fill=fill)
    arrow(d, 99, 131, 118, 131)
    arrow(d, 210, 131, 230, 131)
    arrow(d, 326, 131, 346, 131)
    arrow(d, 394, 110, 278, 74)
    arrow(d, 296, 53, 320, 53)
    arrow(d, 200, 53, 164, 110, color=GREEN)
    d.add(String(28, 80, "More related prompts loop back", fontSize=8, fillColor=MUTED))
    return d


def escalation_flow() -> Drawing:
    d = Drawing(500, 155)
    draw_box(d, 18, 82, 92, 42, "Routine work", fill=colors.HexColor("#ecfdf5"))
    draw_box(d, 138, 82, 102, 42, "Blocked twice?")
    draw_box(d, 268, 82, 102, 42, "Security scope?")
    draw_box(d, 398, 82, 86, 42, "Release gate?")
    draw_box(d, 78, 18, 102, 40, "Stay light", fill=colors.HexColor("#ecfdf5"), stroke=GREEN)
    draw_box(d, 220, 18, 102, 40, "Increase effort", fill=colors.HexColor("#fff7ed"), stroke=AMBER)
    draw_box(d, 360, 18, 102, 40, "review / deep", fill=colors.HexColor("#fff7ed"), stroke=AMBER)
    arrow(d, 110, 103, 138, 103)
    arrow(d, 240, 103, 268, 103)
    arrow(d, 370, 103, 398, 103)
    arrow(d, 189, 82, 260, 58, color=AMBER)
    arrow(d, 318, 82, 398, 58, color=AMBER)
    arrow(d, 441, 82, 411, 58, color=AMBER)
    arrow(d, 64, 82, 128, 58, color=GREEN)
    return d


def worktree_flow() -> Drawing:
    d = Drawing(500, 135)
    draw_box(d, 25, 70, 115, 44, "Parent branch development")
    draw_box(d, 190, 70, 115, 44, "Session worktree", fill=colors.HexColor("#eff6ff"), stroke=ACCENT)
    draw_box(d, 355, 70, 115, 44, "Ask before merge")
    draw_box(d, 190, 14, 115, 36, "Related prompts continue here", fill=colors.HexColor("#ecfdf5"), stroke=GREEN)
    arrow(d, 140, 92, 190, 92)
    arrow(d, 305, 92, 355, 92)
    arrow(d, 247, 70, 247, 50, color=GREEN)
    arrow(d, 247, 50, 247, 70, color=GREEN)
    return d


def table(data, widths):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
                ("TEXTCOLOR", (0, 0), (-1, 0), INK),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.75 * inch, 0.45 * inch, "Agent-Flow Codex Fast Path Guide")
    canvas.drawRightString(7.75 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
        title="Agent-Flow Codex Fast Path Guide",
        author="Agent-Flow",
    )
    story = []
    story.append(Paragraph("Agent-Flow Codex Fast Path Guide", s["Title"]))
    story.append(Paragraph("Use one persistent worktree, targeted context, focused validation, and deliberate escalation.", s["BodyText"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("The Short Version", s["Heading1"]))
    story.append(Paragraph("Agent-Flow should feel like one persistent Codex work session, not a ceremony after every prompt.", s["BodyText"]))
    story.append(Paragraph("start or continue one AF worktree -> keep working there -> wrap up when you ask", s["CodeBlock"]))
    story.append(Spacer(1, 8))
    story.append(daily_flow())
    story.append(Paragraph("Daily Commands", s["Heading1"]))
    story.append(
        table(
            [
                ["Moment", "Action"],
                ["Start or continue file-changing work", "af-flow"],
                ["Check current state", "af-status"],
                ["Ask for a quick checkpoint", "af-review"],
                ["Pick up, audit, or clean worktrees", "af-reconcile"],
                ["Commit and prepare to merge", "af-finish"],
            ],
            [2.6 * inch, 3.8 * inch],
        )
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph("Specialist skills are optional add-ons, not daily mandatory steps.", s["Small"]))
    story.append(PageBreak())

    story.append(Paragraph("Token-Efficient Model Policy", s["Heading1"]))
    story.append(Paragraph("Start with the cheapest setting that matches the risk. Escalate only when evidence demands it.", s["BodyText"]))
    story.append(
        table(
            [
                ["Work", "Codex setting"],
                ["Read-only help, status, command lookup", "fast profile or base medium"],
                ["Routine implementation", "base gpt-5.5 / medium / low verbosity"],
                ["Risky diff, hard debugging, release review", "review profile or high effort"],
                ["Security-sensitive or repeatedly failing work", "deep profile or xhigh effort"],
            ],
            [3.0 * inch, 3.4 * inch],
        )
    )
    story.append(Spacer(1, 10))
    story.append(Paragraph("Escalation Flow", s["Heading1"]))
    story.append(escalation_flow())
    story.append(Paragraph("Avoid In Routine Sessions", s["Heading1"]))
    story.append(
        Paragraph(
            "Avoid full repo scans, full reviews, security reviews, visual capture, audit campaigns, release checks, and subagent fan-out unless requested, risk-triggered, or needed after repeated failure.",
            s["BodyText"],
        )
    )
    story.append(PageBreak())

    story.append(Paragraph("Worktree Mental Model", s["Heading1"]))
    story.append(worktree_flow())
    story.append(Paragraph("The session worktree is the durable working context. Chat can be fluid; Git metadata, files, and the devlog stay grounded.", s["BodyText"]))
    story.append(Paragraph("Practical Prompts", s["Heading1"]))
    story.append(Paragraph("Start or continue work:", s["Heading2"]))
    story.append(
        Paragraph(
            "Use af-flow for this file-changing request. Keep related work in the same AF session worktree until I ask to finish, review, reconcile, merge, or switch direction.",
            s["CodeBlock"],
        )
    )
    story.append(Paragraph("Check status:", s["Heading2"]))
    story.append(Paragraph("Use af-status and tell me what AF sessions are active or ready.", s["CodeBlock"]))
    story.append(Paragraph("Wrap up:", s["Heading2"]))
    story.append(Paragraph("Use af-finish. Validate, update the devlog, commit the session, and report the merge command.", s["CodeBlock"]))
    story.append(Paragraph("Release:", s["Heading2"]))
    story.append(Paragraph("Use af-reconcile, then af-full-review, then af-release.", s["CodeBlock"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Rule of thumb: if the work is routine, stay light. If the work is risky, blocked, or release-facing, escalate deliberately.", s["Heading1"]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)


if __name__ == "__main__":
    build()
