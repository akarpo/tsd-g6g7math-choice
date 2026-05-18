#!/usr/bin/env python3
"""
SEDA national ranking analysis for Troy SD — G6+G7 Math
Computes:
  1. National ranking trajectory (2019, 2022–2025)
  2. Level-matched peer ranking (296 peers, pre vs post)
  3. MI affluent peer rank shifts among the 296 peers
  4. Scatter plot: 2019 vs 2025 scores for 296 peers
"""

import pathlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── paths ─────────────────────────────────────────────────────────────────
BASE = pathlib.Path("/Users/Alex/Downloads/tsd-g6g7math-choice")
SEDA_CSV = BASE / "seda_admindist_long_cs_2025.1.csv"
PEERS_CSV = BASE / "data" / "seda_math_peers_full.csv"
CHART_DIR = BASE / "charts"
CHART_DIR.mkdir(exist_ok=True)

TROY = 2634260
YEARS = [2019, 2022, 2023, 2024, 2025]

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

# ── load SEDA (only needed columns) ──────────────────────────────────────
print("Loading SEDA data …")
cols = ["sedaadmin", "sedaadminname", "subject", "grade", "year", "cs_mn_all"]
seda = pd.read_csv(SEDA_CSV, usecols=cols)

# filter to math, grades 6 & 7
mth = seda[(seda["subject"] == "mth") & (seda["grade"].isin([6, 7]))].copy()
mth = mth.dropna(subset=["cs_mn_all"])

# ── helper: compute district-level G6+G7 average per year ────────────────
def district_year_avg(df, year):
    """Return a DataFrame with one row per district that has BOTH G6 and G7."""
    sub = df[df["year"] == year]
    # keep only districts with both grades
    gcounts = sub.groupby("sedaadmin")["grade"].nunique()
    both = gcounts[gcounts == 2].index
    sub = sub[sub["sedaadmin"].isin(both)]
    avg = (
        sub.groupby(["sedaadmin", "sedaadminname"])["cs_mn_all"]
        .mean()
        .reset_index()
        .rename(columns={"cs_mn_all": "avg_score"})
    )
    return avg


# ══════════════════════════════════════════════════════════════════════════
# 1. National G6+G7 Math ranking trajectory
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("1. NATIONAL G6+G7 MATH RANKING TRAJECTORY")
print("=" * 70)
print(f"{'Year':>6}  {'Troy Score':>11}  {'Rank':>6}  {'Total':>7}  {'Percentile':>11}")
print("-" * 50)

for yr in YEARS:
    avg = district_year_avg(mth, yr)
    avg["rank"] = avg["avg_score"].rank(ascending=False, method="min").astype(int)
    total = len(avg)
    troy_row = avg[avg["sedaadmin"] == TROY]
    if troy_row.empty:
        print(f"{yr:>6}  {'N/A':>11}")
        continue
    score = troy_row["avg_score"].values[0]
    rank = troy_row["rank"].values[0]
    pctile = (1 - (rank - 1) / total) * 100
    print(f"{yr:>6}  {score:>11.4f}  {rank:>6}  {total:>7,}  {pctile:>10.1f}%")

# ══════════════════════════════════════════════════════════════════════════
# 2. Level-matched peer ranking (296 peers)
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("2. LEVEL-MATCHED PEER RANKING (296 peers)")
print("=" * 70)

peers = pd.read_csv(PEERS_CSV)
peer_ids = set(peers["sid"].values)

# Use the pre_avg / post_avg already in the peers file
peers["pre_rank"] = peers["pre_avg"].rank(ascending=False, method="min").astype(int)
peers["post_rank"] = peers["post_avg"].rank(ascending=False, method="min").astype(int)

troy_peer = peers[peers["sid"] == TROY].iloc[0]
print(f"Pre-COVID (2019)  score: {troy_peer['pre_avg']:.4f}   rank: {int(troy_peer['pre_rank'])} / {len(peers)}")
print(f"Post-COVID (2025) score: {troy_peer['post_avg']:.4f}   rank: {int(troy_peer['post_rank'])} / {len(peers)}")
print(f"Rank shift: {int(troy_peer['pre_rank']) - int(troy_peer['post_rank']):+d}  (positive = improved)")

# How many districts leapfrogged Troy?
# "Leapfrogged" = were ranked below Troy pre-COVID but above Troy post-COVID
leapfrogged = peers[
    (peers["pre_rank"] > troy_peer["pre_rank"]) &
    (peers["post_rank"] < troy_peer["post_rank"])
]
print(f"\nDistricts that leapfrogged Troy: {len(leapfrogged)}")
if len(leapfrogged) > 0:
    top_leap = leapfrogged.sort_values("post_rank").head(10)
    print(f"  {'District':<42} {'State':<6} {'Pre Rank':>9} {'Post Rank':>10}")
    print("  " + "-" * 70)
    for _, r in top_leap.iterrows():
        print(f"  {r['name']:<42} {r['state']:<6} {int(r['pre_rank']):>9} {int(r['post_rank']):>10}")

# ══════════════════════════════════════════════════════════════════════════
# 3. MI affluent peer rank shifts among 296 peers
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("3. MI AFFLUENT PEER RANK SHIFTS (among 296 level-matched peers)")
print("=" * 70)

# Some MI districts may not be in the 296-peer set; compute their scores
# from SEDA and rank them within the peer distribution.

# First get 2019 and 2025 G6+G7 averages from SEDA for all MI peers
avg_2019 = district_year_avg(mth, 2019).rename(columns={"avg_score": "score_2019"})
avg_2025 = district_year_avg(mth, 2025).rename(columns={"avg_score": "score_2025"})

mi_data = []
for sid, name in MI_PEERS.items():
    row = {"sid": sid, "name": name}
    # 2019 score
    s19 = avg_2019[avg_2019["sedaadmin"] == sid]
    row["score_2019"] = s19["score_2019"].values[0] if len(s19) else np.nan
    # 2025 score
    s25 = avg_2025[avg_2025["sedaadmin"] == sid]
    row["score_2025"] = s25["score_2025"].values[0] if len(s25) else np.nan

    # rank among the 296 peers using pre_avg and post_avg columns
    if sid in peer_ids:
        p = peers[peers["sid"] == sid].iloc[0]
        row["pre_rank"] = int(p["pre_rank"])
        row["post_rank"] = int(p["post_rank"])
    else:
        # rank by insertion: count how many peers score higher
        if not np.isnan(row["score_2019"]):
            row["pre_rank"] = int((peers["pre_avg"] > row["score_2019"]).sum()) + 1
        else:
            row["pre_rank"] = np.nan
        if not np.isnan(row["score_2025"]):
            row["post_rank"] = int((peers["post_avg"] > row["score_2025"]).sum()) + 1
        else:
            row["post_rank"] = np.nan

    mi_data.append(row)

mi_df = pd.DataFrame(mi_data)
mi_df["rank_shift"] = mi_df["pre_rank"] - mi_df["post_rank"]  # positive = improved

print(f"{'District':<22} {'2019 Score':>11} {'2025 Score':>11} {'Pre Rank':>9} {'Post Rank':>10} {'Shift':>7}")
print("-" * 75)
for _, r in mi_df.sort_values("rank_shift").iterrows():
    pre_r = f"{int(r['pre_rank'])}" if not np.isnan(r['pre_rank']) else "N/A"
    post_r = f"{int(r['post_rank'])}" if not np.isnan(r['post_rank']) else "N/A"
    shift = f"{int(r['rank_shift']):+d}" if not np.isnan(r['rank_shift']) else "N/A"
    s19 = f"{r['score_2019']:.4f}" if not np.isnan(r['score_2019']) else "N/A"
    s25 = f"{r['score_2025']:.4f}" if not np.isnan(r['score_2025']) else "N/A"
    marker = " ◄ Troy" if r["sid"] == TROY else ""
    print(f"{r['name']:<22} {s19:>11} {s25:>11} {pre_r:>9} {post_r:>10} {shift:>7}{marker}")

# ══════════════════════════════════════════════════════════════════════════
# 4. Scatter plot — 296 peers, 2019 vs 2025
# ══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("4. SCATTER PLOT — 296 peers, 2019 vs 2025")
print("=" * 70)

# Use pre_avg and post_avg from peers file (already G6+G7 averages)
others = peers[peers["sid"] != TROY]
troy_pt = peers[peers["sid"] == TROY].iloc[0]

fig, ax = plt.subplots(figsize=(10, 7))
fig.set_facecolor("#F8F8F8")
ax.set_facecolor("#F8F8F8")

# Reference line y=x
lo = min(peers["pre_avg"].min(), peers["post_avg"].min()) - 0.05
hi = max(peers["pre_avg"].max(), peers["post_avg"].max()) + 0.05
ax.plot([lo, hi], [lo, hi], color="#CCCCCC", linestyle="--", linewidth=1, zorder=1)

# Peer dots
ax.scatter(
    others["pre_avg"], others["post_avg"],
    c="#6B9BD2", alpha=0.5, s=20, edgecolors="none", zorder=5,
    label="Level-matched peers"
)

# Troy diamond
ax.scatter(
    troy_pt["pre_avg"], troy_pt["post_avg"],
    c="#B02121", s=100, marker="D", zorder=10, edgecolors="none",
    label="Troy SD"
)

ax.set_xlabel("2019 G6+G7 Math score (cohort-standardised)", fontsize=11, fontfamily="sans-serif")
ax.set_ylabel("2025 G6+G7 Math score (cohort-standardised)", fontsize=11, fontfamily="sans-serif")
ax.set_title("Pre- vs. post-IM absolute level — 296 peers (2019 → 2025)",
             fontsize=13, fontfamily="sans-serif", fontweight="bold")
ax.legend(loc="upper left", fontsize=9, frameon=True, facecolor="white", edgecolor="#CCCCCC")

ax.set_xlim(lo, hi)
ax.set_ylim(lo, hi)
ax.set_aspect("equal")
ax.grid(True, color="#E0E0E0", linewidth=0.5)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
out_path = CHART_DIR / "chart_seda_scatter_math.png"
fig.savefig(out_path, dpi=200, facecolor=fig.get_facecolor())
plt.close()
print(f"Saved scatter plot → {out_path}")

# ── summary stats for the scatter ────────────────────────────────────────
above_line = peers[peers["post_avg"] >= peers["pre_avg"]]
below_line = peers[peers["post_avg"] < peers["pre_avg"]]
print(f"Districts above y=x line (improved): {len(above_line)}")
print(f"Districts below y=x line (declined): {len(below_line)}")
print(f"Troy 2019: {troy_pt['pre_avg']:.4f}   Troy 2025: {troy_pt['post_avg']:.4f}   Δ = {troy_pt['post_avg'] - troy_pt['pre_avg']:.4f}")

print("\n✓ Analysis complete.")
