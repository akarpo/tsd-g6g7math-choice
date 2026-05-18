#!/usr/bin/env python3
"""
build_deck.py - Generate Troy School District G6-G7 Math Executive Summary deck.

Produces a 20-slide PowerPoint at:
  deck/Troy_G6G7_Math_Executive_Summary.pptx

Requires: python-pptx
"""

import os
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# -- paths -------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent
CHARTS  = PROJECT / "charts"
DECK    = PROJECT / "deck"
OUTPUT  = DECK / "Troy_G6G7_Math_Executive_Summary.pptx"

DECK.mkdir(parents=True, exist_ok=True)

# -- colour palette -----------------------------------------------------------
TROY_BLUE     = RGBColor(0x1F, 0x3A, 0x5F)
ACCENT_RED    = RGBColor(0xC8, 0x30, 0x2F)
ACCENT_GREEN  = RGBColor(0x1F, 0x7A, 0x3D)
ACCENT_ORANGE = RGBColor(0xB7, 0x79, 0x1F)
LIGHT_GREEN   = RGBColor(0xE8, 0xF5, 0xEE)
LIGHT_ORANGE  = RGBColor(0xFF, 0xF4, 0xE0)
LIGHT_RED     = RGBColor(0xFB, 0xE7, 0xE6)
GRAY_LIGHT    = RGBColor(0xF2, 0xF4, 0xF7)
GRAY_DARK     = RGBColor(0x33, 0x33, 0x33)
GRAY_MID      = RGBColor(0x77, 0x77, 0x77)
WHITE         = RGBColor(0xFF, 0xFF, 0xFF)

# -- slide geometry constants -------------------------------------------------
SLIDE_W     = Inches(13.333)
SLIDE_H     = Inches(7.5)
TITLE_BAR_H = Inches(0.95)
CONTENT_TOP = Inches(1.15)
FOOTER_Y    = Inches(7.22)
TOTAL_SLIDES = 20

# -- presentation scaffold ----------------------------------------------------
prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
BLANK_LAYOUT = prs.slide_layouts[6]  # blank


# =============================================================================
# Helper functions
# =============================================================================

def hex_to_rgb(hex_str):
    """Convert '#RRGGBB' to RGBColor."""
    h = hex_str.lstrip('#')
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def add_rect(slide, left, top, width, height, color):
    """Add a solid-color filled rectangle shape."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_text(slide, left, top, width, height, text, font_size=14,
             bold=False, color=GRAY_DARK, alignment='left', font_name='Calibri',
             valign='top'):
    """Add a text box with word wrap."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    if valign == 'middle':
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    elif valign == 'bottom':
        tf.vertical_anchor = MSO_ANCHOR.BOTTOM
    else:
        tf.vertical_anchor = MSO_ANCHOR.TOP

    align_map = {
        'left': PP_ALIGN.LEFT,
        'center': PP_ALIGN.CENTER,
        'right': PP_ALIGN.RIGHT,
    }

    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align_map.get(alignment, PP_ALIGN.LEFT)
    return txBox


def add_multiline_text(slide, left, top, width, height, lines, font_size=14,
                       bold=False, color=GRAY_DARK, alignment='left',
                       font_name='Calibri', line_spacing=1.15):
    """Add a text box with multiple paragraphs (one per line in the list)."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP

    align_map = {
        'left': PP_ALIGN.LEFT,
        'center': PP_ALIGN.CENTER,
        'right': PP_ALIGN.RIGHT,
    }

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = align_map.get(alignment, PP_ALIGN.LEFT)
        p.space_after = Pt(font_size * 0.3)
    return txBox


def add_rich_text(slide, left, top, width, height, runs_list, alignment='left',
                  valign='top'):
    """Add a textbox with multiple paragraphs, each paragraph containing multiple runs.

    runs_list: list of lists of dicts
      [ [ {text, font_size, bold, color, font_name}, ... ], ... ]
    Each outer list is a paragraph; each inner dict is a run.
    """
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    if valign == 'middle':
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    else:
        tf.vertical_anchor = MSO_ANCHOR.TOP

    align_map = {
        'left': PP_ALIGN.LEFT,
        'center': PP_ALIGN.CENTER,
        'right': PP_ALIGN.RIGHT,
    }

    for i, para_runs in enumerate(runs_list):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align_map.get(alignment, PP_ALIGN.LEFT)
        p.space_after = Pt(4)

        for j, run_def in enumerate(para_runs):
            if j == 0:
                run = p.runs[0] if p.runs else p.add_run()
            else:
                run = p.add_run()
            run.text = run_def.get('text', '')
            run.font.size = Pt(run_def.get('font_size', 14))
            run.font.bold = run_def.get('bold', False)
            run.font.color.rgb = run_def.get('color', GRAY_DARK)
            run.font.name = run_def.get('font_name', 'Calibri')
    return txBox


def title_bar(slide, title):
    """TROY_BLUE bar at y=0, height=0.95", white bold title text."""
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, TITLE_BAR_H, TROY_BLUE)
    add_text(slide, Inches(0.6), Inches(0.15), Inches(12), Inches(0.65),
             title, font_size=26, bold=True, color=WHITE)


def footer(slide, slide_num, total):
    """Small gray text at y=7.22" with slide number."""
    add_text(slide, Inches(0.5), FOOTER_Y, Inches(12), Inches(0.25),
             f"Troy School District G6-G7 Math Analysis  |  Slide {slide_num} of {total}",
             font_size=8, color=GRAY_MID)


def embed_chart(slide, chart_name, left, top, width, height):
    """Embed a chart PNG if it exists, otherwise add placeholder text."""
    chart_path = CHARTS / chart_name
    if chart_path.exists():
        slide.shapes.add_picture(str(chart_path), left, top, width, height)
    else:
        add_rect(slide, left, top, width, height, GRAY_LIGHT)
        add_text(slide, left, top, width, height,
                 f"[Chart placeholder: {chart_name}]",
                 font_size=12, color=GRAY_MID, alignment='center')


# =============================================================================
# Slide 1 - Title
# =============================================================================
def build_slide_01():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    # Full TROY_BLUE background
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, SLIDE_H, TROY_BLUE)

    # Main title
    add_text(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.2),
             "Troy School District G6–G7 Math Analysis",
             font_size=36, bold=True, color=WHITE, alignment='center')

    # Subtitle
    add_text(slide, Inches(1.5), Inches(3.1), Inches(10.3), Inches(1.0),
             "Has Illustrative Mathematics + Detracking\nOutperformed Its Characteristics?",
             font_size=22, bold=False, color=WHITE, alignment='center')

    # Date / source
    add_text(slide, Inches(1.5), Inches(4.6), Inches(10.3), Inches(0.6),
             "May 2026  |  SEDA 2025.1 + M-STEP Data",
             font_size=16, bold=False, color=WHITE, alignment='center')

    footer(slide, 1, TOTAL_SLIDES)


# =============================================================================
# Slide 2 - The Question + Answer
# =============================================================================
def build_slide_02():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "The Question — and the One-Line Answer")

    col_w = Inches(3.9)
    col_h = Inches(5.0)
    gap = Inches(0.25)
    y = CONTENT_TOP

    # Left column - white bg
    x1 = Inches(0.5)
    add_rect(slide, x1, y, col_w, col_h, WHITE)
    add_text(slide, x1 + Inches(0.2), y + Inches(0.15), col_w - Inches(0.4), Inches(0.4),
             "Question", font_size=16, bold=True, color=TROY_BLUE)
    add_text(slide, x1 + Inches(0.2), y + Inches(0.65), col_w - Inches(0.4), col_h - Inches(0.8),
             "Has Troy's Fall 2023 adoption of Illustrative Mathematics and detracking "
             "of G6+G7 math produced results that outperform its characteristics?",
             font_size=14, color=GRAY_DARK)

    # Center column - LIGHT_RED bg
    x2 = x1 + col_w + gap
    add_rect(slide, x2, y, col_w, col_h, LIGHT_RED)
    add_text(slide, x2 + Inches(0.2), y + Inches(0.15), col_w - Inches(0.4), Inches(0.4),
             "Answer", font_size=16, bold=True, color=ACCENT_RED)
    add_text(slide, x2 + Inches(0.2), y + Inches(0.65), col_w - Inches(0.4), col_h - Inches(0.8),
             "No. Troy ranks 197 of 295 level-matched peers (bottom third) "
             "in math recovery during the exact IM adoption window.",
             font_size=14, color=GRAY_DARK)

    # Right column - GRAY_LIGHT bg
    x3 = x2 + col_w + gap
    add_rect(slide, x3, y, col_w, col_h, GRAY_LIGHT)
    add_text(slide, x3 + Inches(0.2), y + Inches(0.15), col_w - Inches(0.4), Inches(0.4),
             "Key Numbers", font_size=16, bold=True, color=TROY_BLUE)
    add_multiline_text(
        slide, x3 + Inches(0.2), y + Inches(0.65), col_w - Inches(0.4), col_h - Inches(0.8),
        [
            "+0.024 grade levels — Troy's IM-window recovery",
            "+0.058 — Median peer recovery",
            "+0.211 — Birmingham (tracked, same county)",
        ],
        font_size=14, color=GRAY_DARK
    )

    footer(slide, 2, TOTAL_SLIDES)


# =============================================================================
# Slide 3 - Timeline
# =============================================================================
def build_slide_03():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "What Troy Did and When")

    events = [
        ("Fall 2023", "Adopted Illustrative Mathematics, detracked G6 and G7 math", ACCENT_RED),
        ("Spring 2024", "First IM cohort tested (G6 M-STEP)", ACCENT_ORANGE),
        ("Fall 2024", "Second IM year; first G7 IM cohort enters 7th grade", ACCENT_ORANGE),
        ("Spring 2025", "Second IM G6 + first IM G7 tested", TROY_BLUE),
    ]

    y = CONTENT_TOP + Inches(0.3)
    for i, (period, desc, bar_color) in enumerate(events):
        row_y = y + Inches(i * 1.2)
        # Color bar
        add_rect(slide, Inches(0.8), row_y, Inches(0.12), Inches(0.8), bar_color)
        # Period label
        add_text(slide, Inches(1.15), row_y + Inches(0.05), Inches(2.0), Inches(0.4),
                 period, font_size=16, bold=True, color=TROY_BLUE)
        # Description
        add_text(slide, Inches(1.15), row_y + Inches(0.4), Inches(10.5), Inches(0.5),
                 desc, font_size=14, color=GRAY_DARK)

    # Bottom note
    add_rect(slide, Inches(0.5), Inches(6.3), Inches(12.3), Inches(0.6), GRAY_LIGHT)
    add_text(slide, Inches(0.7), Inches(6.35), Inches(12.0), Inches(0.5),
             "Prior: 7th graders had Big Ideas Math 7, Math 7/8 Honors, small Algebra 1 cohort",
             font_size=12, color=GRAY_MID)

    footer(slide, 3, TOTAL_SLIDES)


# =============================================================================
# Slide 4 - Pre-COVID Position
# =============================================================================
def build_slide_04():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "Troy's Pre-COVID Math Position — Strong, Not Invincible")

    embed_chart(slide, "chart01_mi_peers_g6_trend.png",
                Inches(0.4), CONTENT_TOP, Inches(7.5), Inches(5.5))

    # Right panel
    rx = Inches(8.2)
    rw = Inches(4.5)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(4.5), LIGHT_GREEN)
    add_multiline_text(
        slide, rx + Inches(0.25), CONTENT_TOP + Inches(0.3), rw - Inches(0.5), Inches(4.0),
        [
            "Pre-COVID G6+G7 math:",
            "+0.937 grade levels above national norm",
            "",
            "3rd highest among MI affluent peers",
            "",
            "37% above national average",
        ],
        font_size=15, color=GRAY_DARK
    )

    footer(slide, 4, TOTAL_SLIDES)


# =============================================================================
# Slide 5 - Post-COVID Decline
# =============================================================================
def build_slide_05():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "The Post-COVID Decline Hit Troy Hard in Math")

    embed_chart(slide, "chart09_covid_delta_ranking.png",
                Inches(0.4), CONTENT_TOP, Inches(7.5), Inches(5.5))

    rx = Inches(8.2)
    rw = Inches(4.5)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(3.5), LIGHT_RED)
    add_multiline_text(
        slide, rx + Inches(0.25), CONTENT_TOP + Inches(0.3), rw - Inches(0.5), Inches(3.0),
        [
            "Troy declined -0.187 grade levels",
            "",
            "Rank 104 of 296 level-matched peers",
            "(35th percentile)",
        ],
        font_size=15, color=GRAY_DARK
    )

    footer(slide, 5, TOTAL_SLIDES)


# =============================================================================
# Slide 6 - The Critical Test: IM Window
# =============================================================================
def build_slide_06():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "The Critical Test: Recovery During the IM Window (2022–23 → 2024–25)")

    embed_chart(slide, "chart04_level_matched_histogram.png",
                Inches(0.3), CONTENT_TOP, Inches(8.0), Inches(5.5))

    rx = Inches(8.6)
    rw = Inches(4.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(3.0), LIGHT_RED)
    add_multiline_text(
        slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.3), rw - Inches(0.4), Inches(2.5),
        [
            "Troy ranks 197 of 295",
            "— bottom third",
            "",
            "Most peers recovered 2-3x more",
        ],
        font_size=15, bold=True, color=ACCENT_RED
    )

    footer(slide, 6, TOTAL_SLIDES)


# =============================================================================
# Slide 7 - MI Peers: IM Window
# =============================================================================
def build_slide_07():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "Among MI Peers, Troy Ranks 6th of 8 in Recovery")

    embed_chart(slide, "chart03_im_window_ranking.png",
                Inches(0.3), CONTENT_TOP, Inches(7.0), Inches(5.5))

    # Right panel with ranking table
    rx = Inches(7.6)
    rw = Inches(5.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(5.5), GRAY_LIGHT)
    add_text(slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.15), rw - Inches(0.4), Inches(0.4),
             "IM-Window Recovery Ranking", font_size=14, bold=True, color=TROY_BLUE)

    peers = [
        ("Birmingham", "+0.211", "(tracked)", ACCENT_GREEN),
        ("Northville", "+0.102", "(tracked)", ACCENT_GREEN),
        ("Bloomfield Hills", "+0.082", "(tracked)", ACCENT_GREEN),
        ("Walled Lake", "+0.056", "", GRAY_DARK),
        ("Novi", "+0.029", "", GRAY_DARK),
        ("Troy", "+0.024", "(IM + detracked)", ACCENT_RED),
        ("West Bloomfield", "+0.006", "", GRAY_DARK),
        ("Rochester", "+0.000", "", GRAY_DARK),
    ]

    for i, (name, delta, note, clr) in enumerate(peers):
        row_y = CONTENT_TOP + Inches(0.65) + Inches(i * 0.58)
        is_troy = (name == "Troy")
        if is_troy:
            add_rect(slide, rx + Inches(0.1), row_y - Inches(0.03),
                     rw - Inches(0.2), Inches(0.52), LIGHT_RED)
        label = f"{name}  {delta}  {note}"
        add_text(slide, rx + Inches(0.2), row_y, rw - Inches(0.4), Inches(0.45),
                 label, font_size=13, bold=is_troy, color=clr)

    footer(slide, 7, TOTAL_SLIDES)


# =============================================================================
# Slide 8 - G7 Trajectory
# =============================================================================
def build_slide_08():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "G7 Math: The Tracked-vs-IM Comparison Year")

    embed_chart(slide, "chart02_mi_peers_g7_trend.png",
                Inches(0.3), CONTENT_TOP, Inches(8.0), Inches(5.5))

    rx = Inches(8.6)
    rw = Inches(4.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(3.5), GRAY_LIGHT)
    add_multiline_text(
        slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.3), rw - Inches(0.4), Inches(3.0),
        [
            "2023-24: G7 still tracked — Troy matched peers",
            "",
            "2024-25: First G7 IM cohort — recovery stalled",
        ],
        font_size=14, color=GRAY_DARK
    )

    footer(slide, 8, TOTAL_SLIDES)


# =============================================================================
# Slide 9 - Asian Subgroup Crisis
# =============================================================================
def build_slide_09():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "The Asian Subgroup Crisis — 36% of Troy's Enrollment")

    embed_chart(slide, "chart05_asian_g6_trend.png",
                Inches(0.3), CONTENT_TOP, Inches(8.0), Inches(5.5))

    rx = Inches(8.6)
    rw = Inches(4.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(4.0), LIGHT_RED)
    add_multiline_text(
        slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.3), rw - Inches(0.4), Inches(3.5),
        [
            "G6 Asian Δ COVID: -0.409",
            "",
            "G7 Asian Δ COVID: -0.278",
            "",
            "G7 Asian IM-window: -0.094",
            "(still declining)",
        ],
        font_size=15, bold=True, color=ACCENT_RED
    )

    footer(slide, 9, TOTAL_SLIDES)


# =============================================================================
# Slide 10 - G7 Asian Still Declining
# =============================================================================
def build_slide_10():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "G7 Asian Math Is Still Declining Under IM")

    embed_chart(slide, "chart06_asian_g7_trend.png",
                Inches(0.3), CONTENT_TOP, Inches(8.0), Inches(5.5))

    rx = Inches(8.6)
    rw = Inches(4.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(3.8), GRAY_LIGHT)
    add_multiline_text(
        slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.3), rw - Inches(0.4), Inches(3.3),
        [
            "Bellevue (WA, 41% Asian):",
            "  G7 Asian IM-Δ = +0.162",
            "",
            "Issaquah (WA, 30% Asian):",
            "  +0.218",
            "",
            "Troy (MI, 36% Asian):",
            "  -0.094",
        ],
        font_size=14, color=GRAY_DARK
    )

    footer(slide, 10, TOTAL_SLIDES)


# =============================================================================
# Slide 11 - Troy Subgroup Overview
# =============================================================================
def build_slide_11():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "Every Subgroup Declined — But Recovery Is Uneven")

    embed_chart(slide, "chart07_troy_subgroup_waterfall.png",
                Inches(0.3), CONTENT_TOP, Inches(8.0), Inches(5.5))

    rx = Inches(8.6)
    rw = Inches(4.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(3.0), GRAY_LIGHT)
    add_multiline_text(
        slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.3), rw - Inches(0.4), Inches(2.5),
        [
            "Asian and White subgroups show largest absolute declines",
            "",
            "ECD subgroup was already near national average",
        ],
        font_size=14, color=GRAY_DARK
    )

    footer(slide, 11, TOTAL_SLIDES)


# =============================================================================
# Slide 12 - M-STEP Raw Numbers
# =============================================================================
def build_slide_12():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "M-STEP Math Proficiency: The Numbers Parents See")

    embed_chart(slide, "chart08_mstep_troy_proficiency.png",
                Inches(0.3), CONTENT_TOP, Inches(8.0), Inches(5.5))

    rx = Inches(8.6)
    rw = Inches(4.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(4.5), GRAY_LIGHT)
    add_text(slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.15), rw - Inches(0.4), Inches(0.4),
             "% Proficient or Advanced", font_size=14, bold=True, color=TROY_BLUE)
    add_multiline_text(
        slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.7), rw - Inches(0.4), Inches(2.5),
        [
            "G6: 71.4% → 63.2% → 66.3% → 65.8%",
            "",
            "G7: 67.5% → 61.3% → 66.0% → TBD",
        ],
        font_size=14, color=GRAY_DARK
    )
    add_rect(slide, rx, CONTENT_TOP + Inches(3.4), rw, Inches(0.9), LIGHT_RED)
    add_text(slide, rx + Inches(0.2), CONTENT_TOP + Inches(3.5), rw - Inches(0.4), Inches(0.7),
             "IM has not restored Troy to pre-COVID proficiency levels",
             font_size=13, bold=True, color=ACCENT_RED)

    footer(slide, 12, TOTAL_SLIDES)


# =============================================================================
# Slide 13 - SFUSD Detracking
# =============================================================================
def build_slide_13():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "San Francisco: 12 Years of Detracking, Then Reversal")

    findings = [
        (LIGHT_RED, "1. Achievement gaps WIDENED: Hispanic-White gap expanded "
         "31 points (vs 5 statewide)"),
        (LIGHT_ORANGE, "2. AP math enrollment DECLINED 15%, driven by "
         "Asian/Pacific Islander students"),
        (LIGHT_RED, "3. Board voted March 2026 to RESTORE Algebra 1 in 8th grade "
         "at all schools"),
    ]

    y = CONTENT_TOP + Inches(0.3)
    for i, (bg_color, text) in enumerate(findings):
        row_y = y + Inches(i * 1.5)
        add_rect(slide, Inches(0.8), row_y, Inches(11.7), Inches(1.2), bg_color)
        add_text(slide, Inches(1.1), row_y + Inches(0.15), Inches(11.1), Inches(0.9),
                 text, font_size=16, color=GRAY_DARK)

    # Bottom callout
    add_rect(slide, Inches(0.8), Inches(6.1), Inches(11.7), Inches(0.7), TROY_BLUE)
    add_text(slide, Inches(1.1), Inches(6.15), Inches(11.1), Inches(0.6),
             "Troy is replicating a strategy with a well-documented failure pattern",
             font_size=15, bold=True, color=WHITE)

    footer(slide, 13, TOTAL_SLIDES)


# =============================================================================
# Slide 14 - Cambridge Reversal
# =============================================================================
def build_slide_14():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "Cambridge, MA: Detracked 2017–2019, Now Reversing")

    col_w = Inches(5.8)
    col_h = Inches(4.5)
    gap = Inches(0.4)
    y = CONTENT_TOP + Inches(0.5)

    # Left panel
    x1 = Inches(0.6)
    add_rect(slide, x1, y, col_w, col_h, LIGHT_ORANGE)
    add_text(slide, x1 + Inches(0.3), y + Inches(0.15), col_w - Inches(0.6), Inches(0.4),
             "What They Did", font_size=16, bold=True, color=ACCENT_ORANGE)
    add_text(slide, x1 + Inches(0.3), y + Inches(0.7), col_w - Inches(0.6), col_h - Inches(1.0),
             "Eliminated accelerated math tracks to address racial disparities "
             "in advanced course enrollment.",
             font_size=15, color=GRAY_DARK)

    # Right panel
    x2 = x1 + col_w + gap
    add_rect(slide, x2, y, col_w, col_h, LIGHT_RED)
    add_text(slide, x2 + Inches(0.3), y + Inches(0.15), col_w - Inches(0.6), Inches(0.4),
             "What Happened", font_size=16, bold=True, color=ACCENT_RED)
    add_text(slide, x2 + Inches(0.3), y + Inches(0.7), col_w - Inches(0.6), col_h - Inches(1.0),
             "COVID obscured early results. District now reversing course, "
             "restoring algebra to 8th grade, citing persistent achievement gaps.",
             font_size=15, color=GRAY_DARK)

    footer(slide, 14, TOTAL_SLIDES)


# =============================================================================
# Slide 15 - The 50% Algebra 1 Claim
# =============================================================================
def build_slide_15():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "The '50% Algebra 1' Claim — Course Access ≠ Achievement")

    rows = [
        "1. SFUSD made the identical claim for a decade before test scores "
        "revealed no improvement",
        "2. SEDA shows Troy's G6+G7 math readiness dropped from +0.937 to "
        "+0.750 — a quarter-grade-level decline",
        "3. The comparison is not past Troy enrollment — it's what tracked "
        "peers achieve now",
    ]

    y = CONTENT_TOP + Inches(0.3)
    for i, text in enumerate(rows):
        row_y = y + Inches(i * 1.6)
        add_rect(slide, Inches(0.8), row_y, Inches(11.7), Inches(1.3), LIGHT_ORANGE)
        add_text(slide, Inches(1.1), row_y + Inches(0.2), Inches(11.1), Inches(0.9),
                 text, font_size=16, color=GRAY_DARK)

    footer(slide, 15, TOTAL_SLIDES)


# =============================================================================
# Slide 16 - What High-Performing Districts Do
# =============================================================================
def build_slide_16():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "What High-Performing Math Districts Do Differently")

    embed_chart(slide, "chart10_high_asian_peers_delta.png",
                Inches(0.3), CONTENT_TOP, Inches(8.0), Inches(5.5))

    rx = Inches(8.6)
    rw = Inches(4.3)
    add_rect(slide, rx, CONTENT_TOP, rw, Inches(3.5), LIGHT_GREEN)
    add_multiline_text(
        slide, rx + Inches(0.2), CONTENT_TOP + Inches(0.3), rw - Inches(0.4), Inches(3.0),
        [
            "Among 107 high-Asian (≥20%) districts, many California and NJ "
            "districts recovered to or surpassed pre-COVID levels",
            "",
            "— with tracking intact",
        ],
        font_size=14, color=GRAY_DARK
    )

    footer(slide, 16, TOTAL_SLIDES)


# =============================================================================
# Slide 17 - IM Evidence Base
# =============================================================================
def build_slide_17():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "Illustrative Mathematics: Evidence Gaps")

    # Table header
    y = CONTENT_TOP + Inches(0.2)
    col_x = [Inches(0.6), Inches(4.6), Inches(8.4)]
    col_w = [Inches(3.8), Inches(3.6), Inches(4.5)]

    add_rect(slide, Inches(0.5), y, Inches(12.3), Inches(0.55), TROY_BLUE)
    headers = ["District", "Result", "Note"]
    for i, h in enumerate(headers):
        add_text(slide, col_x[i], y + Inches(0.05), col_w[i], Inches(0.45),
                 h, font_size=14, bold=True, color=WHITE)

    # Table rows
    table_data = [
        ("NYC District 11 (Bronx)", "25.8% → 50.6%",
         "High-poverty, low-baseline, not comparable to Troy"),
        ("Fort Zumwalt (MO)", "Effect size 0.16 SD",
         "Modest, comparable to general instructional improvement"),
        ("Philadelphia", "Process study only",
         "No outcomes data"),
    ]

    for i, (district, result, note) in enumerate(table_data):
        row_y = y + Inches(0.55) + Inches(i * 0.9)
        bg = GRAY_LIGHT if i % 2 == 0 else WHITE
        add_rect(slide, Inches(0.5), row_y, Inches(12.3), Inches(0.85), bg)
        add_text(slide, col_x[0], row_y + Inches(0.15), col_w[0], Inches(0.6),
                 district, font_size=13, bold=True, color=GRAY_DARK)
        add_text(slide, col_x[1], row_y + Inches(0.15), col_w[1], Inches(0.6),
                 result, font_size=13, color=GRAY_DARK)
        add_text(slide, col_x[2], row_y + Inches(0.15), col_w[2], Inches(0.6),
                 note, font_size=12, color=GRAY_MID)

    # Bottom callout
    add_rect(slide, Inches(0.5), Inches(4.4), Inches(12.3), Inches(0.9), LIGHT_RED)
    add_text(slide, Inches(0.8), Inches(4.5), Inches(11.7), Inches(0.7),
             "No published evidence of IM success in an affluent, high-performing, "
             "high-Asian district like Troy",
             font_size=14, bold=True, color=ACCENT_RED)

    footer(slide, 17, TOTAL_SLIDES)


# =============================================================================
# Slide 18 - Conclusions
# =============================================================================
def build_slide_18():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "Conclusions")

    conclusions = [
        (ACCENT_RED, "Troy has NOT outperformed its characteristics — "
         "bottom third of 295 peers"),
        (ACCENT_RED, "Asian subgroup is most concerning — "
         "G7 Asian STILL declining"),
        (ACCENT_ORANGE, "Detracking evidence base is against this approach — "
         "SFUSD, Cambridge reversed"),
        (ACCENT_ORANGE, "Course enrollment ≠ achievement — "
         "'50% Algebra 1' claim misleads"),
        (ACCENT_RED, "Opportunity cost is real: Birmingham recovered "
         "9× more in the same window"),
    ]

    y = CONTENT_TOP + Inches(0.15)
    for i, (bar_color, text) in enumerate(conclusions):
        row_y = y + Inches(i * 1.1)
        # Left border bar
        add_rect(slide, Inches(0.7), row_y, Inches(0.1), Inches(0.85), bar_color)
        # Background
        add_rect(slide, Inches(0.85), row_y, Inches(11.5), Inches(0.85), GRAY_LIGHT)
        # Number
        add_text(slide, Inches(1.0), row_y + Inches(0.1), Inches(0.5), Inches(0.6),
                 str(i + 1) + ".", font_size=20, bold=True, color=bar_color)
        # Text
        add_text(slide, Inches(1.5), row_y + Inches(0.15), Inches(10.5), Inches(0.6),
                 text, font_size=15, color=GRAY_DARK)

    footer(slide, 18, TOTAL_SLIDES)


# =============================================================================
# Slide 19 - Methodology
# =============================================================================
def build_slide_19():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "Methodology")

    methods = [
        "Primary metric: SEDA cs (cohort-standardized), NAEP-anchored, "
        "expressed in grade levels above/below national average",
        "Pre-COVID baseline: 2017–2019 mean",
        "Post-COVID: 2022–2025 mean",
        "IM window: 2022–23 → 2024–25 (the exact adoption period)",
        "296 level-matched peers: pre-COVID G6+G7 math ±0.25 of Troy's +0.937",
        "107 high-Asian peers: ≥20% Asian enrollment, pre-COVID ≥+0.50",
        "8 MI affluent peers: same state test, comparable demographics",
        "M-STEP data from Michigan School Data (mischooldata.org)",
    ]

    y = CONTENT_TOP + Inches(0.2)
    for i, text in enumerate(methods):
        row_y = y + Inches(i * 0.68)
        # Bullet dot
        add_rect(slide, Inches(0.9), row_y + Inches(0.12), Inches(0.1), Inches(0.1), TROY_BLUE)
        add_text(slide, Inches(1.2), row_y, Inches(11.3), Inches(0.6),
                 text, font_size=13, color=GRAY_DARK)

    footer(slide, 19, TOTAL_SLIDES)


# =============================================================================
# Slide 20 - References
# =============================================================================
def build_slide_20():
    slide = prs.slides.add_slide(BLANK_LAYOUT)
    title_bar(slide, "References")

    references = [
        "SEDA 2025.1 (Stanford CEPA) — educationdata.urban.org",
        "Education Scorecard 2026 (Harvard-Stanford-Dartmouth)",
        "MI School Data / M-STEP — mischooldata.org",
        "Dee, Huffaker, & Novicoff (2025) — SFUSD detracking study",
        "Education Next — SFUSD detracking analysis",
        "Brookings Institution — detracking evidence review",
    ]

    y = CONTENT_TOP + Inches(0.3)
    for i, ref in enumerate(references):
        row_y = y + Inches(i * 0.8)
        add_rect(slide, Inches(0.9), row_y + Inches(0.12), Inches(0.1), Inches(0.1), TROY_BLUE)
        add_text(slide, Inches(1.2), row_y, Inches(11.3), Inches(0.6),
                 ref, font_size=14, color=GRAY_DARK)

    footer(slide, 20, TOTAL_SLIDES)


# =============================================================================
# Build all slides
# =============================================================================
def main():
    build_slide_01()
    build_slide_02()
    build_slide_03()
    build_slide_04()
    build_slide_05()
    build_slide_06()
    build_slide_07()
    build_slide_08()
    build_slide_09()
    build_slide_10()
    build_slide_11()
    build_slide_12()
    build_slide_13()
    build_slide_14()
    build_slide_15()
    build_slide_16()
    build_slide_17()
    build_slide_18()
    build_slide_19()
    build_slide_20()

    prs.save(str(OUTPUT))
    print(f"Deck saved to {OUTPUT}")
    print(f"  {len(prs.slides)} slides, {SLIDE_W} x {SLIDE_H}")


if __name__ == "__main__":
    main()
