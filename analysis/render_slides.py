#!/usr/bin/env python3
"""
render_slides.py — Generate 20 publication-quality PNG slides (1920x1080)
for the Troy School District G6-G7 Math Analysis deck.
"""

import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHARTS_DIR = os.path.join(ROOT, "charts")
SLIDES_DIR = os.path.join(ROOT, "slides")
os.makedirs(SLIDES_DIR, exist_ok=True)

# ── Color Palette ────────────────────────────────────────────────────────────
TROY_BLUE    = "#1F3A5F"
ACCENT_RED   = "#C8302F"
ACCENT_GREEN = "#1F7A3D"
ACCENT_ORANGE= "#B7791F"
LIGHT_GREEN  = "#E8F5EE"
LIGHT_ORANGE = "#FFF4E0"
LIGHT_RED    = "#FBE7E6"
GRAY_LIGHT   = "#F2F4F7"
GRAY_DARK    = "#333333"
GRAY_MID     = "#777777"
WHITE        = "#FFFFFF"

DPI = 192
FIG_W, FIG_H = 10, 5.625  # 1920x1080 at 192 DPI


# ── Helper Functions ─────────────────────────────────────────────────────────

def new_slide(facecolor=WHITE):
    """Create a 1920x1080 figure with a single axis filling it."""
    fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor=facecolor)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_facecolor(facecolor)
    return fig, ax


def title_bar(ax, title):
    """Draw a TROY_BLUE rectangle at the top with white bold title."""
    rect_patch = mpatches.FancyBboxPatch(
        (0, 0.93), 1.0, 0.07, boxstyle="square,pad=0",
        facecolor=TROY_BLUE, edgecolor="none", transform=ax.transAxes,
    )
    ax.add_patch(rect_patch)
    ax.text(0.04, 0.965, title, fontsize=16, color=WHITE,
            fontweight="bold", ha="left", va="center", transform=ax.transAxes)


def footer(ax, n, total=22):
    """Small gray slide-number text at bottom-right."""
    ax.text(0.96, 0.015, f"{n} / {total}", fontsize=8, color=GRAY_MID,
            ha="right", va="bottom", transform=ax.transAxes)


def rect(ax, x, y, w, h, color, alpha=1):
    """Draw a colored rectangle at normalized coordinates."""
    r = mpatches.FancyBboxPatch(
        (x, y), w, h, boxstyle="square,pad=0",
        facecolor=color, edgecolor="none", alpha=alpha,
        transform=ax.transAxes,
    )
    ax.add_patch(r)
    return r


def text(ax, x, y, txt, fontsize=14, color=GRAY_DARK, ha="left", va="top",
         weight="normal", wrap_width=None, family="sans-serif",
         style="normal"):
    """Place text on the axis. If wrap_width is set, wrap with textwrap.fill."""
    if wrap_width:
        txt = textwrap.fill(txt, width=wrap_width)
    return ax.text(x, y, txt, fontsize=fontsize, color=color, ha=ha, va=va,
                   fontweight=weight, transform=ax.transAxes, family=family,
                   fontstyle=style)


def embed_chart(fig, path, x, y, w, h):
    """Embed a chart PNG into the figure using add_axes + imshow."""
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


# ── Slide Builders ───────────────────────────────────────────────────────────

def slide_01():
    """Title slide — full TROY_BLUE background."""
    fig, ax = new_slide(facecolor=TROY_BLUE)
    text(ax, 0.50, 0.62, "Troy School District G6–G7 Math Analysis",
         fontsize=26, color=WHITE, ha="center", va="center", weight="bold")
    text(ax, 0.50, 0.50, "Has Illustrative Mathematics + Detracking",
         fontsize=18, color=WHITE, ha="center", va="center")
    text(ax, 0.50, 0.43, "Outperformed Its Characteristics?",
         fontsize=18, color=WHITE, ha="center", va="center")
    text(ax, 0.50, 0.30, "May 2026  |  SEDA 2025.1 + M-STEP Data",
         fontsize=12, color="#A0B4CC", ha="center", va="center")
    save_slide(fig, 1)


def slide_02():
    """The Question — and the One-Line Answer."""
    fig, ax = new_slide()
    title_bar(ax, "The Question — and the One-Line Answer")

    # Three columns
    col_w = 0.28
    gap = 0.025
    y_top = 0.88
    col_h = 0.72
    x_starts = [0.04, 0.04 + col_w + gap, 0.04 + 2 * (col_w + gap)]

    # Left column — white bg with light border
    rect(ax, x_starts[0], y_top - col_h, col_w, col_h, WHITE)
    # draw a thin border
    border = mpatches.FancyBboxPatch(
        (x_starts[0], y_top - col_h), col_w, col_h,
        boxstyle="square,pad=0", facecolor="none",
        edgecolor=GRAY_MID, linewidth=0.5, transform=ax.transAxes)
    ax.add_patch(border)
    text(ax, x_starts[0] + 0.015, y_top - 0.02, "Question",
         fontsize=13, weight="bold", color=TROY_BLUE)
    text(ax, x_starts[0] + 0.015, y_top - 0.08,
         "Has Troy’s Fall 2023 adoption of Illustrative Mathematics "
         "and detracking of G6+G7 math produced results that outperform "
         "its characteristics?",
         fontsize=10, color=GRAY_DARK, wrap_width=32)

    # Center column — LIGHT_RED
    rect(ax, x_starts[1], y_top - col_h, col_w, col_h, LIGHT_RED)
    text(ax, x_starts[1] + 0.015, y_top - 0.02, "Answer",
         fontsize=13, weight="bold", color=ACCENT_RED)
    text(ax, x_starts[1] + 0.015, y_top - 0.08,
         "No. Troy ranks 197 of 295 level-matched peers (bottom third) "
         "in math recovery during the exact IM adoption window.",
         fontsize=10, color=GRAY_DARK, wrap_width=32)

    # Right column — GRAY_LIGHT
    rect(ax, x_starts[2], y_top - col_h, col_w, col_h, GRAY_LIGHT)
    text(ax, x_starts[2] + 0.015, y_top - 0.02, "Key Numbers",
         fontsize=13, weight="bold", color=TROY_BLUE)
    stats = [
        ("+0.024", "Troy’s IM-window recovery"),
        ("+0.058", "Median peer recovery"),
        ("+0.211", "Birmingham (tracked, same county)"),
    ]
    sy = y_top - 0.10
    for val, label in stats:
        text(ax, x_starts[2] + 0.015, sy, val,
             fontsize=13, weight="bold", color=ACCENT_RED)
        text(ax, x_starts[2] + 0.015, sy - 0.05, f"— {label}",
             fontsize=9, color=GRAY_MID)
        sy -= 0.14

    footer(ax, 2)
    save_slide(fig, 2)


def slide_03():
    """What Troy Did and When — timeline."""
    fig, ax = new_slide()
    title_bar(ax, "What Troy Did and When")

    events = [
        ("Fall 2023", "Adopted Illustrative Mathematics,\ndetracked G6 and G7 math"),
        ("Spring 2024", "First IM cohort tested\n(G6 M-STEP)"),
        ("Fall 2024", "Second IM year; first G7 IM\ncohort enters 7th grade"),
        ("Spring 2025", "Second IM G6 + first IM\nG7 tested"),
    ]
    n_events = len(events)
    x_margin = 0.10
    x_span = 1 - 2 * x_margin
    y_line = 0.55

    # horizontal line
    ax.plot([x_margin, x_margin + x_span], [y_line, y_line],
            color=GRAY_MID, linewidth=1.5, transform=ax.transAxes,
            solid_capstyle="round")

    for i, (date, desc) in enumerate(events):
        x = x_margin + i * x_span / (n_events - 1)
        # dot
        ax.plot(x, y_line, "o", color=TROY_BLUE, markersize=10,
                transform=ax.transAxes, zorder=5)
        # date above
        text(ax, x, y_line + 0.08, date, fontsize=11, weight="bold",
             color=TROY_BLUE, ha="center", va="center")
        # description below
        text(ax, x, y_line - 0.07, desc, fontsize=9, color=GRAY_DARK,
             ha="center", va="top")

    # Bottom note
    text(ax, 0.50, 0.14,
         "Prior: 7th graders had Big Ideas Math 7, Math 7/8 Honors, "
         "small Algebra 1 cohort",
         fontsize=9, color=GRAY_MID, ha="center", va="center",
         style="italic")

    footer(ax, 3)
    save_slide(fig, 3)


def slide_04():
    """Troy's Pre-COVID Math Position — Strong, Not Invincible."""
    fig, ax = new_slide()
    title_bar(ax, "Troy’s Pre-COVID Math Position — Strong, Not Invincible")

    # Chart on left
    embed_chart(fig, chart_path("chart01_mi_peers_g6_trend.png"),
                0.03, 0.08, 0.58, 0.82)

    # Stats panel on right
    px, pw = 0.65, 0.32
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, LIGHT_GREEN)

    text(ax, px + 0.02, py + ph - 0.03, "Pre-COVID G6+G7 math:",
         fontsize=11, color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.12, "+0.937",
         fontsize=28, weight="bold", color=TROY_BLUE)
    text(ax, px + 0.02, py + ph - 0.26, "grade levels above\nnational norm",
         fontsize=11, color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.45,
         "3rd highest among\nMI affluent peers",
         fontsize=11, color=GRAY_DARK, weight="bold")
    text(ax, px + 0.02, py + ph - 0.60, "37% above national average",
         fontsize=11, color=GRAY_DARK)

    footer(ax, 4)
    save_slide(fig, 4)


def slide_05():
    """The Post-COVID Decline Hit Troy Hard in Math."""
    fig, ax = new_slide()
    title_bar(ax, "The Post-COVID Decline Hit Troy Hard in Math")

    embed_chart(fig, chart_path("chart09_covid_delta_ranking.png"),
                0.03, 0.08, 0.58, 0.82)

    px, pw = 0.65, 0.32
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, LIGHT_RED)

    text(ax, px + 0.02, py + ph - 0.08, "–0.187",
         fontsize=28, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.22, "grade-level decline",
         fontsize=11, color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.40, "Rank 104 of 296",
         fontsize=13, weight="bold", color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.50, "level-matched peers",
         fontsize=11, color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.58, "(35th percentile)",
         fontsize=11, color=GRAY_MID)

    footer(ax, 7)
    save_slide(fig, 5)


def slide_06():
    """The Critical Test: Recovery During the IM Window."""
    fig, ax = new_slide()
    title_bar(ax, "The Critical Test: Recovery During the IM Window (2022–23 → 2024–25)")

    embed_chart(fig, chart_path("chart04_level_matched_histogram.png"),
                0.03, 0.08, 0.62, 0.82)

    px, pw = 0.68, 0.29
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    text(ax, px + 0.02, py + ph - 0.08, "Rank 197 / 295",
         fontsize=20, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.22, "bottom third",
         fontsize=13, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.40, "Most peers recovered",
         fontsize=11, color=GRAY_DARK)
    text(ax, px + 0.02, py + ph - 0.50, "2–3× more than Troy",
         fontsize=11, color=GRAY_DARK)

    footer(ax, 8)
    save_slide(fig, 6)


def slide_07():
    """Among MI Peers, Troy Ranks 6th of 8 in Recovery."""
    fig, ax = new_slide()
    title_bar(ax, "Among MI Peers, Troy Ranks 6th of 8 in Recovery")

    embed_chart(fig, chart_path("chart03_im_window_ranking.png"),
                0.03, 0.08, 0.52, 0.82)

    # Table-style listing on the right
    px, pw = 0.57, 0.40
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    rows = [
        ("Birmingham",       "+0.211", "(tracked)",               GRAY_DARK, "normal"),
        ("Northville",       "+0.102", "(tracked)",               GRAY_DARK, "normal"),
        ("Bloomfield Hills", "+0.082", "(tracked)",               GRAY_DARK, "normal"),
        ("Walled Lake",      "+0.056", "",                        GRAY_DARK, "normal"),
        ("Novi",             "+0.029", "",                        GRAY_DARK, "normal"),
        ("Troy",             "+0.024", "(IM + detracked)",        ACCENT_RED, "bold"),
        ("Rochester",        "+0.000", "",                        GRAY_DARK, "normal"),
        ("West Bloomfield",  "+0.006", "",                        GRAY_DARK, "normal"),
    ]
    y_start = py + ph - 0.05
    row_h = 0.085
    for i, (name, val, note, clr, wt) in enumerate(rows):
        ry = y_start - i * row_h
        # Highlight Troy row
        if name == "Troy":
            rect(ax, px + 0.005, ry - 0.03, pw - 0.01, row_h - 0.01, LIGHT_RED)
        text(ax, px + 0.02, ry, name, fontsize=10, color=clr, weight=wt)
        text(ax, px + 0.22, ry, val, fontsize=10, color=clr, weight=wt,
             family="monospace")
        if note:
            text(ax, px + 0.30, ry, note, fontsize=8, color=GRAY_MID)

    footer(ax, 9)
    save_slide(fig, 7)


def slide_08():
    """G7 Math: The Tracked-vs-IM Comparison Year."""
    fig, ax = new_slide()
    title_bar(ax, "G7 Math: The Tracked-vs-IM Comparison Year")

    embed_chart(fig, chart_path("chart02_mi_peers_g7_trend.png"),
                0.03, 0.08, 0.62, 0.82)

    px, pw = 0.68, 0.29
    py = 0.10
    panel_h = 0.34

    # Top panel — green
    rect(ax, px, py + panel_h + 0.10, pw, panel_h, LIGHT_GREEN)
    text(ax, px + 0.02, py + 2 * panel_h + 0.10 - 0.04,
         "2023–24: G7 still tracked\n— Troy matched peers",
         fontsize=10, color=ACCENT_GREEN, weight="bold")

    # Bottom panel — red
    rect(ax, px, py, pw, panel_h, LIGHT_RED)
    text(ax, px + 0.02, py + panel_h - 0.04,
         "2024–25: First G7 IM cohort\n— recovery stalled",
         fontsize=10, color=ACCENT_RED, weight="bold")

    footer(ax, 10)
    save_slide(fig, 8)


def slide_09():
    """The Asian Subgroup Crisis — 36% of Troy's Enrollment."""
    fig, ax = new_slide()
    title_bar(ax, "The Asian Subgroup Crisis — 36% of Troy’s Enrollment")

    embed_chart(fig, chart_path("chart05_asian_g6_trend.png"),
                0.03, 0.08, 0.62, 0.82)

    px, pw = 0.68, 0.29
    cards = [
        ("G6 Asian Δ COVID:", "–0.409"),
        ("G7 Asian Δ COVID:", "–0.278"),
        ("G7 Asian IM-window:", "–0.094 (still declining)"),
    ]
    card_h = 0.20
    gap = 0.06
    y_start = 0.68
    for i, (label, value) in enumerate(cards):
        cy = y_start - i * (card_h + gap)
        rect(ax, px, cy, pw, card_h, LIGHT_RED)
        text(ax, px + 0.02, cy + card_h - 0.04, label,
             fontsize=10, color=GRAY_DARK)
        text(ax, px + 0.02, cy + card_h - 0.11, value,
             fontsize=14, weight="bold", color=ACCENT_RED)

    footer(ax, 11)
    save_slide(fig, 9)


def slide_10():
    """G7 Asian Math Is Still Declining Under IM."""
    fig, ax = new_slide()
    title_bar(ax, "G7 Asian Math Is Still Declining Under IM")

    embed_chart(fig, chart_path("chart06_asian_g7_trend.png"),
                0.03, 0.08, 0.62, 0.82)

    px, pw = 0.68, 0.29
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    comparisons = [
        ("Bellevue (WA, 41% Asian)", "G7 Asian IM-Δ: +0.162", ACCENT_GREEN),
        ("Issaquah (WA, 30% Asian)", "+0.218", ACCENT_GREEN),
        ("Troy (MI, 36% Asian)", "–0.094", ACCENT_RED),
    ]
    sy = py + ph - 0.06
    for district, val, clr in comparisons:
        text(ax, px + 0.02, sy, district, fontsize=10, weight="bold",
             color=GRAY_DARK)
        text(ax, px + 0.02, sy - 0.07, val, fontsize=13, weight="bold",
             color=clr)
        sy -= 0.24

    footer(ax, 12)
    save_slide(fig, 10)


def slide_11():
    """Every Subgroup Declined — But Recovery Is Uneven."""
    fig, ax = new_slide()
    title_bar(ax, "Every Subgroup Declined — But Recovery Is Uneven")

    embed_chart(fig, chart_path("chart07_troy_subgroup_waterfall.png"),
                0.03, 0.08, 0.62, 0.82)

    px, pw = 0.68, 0.29
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, LIGHT_ORANGE)

    text(ax, px + 0.02, py + ph - 0.06,
         "Asian and White subgroups show largest absolute declines.\n\n"
         "ECD subgroup was already near national average.",
         fontsize=10, color=GRAY_DARK, wrap_width=34)

    footer(ax, 13)
    save_slide(fig, 11)


def slide_12():
    """M-STEP Math Proficiency: The Numbers Parents See."""
    fig, ax = new_slide()
    title_bar(ax, "M-STEP Math Proficiency: The Numbers Parents See")

    embed_chart(fig, chart_path("chart08_mstep_troy_proficiency.png"),
                0.03, 0.08, 0.62, 0.82)

    px, pw = 0.68, 0.29
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    text(ax, px + 0.02, py + ph - 0.05, "Data Summary",
         fontsize=12, weight="bold", color=TROY_BLUE)
    text(ax, px + 0.02, py + ph - 0.14,
         "G6: 71.4% → 63.2% →\n      66.3% → 65.8%",
         fontsize=10, color=GRAY_DARK, family="monospace")
    text(ax, px + 0.02, py + ph - 0.30,
         "G7: 67.5% → 61.3% →\n      66.0% → TBD",
         fontsize=10, color=GRAY_DARK, family="monospace")
    text(ax, px + 0.02, py + ph - 0.52,
         "IM has not restored Troy\nto pre-COVID proficiency\nlevels",
         fontsize=11, weight="bold", color=ACCENT_RED)

    footer(ax, 14)
    save_slide(fig, 12)


def slide_13():
    """San Francisco: 12 Years of Detracking, Then Reversal."""
    fig, ax = new_slide()
    title_bar(ax, "San Francisco: 12 Years of Detracking, Then Reversal")

    findings = [
        (ACCENT_RED, LIGHT_RED,
         "Achievement gaps WIDENED: Hispanic-White gap expanded "
         "31 points (vs 5 statewide)"),
        (ACCENT_ORANGE, LIGHT_ORANGE,
         "AP math enrollment DECLINED 15%, driven by "
         "Asian/Pacific Islander students"),
        (ACCENT_RED, LIGHT_RED,
         "Board voted March 2026 to RESTORE Algebra 1 in "
         "8th grade at all schools"),
    ]
    y_top = 0.82
    panel_h = 0.18
    gap = 0.04
    for i, (border_clr, bg_clr, finding_text) in enumerate(findings):
        py = y_top - i * (panel_h + gap)
        rect(ax, 0.06, py, 0.88, panel_h, bg_clr)
        # Left color border
        rect(ax, 0.06, py, 0.012, panel_h, border_clr)
        # Number
        text(ax, 0.09, py + panel_h / 2 + 0.01, str(i + 1),
             fontsize=16, weight="bold", color=border_clr,
             ha="center", va="center")
        # Text
        text(ax, 0.12, py + panel_h / 2 + 0.01, finding_text,
             fontsize=11, color=GRAY_DARK, va="center", wrap_width=75)

    # Bottom bar
    rect(ax, 0.06, 0.08, 0.88, 0.06, TROY_BLUE)
    text(ax, 0.50, 0.11,
         "Troy is replicating a strategy with a well-documented failure pattern",
         fontsize=11, color=WHITE, ha="center", va="center", weight="bold")

    footer(ax, 15)
    save_slide(fig, 13)


def slide_14():
    """Cambridge, MA: Detracked 2017-2019, Now Reversing."""
    fig, ax = new_slide()
    title_bar(ax, "Cambridge, MA: Detracked 2017–2019, Now Reversing")

    col_w = 0.42
    gap = 0.04
    py, ph = 0.12, 0.74
    x1 = 0.06
    x2 = x1 + col_w + gap

    # Left panel
    rect(ax, x1, py, col_w, ph, LIGHT_ORANGE)
    text(ax, x1 + 0.02, py + ph - 0.04, "What They Did",
         fontsize=13, weight="bold", color=ACCENT_ORANGE)
    text(ax, x1 + 0.02, py + ph - 0.14,
         "Eliminated accelerated math tracks to address racial "
         "disparities in advanced course enrollment",
         fontsize=11, color=GRAY_DARK, wrap_width=40)

    # Right panel
    rect(ax, x2, py, col_w, ph, LIGHT_RED)
    text(ax, x2 + 0.02, py + ph - 0.04, "What Happened",
         fontsize=13, weight="bold", color=ACCENT_RED)
    text(ax, x2 + 0.02, py + ph - 0.14,
         "COVID obscured early results. District now reversing course, "
         "restoring algebra to 8th grade, citing persistent achievement gaps.",
         fontsize=11, color=GRAY_DARK, wrap_width=40)

    footer(ax, 16)
    save_slide(fig, 14)


def slide_15():
    """The '50% Algebra 1' Claim — Course Access != Achievement."""
    fig, ax = new_slide()
    title_bar(ax, "The ‘50% Algebra 1’ Claim — Course Access ≠ Achievement")

    findings = [
        "SFUSD made the identical claim for a decade before test scores "
        "revealed no improvement",
        "SEDA shows Troy’s G6+G7 math readiness dropped from +0.937 to "
        "+0.750 — a quarter-grade-level decline",
        "The comparison is not past Troy enrollment — it’s what "
        "tracked peers achieve now",
    ]
    y_top = 0.80
    panel_h = 0.17
    gap = 0.04
    for i, finding_text in enumerate(findings):
        py = y_top - i * (panel_h + gap)
        rect(ax, 0.06, py, 0.88, panel_h, LIGHT_ORANGE)
        # Number circle
        circle = mpatches.Circle((0.09, py + panel_h / 2), 0.018,
                                  facecolor=ACCENT_ORANGE, edgecolor="none",
                                  transform=ax.transAxes)
        ax.add_patch(circle)
        text(ax, 0.09, py + panel_h / 2 + 0.005, str(i + 1),
             fontsize=11, weight="bold", color=WHITE, ha="center", va="center")
        # Text
        text(ax, 0.13, py + panel_h / 2 + 0.005, finding_text,
             fontsize=10.5, color=GRAY_DARK, va="center", wrap_width=72)

    footer(ax, 17)
    save_slide(fig, 15)


def slide_16():
    """What High-Performing Math Districts Do Differently."""
    fig, ax = new_slide()
    title_bar(ax, "What High-Performing Math Districts Do Differently")

    embed_chart(fig, chart_path("chart10_high_asian_peers_delta.png"),
                0.03, 0.08, 0.62, 0.82)

    px, pw = 0.68, 0.29
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, LIGHT_GREEN)

    text(ax, px + 0.02, py + ph - 0.06,
         "Among 107 high-Asian (≥20%) districts, many California "
         "and NJ districts recovered to or surpassed pre-COVID levels "
         "— with tracking intact.",
         fontsize=10.5, color=GRAY_DARK, wrap_width=32)

    footer(ax, 18)
    save_slide(fig, 16)


def slide_17():
    """Illustrative Mathematics: Evidence Gaps."""
    fig, ax = new_slide()
    title_bar(ax, "Illustrative Mathematics: Evidence Gaps")

    # Table header
    th_y, th_h = 0.82, 0.05
    rect(ax, 0.06, th_y, 0.88, th_h, TROY_BLUE)
    text(ax, 0.10, th_y + th_h / 2, "District",
         fontsize=11, weight="bold", color=WHITE, va="center")
    text(ax, 0.42, th_y + th_h / 2, "Result",
         fontsize=11, weight="bold", color=WHITE, va="center")
    text(ax, 0.70, th_y + th_h / 2, "Note",
         fontsize=11, weight="bold", color=WHITE, va="center")

    rows = [
        ("NYC District 11\n(Bronx)", "25.8% → 50.6%",
         "High-poverty, low-baseline,\nnot comparable"),
        ("Fort Zumwalt (MO)", "Effect size 0.16 SD",
         "Modest, comparable to\ngeneral improvement"),
        ("Philadelphia", "Process study only",
         "No outcomes data"),
    ]
    row_h = 0.16
    for i, (district, result, note) in enumerate(rows):
        ry = th_y - (i + 1) * row_h
        bg = GRAY_LIGHT if i % 2 == 0 else WHITE
        rect(ax, 0.06, ry, 0.88, row_h, bg)
        text(ax, 0.10, ry + row_h / 2, district,
             fontsize=10, color=GRAY_DARK, va="center")
        text(ax, 0.42, ry + row_h / 2, result,
             fontsize=10, color=GRAY_DARK, va="center")
        text(ax, 0.70, ry + row_h / 2, note,
             fontsize=9, color=GRAY_MID, va="center")

    # Bottom note
    rect(ax, 0.06, 0.14, 0.88, 0.08, LIGHT_ORANGE)
    text(ax, 0.50, 0.18,
         "No published evidence of IM success in an affluent, "
         "high-performing, high-Asian district like Troy",
         fontsize=10.5, weight="bold", color=ACCENT_ORANGE,
         ha="center", va="center", wrap_width=80)

    footer(ax, 19)
    save_slide(fig, 17)


def slide_18():
    """Conclusions."""
    fig, ax = new_slide()
    title_bar(ax, "Conclusions")

    conclusions = [
        (ACCENT_RED,    "Troy has NOT outperformed its characteristics "
                        "— bottom third of 295 peers"),
        (ACCENT_RED,    "Asian subgroup is most concerning "
                        "— G7 Asian STILL declining"),
        (ACCENT_ORANGE, "Detracking evidence base is against this approach "
                        "— SFUSD, Cambridge reversed"),
        (ACCENT_ORANGE, "Course enrollment ≠ achievement "
                        "— 50% Algebra 1 claim misleads"),
        (ACCENT_RED,    "Opportunity cost is real: Birmingham recovered "
                        "9× more in the same window"),
    ]
    y_top = 0.82
    row_h = 0.13
    for i, (clr, finding) in enumerate(conclusions):
        cy = y_top - i * row_h
        # Colored circle with number
        circle = mpatches.Circle((0.08, cy), 0.018,
                                  facecolor=clr, edgecolor="none",
                                  transform=ax.transAxes)
        ax.add_patch(circle)
        text(ax, 0.08, cy + 0.005, str(i + 1),
             fontsize=11, weight="bold", color=WHITE, ha="center", va="center")
        # Finding text
        text(ax, 0.12, cy + 0.005, finding,
             fontsize=11, color=GRAY_DARK, va="center", wrap_width=78)

    footer(ax, 20)
    save_slide(fig, 18)


def slide_19():
    """Methodology."""
    fig, ax = new_slide()
    title_bar(ax, "Methodology")

    sections = [
        ("Data Source", "SEDA 2025.1 (Stanford CEPA)"),
        ("Metric", "cs_mn — cohort-standardized mean, NAEP-anchored"),
        ("Time Windows",
         "Pre-COVID: 2017–2019 mean\n"
         "Post-COVID: 2022–2025 mean\n"
         "IM Window: 2022–23 → 2024–25"),
        ("Peer Groups",
         "296 level-matched (pre-COVID G6+G7 math ±0.25 of Troy’s +0.937)\n"
         "107 high-Asian (≥20% Asian, pre-COVID ≥+0.50)\n"
         "8 MI affluent peers (same state test)"),
    ]
    sy = 0.84
    for label, body in sections:
        text(ax, 0.06, sy, label, fontsize=12, weight="bold", color=TROY_BLUE)
        text(ax, 0.06, sy - 0.04, body, fontsize=10, color=GRAY_DARK)
        n_lines = body.count("\n") + 1
        sy -= 0.05 + n_lines * 0.05

    footer(ax, 21)
    save_slide(fig, 19)


def slide_20():
    """References."""
    fig, ax = new_slide()
    title_bar(ax, "References")

    refs = [
        "SEDA 2025.1 — Stanford Center for Education Policy Analysis",
        "Education Scorecard 2026 — Harvard–Stanford–Dartmouth",
        "MI School Data / M-STEP — mischooldata.org",
        "Dee, Huffaker, & Novicoff (2025) — SFUSD detracking study",
        "Education Next — SFUSD detracking analysis",
        "Brookings Institution — detracking evidence review",
    ]
    sy = 0.82
    for i, ref in enumerate(refs):
        text(ax, 0.08, sy, f"{i + 1}.", fontsize=11, weight="bold",
             color=TROY_BLUE)
        text(ax, 0.12, sy, ref, fontsize=11, color=GRAY_DARK)
        sy -= 0.08

    footer(ax, 22)
    save_slide(fig, 20)


# ── NEW: Leaderboard Slides ──────────────────────────────────────────────────

def slide_leaderboard_national(slide_num, total):
    """Troy Fell 59 Places in the National Rankings — rank scatter."""
    fig, ax = new_slide()
    title_bar(ax, "Troy Fell 59 Places in the National Math Rankings")

    embed_chart(fig, chart_path("chart11_rank_shift_scatter.png"),
                0.03, 0.08, 0.58, 0.82)

    px, pw = 0.65, 0.32
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, LIGHT_RED)

    text(ax, px + 0.02, py + ph - 0.05, "Pre-COVID rank:",
         fontsize=10, color=GRAY_MID)
    text(ax, px + 0.02, py + ph - 0.14, "#76 / 296",
         fontsize=22, weight="bold", color=TROY_BLUE)
    text(ax, px + 0.02, py + ph - 0.22, "(top quarter)",
         fontsize=10, color=GRAY_MID)

    text(ax, px + 0.02, py + ph - 0.35, "Post-COVID rank:",
         fontsize=10, color=GRAY_MID)
    text(ax, px + 0.02, py + ph - 0.44, "#135 / 296",
         fontsize=22, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.52, "(mid-pack)",
         fontsize=10, color=GRAY_MID)

    text(ax, px + 0.02, py + ph - 0.66, "Lost 59 positions",
         fontsize=14, weight="bold", color=ACCENT_RED)
    text(ax, px + 0.02, py + ph - 0.75,
         "From top-quarter\nto middle of the pack\namong peers that started\nat the same level",
         fontsize=10, color=GRAY_DARK)

    footer(ax, slide_num, total)
    save_slide(fig, slide_num)


def slide_leaderboard_mi(slide_num, total):
    """MI Peer Leaderboard — Troy Fell From 2nd to 4th, with subgroup detail."""
    fig, ax = new_slide()
    title_bar(ax, "MI Peer Leaderboard: Troy Fell From 2nd to 4th")

    embed_chart(fig, chart_path("chart12_mi_peer_bump.png"),
                0.03, 0.08, 0.48, 0.82)

    px, pw = 0.53, 0.44
    py, ph = 0.10, 0.78
    rect(ax, px, py, pw, ph, GRAY_LIGHT)

    text(ax, px + 0.02, py + ph - 0.04,
         "Troy's Rank Shift by Subgroup",
         fontsize=12, weight="bold", color=TROY_BLUE)

    subgroups = [
        ("All Students",      "2nd → 4th", "–2", ACCENT_RED),
        ("Asian",             "1st → 2nd", "–1", ACCENT_RED),
        ("White",             "6th → 5th", "+1", ACCENT_GREEN),
        ("Econ Disadvantaged", "3rd → 4th", "–1", ACCENT_RED),
        ("Not Econ Disadv",   "2nd → 3rd", "–1", ACCENT_RED),
    ]
    y_start = py + ph - 0.15
    row_h = 0.11
    for i, (sg, shift, delta, clr) in enumerate(subgroups):
        ry = y_start - i * row_h
        if delta.startswith("–") or delta.startswith("-"):
            rect(ax, px + 0.01, ry - 0.025, pw - 0.02, row_h - 0.02, LIGHT_RED)
        else:
            rect(ax, px + 0.01, ry - 0.025, pw - 0.02, row_h - 0.02, LIGHT_GREEN)
        text(ax, px + 0.03, ry + 0.015, sg,
             fontsize=10, weight="bold", color=GRAY_DARK, va="center")
        text(ax, px + 0.25, ry + 0.015, shift,
             fontsize=10, color=GRAY_DARK, va="center", family="monospace")
        text(ax, px + 0.37, ry + 0.015, delta,
             fontsize=11, weight="bold", color=clr, va="center")

    text(ax, px + 0.02, py + 0.06,
         "Was #1 Asian math in MI.\nNorthville now leads.",
         fontsize=10, color=ACCENT_RED, weight="bold")
    text(ax, px + 0.02, py + 0.02,
         "4 of 5 subgroups lost positions under IM + detracking",
         fontsize=9, color=GRAY_MID, style="italic")

    footer(ax, slide_num, total)
    save_slide(fig, slide_num)


# ── Main ─────────────────────────────────────────────────────────────────────

TOTAL_SLIDES = 22

def main():
    print(f"Rendering {TOTAL_SLIDES} slides to", SLIDES_DIR)

    import shutil

    # Step 1: Render original slides 5-20 (they save as 05-20.png)
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

    # Step 2: Rename 05→07, 06→08, ..., 20→22 (work backwards)
    for old_n in range(20, 4, -1):
        new_n = old_n + 2
        src = os.path.join(SLIDES_DIR, f"{old_n:02d}.png")
        dst = os.path.join(SLIDES_DIR, f"{new_n:02d}.png")
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"  Renamed {old_n:02d}.png → {new_n:02d}.png")

    # Step 3: Render slides 1-4 (fixed positions)
    slide_01()
    slide_02()
    slide_03()
    slide_04()

    # Step 4: Render NEW leaderboard slides 5-6
    slide_leaderboard_national(5, TOTAL_SLIDES)
    slide_leaderboard_mi(6, TOTAL_SLIDES)

    print(f"Done — {TOTAL_SLIDES} slides saved.")


if __name__ == "__main__":
    main()
