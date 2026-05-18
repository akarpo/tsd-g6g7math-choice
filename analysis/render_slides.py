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

# ── Color Palette (matched to K-5 ELA deck) ─────────────────────────────────
TROY_BLUE      = "#1F3A5F"
ACCENT_RED     = "#B02121"
ACCENT_GREEN   = "#1F7A3D"
ACCENT_ORANGE  = "#CC6A11"
LIGHT_GREEN    = "#E6F4E8"
LIGHT_ORANGE   = "#FFF4E0"
LIGHT_RED      = "#FCE4E4"
GRAY_BG        = "#EAEDF2"
GRAY_LIGHT     = "#EEEEEE"
GRAY_DARK      = "#333333"
GRAY_MID       = "#707070"
SUBTITLE_COLOR = "#CCDDEE"
WHITE          = "#FFFFFF"

DPI  = 192
FIG_W, FIG_H = 10, 5.625   # 1920x1080 at 192 DPI
TOTAL = 20


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
           "G6+G7 Math: three independent lines of evidence converge")
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
    big_nums = ["197 / 295", "6th of 8", "−0.028"]
    labels = [
        "level-matched peers\nrecovered more in the\nIM window",
        "MI peers outpaced Troy\nin IM-window recovery\n(+0.076 vs +0.080 median)",
        "G7 Asian still declining\nunder IM — only subgroup\nnot recovering",
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
    header(ax, "COVID Erased Troy's Math Advantage",
           "G6+G7 Math: Pre-COVID #76 → Post-COVID #135 among 296 level-matched peers")
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
         "COVID hit Troy harder than\nmost peers. This is the\ndeficit IM inherited — not\ncaused.",
         fontsize=11, color=GRAY_DARK)

    save_slide(fig, 5)


def slide_06():
    """MI Peer Leaderboard: Troy Fell From 2nd to 4th."""
    fig, ax = new_slide()
    header(ax, "MI Peer Leaderboard: Troy Holds at 4th in IM Window",
           "G6+G7 Math: rank unchanged from 2023 to 2025 — no ground gained or lost")
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
        ("All Students",       "4th→4th", "±0", GRAY_MID),
        ("Asian",              "3rd→3rd", "±0", GRAY_MID),
        ("White",              "4th→5th", "−1", ACCENT_RED),
        ("Econ Disadvantaged", "3rd→3rd", "±0", GRAY_MID),
        ("Not Econ Disadv",    "3rd→3rd", "±0", GRAY_MID),
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
    accent_bar(ax, px + 0.02, py + 0.14, 0.10, ACCENT_ORANGE)
    text(ax, px + 0.02, py + 0.12,
         "White subgroup dropped\none spot (4th→5th).",
         fontsize=11, color=ACCENT_ORANGE, weight="bold")
    text(ax, px + 0.02, py + 0.02,
         "Rank stability means Troy\nis not closing the gap\nCOVID opened.",
         fontsize=10, color=GRAY_MID, style="italic")

    save_slide(fig, 6)


def slide_07():
    """The Post-COVID Decline Hit Troy Hard in Math."""
    fig, ax = new_slide()
    header(ax, "IM-Window Recovery: Troy Mid-Pack Among 22 Districts",
           "G6+G7 Math: Troy +0.076 — 13th of 22 analysis districts (2023-2025)")
    footer_bar(ax, 7)

    embed_chart(fig, chart_path("chart09_covid_delta_ranking.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel -- LIGHT_RED
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, LIGHT_RED)

    text(ax, px + 0.02, py + ph - 0.04, "+0.076",
         fontsize=36, weight="bold", color=ACCENT_ORANGE)
    text(ax, px + 0.02, py + ph - 0.15, "grade-level recovery\n(2023 → 2025)",
         fontsize=14, color=GRAY_DARK)

    accent_bar(ax, px + 0.02, py + ph - 0.27, 0.10, ACCENT_ORANGE)

    text(ax, px + 0.02, py + ph - 0.31, "Rank 13 / 22",
         fontsize=15, weight="bold", color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.39, "mid-pack among\nanalysis districts",
         fontsize=12, color=GRAY_MID)

    accent_bar(ax, px + 0.02, py + ph - 0.48, 0.10, ACCENT_ORANGE)

    text(ax, px + 0.02, py + ph - 0.53, "6th of 8 MI peers",
         fontsize=13, weight="bold", color=ACCENT_ORANGE)

    text(ax, px + 0.02, py + ph - 0.64,
         "Troy is recovering, but\nnot closing the gap that\n"
         "COVID opened. Most peers\nare recovering faster.",
         fontsize=10.5, color=GRAY_DARK, style="italic")

    save_slide(fig, 7)


def slide_08():
    """The Critical Test: Recovery During the IM Window."""
    fig, ax = new_slide()
    header(ax, "The Critical Test: Recovery During the IM Window",
           "G6+G7 Math: 296-peer ranking of IM-window recovery — Troy in the bottom third")
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
           "G6+G7 Math: Novi leads with 1.6x more recovery; Troy trails the median")
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
        ("Novi",             "+0.123", "",          False),
        ("Birmingham",       "+0.095", "(tracked)", False),
        ("Northville",       "+0.082", "(tracked)", False),
        ("Rochester",        "+0.080", "",          False),
        ("Bloomfield Hills", "+0.079", "(tracked)", False),
        ("Troy",             "+0.076", "(IM+detracked)", True),
        ("West Bloomfield",  "+0.039", "",          False),
        ("Walled Lake",      "+0.016", "",          False),
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
           "2023–24 G7 tracked (+0.018). 2024–25 first G7 IM cohort (+0.061)")
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
         "Troy gained +0.018 —\n7th of 8 MI peers.",
         fontsize=14, color=GRAY_DARK)

    # Bottom panel -- LIGHT_GREEN (recovery accelerated)
    bot_y = 0.05
    rect(ax, px, bot_y, pw, panel_h, LIGHT_GREEN)
    accent_bar(ax, px, bot_y + panel_h, pw, ACCENT_GREEN, 0.005)
    text(ax, px + 0.02, bot_y + panel_h - 0.04,
         "2024–25: IM + Detracked",
         fontsize=16, weight="bold", color=ACCENT_GREEN)
    text(ax, px + 0.02, bot_y + panel_h - 0.14,
         "First G7 IM cohort.\n\n"
         "Troy gained +0.061 —\n2nd of 8 MI peers.\nRecovery accelerated.",
         fontsize=14, color=GRAY_DARK)

    save_slide(fig, 10)


def slide_11():
    """Asian Subgroup: G6 Leads Recovery, G7 Lags."""
    fig, ax = new_slide()
    header(ax, "Asian Subgroup: G6 Leads Recovery, G7 Lags",
           "36% of Troy — strongest G6 IM-window recovery of any subgroup")
    footer_bar(ax, 11)

    embed_chart(fig, chart_path("chart05_asian_g6_trend.png"),
                0.01, 0.05, 0.64, 0.87)

    # Right panel with three stat cards
    px, pw = 0.66, 0.33
    py, ph = 0.05, 0.87
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    cards = [
        ("G6 Asian IM Δ:", "+0.312", "Strongest recovery of any\nTroy subgroup. #2 among\nMI peers in G6 Asian.",
         ACCENT_GREEN, LIGHT_GREEN),
        ("G7 Asian IM Δ:", "−0.028", "Only subgroup still\ndeclining. G7 had just\none year of IM.",
         ACCENT_RED, LIGHT_RED),
        ("Gap from pre-COVID:", "−0.340", "G7 Asian still far below\n2017–19 baseline despite\nG6 recovery.",
         ACCENT_ORANGE, LIGHT_ORANGE),
    ]
    card_h = 0.27
    gap = 0.02
    y_top = py + ph - 0.04
    for i, (label, value, desc, clr, bg) in enumerate(cards):
        cy = y_top - i * (card_h + gap)
        rect(ax, px + 0.01, cy - card_h + 0.05, pw - 0.02, card_h - 0.02, bg)
        accent_bar(ax, px + 0.01, cy + 0.03, pw - 0.02, clr, 0.004)
        text(ax, px + 0.02, cy, label,
             fontsize=11, color=GRAY_MID)
        text(ax, px + 0.02, cy - 0.07, value,
             fontsize=26, weight="bold", color=clr)
        text(ax, px + 0.02, cy - 0.15, desc,
             fontsize=10, color=GRAY_DARK)

    save_slide(fig, 11)


def slide_12():
    """G7 Asian Math Is Still Declining Under IM."""
    fig, ax = new_slide()
    header(ax, "G7 Asian: First IM Year Shows Slight Decline",
           "High-Asian peers with tracking outpace Troy's G7 Asian (2023 → 2025)")
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
        ("Issaquah (WA)", "30% Asian, tracked", "+0.384", LIGHT_GREEN, ACCENT_GREEN),
        ("Bellevue (WA)", "41% Asian, tracked", "+0.192", LIGHT_GREEN, ACCENT_GREEN),
        ("Troy (MI)",     "36% Asian, IM+detracked", "−0.028", LIGHT_RED, ACCENT_RED),
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
    header(ax, "IM-Window Recovery by Subgroup (2023-2025)",
           "G6+G7 Math: Asian leads combined recovery; White lags peers")
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
         "Every subgroup recovered\n"
         "except G7 Asian (−0.028).\n\n"
         "Asian G6 leads recovery\n"
         "(+0.312), strongest of any\n"
         "Troy subgroup.\n\n"
         "White subgroup barely\n"
         "improved (+0.023 combined),\n"
         "7th of 8 MI peers in G6.\n\n"
         "ECD recovery is mixed:\n"
         "G6 flat (−0.007), G7\n"
         "strong (+0.149, 3rd of 8).\n\n"
         "All subgroups remain below\n"
         "pre-COVID levels.",
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
    """The '50% Algebra 1' Claim."""
    fig, ax = new_slide()
    header(ax, "The ‘50% Algebra 1’ Claim",
           "G6+G7 Math: course enrollment is not an achievement metric")
    footer_bar(ax, 15)

    findings = [
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "Enrollment is not achievement",
         "More students enrolled in Algebra 1 does not mean more students "
         "have mastered prerequisite skills. Course access and course "
         "readiness are different metrics."),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "SEDA scores tell a different story",
         "G6+G7 math rose +0.076 in the IM window (2023-2025) but remains "
         "far below pre-COVID +0.937. Recovery is real but slow. "
         "More students in Algebra 1 does not mean more are ready for it."),
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

    save_slide(fig, 15)


def slide_16():
    """What High-Performing Districts Do Differently."""
    fig, ax = new_slide()
    header(ax, "What High-Performing Districts Do Differently",
           "G6+G7 Math: among 107 high-Asian (>=20%) peers, many recovered with tracking intact")
    footer_bar(ax, 16)

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

    save_slide(fig, 16)


def slide_17():
    """Conclusions."""
    fig, ax = new_slide()
    header(ax, "Conclusions",
           "G6+G7 Math: four findings from SEDA and M-STEP data")
    footer_bar(ax, 17)

    conclusions = [
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "Troy has NOT outperformed its characteristics",
         "Bottom third of 295 level-matched peers in IM-window recovery. "
         "6th of 8 MI peers. Rank 197 of 295 nationally."),
        (ACCENT_RED, LIGHT_RED,
         "G7 Asian is the most concerning subgroup",
         "G7 Asian is the only subgroup still declining (-0.028) in the "
         "IM window. High-Asian peers with tracking recover strongly."),
        (ACCENT_GREEN, LIGHT_GREEN,
         "G6 Asian shows strong IM-window recovery",
         "G6 Asian gained +0.312 — strongest of any Troy subgroup and "
         "#2 among MI peers. G6 is a bright spot."),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "Recovery is real but slow — gap remains",
         "Troy is recovering (+0.076), but not closing the deficit "
         "COVID opened. All subgroups still below pre-COVID levels."),
    ]
    row_h = 0.19
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

    save_slide(fig, 17)


def slide_18():
    """Methodology."""
    fig, ax = new_slide()
    header(ax, "Methodology",
           "G6+G7 Math — SEDA 2025.1 (Stanford CEPA)")
    footer_bar(ax, 18)

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
         "IM Window: 2023 → 2025 (last pre-IM test to latest data)"),
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

    save_slide(fig, 18)


def slide_19():
    """References."""
    fig, ax = new_slide()
    header(ax, "References",
           "Primary data sources")
    footer_bar(ax, 19)

    refs = [
        ("SEDA 2025.1",
         "Stanford Center for Education Policy Analysis. "
         "edopportunity.org. Reardon et al."),
        ("Education Scorecard 2026",
         "Harvard-Stanford-Dartmouth. Demographic-adjusted "
         "gain methodology."),
        ("MI School Data / M-STEP",
         "Michigan Department of Education. mischooldata.org. "
         "State assessment proficiency rates."),
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

    save_slide(fig, 19)


def slide_20():
    """Appendix -- SEDA National Ranking (matches K-5 ELA slide 24 layout)."""
    fig, ax = new_slide()
    header(ax, "Appendix -- Troy Slid from Top 2% to Top 4% Nationally in G6+G7 Math",
           "Year-by-year SEDA national ranking (all U.S. districts) + absolute level among 296 level-matched peers")
    footer_bar(ax, 20)

    # ── LEFT PANEL: national ranking table ──
    lp_x, lp_w = 0.02, 0.39
    lp_y, lp_h = 0.08, 0.57
    rect(ax, lp_x, lp_y, lp_w, lp_h, LIGHT_RED)
    accent_bar(ax, lp_x, lp_y + lp_h, lp_w, ACCENT_RED, 0.004)

    text(ax, lp_x + 0.015, lp_y + lp_h - 0.035,
         "National G6+G7 Math ranking trajectory",
         fontsize=12, weight="bold", color=ACCENT_RED)
    text(ax, lp_x + 0.015, lp_y + lp_h - 0.065,
         "SEDA 2025.1 cs scale -- all U.S. districts with G6+G7 math data",
         fontsize=7.5, color=GRAY_MID, style="italic")

    # Table header
    hdr_y = lp_y + lp_h - 0.10
    cols = [lp_x + 0.015, lp_x + 0.07, lp_x + 0.15, lp_x + 0.27]
    rect(ax, lp_x + 0.01, hdr_y - 0.035, lp_w - 0.02, 0.035, ACCENT_RED)
    for cx, hdr in zip(cols, ["Year", "Score", "Rank", "Percentile"]):
        text(ax, cx, hdr_y - 0.005, hdr,
             fontsize=8, weight="bold", color="white")

    rows = [
        ("2019", "+0.952", "173 / 8,751", "Top 2.0%", False),
        ("2022", "+0.763", "229 / 8,215", "Top 2.8%", False),
        ("2023", "+0.713", "269 / 7,190", "Top 3.7%", True),
        ("2024", "+0.734", "294 / 6,995", "Top 4.2%", True),
        ("2025", "+0.790", "240 / 5,896", "Top 4.1%", True),
    ]
    for i, (yr, score, rank, pct, warn) in enumerate(rows):
        ry = hdr_y - 0.07 - i * 0.045
        clr = ACCENT_RED if warn else GRAY_DARK
        if i == 0:
            rect(ax, lp_x + 0.01, ry - 0.015, lp_w - 0.02, 0.045, LIGHT_GREEN)
        text(ax, cols[0], ry, yr, fontsize=9, weight="bold", color=clr)
        text(ax, cols[1], ry, score, fontsize=9, color=clr, family="monospace")
        text(ax, cols[2], ry, rank, fontsize=8, color=clr, family="monospace")
        pct_clr = ACCENT_GREEN if i == 0 else (ACCENT_RED if warn else GRAY_DARK)
        text(ax, cols[3], ry, pct, fontsize=9, weight="bold", color=pct_clr)

    # Callout below table
    text(ax, lp_x + 0.015, lp_y + lp_h - 0.44,
         "Dropped ~70 national places since 2019",
         fontsize=11, weight="bold", color=ACCENT_RED)
    text(ax, lp_x + 0.015, lp_y + lp_h - 0.50,
         "Troy went from top 2% nationally to top 4%.\n"
         "Score declined -0.162 grade levels.\n"
         "2025 rank ticks up as score partially recovered.",
         fontsize=9, color=GRAY_DARK)

    # ── RIGHT PANEL: scatter plot ──
    embed_chart(fig, chart_path("chart_seda_scatter_math.png"),
                0.42, 0.08, 0.57, 0.57)

    # ── BOTTOM STRIP: peer + MI context ──
    bot_y, bot_h = 0.045, 0.18
    rect(ax, 0.02, bot_y - 0.005, 0.96, bot_h, GRAY_LIGHT)

    # Left: 296-peer context
    text(ax, 0.035, bot_y + bot_h - 0.025,
         "Among 296 level-matched peers",
         fontsize=9, weight="bold", color=TROY_BLUE)
    text(ax, 0.035, bot_y + bot_h - 0.07,
         "Pre-COVID rank:  76 / 296  (top quarter)\n"
         "Post-COVID rank: 135 / 296  (bottom 55%)\n"
         "70 districts leapfrogged Troy",
         fontsize=8, color=GRAY_DARK, family="monospace")

    # Right: MI peers
    text(ax, 0.44, bot_y + bot_h - 0.025,
         "Michigan affluent peers -- score delta (2019 to 2025)",
         fontsize=9, weight="bold", color=TROY_BLUE)

    mi_peers = [
        ("Birmingham",      "+0.131", ACCENT_GREEN),
        ("Northville",      "+0.087", ACCENT_GREEN),
        ("Bloomfield Hills", "+0.085", ACCENT_GREEN),
        ("Troy SD",         "-0.162", ACCENT_RED),
        ("Novi",            "-0.167", ACCENT_RED),
        ("W. Bloomfield",   "-0.181", ACCENT_RED),
        ("Rochester",       "-0.188", ACCENT_RED),
        ("Walled Lake",     "-0.197", ACCENT_RED),
    ]
    for i, (dist, delta, clr) in enumerate(mi_peers):
        mx = 0.44 + (i % 4) * 0.14
        my = bot_y + bot_h - 0.07 - (i // 4) * 0.05
        text(ax, mx, my, dist, fontsize=7, color=GRAY_DARK)
        text(ax, mx + 0.09, my, delta, fontsize=7.5, weight="bold", color=clr)

    save_slide(fig, 20)


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

    print(f"Done -- {TOTAL} slides saved.")


if __name__ == "__main__":
    main()
