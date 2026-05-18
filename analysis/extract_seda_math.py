"""Extract SEDA 2025.1 math data for target districts — G6 and G7 only."""
import csv, os
from collections import defaultdict

SEDA_FILE = "/Users/Alex/Downloads/tsd-g6g7math/seda_admindist_long_cs_2025.1.csv"
OUT_FILE = "/Users/Alex/Downloads/tsd-g6g7math/seda_math_g67_subset.csv"

TARGET_IDS = {
    # Michigan peers
    "2634260": "Troy SD (MI)",
    "2606090": "Bloomfield Hills (MI)",
    "2605850": "Birmingham (MI)",
    "2625980": "Northville (MI)",
    "2626130": "Novi (MI)",
    "2629940": "Rochester (MI)",
    "2635160": "Walled Lake (MI)",
    "2635820": "West Bloomfield (MI)",
    # High-Asian suburban demographic peers
    "4815210": "Coppell ISD (TX)",
    "4835100": "Plano ISD (TX)",
    "3417700": "West Windsor-Plainsboro (NJ)",
    "3410200": "Millburn (NJ)",
    # Detracking case study
    "634410":  "San Francisco Unified (CA)",
    # Education Scorecard 2026 Math DOTR
    "103360":  "Tuscaloosa City (AL)",
    "508280":  "Jonesboro (AR)",
    "2708190": "Eastern Carver County (MN)",
    "3200060": "Clark County (NV)",
    "5401470": "Upshur County (WV)",
    "4226390": "William Penn (PA)",
    # WA Asian-demographic peers
    "5300390": "Bellevue (WA)",
    "5303750": "Issaquah (WA)",
    "5304230": "Lake Washington (WA)",
}

rows_out = []
with open(SEDA_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["subject"] != "mth":
            continue
        if row["grade"] not in ("6", "7"):
            continue
        if row["sedaadmin"] in TARGET_IDS:
            rows_out.append(row)

print(f"Extracted {len(rows_out)} rows")

with open(OUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows_out[0].keys() if rows_out else [])
    writer.writeheader()
    writer.writerows(rows_out)

by_dist = defaultdict(list)
for r in rows_out:
    by_dist[r["sedaadminname"]].append(r)

print(f"\n{'District':<45} {'Grades':<8} {'Years':<80} {'Rows'}")
print("-" * 140)
for name, recs in sorted(by_dist.items()):
    years = sorted(set(r["year"] for r in recs))
    grades = sorted(set(r["grade"] for r in recs))
    label = TARGET_IDS.get(recs[0]["sedaadmin"], name)
    print(f"  {label:<43} G{','.join(grades):<6} {','.join(years):<78} {len(recs)}")

# Quick analysis: Troy pre/post-COVID delta
print("\n\n=== Troy SD Math G6+G7 Trend (cs_mn_all = grade-level units above national avg) ===")
troy = [r for r in rows_out if r["sedaadmin"] == "2634260"]
for grade in ("6", "7"):
    print(f"\n  Grade {grade}:")
    g_rows = sorted([r for r in troy if r["grade"] == grade], key=lambda x: x["year"])
    for r in g_rows:
        cs_all = r["cs_mn_all"]
        cs_asn = r["cs_mn_asn"]
        cs_wht = r["cs_mn_wht"]
        cs_ecd = r["cs_mn_ecd"]
        print(f"    {r['year']}: All={cs_all:>7s}  Asian={cs_asn:>7s}  "
              f"White={cs_wht:>7s}  ECD={cs_ecd:>7s}")
