"""Comprehensive SEDA 2025.1 Math Analysis: Troy SD vs. peers, G6 & G7.

Computes pre-COVID baselines, post-COVID trajectories, and the specific
IM adoption window (2024-2025) to evaluate whether Troy has outperformed
its characteristics.
"""
import csv
from collections import defaultdict

DATA = "/Users/Alex/Downloads/tsd-g6g7math/seda_math_g67_subset.csv"

DISTRICT_GROUPS = {
    "Troy SD (MI)": "MI Affluent Peers + Subject",
    "Bloomfield Hills (MI)": "MI Affluent Peers + Subject",
    "Birmingham (MI)": "MI Affluent Peers + Subject",
    "Northville (MI)": "MI Affluent Peers + Subject",
    "Novi (MI)": "MI Affluent Peers + Subject",
    "Rochester (MI)": "MI Affluent Peers + Subject",
    "Walled Lake (MI)": "MI Affluent Peers + Subject",
    "West Bloomfield (MI)": "MI Affluent Peers + Subject",
    "Coppell ISD (TX)": "High-Asian Demographic Peers",
    "Plano ISD (TX)": "High-Asian Demographic Peers",
    "West Windsor-Plainsboro (NJ)": "High-Asian Demographic Peers",
    "Millburn (NJ)": "High-Asian Demographic Peers",
    "Bellevue (WA)": "High-Asian Demographic Peers",
    "Issaquah (WA)": "High-Asian Demographic Peers",
    "Lake Washington (WA)": "High-Asian Demographic Peers",
    "San Francisco Unified (CA)": "Detracking Case Study",
    "Tuscaloosa City (AL)": "EdScorecard 2026 Math DOTR",
    "Jonesboro (AR)": "EdScorecard 2026 Math DOTR",
    "Eastern Carver County (MN)": "EdScorecard 2026 Math DOTR",
    "Clark County (NV)": "EdScorecard 2026 Math DOTR",
    "Upshur County (WV)": "EdScorecard 2026 Math DOTR",
    "William Penn (PA)": "EdScorecard 2026 Math DOTR",
}

# Load data
rows = []
with open(DATA) as f:
    for r in csv.DictReader(f):
        rows.append(r)

# Build lookup: (district, grade, year) -> row
lookup = {}
for r in rows:
    name = r["sedaadminname"]
    # Map to our short labels
    for sid, label in {
        "2634260": "Troy SD (MI)", "2606090": "Bloomfield Hills (MI)",
        "2605850": "Birmingham (MI)", "2625980": "Northville (MI)",
        "2626130": "Novi (MI)", "2629940": "Rochester (MI)",
        "2635160": "Walled Lake (MI)", "2635820": "West Bloomfield (MI)",
        "4815210": "Coppell ISD (TX)", "4835100": "Plano ISD (TX)",
        "3417700": "West Windsor-Plainsboro (NJ)", "3410200": "Millburn (NJ)",
        "634410": "San Francisco Unified (CA)",
        "103360": "Tuscaloosa City (AL)", "508280": "Jonesboro (AR)",
        "2708190": "Eastern Carver County (MN)", "3200060": "Clark County (NV)",
        "5401470": "Upshur County (WV)", "4226390": "William Penn (PA)",
        "5300390": "Bellevue (WA)", "5303750": "Issaquah (WA)",
        "5304230": "Lake Washington (WA)",
    }.items():
        if r["sedaadmin"] == sid:
            key = (label, r["grade"], r["year"])
            lookup[key] = r
            break


def safe_float(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def avg(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def compute_metrics(district):
    """Compute key metrics for a district across G6 and G7."""
    out = {}
    for grade in ("6", "7"):
        for subgroup, col in [("All", "cs_mn_all"), ("Asian", "cs_mn_asn"),
                               ("White", "cs_mn_wht"), ("ECD", "cs_mn_ecd"),
                               ("Black", "cs_mn_blk"), ("Hispanic", "cs_mn_hsp"),
                               ("NotECD", "cs_mn_nec")]:
            # Pre-COVID baseline: 2017-2019
            pre = avg([safe_float(lookup.get((district, grade, str(y)), {}).get(col))
                       for y in (2017, 2018, 2019)])
            # Post-COVID: 2022-2025
            post = avg([safe_float(lookup.get((district, grade, str(y)), {}).get(col))
                        for y in (2022, 2023, 2024, 2025)])
            # Pre-IM: 2022-2023 (post-COVID but before IM for Troy)
            pre_im = avg([safe_float(lookup.get((district, grade, str(y)), {}).get(col))
                          for y in (2022, 2023)])
            # Post-IM: 2024-2025
            post_im = avg([safe_float(lookup.get((district, grade, str(y)), {}).get(col))
                           for y in (2024, 2025)])
            # Individual years
            y2019 = safe_float(lookup.get((district, grade, "2019"), {}).get(col))
            y2023 = safe_float(lookup.get((district, grade, "2023"), {}).get(col))
            y2024 = safe_float(lookup.get((district, grade, "2024"), {}).get(col))
            y2025 = safe_float(lookup.get((district, grade, "2025"), {}).get(col))

            delta_covid = (post - pre) if (post is not None and pre is not None) else None
            delta_im = (post_im - pre_im) if (post_im is not None and pre_im is not None) else None

            out[(grade, subgroup)] = {
                "pre_covid": pre,
                "post_covid": post,
                "pre_im": pre_im,
                "post_im": post_im,
                "delta_covid": delta_covid,
                "delta_im": delta_im,
                "y2019": y2019,
                "y2023": y2023,
                "y2024": y2024,
                "y2025": y2025,
            }
    return out


# === ANALYSIS 1: All Students Pre/Post-COVID Delta Ranking ===
print("=" * 100)
print("ANALYSIS 1: Pre/Post-COVID Math Delta — All Students, G6+G7 Pooled")
print("Pre-COVID = mean(2017-2019), Post-COVID = mean(2022-2025)")
print("Metric: SEDA cs (grade-level units above national norm; 0 = national avg)")
print("=" * 100)

deltas = []
for district in DISTRICT_GROUPS:
    m = compute_metrics(district)
    d6 = m.get(("6", "All"), {}).get("delta_covid")
    d7 = m.get(("7", "All"), {}).get("delta_covid")
    pooled = avg([d6, d7])
    pre6 = m.get(("6", "All"), {}).get("pre_covid")
    pre7 = m.get(("7", "All"), {}).get("pre_covid")
    pre_pooled = avg([pre6, pre7])
    post6 = m.get(("6", "All"), {}).get("post_covid")
    post7 = m.get(("7", "All"), {}).get("post_covid")
    post_pooled = avg([post6, post7])
    deltas.append((district, pre_pooled, post_pooled, pooled, d6, d7))

deltas.sort(key=lambda x: x[3] if x[3] is not None else -99)

print(f"\n{'Rank':<5} {'District':<40} {'Pre-COVID':>10} {'Post-COVID':>11} {'Δ':>8} {'ΔG6':>8} {'ΔG7':>8} {'Group'}")
print("-" * 110)
for i, (d, pre, post, delta, d6, d7) in enumerate(deltas, 1):
    group = DISTRICT_GROUPS[d][:20]
    pre_s = f"{pre:+.3f}" if pre is not None else "n/a"
    post_s = f"{post:+.3f}" if post is not None else "n/a"
    delta_s = f"{delta:+.3f}" if delta is not None else "n/a"
    d6_s = f"{d6:+.3f}" if d6 is not None else "n/a"
    d7_s = f"{d7:+.3f}" if d7 is not None else "n/a"
    marker = " <<<" if "Troy" in d else ""
    print(f" {i:<4} {d:<40} {pre_s:>10} {post_s:>11} {delta_s:>8} {d6_s:>8} {d7_s:>8} {group}{marker}")


# === ANALYSIS 2: IM Adoption Window (2022-23 → 2024-25) ===
print("\n\n" + "=" * 100)
print("ANALYSIS 2: IM Adoption Window — Δ from Pre-IM (2022-23) to Post-IM (2024-25)")
print("For Troy, 2024 = first G6 IM cohort tested, 2025 = second G6 + first G7 IM")
print("For peers, this is the same time window (general recovery signal)")
print("=" * 100)

im_deltas = []
for district in DISTRICT_GROUPS:
    m = compute_metrics(district)
    d6 = m.get(("6", "All"), {}).get("delta_im")
    d7 = m.get(("7", "All"), {}).get("delta_im")
    pooled = avg([d6, d7])
    im_deltas.append((district, pooled, d6, d7))

im_deltas.sort(key=lambda x: x[1] if x[1] is not None else -99, reverse=True)

print(f"\n{'Rank':<5} {'District':<40} {'Δ Pooled':>10} {'ΔG6':>8} {'ΔG7':>8} {'Group'}")
print("-" * 90)
for i, (d, pooled, d6, d7) in enumerate(im_deltas, 1):
    group = DISTRICT_GROUPS[d][:20]
    ps = f"{pooled:+.3f}" if pooled is not None else "n/a"
    d6s = f"{d6:+.3f}" if d6 is not None else "n/a"
    d7s = f"{d7:+.3f}" if d7 is not None else "n/a"
    marker = " <<<" if "Troy" in d else ""
    print(f" {i:<4} {d:<40} {ps:>10} {d6s:>8} {d7s:>8} {group}{marker}")


# === ANALYSIS 3: Troy Subgroup Deep-Dive ===
print("\n\n" + "=" * 100)
print("ANALYSIS 3: Troy SD Subgroup Deep-Dive — Math G6 and G7")
print("=" * 100)

troy_m = compute_metrics("Troy SD (MI)")
for grade in ("6", "7"):
    print(f"\n  Grade {grade}:")
    print(f"  {'Subgroup':<20} {'2019':>8} {'2023':>8} {'2024':>8} {'2025':>8} {'Δ COVID':>9} {'Δ IM':>8}")
    print(f"  {'-'*75}")
    for sub in ("All", "Asian", "White", "Black", "Hispanic", "ECD", "NotECD"):
        vals = troy_m.get((grade, sub), {})
        y19 = vals.get("y2019")
        y23 = vals.get("y2023")
        y24 = vals.get("y2024")
        y25 = vals.get("y2025")
        dc = vals.get("delta_covid")
        di = vals.get("delta_im")
        fmt = lambda v: f"{v:+.3f}" if v is not None else "  n/a "
        print(f"  {sub:<20} {fmt(y19):>8} {fmt(y23):>8} {fmt(y24):>8} {fmt(y25):>8} {fmt(dc):>9} {fmt(di):>8}")


# === ANALYSIS 4: Year-by-Year Comparison — Troy vs MI Peers ===
print("\n\n" + "=" * 100)
print("ANALYSIS 4: Year-by-Year All Students — Troy vs MI Peers")
print("(cs_mn_all — grade levels above national norm)")
print("=" * 100)

mi_districts = [d for d, g in DISTRICT_GROUPS.items() if "MI" in g]

for grade in ("6", "7"):
    print(f"\n  Grade {grade}:")
    years = ["2017", "2018", "2019", "2022", "2023", "2024", "2025"]
    header = f"  {'District':<35}" + "".join(f"{y:>8}" for y in years) + f"{'Δ COVID':>9}"
    print(header)
    print(f"  {'-' * (35 + 8*len(years) + 9)}")
    for d in mi_districts:
        m = compute_metrics(d)
        vals = []
        for y in years:
            v = safe_float(lookup.get((d, grade, y), {}).get("cs_mn_all"))
            vals.append(f"{v:+.3f}" if v is not None else "  n/a " )
        dc = m.get((grade, "All"), {}).get("delta_covid")
        dc_s = f"{dc:+.3f}" if dc is not None else "  n/a "
        marker = " <<<" if "Troy" in d else ""
        print(f"  {d:<35}" + "".join(f"{v:>8}" for v in vals) + f"{dc_s:>9}{marker}")


# === ANALYSIS 5: Asian Subgroup — Troy vs High-Asian Peers ===
print("\n\n" + "=" * 100)
print("ANALYSIS 5: Asian Subgroup — Troy vs High-Asian Demographic Peers")
print("(cs_mn_asn — grade levels above national norm)")
print("=" * 100)

asian_districts = ["Troy SD (MI)", "Novi (MI)", "Coppell ISD (TX)", "Plano ISD (TX)",
                   "West Windsor-Plainsboro (NJ)", "Bellevue (WA)", "Issaquah (WA)",
                   "Lake Washington (WA)", "Bloomfield Hills (MI)"]

for grade in ("6", "7"):
    print(f"\n  Grade {grade}:")
    years = ["2017", "2018", "2019", "2022", "2023", "2024", "2025"]
    header = f"  {'District':<35}" + "".join(f"{y:>8}" for y in years) + f"{'Δ COVID':>9} {'Δ IM':>8}"
    print(header)
    print(f"  {'-' * (35 + 8*len(years) + 18)}")
    for d in asian_districts:
        m = compute_metrics(d)
        vals = []
        for y in years:
            v = safe_float(lookup.get((d, grade, y), {}).get("cs_mn_asn"))
            vals.append(f"{v:+.3f}" if v is not None else "  n/a ")
        dc = m.get((grade, "Asian"), {}).get("delta_covid")
        di = m.get((grade, "Asian"), {}).get("delta_im")
        dc_s = f"{dc:+.3f}" if dc is not None else "  n/a "
        di_s = f"{di:+.3f}" if di is not None else "  n/a "
        marker = " <<<" if "Troy" in d else ""
        print(f"  {d:<35}" + "".join(f"{v:>8}" for v in vals) + f"{dc_s:>9} {di_s:>8}{marker}")


# === ANALYSIS 6: SFUSD Detracking Comparison ===
print("\n\n" + "=" * 100)
print("ANALYSIS 6: Detracking Comparison — SFUSD (detracked 2014) vs Troy (detracked 2023)")
print("=" * 100)

sf_m = compute_metrics("San Francisco Unified (CA)")
print(f"\n  {'Metric':<50} {'SFUSD':>10} {'Troy':>10}")
print(f"  {'-'*70}")
for grade in ("6", "7"):
    for sub in ("All", "Asian", "White", "ECD"):
        sf_dc = sf_m.get((grade, sub), {}).get("delta_covid")
        tr_dc = troy_m.get((grade, sub), {}).get("delta_covid")
        sf_s = f"{sf_dc:+.3f}" if sf_dc is not None else "n/a"
        tr_s = f"{tr_dc:+.3f}" if tr_dc is not None else "n/a"
        print(f"  G{grade} {sub:<45} {sf_s:>10} {tr_s:>10}")


# === Summary Statistics ===
print("\n\n" + "=" * 100)
print("SUMMARY: Troy's Position in the District Universe")
print("=" * 100)

# Rank Troy among all districts
all_deltas = [(d, avg([compute_metrics(d).get(("6", "All"), {}).get("delta_covid"),
                       compute_metrics(d).get(("7", "All"), {}).get("delta_covid")]))
              for d in DISTRICT_GROUPS]
all_deltas = [(d, v) for d, v in all_deltas if v is not None]
all_deltas.sort(key=lambda x: x[1])
troy_rank = next(i for i, (d, _) in enumerate(all_deltas, 1) if "Troy" in d)
n = len(all_deltas)

all_im = [(d, avg([compute_metrics(d).get(("6", "All"), {}).get("delta_im"),
                    compute_metrics(d).get(("7", "All"), {}).get("delta_im")]))
           for d in DISTRICT_GROUPS]
all_im = [(d, v) for d, v in all_im if v is not None]
all_im.sort(key=lambda x: x[1], reverse=True)
troy_im_rank = next(i for i, (d, _) in enumerate(all_im, 1) if "Troy" in d)
n_im = len(all_im)

troy_dc = next(v for d, v in all_deltas if "Troy" in d)
troy_di = next(v for d, v in all_im if "Troy" in d)

print(f"\n  Pre/Post-COVID Δ (All Students, G6+G7 pooled):")
print(f"    Troy: {troy_dc:+.3f} — Rank {troy_rank} of {n} (1=worst decline)")
print(f"    Worst:  {all_deltas[0][0]} ({all_deltas[0][1]:+.3f})")
print(f"    Best:   {all_deltas[-1][0]} ({all_deltas[-1][1]:+.3f})")
print(f"    Median: {all_deltas[n//2][0]} ({all_deltas[n//2][1]:+.3f})")

print(f"\n  IM-Window Δ (2022-23 → 2024-25, All Students, G6+G7 pooled):")
print(f"    Troy: {troy_di:+.3f} — Rank {troy_im_rank} of {n_im} (1=best gain)")
print(f"    Best:  {all_im[0][0]} ({all_im[0][1]:+.3f})")
print(f"    Worst: {all_im[-1][0]} ({all_im[-1][1]:+.3f})")
print(f"    Median: {all_im[n_im//2][0]} ({all_im[n_im//2][1]:+.3f})")

# MI peer comparison
mi_deltas = [(d, avg([compute_metrics(d).get(("6", "All"), {}).get("delta_covid"),
                      compute_metrics(d).get(("7", "All"), {}).get("delta_covid")]))
             for d in DISTRICT_GROUPS if "MI" in DISTRICT_GROUPS[d]]
mi_deltas = [(d, v) for d, v in mi_deltas if v is not None]
mi_deltas.sort(key=lambda x: x[1])
troy_mi_rank = next(i for i, (d, _) in enumerate(mi_deltas, 1) if "Troy" in d)

print(f"\n  Among MI Affluent Peers only:")
print(f"    Troy: {troy_dc:+.3f} — Rank {troy_mi_rank} of {len(mi_deltas)}")
for d, v in mi_deltas:
    marker = " <<<" if "Troy" in d else ""
    print(f"      {d:<35} {v:+.3f}{marker}")
