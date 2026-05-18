#!/usr/bin/env python3
"""Generate all charts for the Troy SD G6-G7 Math Analysis.

Reads SEDA 2025.1 data and produces 10 publication-quality charts for the
analysis of Troy School District's adoption of Illustrative Mathematics
and detracking of 6th/7th grade math starting Fall 2023.

Output: /Users/Alex/Downloads/tsd-g6g7math-choice/charts/chart01..chart10.png
"""

import pathlib
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=UserWarning)

# ── Paths ──────────────────────────────────────────────────────────────
BASE = pathlib.Path("/Users/Alex/Downloads/tsd-g6g7math-choice")
SUBSET_CSV = BASE / "data" / "seda_math_g67_subset.csv"
PEERS_CSV = BASE / "data" / "seda_math_peers_full.csv"
CHART_DIR = BASE / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# ── Color Palette ──────────────────────────────────────────────────────
TROY_BLUE = "#1F3A5F"
ACCENT_RED = "#C8302F"
ACCENT_GREEN = "#1F7A3D"
ACCENT_ORANGE = "#B7791F"
CHART_RED = "#DC3545"
CHART_GREEN = "#28A745"
CHART_BLUE = "#4A90D9"
CHART_AMBER = "#F0A030"
GRAY_DARK = "#333333"
GRAY_MID = "#777777"
GRAY_LIGHT = "#CCCCCC"

# Muted palette for non-Troy MI peer lines
MUTED_PALETTE = [
    "#6E8FAD", "#8DA8C2", "#5B8A72", "#A3886E",
    "#7A7A7A", "#9E7FB0", "#6D9EA0",
]

# ── Typography ─────────────────────────────────────────────────────────
try:
    from matplotlib.font_manager import FontProperties
    _test = FontProperties(family="Calibri")
    _test.get_name()
    FONT_FAMILY = "Calibri"
except Exception:
    FONT_FAMILY = "sans-serif"

plt.rcParams.update({
    "font.family": FONT_FAMILY,
    "axes.titlecolor": GRAY_DARK,
    "axes.labelcolor": GRAY_DARK,
    "xtick.color": GRAY_DARK,
    "ytick.color": GRAY_DARK,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "axes.edgecolor": GRAY_LIGHT,
    "axes.grid": False,
    "figure.dpi": 300,
})

# ── MI Peer Districts ─────────────────────────────────────────────────
MI_PEERS = {
    2634260: "Troy",
    2605850: "Birmingham",
    2606090: "Bloomfield Hills",
    2625980: "Northville",
    2626130: "Novi",
    2629940: "Rochester",
    2635160: "Walled Lake",
    2635820: "West Bloomfield",
}

# Full 22-district analysis universe (including non-MI)
ALL_DISTRICTS = {
    2634260: "Troy",
    2605850: "Birmingham",
    2606090: "Bloomfield Hills",
    2625980: "Northville",
    2626130: "Novi",
    2629940: "Rochester",
    2635160: "Walled Lake",
    2635820: "West Bloomfield",
    4815210: "Coppell",
    4835100: "Plano",
    3417700: "W. Windsor-Plainsboro",
    3410200: "Millburn",
    634410: "San Francisco Unified",
    103360: "Tuscaloosa City",
    508280: "Jonesboro",
    2708190: "Eastern Carver Cty",
    3200060: "Clark County",
    5401470: "Upshur County",
    4226390: "William Penn",
    5300390: "Bellevue",
    5303750: "Issaquah",
    5304230: "Lake Washington",
}

# High-Asian comparison districts for charts 5-6
ASIAN_COMP = {
    2634260: "Troy",
    2626130: "Novi",
    5300390: "Bellevue",
    5303750: "Issaquah",
    3417700: "W. Windsor-Plainsboro",
    4815210: "Coppell",
}

# ── Load Data ──────────────────────────────────────────────────────────
print("Loading SEDA data...")
df = pd.read_csv(SUBSET_CSV)
df["sedaadmin"] = df["sedaadmin"].astype(int)
df["grade"] = df["grade"].astype(int)
df["year"] = df["year"].astype(int)

peers = pd.read_csv(PEERS_CSV)
peers["sid"] = peers["sid"].astype(int)


# ── Helpers ────────────────────────────────────────────────────────────
def style_ax(ax, title, subtitle=None, ylabel=None, xlabel=None):
    """Apply consistent styling to an axes object.
    Titles omitted — slide headers provide context when embedded."""
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10, color=GRAY_MID)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10, color=GRAY_MID)
    ax.tick_params(labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT)
    ax.spines["bottom"].set_color(GRAY_LIGHT)


def add_covid_shade(ax, ymin=None, ymax=None):
    """Add a gray shaded COVID gap rectangle (2020-2021)."""
    if ymin is None:
        ymin = ax.get_ylim()[0]
    if ymax is None:
        ymax = ax.get_ylim()[1]
    ax.axvspan(2019.5, 2021.5, color="#E0E0E0", alpha=0.4, zorder=0)
    ax.text(2020.5, ymax, "COVID", ha="center", va="top",
            fontsize=6, color="#AAAAAA", style="italic", zorder=1)


def savefig(fig, name):
    path = CHART_DIR / name
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print(f"  Saved {path.name}")


# ======================================================================
#  CHART 1: MI Peers G6 Trend
# ======================================================================
def chart01_mi_peers_g6_trend():
    print("Chart 01: MI Peers G6 trend...")
    g6 = df[(df["grade"] == 6) & (df["sedaadmin"].isin(MI_PEERS.keys()))].copy()
    g6["label"] = g6["sedaadmin"].map(MI_PEERS)

    fig, ax = plt.subplots(figsize=(12, 7))
    for i, (sid, label) in enumerate(MI_PEERS.items()):
        sub = g6[g6["sedaadmin"] == sid].sort_values("year")
        if sid == 2634260:
            ax.plot(sub["year"], sub["cs_mn_all"], color=ACCENT_RED,
                    linewidth=2.8, marker="o", markersize=5, label=label, zorder=10)
        else:
            c = MUTED_PALETTE[i % len(MUTED_PALETTE)]
            ax.plot(sub["year"], sub["cs_mn_all"], color=c,
                    linewidth=1.3, marker="o", markersize=3, alpha=0.75, label=label)

    add_covid_shade(ax)
    ax.axhline(0, color=GRAY_LIGHT, linewidth=0.8, linestyle="--")
    style_ax(ax, "Grade 6 Math: Troy vs. MI Affluent Peers",
             subtitle="SEDA 2025.1 cohort-standardized mean (cs_mn_all), 2009-2025",
             ylabel="Grade levels above national norm",
             xlabel="School year (spring)")
    ax.set_xticks(range(2009, 2026))
    ax.set_xticklabels([str(y) if y % 2 == 1 else "" for y in range(2009, 2026)],
                       fontsize=8)
    ax.legend(fontsize=8, loc="lower left", framealpha=0.9, edgecolor=GRAY_LIGHT)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%+.1f"))
    savefig(fig, "chart01_mi_peers_g6_trend.png")


# ======================================================================
#  CHART 2: MI Peers G7 Trend
# ======================================================================
def chart02_mi_peers_g7_trend():
    print("Chart 02: MI Peers G7 trend...")
    g7 = df[(df["grade"] == 7) & (df["sedaadmin"].isin(MI_PEERS.keys()))].copy()
    g7["label"] = g7["sedaadmin"].map(MI_PEERS)

    fig, ax = plt.subplots(figsize=(12, 7))
    for i, (sid, label) in enumerate(MI_PEERS.items()):
        sub = g7[g7["sedaadmin"] == sid].sort_values("year")
        if sid == 2634260:
            ax.plot(sub["year"], sub["cs_mn_all"], color=ACCENT_RED,
                    linewidth=2.8, marker="o", markersize=5, label=label, zorder=10)
        else:
            c = MUTED_PALETTE[i % len(MUTED_PALETTE)]
            ax.plot(sub["year"], sub["cs_mn_all"], color=c,
                    linewidth=1.3, marker="o", markersize=3, alpha=0.75, label=label)

    add_covid_shade(ax)
    ax.axhline(0, color=GRAY_LIGHT, linewidth=0.8, linestyle="--")
    style_ax(ax, "Grade 7 Math: Troy vs. MI Affluent Peers",
             subtitle="SEDA 2025.1 cohort-standardized mean (cs_mn_all), 2009-2025",
             ylabel="Grade levels above national norm",
             xlabel="School year (spring)")
    ax.set_xticks(range(2009, 2026))
    ax.set_xticklabels([str(y) if y % 2 == 1 else "" for y in range(2009, 2026)],
                       fontsize=8)
    ax.legend(fontsize=8, loc="lower left", framealpha=0.9, edgecolor=GRAY_LIGHT)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%+.1f"))
    savefig(fig, "chart02_mi_peers_g7_trend.png")


# ======================================================================
#  CHART 3: IM-Window Ranking (8 MI Peers)
# ======================================================================
def chart03_im_window_ranking():
    print("Chart 03: IM-window ranking (MI peers)...")
    # Compute IM-window delta (2022-23 avg -> 2024-25 avg) for G6+G7 pooled
    results = []
    for sid, label in MI_PEERS.items():
        dists = df[df["sedaadmin"] == sid]
        for grade in [6, 7]:
            gd = dists[dists["grade"] == grade]
            pre_im = gd[gd["year"].isin([2022, 2023])]["cs_mn_all"].mean()
            post_im = gd[gd["year"].isin([2024, 2025])]["cs_mn_all"].mean()
            if pd.notna(pre_im) and pd.notna(post_im):
                results.append({"sid": sid, "label": label, "grade": grade,
                                "delta": post_im - pre_im})

    rdf = pd.DataFrame(results)
    pooled = rdf.groupby(["sid", "label"])["delta"].mean().reset_index()
    pooled = pooled.sort_values("delta", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = []
    for _, row in pooled.iterrows():
        if row["sid"] == 2634260:
            colors.append(ACCENT_RED)
        elif row["delta"] > 0:
            colors.append(CHART_GREEN)
        else:
            colors.append(CHART_AMBER)

    bars = ax.barh(pooled["label"], pooled["delta"], color=colors, height=0.6,
                   edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, pooled["delta"]):
        offset = 0.005 if val >= 0 else -0.005
        ha = "left" if val >= 0 else "right"
        ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
                f"{val:+.3f}", va="center", ha=ha, fontsize=9, fontweight="bold",
                color=GRAY_DARK)

    ax.axvline(0, color=GRAY_DARK, linewidth=0.8)
    style_ax(ax, "IM-Window Recovery: MI Affluent Peers",
             subtitle="Change in G6+G7 math scores from pre-IM (2022-23) to post-IM (2024-25)",
             xlabel="Change in grade levels (cs_mn_all)")
    ax.set_xlim(min(pooled["delta"]) - 0.05, max(pooled["delta"]) + 0.07)
    savefig(fig, "chart03_im_window_ranking.png")


# ======================================================================
#  CHART 4: Level-Matched Peers Histogram
# ======================================================================
def chart04_level_matched_histogram():
    print("Chart 04: Level-matched peers histogram...")
    # Use the im_delta column from peers file (IM-window delta: 2022-23 -> 2024-25)
    pf = peers.dropna(subset=["im_delta"]).copy()
    troy_row = pf[pf["sid"] == 2634260].iloc[0]
    troy_im = troy_row["im_delta"]

    # Compute rank: sort ascending by im_delta, Troy's 1-indexed position
    # = number of peers with worse (lower) IM-window delta + 1.
    # The user's analysis established Troy at rank 197/295 (67th percentile),
    # meaning 197 of 295 peers had a worse IM-window recovery than Troy.
    pf_sorted = pf.sort_values("im_delta", ascending=True).reset_index(drop=True)
    troy_pos = pf_sorted[pf_sorted["sid"] == 2634260].index[0] + 1
    n_peers = len(pf_sorted)
    # Use data-computed rank/percentile
    troy_rank = troy_pos
    pct = round(troy_rank / n_peers * 100)

    fig, ax = plt.subplots(figsize=(12, 6))
    bins = np.linspace(pf["im_delta"].min() - 0.02, pf["im_delta"].max() + 0.02, 40)
    ax.hist(pf["im_delta"], bins=bins, color=CHART_BLUE, alpha=0.7,
            edgecolor="white", linewidth=0.5)

    # Troy vertical line
    ax.axvline(troy_im, color=ACCENT_RED, linewidth=2.5, linestyle="--", zorder=10)
    ylim = ax.get_ylim()
    ax.text(troy_im + 0.008, ylim[1] * 0.92,
            f"Troy: {troy_im:+.3f}\nRank {troy_rank}/{n_peers}\n({pct}th percentile)",
            fontsize=9, color=ACCENT_RED, fontweight="bold", va="top")

    style_ax(ax, "Troy Among Level-Matched Peers: IM-Window Recovery",
             subtitle=f"{n_peers} districts with similar pre-COVID math levels (within +/-0.25 GL of Troy)",
             ylabel="Number of districts",
             xlabel="IM-window delta (2022-23 to 2024-25)")
    savefig(fig, "chart04_level_matched_histogram.png")


# ======================================================================
#  CHART 5: Asian Subgroup G6 Trend
# ======================================================================
def chart05_asian_g6_trend():
    print("Chart 05: Asian subgroup G6 trend...")
    g6 = df[(df["grade"] == 6) & (df["sedaadmin"].isin(ASIAN_COMP.keys()))].copy()
    g6 = g6[g6["year"] >= 2015]

    fig, ax = plt.subplots(figsize=(12, 7))
    comp_colors = {
        2634260: ACCENT_RED,
        2626130: CHART_BLUE,
        5300390: "#6E8FAD",
        5303750: "#8DA8C2",
        3417700: ACCENT_ORANGE,
        4815210: "#5B8A72",
    }
    for sid, label in ASIAN_COMP.items():
        sub = g6[g6["sedaadmin"] == sid].sort_values("year")
        sub = sub.dropna(subset=["cs_mn_asn"])
        if sub.empty:
            continue
        lw = 2.8 if sid == 2634260 else 1.5
        ms = 5 if sid == 2634260 else 3
        zord = 10 if sid == 2634260 else 5
        ax.plot(sub["year"], sub["cs_mn_asn"], color=comp_colors[sid],
                linewidth=lw, marker="o", markersize=ms, label=label, zorder=zord)

    add_covid_shade(ax)
    style_ax(ax, "Grade 6 Math: Asian Subgroup, Troy vs. High-Asian Peers",
             subtitle="SEDA 2025.1 Asian subgroup (cs_mn_asn), 2015-2025",
             ylabel="Grade levels above national norm",
             xlabel="School year (spring)")
    ax.set_xticks(range(2015, 2026))
    ax.legend(fontsize=8, loc="lower left", framealpha=0.9, edgecolor=GRAY_LIGHT)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%+.1f"))
    savefig(fig, "chart05_asian_g6_trend.png")


# ======================================================================
#  CHART 6: Asian Subgroup G7 Trend
# ======================================================================
def chart06_asian_g7_trend():
    print("Chart 06: Asian subgroup G7 trend...")
    g7 = df[(df["grade"] == 7) & (df["sedaadmin"].isin(ASIAN_COMP.keys()))].copy()
    g7 = g7[g7["year"] >= 2015]

    fig, ax = plt.subplots(figsize=(12, 7))
    comp_colors = {
        2634260: ACCENT_RED,
        2626130: CHART_BLUE,
        5300390: "#6E8FAD",
        5303750: "#8DA8C2",
        3417700: ACCENT_ORANGE,
        4815210: "#5B8A72",
    }
    for sid, label in ASIAN_COMP.items():
        sub = g7[g7["sedaadmin"] == sid].sort_values("year")
        sub = sub.dropna(subset=["cs_mn_asn"])
        if sub.empty:
            continue
        lw = 2.8 if sid == 2634260 else 1.5
        ms = 5 if sid == 2634260 else 3
        zord = 10 if sid == 2634260 else 5
        ax.plot(sub["year"], sub["cs_mn_asn"], color=comp_colors[sid],
                linewidth=lw, marker="o", markersize=ms, label=label, zorder=zord)

    add_covid_shade(ax)
    style_ax(ax, "Grade 7 Math: Asian Subgroup, Troy vs. High-Asian Peers",
             subtitle="SEDA 2025.1 Asian subgroup (cs_mn_asn), 2015-2025",
             ylabel="Grade levels above national norm",
             xlabel="School year (spring)")
    ax.set_xticks(range(2015, 2026))
    ax.legend(fontsize=8, loc="lower left", framealpha=0.9, edgecolor=GRAY_LIGHT)
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%+.1f"))
    savefig(fig, "chart06_asian_g7_trend.png")


# ======================================================================
#  CHART 7: Troy Subgroup Waterfall (Pre-COVID vs Post-COVID)
# ======================================================================
def chart07_troy_subgroup_waterfall():
    print("Chart 07: Troy subgroup waterfall...")
    troy = df[df["sedaadmin"] == 2634260].copy()
    subgroups = {
        "All": "cs_mn_all",
        "Asian": "cs_mn_asn",
        "White": "cs_mn_wht",
        "ECD": "cs_mn_ecd",
        "Not ECD": "cs_mn_nec",
    }

    pre_vals = {}
    post_vals = {}
    for label, col in subgroups.items():
        # Pre-COVID: 2017-2019, G6+G7 pooled
        pre = troy[troy["year"].isin([2017, 2018, 2019])][col].mean()
        # Post-COVID: 2022-2025, G6+G7 pooled
        post = troy[troy["year"].isin([2022, 2023, 2024, 2025])][col].mean()
        pre_vals[label] = pre
        post_vals[label] = post

    labels = list(subgroups.keys())
    pre_arr = [pre_vals[l] for l in labels]
    post_arr = [post_vals[l] for l in labels]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bars_pre = ax.bar(x - width / 2, pre_arr, width, label="Pre-COVID (2017-19)",
                      color=TROY_BLUE, edgecolor="white", linewidth=0.5)
    bars_post = ax.bar(x + width / 2, post_arr, width, label="Post-COVID (2022-25)",
                       color=CHART_AMBER, edgecolor="white", linewidth=0.5)

    # Add delta labels
    for i, (pre, post) in enumerate(zip(pre_arr, post_arr)):
        if pd.notna(pre) and pd.notna(post):
            delta = post - pre
            color = ACCENT_GREEN if delta >= 0 else ACCENT_RED
            y_pos = max(pre, post) + 0.04
            ax.text(x[i], y_pos, f"{delta:+.2f}", ha="center", va="bottom",
                    fontsize=9, fontweight="bold", color=color)

    # Value labels on bars
    for bar in bars_pre:
        h = bar.get_height()
        if pd.notna(h):
            ax.text(bar.get_x() + bar.get_width() / 2, h - 0.05,
                    f"{h:+.2f}", ha="center", va="top", fontsize=7.5,
                    color="white", fontweight="bold")
    for bar in bars_post:
        h = bar.get_height()
        if pd.notna(h):
            ax.text(bar.get_x() + bar.get_width() / 2, h - 0.05,
                    f"{h:+.2f}", ha="center", va="top", fontsize=7.5,
                    color="white", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.axhline(0, color=GRAY_LIGHT, linewidth=0.8, linestyle="--")
    style_ax(ax, "Troy SD: Math Scores by Subgroup, Pre- vs. Post-COVID",
             subtitle="G6+G7 pooled; SEDA cohort-standardized mean (grade levels above national norm)",
             ylabel="Grade levels above national norm")
    ax.legend(fontsize=9, loc="upper right", framealpha=0.9, edgecolor=GRAY_LIGHT)
    savefig(fig, "chart07_troy_subgroup_waterfall.png")


# ======================================================================
#  CHART 8: M-STEP Troy Proficiency
# ======================================================================
def chart08_mstep_troy_proficiency():
    print("Chart 08: M-STEP Troy proficiency...")
    years = ["2018-19", "2022-23", "2023-24", "2024-25"]
    troy_g6 = [71.4, 63.2, 66.3, 65.8]
    troy_g7 = [67.5, 61.3, 66.0, None]
    state_g6 = [35.1, 29.6, 31.0, 32.2]
    state_g7 = [35.7, 31.0, 32.1, 32.8]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

    datasets = [
        (axes[0], troy_g6, state_g6, "Grade 6"),
        (axes[1], troy_g7, state_g7, "Grade 7"),
    ]

    for ax, troy_data, state_data, grade_label in datasets:
        x = np.arange(len(years))
        width = 0.35

        # Handle None for missing data
        troy_plot = [v if v is not None else 0 for v in troy_data]
        state_plot = [v if v is not None else 0 for v in state_data]

        bars_troy = ax.bar(x - width / 2, troy_plot, width,
                           label="Troy", color=TROY_BLUE,
                           edgecolor="white", linewidth=0.5)
        bars_state = ax.bar(x + width / 2, state_plot, width,
                            label="State avg", color=GRAY_LIGHT,
                            edgecolor=GRAY_MID, linewidth=0.5)

        # Mark missing data
        for i, v in enumerate(troy_data):
            if v is None:
                ax.text(x[i] - width / 2, 2, "N/A", ha="center",
                        fontsize=8, color=GRAY_MID, style="italic")

        # Value labels
        for bars, vals in [(bars_troy, troy_data), (bars_state, state_data)]:
            for bar, v in zip(bars, vals):
                if v is not None and v > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() + 1,
                            f"{v:.1f}%", ha="center", va="bottom",
                            fontsize=8, fontweight="bold",
                            color=GRAY_DARK)

        # IM adoption annotation on 2023-24
        im_idx = 2  # 2023-24
        ax.annotate("IM adopted",
                    xy=(im_idx - width / 2, troy_plot[im_idx] + 4),
                    xytext=(im_idx - width / 2, troy_plot[im_idx] + 12),
                    fontsize=8, color=ACCENT_RED, fontweight="bold",
                    ha="center",
                    arrowprops=dict(arrowstyle="->", color=ACCENT_RED,
                                    lw=1.5))

        ax.set_xticks(x)
        ax.set_xticklabels(years, fontsize=9)
        ax.set_ylim(0, 85)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(GRAY_LIGHT)
        ax.spines["bottom"].set_color(GRAY_LIGHT)

    axes[0].set_ylabel("% Proficient", fontsize=10, color=GRAY_MID)
    axes[1].legend(fontsize=9, loc="upper right", framealpha=0.9,
                   edgecolor=GRAY_LIGHT)

    fig.tight_layout()
    savefig(fig, "chart08_mstep_troy_proficiency.png")


# ======================================================================
#  CHART 9: COVID-Delta Ranking (All 22 Districts)
# ======================================================================
def chart09_covid_delta_ranking():
    print("Chart 09: COVID-delta ranking (22 districts)...")
    results = []
    for sid, label in ALL_DISTRICTS.items():
        dists = df[df["sedaadmin"] == sid]
        deltas = []
        for grade in [6, 7]:
            gd = dists[dists["grade"] == grade]
            pre = gd[gd["year"].isin([2017, 2018, 2019])]["cs_mn_all"].mean()
            post = gd[gd["year"].isin([2022, 2023, 2024, 2025])]["cs_mn_all"].mean()
            if pd.notna(pre) and pd.notna(post):
                deltas.append(post - pre)
        if deltas:
            results.append({"sid": sid, "label": label, "delta": np.mean(deltas)})

    rdf = pd.DataFrame(results).sort_values("delta", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    colors = [ACCENT_RED if r["sid"] == 2634260 else CHART_BLUE
              for _, r in rdf.iterrows()]
    bars = ax.barh(rdf["label"], rdf["delta"], color=colors, height=0.65,
                   edgecolor="white", linewidth=0.5)

    for bar, (_, row) in zip(bars, rdf.iterrows()):
        val = row["delta"]
        offset = 0.005 if val >= 0 else -0.005
        ha = "left" if val >= 0 else "right"
        fw = "bold" if row["sid"] == 2634260 else "normal"
        ax.text(val + offset, bar.get_y() + bar.get_height() / 2,
                f"{val:+.3f}", va="center", ha=ha, fontsize=8, fontweight=fw,
                color=GRAY_DARK)

    ax.axvline(0, color=GRAY_DARK, linewidth=0.8)
    style_ax(ax, "Pre/Post-COVID Math Delta: All Analysis Districts",
             subtitle="G6+G7 pooled; pre=mean(2017-19), post=mean(2022-25); SEDA cs_mn_all",
             xlabel="Change in grade levels above national norm")
    savefig(fig, "chart09_covid_delta_ranking.png")


# ======================================================================
#  CHART 10: High-Asian Peers Delta (Lollipop/Dot Plot)
# ======================================================================
def chart10_high_asian_peers_delta():
    print("Chart 10: High-Asian peers delta (lollipop)...")
    # Filter peers with >=20% Asian enrollment
    ha = peers[peers["asn_share"] >= 0.20].copy()
    ha = ha.sort_values("delta", ascending=True).reset_index(drop=True)

    troy_idx = ha[ha["sid"] == 2634260].index[0]
    troy_delta = ha.loc[troy_idx, "delta"]
    n_total = len(ha)

    # Select which districts to show: top 20, bottom 10, and Troy's neighborhood
    show_top = list(range(max(0, n_total - 20), n_total))  # top 20 (highest delta)
    show_bottom = list(range(min(10, n_total)))  # bottom 10 (worst delta)
    show_troy = list(range(max(0, troy_idx - 2), min(n_total, troy_idx + 3)))
    show = sorted(set(show_top + show_bottom + show_troy))

    ha_show = ha.loc[show].copy()
    # Create short labels
    ha_show["short"] = ha_show.apply(
        lambda r: f"{r['name'][:30]} ({r['state']})", axis=1)

    fig, ax = plt.subplots(figsize=(12, max(8, len(ha_show) * 0.3)))
    y_pos = np.arange(len(ha_show))

    colors = []
    for _, row in ha_show.iterrows():
        if row["sid"] == 2634260:
            colors.append(ACCENT_RED)
        elif row["delta"] >= 0:
            colors.append(CHART_GREEN)
        else:
            colors.append(CHART_AMBER)

    # Lollipop stems
    for i, (_, row) in enumerate(ha_show.iterrows()):
        ax.plot([0, row["delta"]], [i, i], color=colors[i], linewidth=1.2, zorder=3)

    # Dots
    ax.scatter(ha_show["delta"], y_pos, c=colors, s=60, zorder=5, edgecolor="white",
               linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(ha_show["short"], fontsize=7.5)
    ax.axvline(0, color=GRAY_DARK, linewidth=0.8)

    # Annotate Troy
    troy_y = y_pos[ha_show["sid"].values == 2634260][0]
    ax.annotate(f"Troy: {troy_delta:+.3f}\n(rank {troy_idx+1}/{n_total})",
                xy=(troy_delta, troy_y), xytext=(troy_delta + 0.08, troy_y + 1.5),
                fontsize=9, color=ACCENT_RED, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.5))

    # Add gap markers where indices are not contiguous
    prev_orig_idx = None
    for i, orig_idx in enumerate(show):
        if prev_orig_idx is not None and orig_idx > prev_orig_idx + 1:
            gap_count = orig_idx - prev_orig_idx - 1
            ax.axhline(i - 0.5, color=GRAY_LIGHT, linewidth=0.5, linestyle=":")
            ax.text(ax.get_xlim()[0] + 0.01, i - 0.5,
                    f"  ... {gap_count} districts ...",
                    fontsize=7, color=GRAY_MID, va="center", style="italic")
        prev_orig_idx = orig_idx

    style_ax(ax, "High-Asian Peer Districts: Pre/Post-COVID Math Delta",
             subtitle=f"{n_total} districts with >=20% Asian enrollment and pre-COVID math >=+0.50",
             xlabel="Change in grade levels (pre-COVID to post-COVID)")
    savefig(fig, "chart10_high_asian_peers_delta.png")


# ======================================================================
#  CHART 11: Rank-Shift Scatter (Pre vs Post COVID rank)
# ======================================================================
def chart11_rank_shift_scatter():
    print("Chart 11: Rank-shift scatter...")
    p = peers.copy()
    p["pre_rank"] = p["pre_avg"].rank(ascending=False).astype(int)
    p["post_rank"] = p["post_avg"].rank(ascending=False).astype(int)

    troy_row = p[p["name"].str.contains("Troy School District")]
    troy_pre = troy_row["pre_rank"].values[0]
    troy_post = troy_row["post_rank"].values[0]

    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    ax.scatter(p["pre_rank"], p["post_rank"], s=25, alpha=0.45,
               color=CHART_BLUE, edgecolors="white", linewidths=0.3, zorder=3)
    ax.plot([1, 296], [1, 296], ls="--", color=GRAY_LIGHT, lw=1, zorder=1)
    ax.scatter([troy_pre], [troy_post], s=90, color=ACCENT_RED,
               edgecolors="white", linewidths=1.2, zorder=5)
    ax.annotate(f"Troy: #{troy_pre} → #{troy_post}\n(lost {troy_post - troy_pre} positions)",
                xy=(troy_pre, troy_post), xytext=(troy_pre + 35, troy_post - 30),
                fontsize=10, fontweight="bold", color=ACCENT_RED,
                arrowprops=dict(arrowstyle="->", color=ACCENT_RED, lw=1.5))
    ax.text(0.97, 0.05, "Rise in ranking\n(above diagonal)",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=8, color=GRAY_MID, style="italic")
    ax.text(0.03, 0.95, "Fall in ranking\n(below diagonal)",
            transform=ax.transAxes, ha="left", va="top",
            fontsize=8, color=GRAY_MID, style="italic")
    ax.set_xlabel("Pre-COVID Rank (1 = highest math)", fontsize=10, color=GRAY_MID)
    ax.set_ylabel("Post-COVID Rank (1 = highest math)", fontsize=10, color=GRAY_MID)
    ax.set_xlim(0, 300)
    ax.set_ylim(0, 300)
    ax.invert_yaxis()
    ax.invert_xaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRAY_LIGHT)
    ax.spines["bottom"].set_color(GRAY_LIGHT)
    ax.tick_params(labelsize=9)
    savefig(fig, "chart11_rank_shift_scatter.png")


# ======================================================================
#  CHART 12: MI Peer Bump Chart (Sankey-style ranking flow)
# ======================================================================
def chart12_mi_peer_bump():
    print("Chart 12: MI peer bump chart...")
    mi = df[df["sedaadmin"].isin(MI_PEERS.keys())].copy()
    mi["label"] = mi["sedaadmin"].map(MI_PEERS)

    g67 = mi[mi["grade"].isin([6, 7])]
    pre = g67[g67["year"].between(2017, 2019)].groupby("label")["cs_mn_all"].mean()
    post = g67[g67["year"].between(2022, 2025)].groupby("label")["cs_mn_all"].mean()

    pre_rank = pre.rank(ascending=False).astype(int)
    post_rank = post.rank(ascending=False).astype(int)

    districts = pre_rank.sort_values().index.tolist()
    n = len(districts)

    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(0.5, n + 0.5)
    ax.invert_yaxis()
    ax.axis("off")

    ax.text(0, 0.2, "Pre-COVID (2017–19)", ha="center", fontsize=11,
            fontweight="bold", color=GRAY_DARK, transform=ax.transData)
    ax.text(1, 0.2, "Post-COVID (2022–25)", ha="center", fontsize=11,
            fontweight="bold", color=GRAY_DARK, transform=ax.transData)

    from matplotlib.path import Path
    import matplotlib.patches as mpatches

    for d in districts:
        y1 = pre_rank[d]
        y2 = post_rank[d]
        is_troy = (d == "Troy")
        clr = ACCENT_RED if is_troy else GRAY_LIGHT
        lw = 3.5 if is_troy else 1.5
        alpha = 1.0 if is_troy else 0.6

        verts = [(0.08, y1), (0.35, y1), (0.65, y2), (0.92, y2)]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        path = Path(verts, codes)
        patch = mpatches.FancyArrowPatch(
            path=path, arrowstyle="-", color=clr, lw=lw, alpha=alpha, zorder=4 if is_troy else 2)
        ax.add_patch(patch)

        delta = int(y2 - y1)
        delta_str = f"(↓{abs(delta)})" if delta > 0 else f"(↑{abs(delta)})" if delta < 0 else "(±0)"
        weight = "bold" if is_troy else "normal"
        tclr = ACCENT_RED if is_troy else GRAY_DARK

        ax.text(-0.02, y1, f"{int(y1)}. {d}", ha="right", va="center",
                fontsize=10, fontweight=weight, color=tclr)
        ax.text(1.02, y2, f"{int(y2)}. {d}  {delta_str}", ha="left", va="center",
                fontsize=10, fontweight=weight, color=tclr)

    savefig(fig, "chart12_mi_peer_bump.png")


# ======================================================================
#  Main
# ======================================================================
if __name__ == "__main__":
    print(f"Data loaded: {len(df)} rows (subset), {len(peers)} rows (peers)")
    print(f"Output directory: {CHART_DIR}\n")

    chart01_mi_peers_g6_trend()
    chart02_mi_peers_g7_trend()
    chart03_im_window_ranking()
    chart04_level_matched_histogram()
    chart05_asian_g6_trend()
    chart06_asian_g7_trend()
    chart07_troy_subgroup_waterfall()
    chart08_mstep_troy_proficiency()
    chart09_covid_delta_ranking()
    chart10_high_asian_peers_delta()
    chart11_rank_shift_scatter()
    chart12_mi_peer_bump()

    print(f"\nAll charts saved to {CHART_DIR}")
