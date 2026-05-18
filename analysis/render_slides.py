#!/usr/bin/env python3
"""
render_slides.py — Generate 22 publication-quality PNG slides (1920x1080)
for the Troy School District G6-G7 Math Analysis deck.

Visual style matches the Troy SD K-5 ELA Executive Summary presentation.
"""

import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image
import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTS_DIR = os.path.join(ROOT, "charts")
SLIDES_DIR = os.path.join(ROOT, "slides")
os.makedirs(SLIDES_DIR, exist_ok=True)

# ── Color Palette ────────────────────────────────────────────────────────────
TROY_BLUE      = "#1F3A5F"
ACCENT_RED     = "#C8302F"
ACCENT_GREEN   = "#1F7A3D"
ACCENT_ORANGE  = "#B7791F"
LIGHT_GREEN    = "#E8F5EE"
LIGHT_ORANGE   = "#FFF4E0"
LIGHT_RED      = "#FBE7E6"
GRAY_BG        = "#EAEDF2"
GRAY_LIGHT     = "#F2F4F7"
GRAY_DARK      = "#333333"
GRAY_MID       = "#777777"
SUBTITLE_COLOR = "#A0B4CC"
WHITE          = "#FFFFFF"

DPI  = 192
FIG_W, FIG_H = 10, 5.625   # 1920x1080 at 192 DPI
TOTAL = 22


# ── Helper Functions ─────────────────────────────────────────────────────────

def new_slide(facecolor=GRAY_BG):
    """Create a 1920x1080 figure with a single axis filling it."""
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=facecolor)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(facecolor)
    return fig, ax


def header(ax, title, subtitle=""):
    """Navy bar from y=0.93 to y=1.0 with white title and optional subtitle."""
    rect(ax, 0, 0.93, 1, 0.07, TROY_BLUE)
    ax.text(0.03, 0.97, title, fontsize=15, color="white",
            fontweight="bold", ha="left", va="center", transform=ax.transAxes)
    if subtitle:
        ax.text(0.03, 0.941, subtitle, fontsize=9, color=SUBTITLE_COLOR,
                ha="left", va="center", transform=ax.transAxes)


def footer_bar(ax, n, total=TOTAL):
    """Navy bar from y=0 to y=0.04 with left text and right page number."""
    rect(ax, 0, 0, 1, 0.04, TROY_BLUE)
    ax.text(0.02, 0.02,
            "Troy SD G6-G7 Math — Executive Summary • "
            "github.com/akarpo/tsd-g6g7math-choice",
            fontsize=6.5, color="white", va="center", ha="left",
            transform=ax.transAxes)
    ax.text(0.97, 0.02, f"{n} / {total}",
            fontsize=7, color="white", ha="right", va="center",
            transform=ax.transAxes)


def rect(ax, x, y, w, h, color, alpha=1):
    """Draw a colored rectangle at normalized coordinates."""
    r = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="square,pad=0",
        facecolor=color, edgecolor="none", alpha=alpha,
        transform=ax.transAxes, zorder=1,
    )
    ax.add_patch(r)
    return r


def text(ax, x, y, txt, fontsize=12, color=GRAY_DARK, ha="left", va="top",
         weight="normal", wrap_width=None, style="normal", family="sans-serif",
         zorder=5):
    """Place text on the axis. If wrap_width, textwrap.fill first."""
    if wrap_width:
        txt = textwrap.fill(str(txt), width=wrap_width)
    return ax.text(x, y, txt, fontsize=fontsize, color=color, ha=ha, va=va,
                   fontweight=weight, fontstyle=style, family=family,
                   transform=ax.transAxes, zorder=zorder)


def accent_bar(ax, x, y, w, color, thickness=0.004):
    """Small colored horizontal accent bar."""
    rect(ax, x, y, w, thickness, color)


def embed_chart(fig, path, x, y, w, h):
    """Embed a chart PNG into the figure using add_axes + imshow."""
    if not os.path.exists(path):
        print(f"  WARNING: chart not found: {path}")
        return None
    img = Image.open(path)
    img_arr = np.asarray(img)
    ax_img = fig.add_axes([x, y, w, h])
    ax_img.imshow(img_arr)
    ax_img.axis("off")
    return ax_img


def save_slide(fig, n):
    """Save the figure to slides/NN.png."""
    path = os.path.join(SLIDES_DIR, f"{n:02d}.png")
    fig.savefig(path, dpi=DPI, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"  Saved {path}")


def chart_path(name):
    return os.path.join(CHARTS_DIR, name)


def section_header_rect(ax, x, y, w, h, label, bg=TROY_BLUE, fontsize=10):
    """Dark colored rectangle with white text label."""
    rect(ax, x, y, w, h, bg)
    ax.text(x + 0.01, y + h / 2, label, fontsize=fontsize, color="white",
            fontweight="bold", va="center", ha="left", transform=ax.transAxes,
            zorder=5)


# ── Slide Builders ───────────────────────────────────────────────────────────

def slide_01():
    """Title slide -- full TROY_BLUE background, no header/footer bars."""
    fig, ax = new_slide(facecolor=TROY_BLUE)

    # Main title — vertically centered content block
    text(ax, 0.06, 0.72, "Troy SD G6-G7 Math",
         fontsize=32, color="white", weight="bold")
    text(ax, 0.06, 0.60,
         "Has IM + Detracking Outperformed Its Characteristics?",
         fontsize=18, color="white")

    # White horizontal line
    ax.plot([0.06, 0.50], [0.54, 0.54], color="white", linewidth=1.5,
            transform=ax.transAxes, solid_capstyle="round")

    text(ax, 0.06, 0.49,
         "Executive Summary — SEDA 2025.1 + M-STEP Data",
         fontsize=14, color="white")

    # Bottom lines — pulled up to close gap
    text(ax, 0.06, 0.33,
         "Prepared May 2026  •  296-district national benchmark  "
         "•  2009–2025 coverage",
         fontsize=11, color=SUBTITLE_COLOR)
    text(ax, 0.06, 0.27,
         "Repo: github.com/akarpo/tsd-g6g7math-choice   "
         "Live: tsd-g6g7math-choice.pages.dev",
         fontsize=11, color=SUBTITLE_COLOR, style="italic")

    save_slide(fig, 1)


def slide_02():
    """The Question -- and the One-Line Answer."""
    fig, ax = new_slide()
    header(ax, "The Question — and the One-Line Answer",
           "Three independent lines of evidence converge on the same answer")
    footer_bar(ax, 2)

    # Question label
    text(ax, 0.03, 0.89, "QUESTION", fontsize=8, weight="bold", color=GRAY_MID)
    text(ax, 0.03, 0.86,
         "Has Troy’s Fall 2023 adoption of Illustrative Mathematics and "
         "detracking of G6+G7 math produced results that outperform its "
         "characteristics?",
         fontsize=12, weight="bold", color=GRAY_DARK, wrap_width=100)

    # Answer
    text(ax, 0.03, 0.76, "ANSWER", fontsize=8, weight="bold", color=ACCENT_RED)
    text(ax, 0.03, 0.62, "No.", fontsize=48, weight="bold", color=ACCENT_RED,
         va="center")
    text(ax, 0.14, 0.62,
         "The evidence converges from three independent directions:",
         fontsize=12, weight="bold", color=GRAY_DARK, va="center")

    # Three evidence boxes spanning full width
    col_w = 0.305
    gap = 0.02
    box_h = 0.46
    y_bot = 0.05
    x_starts = [0.02, 0.02 + col_w + gap, 0.02 + 2 * (col_w + gap)]
    bg_colors = [LIGHT_RED, LIGHT_RED, LIGHT_GREEN]
    accent_colors = [ACCENT_RED, ACCENT_RED, ACCENT_GREEN]
    big_nums = ["197 / 295", "59 positions", "9×"]
    labels = [
        "level-matched peers rank\nTroy in the bottom third",
        "lost in national rankings\n— #76 to #135",
        "Birmingham recovered 9×\nmore, same county,\ntracking intact",
    ]

    for i in range(3):
        x = x_starts[i]
        rect(ax, x, y_bot, col_w, box_h, bg_colors[i])
        accent_bar(ax, x, y_bot + box_h, col_w, accent_colors[i], 0.005)
        text(ax, x + 0.02, y_bot + box_h - 0.05, big_nums[i],
             fontsize=32, weight="bold", color=accent_colors[i])
        text(ax, x + 0.02, y_bot + box_h - 0.18, labels[i],
             fontsize=13, color=GRAY_DARK)

    save_slide(fig, 2)


def slide_03():
    """What Troy Did and When -- horizontal timeline."""
    fig, ax = new_slide()
    header(ax, "What Troy Did and When",
           "Fall 2023: Illustrative Mathematics adopted, G6+G7 math detracked")
    footer_bar(ax, 3)

    events = [
        ("Fall 2023", "Adopted Illustrative\nMathematics, detracked\nG6 and G7 math"),
        ("Spring 2024", "First IM cohort tested\n(G6 M-STEP)"),
        ("Fall 2024", "Second IM year; first\nG7 IM cohort enters\n7th grade"),
        ("Spring 2025", "Second IM G6 + first\nIM G7 tested"),
    ]
    n_events = len(events)
    x_margin = 0.10
    x_span = 0.80
    y_line = 0.55

    # Horizontal line
    ax.plot([x_margin, x_margin + x_span], [y_line, y_line],
            color=TROY_BLUE, linewidth=2, transform=ax.transAxes,
            solid_capstyle="round")

    for i, (date, desc) in enumerate(events):
        x = x_margin + i * x_span / (n_events - 1)
        ax.plot(x, y_line, "o", color=TROY_BLUE, markersize=12,
                transform=ax.transAxes, zorder=5)
        text(ax, x, y_line + 0.09, date, fontsize=12, weight="bold",
             color=TROY_BLUE, ha="center", va="center")
        text(ax, x, y_line - 0.07, desc, fontsize=10, color=GRAY_DARK,
             ha="center", va="top")

    # Bottom note
    rect(ax, 0.06, 0.08, 0.88, 0.09, GRAY_LIGHT)
    text(ax, 0.50, 0.125,
         "Prior: Big Ideas Math 7, Math 7/8 Honors, small Algebra 1 cohort",
         fontsize=10, color=GRAY_MID, ha="center", va="center", style="italic")

    save_slide(fig, 3)


def slide_04():
    """Troy's Pre-COVID Math Position -- Strong, Not Invincible."""
    fig, ax = new_slide()
    header(ax, "Troy’s Pre-COVID Math Position — Strong, Not Invincible",
           "Pre-COVID G6+G7: +0.937 grade levels above national norm")
    footer_bar(ax, 4)

    embed_chart(fig, chart_path("chart01_mi_peers_g6_trend.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_GREEN
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_GREEN)

    text(ax, px + 0.02, py + ph - 0.04, "+0.937",
         fontsize=36, weight="bold", color=TROY_BLUE)
    text(ax, px + 0.02, py + ph - 0.15, "grade levels above\nnational norm",
         fontsize=14, color=GRAY_DARK)

    accent_bar(ax, px + 0.02, py + ph - 0.26, 0.12, ACCENT_GREEN)

    text(ax, px + 0.02, py + ph - 0.30,
         "2nd highest among\nMI affluent peers",
         fontsize=14, weight="bold", color=GRAY_DARK)

    text(ax, px + 0.02, py + ph - 0.44,
         "Top quarter nationally\n(#76 / 296)",
         fontsize=14, color=GRAY_DARK)

    text(ax, px + 0.02, py + ph - 0.58,
         "37% above national average.\n"
         "Troy entered the pandemic\n"
         "from a position of math\n"
         "strength — not weakness.",
         fontsize=12, color=GRAY_MID, style="italic")

    save_slide(fig, 4)


def slide_05():
    """Troy Fell 59 Places in the National Math Rankings."""
    fig, ax = new_slide()
    header(ax, "Troy Fell 59 Places in the National Math Rankings",
           "From top-quarter to mid-pack among 296 level-matched peers")
    footer_bar(ax, 5)

    embed_chart(fig, chart_path("chart11_rank_shift_scatter.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_RED
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_RED)

    text(ax, px + 0.02, py + ph - 0.04, "Pre-COVID rank:",
         fontsize=10, color=GRAY_MID)
    text(ax, px + 0.02, py + ph - 0.11, "#76 / 296",
         fontsize=28, weight="bold", color=TROY_BLUE)
    text(ax, px + 0.02, py + ph - 0.20, "(top quarter)",
         fontsize=11, color=GRAY_MID)

    accent_bar(ax, px + 0.02, py + ph - 0.26, 0.12, ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.30, "Post-COVID rank:",
         fontsize=10, color=GRAY_MID)
    text(ax, px + 0.02, py + ph - 0.37, "#135 / 296",
         fontsize=28, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.46, "(mid-pack)",
         fontsize=11, color=GRAY_MID)

    accent_bar(ax, px + 0.02, py + ph - 0.52, 0.12, ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.56, "Lost 59 positions",
         fontsize=15, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.64,
         "From top-quarter to middle\nof the pack among peers\nthat started at the same level.",
         fontsize=11, color=GRAY_DARK)

    save_slide(fig, 5)


def slide_06():
    """MI Peer Leaderboard: Troy Fell From 2nd to 4th."""
    fig, ax = new_slide()
    header(ax, "MI Peer Leaderboard: Troy Fell From 2nd to 4th",
           "4 of 5 subgroups lost positions under IM + detracking")
    footer_bar(ax, 6)

    embed_chart(fig, chart_path("chart12_mi_peer_bump.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_RED
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_RED)

    # Subgroup table header
    section_header_rect(ax, px + 0.01, py + ph - 0.06, pw - 0.02, 0.05,
                        "Subgroup Rank Shifts", fontsize=10)

    subgroups = [
        ("All Students",       "2nd→4th", "−2", ACCENT_RED),
        ("Asian",              "1st→2nd", "−1", ACCENT_RED),
        ("White",              "6th→5th", "+1",      ACCENT_GREEN),
        ("Econ Disadvantaged", "3rd→4th", "−1", ACCENT_RED),
        ("Not Econ Disadv",    "2nd→3rd", "−1", ACCENT_RED),
    ]
    row_h = 0.10
    y_start = py + ph - 0.14
    for i, (sg, shift, delta, clr) in enumerate(subgroups):
        ry = y_start - i * row_h
        row_bg = LIGHT_RED if delta.startswith("−") or delta.startswith("-") else LIGHT_GREEN
        rect(ax, px + 0.01, ry - 0.025, pw - 0.02, row_h - 0.01, row_bg)
        text(ax, px + 0.02, ry + 0.01, sg,
             fontsize=10, weight="bold", color=GRAY_DARK, va="center")
        text(ax, px + 0.18, ry + 0.01, shift,
             fontsize=10, color=GRAY_DARK, va="center")
        text(ax, px + 0.27, ry + 0.01, delta,
             fontsize=11, weight="bold", color=clr, va="center")

    # Bottom callout
    accent_bar(ax, px + 0.02, py + 0.14, 0.10, ACCENT_RED)
    text(ax, px + 0.02, py + 0.12,
         "Was #1 Asian math in MI.\nNorthville now leads.",
         fontsize=11, color=ACCENT_RED, weight="bold")
    text(ax, px + 0.02, py + 0.02,
         "4 of 5 subgroups lost positions\nunder IM + detracking.",
         fontsize=10, color=GRAY_MID, style="italic")

    save_slide(fig, 6)


def slide_07():
    """The Post-COVID Decline Hit Troy Hard in Math."""
    fig, ax = new_slide()
    header(ax, "The Post-COVID Decline Hit Troy Hard in Math",
           "Troy declined −0.187 grade levels — rank 104 of 296")
    footer_bar(ax, 7)

    embed_chart(fig, chart_path("chart09_covid_delta_ranking.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_RED
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_RED)

    text(ax, px + 0.02, py + ph - 0.04, "−0.187",
         fontsize=36, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.15, "grade-level decline",
         fontsize=14, color=GRAY_DARK)

    accent_bar(ax, px + 0.02, py + ph - 0.22, 0.10, ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.27, "Rank 104 / 296",
         fontsize=15, weight="bold", color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.35, "35th percentile",
         fontsize=12, color=GRAY_MID)

    accent_bar(ax, px + 0.02, py + ph - 0.43, 0.10, ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.48, "3rd worst of 8\nMI peers",
         fontsize=13, weight="bold", color=ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.64,
         "Troy lost more ground than\nmost comparably-positioned\n"
         "districts nationwide. The\ndecline was not inevitable —\n"
         "many peers held steady or\nrecovered faster.",
         fontsize=10.5, color=GRAY_DARK, style="italic")

    save_slide(fig, 7)


def slide_08():
    """The Critical Test: Recovery During the IM Window."""
    fig, ax = new_slide()
    header(ax, "The Critical Test: Recovery During the IM Window",
           "2022–23 → 2024–25 — if IM were working, Troy should outpace peers")
    footer_bar(ax, 8)

    embed_chart(fig, chart_path("chart04_level_matched_histogram.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_RED
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_RED)

    text(ax, px + 0.02, py + ph - 0.04, "197 / 295",
         fontsize=32, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.15, "level-matched peers\nrank Troy in the bottom third",
         fontsize=13, color=GRAY_DARK)

    accent_bar(ax, px + 0.02, py + ph - 0.27, 0.12, ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.31, "Troy:  +0.024",
         fontsize=13, weight="bold", color=ACCENT_RED, family="monospace")
    text(ax, px + 0.02, py + ph - 0.39, "Peer median:  +0.058",
         fontsize=13, weight="bold", color=GRAY_DARK, family="monospace")

    accent_bar(ax, px + 0.02, py + ph - 0.48, 0.12, ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.53,
         "Most peers recovered\n2–3× more than Troy\nduring the exact period\n"
         "IM was adopted.",
         fontsize=11, color=GRAY_DARK)

    text(ax, px + 0.02, py + ph - 0.74,
         "If IM + detracking were\nworking, Troy should be\noutpacing — not trailing —\n"
         "its peers.",
         fontsize=10.5, color=GRAY_MID, style="italic")

    save_slide(fig, 8)


def slide_09():
    """Among MI Peers, Troy Ranks 6th of 8."""
    fig, ax = new_slide()
    header(ax, "Among MI Peers, Troy Ranks 6th of 8",
           "Birmingham recovered 9× more with tracking intact")
    footer_bar(ax, 9)

    embed_chart(fig, chart_path("chart03_im_window_ranking.png"),
                0.01, 0.05, 0.54, 0.87)

    # Right panel -- GRAY_LIGHT with 8-row table
    px, pw = 0.56, 0.43
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    # Table header
    section_header_rect(ax, px + 0.01, py + ph - 0.06, pw - 0.02, 0.05,
                        "MI Peer IM-Window Recovery (Δ)", fontsize=10)

    districts = [
        ("Birmingham",       "+0.211", "(tracked)", False),
        ("Northville",       "+0.102", "(tracked)", False),
        ("Bloomfield Hills", "+0.082", "(tracked)", False),
        ("Walled Lake",      "+0.056", "",          False),
        ("Novi",             "+0.029", "",          False),
        ("Troy",             "+0.024", "(IM+detracked)", True),
        ("West Bloomfield",  "+0.006", "",          False),
        ("Rochester",        "+0.000", "",          False),
    ]
    row_h = 0.095
    y_start = py + ph - 0.13
    for i, (name, val, note, is_troy) in enumerate(districts):
        ry = y_start - i * row_h
        if is_troy:
            rect(ax, px + 0.01, ry - 0.025, pw - 0.02, row_h - 0.01, LIGHT_RED)
        text(ax, px + 0.02, ry + 0.01, name,
             fontsize=10.5, weight="bold" if is_troy else "normal",
             color=ACCENT_RED if is_troy else GRAY_DARK, va="center")
        text(ax, px + 0.24, ry + 0.01, val,
             fontsize=10.5, weight="bold" if is_troy else "normal",
             color=ACCENT_RED if is_troy else GRAY_DARK,
             va="center", family="monospace")
        if note:
            text(ax, px + 0.32, ry + 0.01, note,
                 fontsize=8, color=GRAY_MID, va="center")

    save_slide(fig, 9)


def slide_10():
    """G7 Math: The Tracked-vs-IM Comparison Year."""
    fig, ax = new_slide()
    header(ax, "G7 Math: The Tracked-vs-IM Comparison Year",
           "2023–24 G7 tracked. 2024–25 first G7 IM cohort — recovery stalled")
    footer_bar(ax, 10)

    embed_chart(fig, chart_path("chart02_mi_peers_g7_trend.png"),
                0.01, 0.05, 0.64, 0.87)

    # Two stacked panels on right
    px, pw = 0.66, 0.33
    panel_h = 0.40

    # Top panel -- LIGHT_GREEN
    top_y = 0.05 + panel_h + 0.07
    rect(ax, px, top_y, pw, panel_h, LIGHT_GREEN)
    accent_bar(ax, px, top_y + panel_h, pw, ACCENT_GREEN, 0.005)
    text(ax, px + 0.02, top_y + panel_h - 0.04,
         "2023–24: Tracked",
         fontsize=16, weight="bold", color=ACCENT_GREEN)
    text(ax, px + 0.02, top_y + panel_h - 0.14,
         "G7 still used Big Ideas\nMath with tracking.\n\n"
         "Troy matched MI peers\nin recovery pace.",
         fontsize=14, color=GRAY_DARK)

    # Bottom panel -- LIGHT_RED
    bot_y = 0.05
    rect(ax, px, bot_y, pw, panel_h, LIGHT_RED)
    accent_bar(ax, px, bot_y + panel_h, pw, ACCENT_RED, 0.005)
    text(ax, px + 0.02, bot_y + panel_h - 0.04,
         "2024–25: IM + Detracked",
         fontsize=16, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, bot_y + panel_h - 0.14,
         "First G7 IM cohort.\n\n"
         "Recovery stalled — peers\nwith tracking continued\nto improve.",
         fontsize=14, color=GRAY_DARK)

    save_slide(fig, 10)


def slide_11():
    """The Asian Subgroup Crisis -- 36% of Troy."""
    fig, ax = new_slide()
    header(ax, "The Asian Subgroup Crisis — 36% of Troy",
           "Troy’s strongest demographic shows the sharpest decline")
    footer_bar(ax, 11)

    embed_chart(fig, chart_path("chart05_asian_g6_trend.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_RED with three stat cards
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_RED)

    cards = [
        ("G6 Asian Δ COVID:", "−0.409", "Sharpest decline of any\nTroy subgroup"),
        ("G7 Asian Δ COVID:", "−0.278", "Second sharpest —\nstill steep"),
        ("G7 IM-window:", "−0.094", "Still declining under IM\n(peers are recovering)"),
    ]
    card_h = 0.27
    gap = 0.02
    y_top = py + ph - 0.04
    for i, (label, value, desc) in enumerate(cards):
        cy = y_top - i * (card_h + gap)
        accent_bar(ax, px + 0.02, cy, 0.10, ACCENT_RED)
        text(ax, px + 0.02, cy - 0.02, label,
             fontsize=11, color=GRAY_MID)
        text(ax, px + 0.02, cy - 0.09, value,
             fontsize=26, weight="bold", color=ACCENT_RED)
        text(ax, px + 0.02, cy - 0.17, desc,
             fontsize=11, color=GRAY_DARK)

    save_slide(fig, 11)


def slide_12():
    """G7 Asian Math Is Still Declining Under IM."""
    fig, ax = new_slide()
    header(ax, "G7 Asian Math Is Still Declining Under IM",
           "High-Asian peers with tracking show robust recovery")
    footer_bar(ax, 12)

    embed_chart(fig, chart_path("chart06_asian_g7_trend.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel with three comparison cards
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    section_header_rect(ax, px + 0.01, py + ph - 0.06, pw - 0.02, 0.05,
                        "G7 Asian IM-Window Δ", fontsize=10)

    comparisons = [
        ("Bellevue (WA)", "41% Asian, tracked", "+0.162", LIGHT_GREEN, ACCENT_GREEN),
        ("Issaquah (WA)", "30% Asian, tracked", "+0.218", LIGHT_GREEN, ACCENT_GREEN),
        ("Troy (MI)",     "36% Asian, IM+detracked", "−0.094", LIGHT_RED, ACCENT_RED),
    ]
    card_h = 0.24
    gap = 0.03
    y_top = py + ph - 0.14
    for i, (district, demo, delta, bg, clr) in enumerate(comparisons):
        cy = y_top - i * (card_h + gap)
        rect(ax, px + 0.01, cy - card_h + 0.02, pw - 0.02, card_h, bg)
        accent_bar(ax, px + 0.01, cy + 0.02, pw - 0.02, clr, 0.004)
        text(ax, px + 0.03, cy - 0.01, district,
             fontsize=12, weight="bold", color=GRAY_DARK)
        text(ax, px + 0.03, cy - 0.06, demo,
             fontsize=10, color=GRAY_MID)
        text(ax, px + 0.03, cy - 0.14, delta,
             fontsize=22, weight="bold", color=clr)

    save_slide(fig, 12)


def slide_13():
    """Every Subgroup Declined -- Recovery Is Uneven."""
    fig, ax = new_slide()
    header(ax, "Every Subgroup Declined — Recovery Is Uneven",
           "Asian and White subgroups show largest absolute declines")
    footer_bar(ax, 13)

    embed_chart(fig, chart_path("chart07_troy_subgroup_waterfall.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_ORANGE)

    section_header_rect(ax, px + 0.01, py + ph - 0.06, pw - 0.02, 0.05,
                        "Key Findings", fontsize=10)

    text(ax, px + 0.02, py + ph - 0.12,
         "Every Troy subgroup declined\n"
         "from pre-COVID levels.\n\n"
         "Asian students lost the most\n"
         "ground (−0.409 G6, −0.278 G7).\n\n"
         "White students show the\n"
         "second-largest decline.\n\n"
         "ECD subgroup was already\n"
         "near national average —\n"
         "least room to fall.\n\n"
         "Recovery has been uneven:\n"
         "the highest-performing groups\n"
         "pre-COVID show the weakest\n"
         "bounce-back under IM.",
         fontsize=11.5, color=GRAY_DARK)

    save_slide(fig, 13)


def slide_14():
    """M-STEP: The Numbers Parents See."""
    fig, ax = new_slide()
    header(ax, "M-STEP: The Numbers Parents See",
           "Michigan M-STEP % proficient, grades 6 and 7")
    footer_bar(ax, 14)

    embed_chart(fig, chart_path("chart08_mstep_troy_proficiency.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    section_header_rect(ax, px + 0.01, py + ph - 0.06, pw - 0.02, 0.05,
                        "M-STEP Proficiency", fontsize=10)

    text(ax, px + 0.02, py + ph - 0.13, "Grade 6",
         fontsize=13, weight="bold", color=TROY_BLUE)
    text(ax, px + 0.02, py + ph - 0.19,
         "2019: 71.4%\n2022: 63.2%\n2023: 66.3%  (1st IM)\n2024: 65.8%  (2nd IM)",
         fontsize=11, color=GRAY_DARK, family="monospace")

    accent_bar(ax, px + 0.02, py + ph - 0.42, 0.12, TROY_BLUE)

    text(ax, px + 0.02, py + ph - 0.46, "Grade 7",
         fontsize=13, weight="bold", color=TROY_BLUE)
    text(ax, px + 0.02, py + ph - 0.52,
         "2019: 67.5%\n2022: 61.3%\n2023: 66.0%  (tracked)\n2024: TBD   (1st IM)",
         fontsize=11, color=GRAY_DARK, family="monospace")

    accent_bar(ax, px + 0.02, py + ph - 0.73, 0.12, ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.77,
         "IM has not restored\npre-COVID proficiency",
         fontsize=13, weight="bold", color=ACCENT_RED)

    text(ax, px + 0.02, py + ph - 0.88,
         "G6 proficiency is still 5.6\n"
         "points below the 2019 peak\n"
         "after two years of IM.",
         fontsize=11, color=GRAY_DARK, style="italic")

    save_slide(fig, 14)


def slide_15():
    """San Francisco: 12 Years of Detracking, Then Reversal."""
    fig, ax = new_slide()
    header(ax, "San Francisco: 12 Years of Detracking, Then Reversal",
           "SFUSD eliminated Algebra 1 in 8th grade in 2014 — reversed March 2026")
    footer_bar(ax, 15)

    findings = [
        (ACCENT_RED, LIGHT_RED,
         "Achievement gaps WIDENED",
         "Hispanic–White gap expanded 31 points (vs 5 statewide). "
         "The equity rationale failed on its own terms."),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "AP math enrollment DECLINED 15%",
         "Driven by Asian/Pacific Islander students. Fewer students "
         "reached advanced coursework."),
        (ACCENT_RED, LIGHT_RED,
         "Board voted March 2026 to RESTORE Algebra 1",
         "After 12 years, SFUSD reversed course. The longest-running "
         "U.S. detracking experiment ended in retreat."),
    ]
    panel_h = 0.23
    gap = 0.02
    y_top = 0.66
    for i, (accent_clr, bg_clr, heading, detail) in enumerate(findings):
        py_f = y_top - i * (panel_h + gap)
        rect(ax, 0.03, py_f, 0.94, panel_h, bg_clr)
        accent_bar(ax, 0.03, py_f + panel_h, 0.94, accent_clr, 0.005)
        text(ax, 0.06, py_f + panel_h - 0.04, heading,
             fontsize=15, weight="bold", color=accent_clr)
        text(ax, 0.06, py_f + panel_h - 0.11, detail,
             fontsize=12, color=GRAY_DARK, wrap_width=90)

    # Bottom callout bar
    rect(ax, 0.03, 0.05, 0.94, 0.08, TROY_BLUE)
    text(ax, 0.50, 0.09,
         "Troy is replicating a strategy with a well-documented failure pattern",
         fontsize=13, color="white", ha="center", va="center", weight="bold")

    save_slide(fig, 15)


def slide_16():
    """Cambridge: Detracked 2017-2019, Now Reversing."""
    fig, ax = new_slide()
    header(ax, "Cambridge: Detracked 2017–2019, Now Reversing",
           "A second major detracking experiment being reversed")
    footer_bar(ax, 16)

    col_w = 0.46
    gap = 0.03
    col_h = 0.82
    py = 0.05
    x1 = 0.02
    x2 = x1 + col_w + gap

    # Left panel -- LIGHT_ORANGE
    rect(ax, x1, py, col_w, col_h, LIGHT_ORANGE)
    accent_bar(ax, x1, py + col_h, col_w, ACCENT_ORANGE, 0.005)
    section_header_rect(ax, x1 + 0.01, py + col_h - 0.07, col_w - 0.02, 0.05,
                        "What They Did", bg=ACCENT_ORANGE, fontsize=12)
    text(ax, x1 + 0.02, py + col_h - 0.12,
         "Eliminated accelerated math\n"
         "tracks to address racial\n"
         "disparities in advanced\n"
         "course enrollment.\n\n"
         "All students placed in the\n"
         "same math class regardless\n"
         "of prior achievement.\n\n"
         "Implemented 2017–2019.\n"
         "COVID hit during early\n"
         "rollout, obscuring results.",
         fontsize=14, color=GRAY_DARK)

    # Right panel -- LIGHT_RED
    rect(ax, x2, py, col_w, col_h, LIGHT_RED)
    accent_bar(ax, x2, py + col_h, col_w, ACCENT_RED, 0.005)
    section_header_rect(ax, x2 + 0.01, py + col_h - 0.07, col_w - 0.02, 0.05,
                        "What Happened", bg=ACCENT_RED, fontsize=12)
    text(ax, x2 + 0.02, py + col_h - 0.12,
         "Achievement gaps persisted.\n\n"
         "Advanced students\n"
         "underserved — families\n"
         "sought outside tutoring.\n\n"
         "District now reversing\n"
         "course, restoring algebra\n"
         "to 8th grade.\n\n"
         "Same pattern as SFUSD:\n"
         "equity goal unmet, advanced\n"
         "students harmed, eventual\n"
         "policy reversal.",
         fontsize=14, color=GRAY_DARK)

    save_slide(fig, 16)


def slide_17():
    """The '50% Algebra 1' Claim."""
    fig, ax = new_slide()
    header(ax, "The ‘50% Algebra 1’ Claim",
           "Course enrollment is not an achievement metric")
    footer_bar(ax, 17)

    findings = [
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "SFUSD made the identical claim",
         "For a decade SFUSD cited rising enrollment in gateway courses. "
         "Test scores eventually revealed no improvement. "
         "Enrollment =/= mastery."),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "Troy’s SEDA scores tell a different story",
         "G6+G7 math readiness dropped from +0.937 to +0.750 — "
         "a quarter-grade-level decline. More students in Algebra 1 "
         "does not mean more students ready for it."),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "The real comparison is peer performance",
         "The question is not whether more Troy students now take Algebra 1. "
         "It is whether Troy students learn as much math as peers at "
         "comparable districts — and the answer is no."),
    ]
    panel_h = 0.25
    gap = 0.02
    y_top = 0.67
    for i, (accent_clr, bg_clr, heading, detail) in enumerate(findings):
        py_f = y_top - i * (panel_h + gap)
        rect(ax, 0.03, py_f, 0.94, panel_h, bg_clr)
        accent_bar(ax, 0.03, py_f + panel_h, 0.94, accent_clr, 0.005)
        text(ax, 0.06, py_f + panel_h - 0.04, heading,
             fontsize=15, weight="bold", color=accent_clr)
        text(ax, 0.06, py_f + panel_h - 0.12, detail,
             fontsize=12, color=GRAY_DARK, wrap_width=90)

    save_slide(fig, 17)


def slide_18():
    """What High-Performing Districts Do Differently."""
    fig, ax = new_slide()
    header(ax, "What High-Performing Districts Do Differently",
           "Many California and NJ districts recovered with tracking intact")
    footer_bar(ax, 18)

    embed_chart(fig, chart_path("chart10_high_asian_peers_delta.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_GREEN
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_GREEN)

    section_header_rect(ax, px + 0.01, py + ph - 0.06, pw - 0.02, 0.05,
                        "High-Asian Peer Analysis", fontsize=10)

    text(ax, px + 0.02, py + ph - 0.13,
         "Among 107 high-Asian\n"
         "(≥20%) districts:\n\n"
         "Many California and NJ\n"
         "districts recovered to or\n"
         "surpassed pre-COVID levels\n"
         "— with tracking intact.\n\n"
         "Districts that maintained\n"
         "differentiated math pathways\n"
         "show stronger recovery\n"
         "trajectories.\n\n"
         "Troy’s approach of removing\n"
         "tracks is the outlier, not\n"
         "the norm, among high-\n"
         "performing peers.",
         fontsize=12, color=GRAY_DARK)

    save_slide(fig, 18)


def slide_19():
    """Illustrative Mathematics: Evidence Gaps."""
    fig, ax = new_slide()
    header(ax, "Illustrative Mathematics: Evidence Gaps",
           "No published evidence of IM success in a district like Troy")
    footer_bar(ax, 19)

    # Table header
    th_y = 0.84
    th_h = 0.06
    section_header_rect(ax, 0.03, th_y, 0.94, th_h,
                        "   District                            Result"
                        "                              Note",
                        fontsize=10)

    rows = [
        ("NYC District 11 (Bronx)", "25.8% → 50.6%",
         "High-poverty, low-baseline—not comparable to Troy"),
        ("Fort Zumwalt (MO)",       "Effect size 0.16 SD",
         "Modest, comparable to general improvement trend"),
        ("Philadelphia",            "Process study only",
         "No student outcomes data published"),
    ]
    row_h = 0.18
    for i, (district, result, note) in enumerate(rows):
        ry = th_y - (i + 1) * row_h
        bg = GRAY_LIGHT if i % 2 == 0 else WHITE
        rect(ax, 0.03, ry, 0.94, row_h, bg)
        text(ax, 0.05, ry + row_h / 2 + 0.01, district,
             fontsize=11, weight="bold", color=GRAY_DARK, va="center")
        text(ax, 0.35, ry + row_h / 2 + 0.01, result,
             fontsize=11, color=GRAY_DARK, va="center", family="monospace")
        text(ax, 0.60, ry + row_h / 2 + 0.01, note,
             fontsize=10, color=GRAY_MID, va="center", wrap_width=40)

    # Bottom callout
    rect(ax, 0.03, 0.06, 0.94, 0.11, LIGHT_ORANGE)
    accent_bar(ax, 0.03, 0.17, 0.94, ACCENT_ORANGE, 0.005)
    text(ax, 0.50, 0.115,
         "No published evidence of IM success in an affluent, "
         "high-performing, high-Asian district like Troy",
         fontsize=12, weight="bold", color=ACCENT_ORANGE,
         ha="center", va="center", wrap_width=90)

    save_slide(fig, 19)


def slide_20():
    """Conclusions."""
    fig, ax = new_slide()
    header(ax, "Conclusions",
           "Five findings from three independent lines of evidence")
    footer_bar(ax, 20)

    conclusions = [
        (ACCENT_RED, LIGHT_RED,
         "Troy has NOT outperformed its characteristics",
         "Bottom third of 295 level-matched peers in IM-window recovery. "
         "Rank 197 of 295."),
        (ACCENT_RED, LIGHT_RED,
         "Asian subgroup is most concerning",
         "G7 Asian math is STILL declining (−0.094) while high-Asian "
         "peers with tracking recover."),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "Detracking evidence base is against this approach",
         "SFUSD (12 years) and Cambridge both reversed. Gaps widened, "
         "not narrowed."),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "Course enrollment ≠ achievement",
         "50% Algebra 1 claim mirrors SFUSD’s decade of misleading metrics. "
         "SEDA shows actual readiness declined."),
        (ACCENT_RED, LIGHT_RED,
         "Opportunity cost is real",
         "Birmingham recovered 9× more in the same window with tracking "
         "intact. Every year of delay compounds the gap."),
    ]
    row_h = 0.16
    y_top = 0.88
    for i, (clr, bg, heading, detail) in enumerate(conclusions):
        cy = y_top - i * row_h
        rect(ax, 0.08, cy - row_h + 0.02, 0.89, row_h - 0.01, bg)
        circle = mpatches.Circle((0.05, cy - row_h / 2 + 0.02), 0.022,
                                 facecolor=clr, edgecolor="none",
                                 transform=ax.transAxes, zorder=5)
        ax.add_patch(circle)
        ax.text(0.05, cy - row_h / 2 + 0.02, str(i + 1),
                fontsize=13, fontweight="bold", color="white",
                ha="center", va="center", transform=ax.transAxes, zorder=6)
        text(ax, 0.09, cy - 0.005, heading,
             fontsize=13, weight="bold", color=clr)
        text(ax, 0.09, cy - 0.06, detail,
             fontsize=11, color=GRAY_DARK, wrap_width=80)

    save_slide(fig, 20)


def slide_21():
    """Methodology."""
    fig, ax = new_slide()
    header(ax, "Methodology",
           "SEDA 2025.1 (Stanford CEPA)")
    footer_bar(ax, 21)

    sections = [
        ("Data Source",
         "SEDA 2025.1 (Stanford Center for Education Policy Analysis). "
         "Nationally standardized, NAEP-anchored achievement data covering "
         "2009–2025."),
        ("Metric",
         "cs_mn — cohort-standardized mean. One unit = one grade level of "
         "learning. NAEP-anchored for cross-state comparability."),
        ("Time Windows",
         "Pre-COVID: 2017–2019 mean\n"
         "Post-COVID: 2022–2025 mean\n"
         "IM Window: 2022–23 → 2024–25 (exact adoption period)"),
        ("Peer Groups",
         "296 level-matched (pre-COVID G6+G7 math ±0.25 of Troy’s +0.937)\n"
         "107 high-Asian (≥20% Asian, pre-COVID ≥+0.50)\n"
         "8 MI affluent peers (same state test, Oakland County focus)"),
        ("Subgroups",
         "All Students, Asian, White, Black, Hispanic, Economically "
         "Disadvantaged, Not Economically Disadvantaged"),
    ]
    sy = 0.87
    for label, body in sections:
        section_header_rect(ax, 0.03, sy - 0.045, 0.17, 0.045, label,
                            fontsize=10)
        text(ax, 0.22, sy, body, fontsize=13, color=GRAY_DARK,
             wrap_width=75)
        n_lines = body.count("\n") + 1
        line_h = max(0.06, 0.05 * n_lines + 0.035)
        sy -= line_h + 0.02

    save_slide(fig, 21)


def slide_22():
    """References."""
    fig, ax = new_slide()
    header(ax, "References",
           "Primary data sources and research")
    footer_bar(ax, 22)

    refs = [
        ("SEDA 2025.1",
         "Stanford Center for Education Policy Analysis. "
         "edopportunity.org. Reardon et al."),
        ("Education Scorecard 2026",
         "Harvard–Stanford–Dartmouth. Demographic-adjusted "
         "gain methodology."),
        ("MI School Data / M-STEP",
         "Michigan Department of Education. mischooldata.org. "
         "State assessment proficiency rates."),
        ("Dee, Huffaker & Novicoff (2025)",
         "\"The Effects of San Francisco’s Math Course Sequence "
         "Reform.\" SFUSD detracking study."),
        ("Education Next / SFUSD Analysis",
         "Detracking policy analysis including AP enrollment "
         "trends and achievement gap data."),
        ("Brookings Institution",
         "Detracking evidence review. Cross-district analysis "
         "of tracking vs. heterogeneous grouping outcomes."),
    ]
    sy = 0.87
    row_h = 0.13
    for i, (title_text, desc) in enumerate(refs):
        ry = sy - i * row_h
        bg = GRAY_LIGHT if i % 2 == 0 else WHITE
        rect(ax, 0.03, ry - row_h + 0.02, 0.94, row_h - 0.01, bg)
        text(ax, 0.05, ry - 0.01, f"{i + 1}.",
             fontsize=12, weight="bold", color=TROY_BLUE)
        text(ax, 0.08, ry - 0.01, title_text,
             fontsize=11, weight="bold", color=TROY_BLUE)
        text(ax, 0.08, ry - 0.055, desc,
             fontsize=10, color=GRAY_DARK, wrap_width=85)

    save_slide(fig, 22)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print(f"Rendering {TOTAL} slides to {SLIDES_DIR}")

    slide_01()
    slide_02()
    slide_03()
    slide_04()
    slide_05()
    slide_06()
    slide_07()
    slide_08()
    slide_09()
    slide_10()
    slide_11()
    slide_12()
    slide_13()
    slide_14()
    slide_15()
    slide_16()
    slide_17()
    slide_18()
    slide_19()
    slide_20()
    slide_21()
    slide_22()

    print(f"Done -- {TOTAL} slides saved.")


if __name__ == "__main__":
    main()
