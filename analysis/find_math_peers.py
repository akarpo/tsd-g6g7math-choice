"""Find Troy's math peers from the full SEDA 2025.1 dataset.

Peer selection criteria:
1. Pre-COVID math G6+G7 cs_mn_all within ±0.25 of Troy's (~0.94)
2. Must have data for 2017-2019 AND 2022-2025
3. Minimum enrollment (>200 tested per grade)

Then rank all peers by post-COVID recovery to see where Troy falls.
"""
import csv
from collections import defaultdict

SEDA_FILE = "/Users/Alex/Downloads/tsd-g6g7math/seda_admindist_long_cs_2025.1.csv"

def safe_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None

def avg(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None

# Pass 1: Build district-level math G6+G7 time series
print("Scanning full SEDA file (426MB)...")
districts = defaultdict(lambda: defaultdict(dict))
# Key: sedaadmin -> grade -> year -> {cs_mn_all, cs_mn_asn, tot_asmt_all, ...}

row_count = 0
with open(SEDA_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row_count += 1
        if row["subject"] != "mth":
            continue
        if row["grade"] not in ("6", "7"):
            continue
        sid = row["sedaadmin"]
        gr = row["grade"]
        yr = row["year"]
        districts[sid][(gr, yr)] = {
            "name": row["sedaadminname"],
            "state": row["stateabb"],
            "cs_all": safe_float(row["cs_mn_all"]),
            "cs_asn": safe_float(row["cs_mn_asn"]),
            "cs_wht": safe_float(row["cs_mn_wht"]),
            "cs_ecd": safe_float(row["cs_mn_ecd"]),
            "cs_nec": safe_float(row["cs_mn_nec"]),
            "n_all": safe_float(row["tot_asmt_all"]),
            "n_asn": safe_float(row["tot_asmt_asn"]),
        }

print(f"Scanned {row_count} rows, found {len(districts)} districts with G6/G7 math data")

# Pass 2: Compute pre-COVID and post-COVID metrics for each district
results = []
for sid, data in districts.items():
    name = None
    state = None
    for k, v in data.items():
        name = v["name"]
        state = v["state"]
        break

    # Pre-COVID: 2017-2019 G6+G7 pooled
    pre_vals = []
    pre_n = []
    for gr in ("6", "7"):
        for yr in ("2017", "2018", "2019"):
            d = data.get((gr, yr))
            if d and d["cs_all"] is not None:
                pre_vals.append(d["cs_all"])
            if d and d["n_all"] is not None:
                pre_n.append(d["n_all"])
    pre_avg = avg(pre_vals) if len(pre_vals) >= 3 else None
    pre_n_avg = avg(pre_n) if pre_n else None

    # Post-COVID: 2022-2025 G6+G7 pooled
    post_vals = []
    for gr in ("6", "7"):
        for yr in ("2022", "2023", "2024", "2025"):
            d = data.get((gr, yr))
            if d and d["cs_all"] is not None:
                post_vals.append(d["cs_all"])
    post_avg = avg(post_vals) if len(post_vals) >= 3 else None

    # Pre-IM window: 2022-2023
    pre_im = []
    for gr in ("6", "7"):
        for yr in ("2022", "2023"):
            d = data.get((gr, yr))
            if d and d["cs_all"] is not None:
                pre_im.append(d["cs_all"])
    pre_im_avg = avg(pre_im) if pre_im else None

    # Post-IM window: 2024-2025
    post_im = []
    for gr in ("6", "7"):
        for yr in ("2024", "2025"):
            d = data.get((gr, yr))
            if d and d["cs_all"] is not None:
                post_im.append(d["cs_all"])
    post_im_avg = avg(post_im) if post_im else None

    # Asian subgroup pre-COVID
    asn_pre = []
    for gr in ("6", "7"):
        for yr in ("2017", "2018", "2019"):
            d = data.get((gr, yr))
            if d and d["cs_asn"] is not None:
                asn_pre.append(d["cs_asn"])
    asn_pre_avg = avg(asn_pre) if len(asn_pre) >= 2 else None

    asn_post = []
    for gr in ("6", "7"):
        for yr in ("2022", "2023", "2024", "2025"):
            d = data.get((gr, yr))
            if d and d["cs_asn"] is not None:
                asn_post.append(d["cs_asn"])
    asn_post_avg = avg(asn_post) if len(asn_post) >= 2 else None

    # Asian enrollment share
    asn_n_vals = [data.get((gr, yr), {}).get("n_asn")
                  for gr in ("6", "7") for yr in ("2018", "2019")]
    all_n_vals = [data.get((gr, yr), {}).get("n_all")
                  for gr in ("6", "7") for yr in ("2018", "2019")]
    asn_n = sum(v for v in asn_n_vals if v) if any(v for v in asn_n_vals) else 0
    all_n = sum(v for v in all_n_vals if v) if any(v for v in all_n_vals) else 0
    asn_share = asn_n / all_n if all_n > 0 else 0

    if pre_avg is not None and post_avg is not None:
        delta = post_avg - pre_avg
        im_delta = (post_im_avg - pre_im_avg) if (post_im_avg is not None and pre_im_avg is not None) else None
        asn_delta = (asn_post_avg - asn_pre_avg) if (asn_post_avg is not None and asn_pre_avg is not None) else None

        results.append({
            "sid": sid,
            "name": name,
            "state": state,
            "pre_avg": pre_avg,
            "post_avg": post_avg,
            "delta": delta,
            "im_delta": im_delta,
            "pre_n_avg": pre_n_avg,
            "asn_share": asn_share,
            "asn_pre": asn_pre_avg,
            "asn_post": asn_post_avg,
            "asn_delta": asn_delta,
        })

print(f"\n{len(results)} districts with complete pre/post-COVID data")

# Find Troy
troy = next(r for r in results if r["sid"] == "2634260")
print(f"\nTroy SD: pre={troy['pre_avg']:+.3f}, post={troy['post_avg']:+.3f}, "
      f"Δ={troy['delta']:+.3f}, IM-Δ={troy['im_delta']:+.3f}, "
      f"Asian share={troy['asn_share']:.1%}")

# === PEER SET 1: Similar pre-COVID math level (±0.25 of Troy's 0.937) ===
TROY_PRE = troy["pre_avg"]
MIN_N = 150  # minimum avg tested per grade-year
peers_level = [r for r in results
               if abs(r["pre_avg"] - TROY_PRE) <= 0.25
               and (r["pre_n_avg"] or 0) >= MIN_N]
peers_level.sort(key=lambda x: x["delta"])

print(f"\n\n{'='*110}")
print(f"PEER SET 1: Districts with pre-COVID G6+G7 math within ±0.25 of Troy ({TROY_PRE:+.3f})")
print(f"Enrollment ≥{MIN_N}/grade-year — {len(peers_level)} districts found")
print(f"{'='*110}")

troy_rank = next(i for i, r in enumerate(peers_level, 1) if r["sid"] == "2634260")
print(f"\nTroy rank: {troy_rank} of {len(peers_level)} (1=worst decline)")
print(f"\n{'Rank':<5} {'District':<45} {'State':>5} {'Pre':>8} {'Post':>8} {'Δ':>8} {'IM-Δ':>8} {'N':>6}")
print("-" * 100)
# Show top 10 worst, Troy's neighbors, and top 10 best
show_indices = (
    list(range(min(10, len(peers_level))))
    + list(range(max(0, troy_rank-4), min(len(peers_level), troy_rank+3)))
    + list(range(max(0, len(peers_level)-10), len(peers_level)))
)
show_indices = sorted(set(show_indices))
last_i = -1
for i in show_indices:
    if i > last_i + 1:
        print("  ...")
    r = peers_level[i]
    marker = " <<<" if r["sid"] == "2634260" else ""
    im_s = f"{r['im_delta']:+.3f}" if r["im_delta"] is not None else "  n/a "
    print(f" {i+1:<4} {r['name']:<45} {r['state']:>5} "
          f"{r['pre_avg']:+.3f}  {r['post_avg']:+.3f}  {r['delta']:+.3f}  {im_s}  "
          f"{r['pre_n_avg']:>5.0f}{marker}")
    last_i = i

# Percentile
pct = troy_rank / len(peers_level) * 100
print(f"\nTroy is at the {pct:.0f}th percentile (lower = worse decline)")

# === PEER SET 2: High-Asian enrollment (≥20%) with high pre-COVID math ===
peers_asian = [r for r in results
               if r["asn_share"] >= 0.20
               and r["pre_avg"] >= 0.5
               and (r["pre_n_avg"] or 0) >= 100]
peers_asian.sort(key=lambda x: x["delta"])

print(f"\n\n{'='*110}")
print(f"PEER SET 2: High-Asian (≥20%) districts with pre-COVID math ≥+0.50 — {len(peers_asian)} found")
print(f"{'='*110}")

troy_rank2 = next(i for i, r in enumerate(peers_asian, 1) if r["sid"] == "2634260")
print(f"\nTroy rank: {troy_rank2} of {len(peers_asian)}")
print(f"\n{'Rank':<5} {'District':<45} {'State':>5} {'Asian%':>7} {'Pre':>8} {'Post':>8} {'Δ':>8} {'AsnΔ':>8}")
print("-" * 105)
for i, r in enumerate(peers_asian):
    marker = " <<<" if r["sid"] == "2634260" else ""
    asn_d = f"{r['asn_delta']:+.3f}" if r["asn_delta"] is not None else "  n/a "
    print(f" {i+1:<4} {r['name']:<45} {r['state']:>5} {r['asn_share']:>6.1%}  "
          f"{r['pre_avg']:+.3f}  {r['post_avg']:+.3f}  {r['delta']:+.3f}  {asn_d}{marker}")

# === PEER SET 3: IM-Window Recovery Ranking (same level-matched set) ===
peers_im = [r for r in peers_level if r["im_delta"] is not None]
peers_im.sort(key=lambda x: x["im_delta"], reverse=True)

print(f"\n\n{'='*110}")
print(f"PEER SET 3: IM-Window Recovery (2022-23 → 2024-25) — Same level-matched peers")
print(f"{'='*110}")

troy_im_rank = next(i for i, r in enumerate(peers_im, 1) if r["sid"] == "2634260")
n_im = len(peers_im)
print(f"\nTroy rank: {troy_im_rank} of {n_im} (1=best recovery)")
pct_im = troy_im_rank / n_im * 100
print(f"Troy is at the {pct_im:.0f}th percentile (lower = better recovery)")

print(f"\n{'Rank':<5} {'District':<45} {'State':>5} {'IM-Δ':>8} {'Pre':>8}")
print("-" * 80)
show_im = (
    list(range(min(15, n_im)))
    + list(range(max(0, troy_im_rank-4), min(n_im, troy_im_rank+3)))
    + list(range(max(0, n_im-10), n_im))
)
show_im = sorted(set(show_im))
last_i = -1
for i in show_im:
    if i > last_i + 1:
        print("  ...")
    r = peers_im[i]
    marker = " <<<" if r["sid"] == "2634260" else ""
    print(f" {i+1:<4} {r['name']:<45} {r['state']:>5} "
          f"{r['im_delta']:+.3f}  {r['pre_avg']:+.3f}{marker}")
    last_i = i

# === Write full peer data to CSV ===
OUT = "/Users/Alex/Downloads/tsd-g6g7math/seda_math_peers_full.csv"
peers_level.sort(key=lambda x: x["delta"])
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["sid", "name", "state", "pre_avg", "post_avg",
                                       "delta", "im_delta", "pre_n_avg", "asn_share",
                                       "asn_pre", "asn_post", "asn_delta"])
    w.writeheader()
    for r in peers_level:
        w.writerow(r)
print(f"\n\nWrote {len(peers_level)} level-matched peers to {OUT}")
