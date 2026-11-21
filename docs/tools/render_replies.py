#!/usr/bin/env python3
"""Render README examples as SVG images styled like a Claude Code reply.

All data is synthetic. Run: python3 -I docs/tools/render_replies.py
Writes docs/assets/screens/<name>.svg. Character widths were measured in a
browser for system-ui (regular and 600) at 15px; Menlo is a flat 0.6 em.
"""
import json
import os

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "char_widths.json"), encoding="utf-8") as _f:
    WIDTHS = json.load(_f)  # measured at 15px, where SF uses its Text metrics
SAFE = 1.0  # scale on measured widths; raise above 1.0 to leave room for wider fonts

SANS = "system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "Menlo, ui-monospace, SFMono-Regular, Consolas, monospace"
BG, BORDER, TEXT, MUTED = "#faf9f5", "#e5e2d8", "#1f1e1b", "#73726c"
RULE, HEAD_BG, CODE_BG, BUBBLE, LINK = "#e5e2d8", "#f2f0e9", "#ecebe4", "#efede6", "#2f6fbd"

CANVAS_W, PAD_X = 880, 36
CONTENT_W = CANVAS_W - 2 * PAD_X


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def width(text, size, kind):
    if kind == "m":
        return len(text) * 0.6 * size
    table = WIDTHS[kind]
    return sum(table.get(c, 0.56) for c in text) * size * SAFE


def parse(markup):
    """Split **bold**, `code` and [link] spans into (kind, text) pieces."""
    out, i = [], 0
    while i < len(markup):
        if markup.startswith("**", i):
            j = markup.index("**", i + 2)
            out.append(("b", markup[i + 2:j])); i = j + 2
        elif markup[i] == "`":
            j = markup.index("`", i + 1)
            out.append(("m", markup[i + 1:j])); i = j + 1
        elif markup[i] == "[":
            j = markup.index("]", i + 1)
            out.append(("a", markup[i + 1:j])); i = j + 1
        else:
            j = i
            while j < len(markup) and not markup.startswith("**", j) and markup[j] not in "`[":
                j += 1
            out.append(("r", markup[i:j])); i = j
    return out


def inline(markup, x, y, size=15, base="r", color=TEXT):
    """Draw one line of inline markup with its baseline at y. Returns (svg, width).

    Plain, bold and link text in a row share one <text> element, so the browser
    spaces it with its own font metrics. Only a `code` pill needs an estimated x,
    so keep the text in front of a pill short.
    """
    parts, run = [], []
    cx = x

    def flush():
        nonlocal cx
        if not run:
            return
        spans, total = [], 0.0
        for kind, text in run:
            k = "b" if (kind == "b" or base == "b") else "r"
            attrs = ' font-weight="600"' if k == "b" else ""
            if kind == "a":
                attrs += f' fill="{LINK}" text-decoration="underline"'
            spans.append(f"<tspan{attrs}>{esc(text)}</tspan>")
            total += width(text, size, k)
        parts.append(f'<text x="{cx:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}">{"".join(spans)}</text>')
        cx += total
        run.clear()

    for kind, text in parse(markup):
        if kind == "m":
            flush()
            cx += 1
            w = width(text, size - 1.5, "m") + 8
            parts.append(f'<rect x="{cx:.1f}" y="{y - size * 0.86:.1f}" width="{w:.1f}" height="{size * 1.2:.1f}" rx="4" fill="{CODE_BG}"/>')
            parts.append(f'<text x="{cx + 4:.1f}" y="{y - 0.5:.1f}" font-family="{MONO}" font-size="{size - 1.5}" fill="{TEXT}">{esc(text)}</text>')
            cx += w + 2
        else:
            run.append((kind, text))
    flush()
    return "".join(parts), cx - x


def inline_width(markup, size=15, base="r"):
    return inline(markup, 0, 0, size, base)[1]


# Diagrams, drawn in a 680-wide frame like an inline widget.
GRAY = ("#f1efe8", "#b4b2a9", "#444441", "#5f5e5a")
AMBER = ("#faeeda", "#ba7517", "#633806", "#854f0b")
ARROW = "#888780"


def box(x, y, w, h, colors, title, *subs):
    fill, stroke, tc, sc = colors
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="0.75"/>']
    lines = [(title, 14, "600", tc)] + [(t, 12, "400", sc) for t in subs]
    gap = 18
    top = y + h / 2 - gap * (len(lines) - 1) / 2
    for n, (t, size, wt, c) in enumerate(lines):
        assert width(t, size, "b" if wt == "600" else "r") <= w - 10, ("box text too wide", t)
        s.append(f'<text x="{x + w / 2}" y="{top + n * gap:.1f}" text-anchor="middle" dominant-baseline="central" font-size="{size}" font-weight="{wt}" fill="{c}">{esc(t)}</text>')
    return "".join(s)


def arrow_path(d, dashed=False):
    dash = ' stroke-dasharray="4 3"' if dashed else ""
    return f'<path d="{d}" fill="none" stroke="{ARROW}" stroke-width="1.25"{dash} marker-end="url(#ah)"/>'


def diagram_architecture():
    s = [
        box(15, 30, 200, 72, AMBER, "Local clone", "~/code/assistant", "⚠ 58 behind · 3 uncommitted"),
        box(15, 120, 200, 72, AMBER, "13 worktrees", "wt/", "⚠ 12 merged · 1 unpushed"),
        box(240, 75, 200, 72, GRAY, "GitHub · main", "contoso/assistant · a1c4e02", "the reference"),
        box(465, 30, 200, 72, AMBER, "Cloud Run", "assistant-web · image 7d91b3f", "⚠ 12 commits behind main"),
        box(465, 120, 200, 72, GRAY, "Client GitLab", "the client's own repo", "— can't check, needs VPN"),
        arrow_path("M238 111 H227 V66 H219"), arrow_path("M227 111 V156 H219"),
        arrow_path("M442 111 H452 V66 H461"), arrow_path("M452 111 V156 H461", dashed=True),
    ]
    return "".join(s), 222


def diagram_visual():
    s = []
    for row, (label, y, items) in enumerate([
        ("Today", 24, [("Export job",), ("Changing IP", "new one each run"), ("Partner firewall",), ("Blocked",)]),
        ("Proposed", 104, [("Export job",), ("NAT gateway", "one static IP"), ("Partner firewall",), ("Delivered",)]),
    ]):
        s.append(f'<text x="12" y="{y + 30}" dominant-baseline="central" font-size="13" font-weight="600" fill="{MUTED}">{label}</text>')
        for n, item in enumerate(items):
            x = 92 + n * 146
            colors = AMBER if (row == 0 and n == 3) else GRAY
            s.append(box(x, y, 124, 60, colors, *item))
            if n < 3:
                s.append(arrow_path(f"M{x + 126} {y + 30} H{x + 142}"))
    return "".join(s), 188


def line_path(d):
    return f'<path d="{d}" fill="none" stroke="{ARROW}" stroke-width="1.25"/>'


def note(x, y, text, anchor="start"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" dominant-baseline="central" font-size="12" fill="{MUTED}">{esc(text)}</text>'


def diagram_session():
    """The five parts of a session, and the vault they read from and write to."""
    s = []
    steps = [("1 · Start", "one status message"), ("2 · Work", "agents in worktrees"),
             ("3 · Ship", "PRs with diagrams"), ("5 · Close", "notes written back")]
    for n, (title, sub_) in enumerate(steps):
        x = 14 + n * 168
        s.append(box(x, 20, 148, 64, GRAY, title, sub_))
        if n < 3:
            s.append(arrow_path(f"M{x + 151} 52 H{x + 164}"))
    s.append(box(182, 114, 316, 50, GRAY, "4 · Story page", "progress as it happens, ready to share"))
    s.append(arrow_path("M256 87 V110", dashed=True))
    s.append(arrow_path("M424 87 V110", dashed=True))
    s.append(box(14, 196, 652, 52, GRAY, "Private vault", "facts, timeline and meeting notes for every project"))
    s.append(arrow_path("M88 193 V88"))
    s.append(note(98, 140, "reads"))
    s.append(arrow_path("M592 87 V192"))
    s.append(note(582, 140, "writes back", anchor="end"))
    return "".join(s), 262


def diagram_team():
    """The orchestrator and the agents it briefs."""
    s = [box(14, 16, 652, 56, GRAY, "Orchestrator · Opus", "plans, briefs, reviews and tracks · writes no product code")]
    agents = [("Scout", "maps the code"), ("Platform", "cloud, deploys"), ("Feature", "one per feature"),
              ("Integrator", "merges, tests"), ("Reviewer", "before deploys"), ("QA", "red team, UX")]
    s.append(line_path("M340 72 V86"))
    s.append(line_path("M64 86 H616"))
    for n, (title, sub_) in enumerate(agents):
        x = 14 + n * 110.4
        s.append(box(round(x, 1), 102, 100, 58, GRAY, title, sub_))
        s.append(arrow_path(f"M{x + 50:.1f} 86 V98"))
    s.append(box(14, 182, 652, 50, GRAY, "Story", "turns the run log and git history into the story page"))
    return "".join(s), 246


DIAGRAMS = {"architecture": diagram_architecture, "visual": diagram_visual,
            "session": diagram_session, "team": diagram_team}


def render(blocks):
    out, y = [], 28
    for b in blocks:
        kind = b[0]
        if kind == "user":
            w = width(b[1], 15, "r") + 32
            x = CANVAS_W - PAD_X - w
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="40" rx="14" fill="{BUBBLE}"/>')
            out.append(f'<text x="{x + 16:.1f}" y="{y + 25}" font-size="15" fill="{TEXT}">{esc(b[1])}</text>')
            y += 62
        elif kind == "tool":
            out.append(f'<text x="{PAD_X}" y="{y + 14}" font-size="14" fill="{MUTED}">{esc(b[1])}  ›</text>')
            y += 34
        elif kind == "p":
            svg, w = inline(b[1], PAD_X, y + 17)
            assert w <= CONTENT_W, ("line too long", b[1], w)
            out.append(svg); y += 30
        elif kind == "h":
            y += 6
            svg, w = inline(b[1], PAD_X, y + 18, size=16.5, base="b")
            out.append(svg); y += 34
        elif kind == "hr":
            out.append(f'<line x1="{PAD_X}" y1="{y + 10}" x2="{CANVAS_W - PAD_X}" y2="{y + 10}" stroke="{RULE}"/>')
            y += 22
        elif kind == "bullets":
            for item in b[1]:
                out.append(f'<text x="{PAD_X + 6}" y="{y + 17}" font-size="15" fill="{TEXT}">•</text>')
                svg, w = inline(item, PAD_X + 22, y + 17)
                out.append(svg); y += 28
            y += 4
        elif kind == "table":
            header, rows = b[1], b[2]
            ncol = len(header)
            cols = [0.0] * ncol
            for r in [header] + rows:
                for c, cell in enumerate(r):
                    cols[c] = max(cols[c], inline_width(cell, 14, "b" if r is header else "r") + 26)
            tw = sum(cols)
            assert tw <= CONTENT_W, ("table too wide", header, tw)
            rh = 36
            th = rh * (len(rows) + 1)
            out.append(f'<rect x="{PAD_X}" y="{y}" width="{tw:.1f}" height="{th}" rx="8" fill="#ffffff" stroke="{RULE}"/>')
            out.append(f'<path d="M{PAD_X + 0.5} {y + rh} V{y + 8} Q{PAD_X + 0.5} {y + 0.5} {PAD_X + 8} {y + 0.5} H{PAD_X + tw - 8} Q{PAD_X + tw - 0.5} {y + 0.5} {PAD_X + tw - 0.5} {y + 8} V{y + rh} Z" fill="{HEAD_BG}"/>')
            for n, r in enumerate([header] + rows):
                ry = y + n * rh
                if n:
                    out.append(f'<line x1="{PAD_X}" y1="{ry}" x2="{PAD_X + tw:.1f}" y2="{ry}" stroke="{RULE}"/>')
                cx = PAD_X + 13
                for c, cell in enumerate(r):
                    svg, _ = inline(cell, cx, ry + 23, size=14, base="b" if n == 0 else "r")
                    out.append(svg); cx += cols[c]
            y += th + 18
        elif kind == "code":
            lines = b[2].split("\n")
            h = 34 + 20 * len(lines)
            out.append(f'<rect x="{PAD_X}" y="{y}" width="{CONTENT_W}" height="{h}" rx="8" fill="{HEAD_BG}" stroke="{RULE}"/>')
            out.append(f'<text x="{PAD_X + 14}" y="{y + 20}" font-size="12" fill="{MUTED}">{esc(b[1])}</text>')
            out.append(f'<text x="{CANVAS_W - PAD_X - 14}" y="{y + 20}" text-anchor="end" font-size="12" fill="{MUTED}">Run</text>')
            for n, line in enumerate(lines):
                out.append(f'<text x="{PAD_X + 14}" y="{y + 44 + 20 * n}" font-family="{MONO}" font-size="13.5" fill="{TEXT}">{esc(line)}</text>')
            y += h + 16
        elif kind == "diagram":
            inner, h = DIAGRAMS[b[1]]()
            scale = (CONTENT_W - 24) / 680
            dh = h * scale
            out.append(f'<rect x="{PAD_X}" y="{y}" width="{CONTENT_W}" height="{dh + 24:.1f}" rx="10" fill="#ffffff" stroke="{RULE}"/>')
            out.append(f'<svg x="{PAD_X + 12}" y="{y + 12}" width="{CONTENT_W - 24}" height="{dh:.1f}" viewBox="0 0 680 {h}" font-family="{SANS}">{inner}</svg>')
            y += dh + 24 + 18
        elif kind == "next":
            text, buttons = b[1], b[2]
            h = 92
            out.append(f'<rect x="{PAD_X}" y="{y}" width="{CONTENT_W}" height="{h}" rx="12" fill="#ffffff" stroke="{RULE}"/>')
            out.append(f'<text x="{PAD_X + 18}" y="{y + 30}" font-size="14" fill="{MUTED}">{esc(text)}</text>')
            bx = PAD_X + 18
            for n, label in enumerate(buttons):
                bw = width(label, 14, "b") + 28
                fill, fc = ("#1f1e1b", "#ffffff") if n == 0 else ("#ffffff", TEXT)
                out.append(f'<rect x="{bx:.1f}" y="{y + 46}" width="{bw:.1f}" height="32" rx="8" fill="{fill}" stroke="#1f1e1b" stroke-width="{0 if n == 0 else 0.75}"/>')
                out.append(f'<text x="{bx + 14:.1f}" y="{y + 67}" font-size="14" font-weight="600" fill="{fc}">{esc(label)}</text>')
                bx += bw + 10
            y += h + 10
        else:
            raise ValueError(kind)
    total = y + 18
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{total:.0f}" viewBox="0 0 {CANVAS_W} {total:.0f}" '
            f'role="img" font-family="{SANS}" xml:space="preserve">')
    defs = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M2 1L8 5L2 9" fill="none" stroke="{ARROW}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    frame = f'<rect x="0.5" y="0.5" width="{CANVAS_W - 1}" height="{total - 1:.0f}" rx="14" fill="{BG}" stroke="{BORDER}"/>'
    return head, defs + frame + "".join(out) + "</svg>"


def card(title, desc, blocks):
    head, body = render(blocks)
    return f"{head}<title>{esc(title)}</title><desc>{esc(desc)}</desc>{body}"


# The examples show the sample vault in skills/fde/sample-vault. These rows must
# match contoso-retail/project.md there; docs/tools/check_repo.py checks it.
PROGRESS_ROWS = [
    ["SOW", "`████████░░`", "80%", "With legal since 3/5"],
    ["Scope", "`█████░░░░░`", "50%", "Returns added 3/3"],
    ["Access", "`██░░░░░░░░`", "20%", "VPN pending"],
    ["First build", "`█░░░░░░░░░`", "10%", "Chat skeleton live 3/4"],
]

EXAMPLES = {
    "fde": ("Example /fde reply", "A synthetic status message for a project called Contoso Retail.", [
        ("user", "/fde"),
        ("tool", "Ran 9 commands, read 6 files"),
        ("p", "▶ Chase client VPN access before Monday's kickoff"),
        ("p", "**Contoso Retail** · support assistant · pre-start · kickoff Mon 3/9"),
        ("hr",),
        ("h", "1 · Status"),
        ("table", ["Item", "State"], [["Code", "✓ `main` @ `a1c4e02`"], ["Deploy", "⚠ `7d91b3f` live on assistant-web, 12 behind"], ["Access", "✓ GitHub · ✓ GCP · ⚠ client VPN"]]),
        ("hr",),
        ("h", "2 · What changed since 3/2 · [timeline]"),
        ("table", ["Date", "Source", "What changed"], [
            ["3/3", "[Scope call]", "Returns into phase 1 · loyalty cut"],
            ["3/5", "[Email from the client PM]", "Pilot date fixed: 4/14"],
            ["3/6", "[Teams, core chat]", "VPN request filed · loyalty back in, reverses 3/3"]]),
        ("hr",),
        ("h", "3 · Progress (estimate)"),
        ("table", ["Workstream", "", "", "Why"], [
            ["SOW", "`████████░░`", "80% ↑", "With legal since 3/5"],
            ["Scope", "`█████░░░░░`", "50% ↑", "Returns added 3/3"],
            ["Access", "`██░░░░░░░░`", "20% =", "VPN pending"],
            ["First build", "`█░░░░░░░░░`", "10% ↑", "Chat skeleton live 3/4"]]),
        ("hr",),
        ("h", "4 · Yours"),
        ("bullets", ["Chase VPN with the client PM ([why])", "Approve the returns design ([why])"]),
        ("next", "Contoso is pre-start, and client VPN access is the blocker. 3 questions waiting.", ["Next question"]),
    ]),
    "initialize": ("Example /fde initialize reply", "A synthetic readiness checklist: 6 of 10 checks pass.", [
        ("user", "/fde initialize"),
        ("tool", "Ran 11 commands, read 4 files"),
        ("p", "**Contoso Retail** · initialize · 6 of 10 ready"),
        ("table", ["", "Check", "Result", "Fix"], [
            ["✓", "Vault", "private, current", ""],
            ["✓", "Project folder", "facts card and timeline", ""],
            ["✓", "GitHub", "contoso/assistant, write access", ""],
            ["⚠", "Local code", "~/code/assistant 58 behind, 3 uncommitted", "question 1"],
            ["✗", "Cloud", "gcloud sign-in expired", "run the login below"],
            ["—", "Live version", "can't check until signed in", ""],
            ["✓", "Keys and services", "2 of 2 recorded, secrets exist", ""],
            ["⚠", "Meetings", "3/3 scope call has no transcript", "question 2"],
            ["✓", "Teams and email", "screenshots, as recorded", ""],
            ["✓", "Latest context", "newest entry 3/6", ""]]),
        ("p", "Sign in first, then I'll take the rest one question at a time:"),
        ("code", "bash", "gcloud auth login"),
        ("next", "6 of 10 checks pass. Sign in to gcloud; 2 questions waiting.", ["Next question"]),
    ]),
    "architecture": ("Example /fde architecture reply", "A synthetic map of where the code lives and runs, and how current each copy is.", [
        ("user", "/fde architecture"),
        ("tool", "Ran 6 commands"),
        ("p", "**Live runs an image 12 commits behind main, and the local main is 58 behind.**"),
        ("diagram", "architecture"),
        ("table", ["Where", "What", "Version", ""], [
            ["GitHub", "`main` on contoso/assistant", "`a1c4e02` · 3/6", "latest"],
            ["Local", "~/code/assistant", "`e58a0c4`", "⚠ 58 behind · 3 uncommitted"],
            ["Local", "13 worktrees in wt/", "", "⚠ 12 merged, can be pruned"],
            ["Local", "`build/qa-agent` in wt/qa-agent", "1 commit, 3/5", "⚠ not merged, not pushed"],
            ["GCP", "Cloud Run assistant-web · 00012", "image `7d91b3f`", "⚠ 12 commits behind main"],
            ["Client", "GitLab", "", "— can't check, needs VPN"]]),
        ("p", "`qa-agent` holds the only copy of its commit: push or merge it before you prune the other 12."),
    ]),
    "progress": ("Example /fde progress reply", "Synthetic progress bars, one per workstream.", [
        ("user", "/fde progress"),
        ("tool", "Read project.md"),
        ("p", "**Contoso Retail** · progress (estimate, as of 3/6)"),
        ("table", ["Workstream", "", "", "Why"], PROGRESS_ROWS),
    ]),
    "timeline": ("Example /fde timeline reply", "A synthetic timeline, one row per day.", [
        ("user", "/fde timeline"),
        ("tool", "Read timeline.md"),
        ("table", ["Date", "Source", "What changed"], [
            ["3/2", "[Internal kickoff]", "Two FDEs, six-week pilot"],
            ["3/3", "[Scope call] · ⚠ no transcript", "Returns into phase 1 · loyalty cut"],
            ["3/5", "[Email from the client PM]", "Pilot date fixed: 4/14"],
            ["3/6", "[Teams, core chat]", "VPN request filed · loyalty back in, reverses 3/3"]]),
    ]),
    "context": ("Example /fde context reply", "A synthetic facts card for one project.", [
        ("user", "/fde context"),
        ("tool", "Read 2 files"),
        ("p", "**Contoso Retail** · pre-start · facts as of 3/6"),
        ("table", ["Fact", "Recorded"], [
            ["Code", "`main` @ `a1c4e02` · contoso/assistant · merges: lead FDE"],
            ["Deploy", "GCP · contoso-assistant-dev · 00012 · [app]"],
            ["Access", "✓ GitHub · ✓ GCP · ⚠ client VPN"],
            ["Models and keys", "Gemini on Vertex, runtime service account"],
            ["People", "Dana (lead FDE) · Sam (client PM)"],
            ["Data rules", "No client data outside the client's cloud"]]),
        ("p", "Latest: [Teams, core chat] · 3/6"),
    ]),
    "project": ("Example /fde project reply", "A synthetic list of projects in a vault.", [
        ("user", "/fde project"),
        ("tool", "Ran 2 commands"),
        ("p", "**Projects in the vault** · 2 of 3 set up"),
        ("table", ["Project", "Stage", "Last entry", ""], [
            ["[contoso-retail]", "support assistant · pre-start", "3/6", "✓"],
            ["[fabrikam-pilot]", "inventory agent · build week 3", "2/27", "✓"],
            ["[northwind-proposal]", "search revamp · proposal", "2/10", "— no facts card"]]),
    ]),
    "visual": ("Example /fde visual reply", "A synthetic reply redrawn as one diagram: today the export is blocked, proposed it is delivered.", [
        ("user", "/fde visual"),
        ("diagram", "visual"),
    ]),
    "recap": ("Example /fde recap reply", "A synthetic reply cut to a verdict, a table, a diagram and a proposal.", [
        ("user", "/fde recap"),
        ("p", "**Exports fail because the partner only accepts one fixed IP.**"),
        ("table", ["Date", "Ran from", "Result"], [
            ["3/2", "Cron on the old VM", "✗ 9 of 12 runs timed out"],
            ["3/4", "Cloud Run job", "✗ ran, then blocked by the partner's allowlist"],
            ["3/6 to 3/8", "Partner ticket PT-1042", "confirmed: one static IP only"]]),
        ("p", "The weekly export is set up the same way and will hit the same wall."),
        ("diagram", "visual"),
        ("p", "**Proposal:** route both jobs through a NAT gateway with one static IP, and send it to the partner."),
    ]),
}


FIGURES = {
    "how-it-works": ("How a session runs", "Start, work, ship and close in a row, the story page under work and ship, and the private vault under all of it.", [
        ("diagram", "session"),
    ]),
    "agent-team": ("The agent team", "An Opus orchestrator above six agents (scout, platform, feature, integrator, reviewer, QA), with the story agent below.", [
        ("diagram", "team"),
    ]),
}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.join(here, "..", "assets", "screens")
    os.makedirs(out_dir, exist_ok=True)
    for name, (title, desc, blocks) in EXAMPLES.items():
        path = os.path.join(out_dir, f"fde-{name}.svg" if name != "fde" else "fde.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(card(title, desc, blocks))
        print("wrote", os.path.relpath(path, os.path.join(here, "..", "..")))
    for name, (title, desc, blocks) in FIGURES.items():
        path = os.path.join(here, "..", "assets", f"{name}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(card(title, desc, blocks))
        print("wrote", os.path.relpath(path, os.path.join(here, "..", "..")))


if __name__ == "__main__":
    main()
