"""M-STEP Math G6+G7 scraper — v2 with explicit timing between every step.

The mischooldata.org AJAX cascades need 8-10 seconds to settle after each
dropdown change. The page also resets the 'subjects' dropdown to ELA after
both schoolYears and grades changes. We handle this by:
1. Using generous explicit waits after every select
2. Re-selecting 'Math' as the very last step before firing
3. Verifying the subject value before each fire
"""
import csv, os, sys, time
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.path.insert(0, "/Users/Alex/Downloads/tools-mischooldata")
from mischooldata import MiSchoolDataReport

URL = "https://www.mischooldata.org/grades-3-8-state-testing-includes-psat-data-proficiency/"
WAIT = 9000  # ms to wait after each cascade step

DISTRICTS = [
    ("106", "1608", "Troy School District"),
    ("106", "943",  "Birmingham Public Schools"),
    ("106", "947",  "Bloomfield Hills Schools"),
    ("106", "1435", "Novi Community School District"),
    ("106", "1518", "Rochester Community School District"),
    ("119", "1430", "Northville Public Schools"),
]

YEARS = [
    ("20", "2018-19"),
    ("24", "2022-23"),
    ("25", "2023-24"),
    ("26", "2024-25"),
]

GRADES = [("Grade06", 6), ("Grade07", 7)]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mstep_math_g67.csv")
FIELDS = ["district", "school_year", "grade", "subgroup",
          "pct_proficient", "pct_advanced", "n_tested",
          "state_pct", "isd_pct"]


def pct(s):
    s = (s or "").strip().rstrip("%").replace(",", "")
    if not s or s in ("*", "<", ">") or "≤" in s or s.lower() in ("ns", "n/a"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def num(s):
    s = (s or "").strip().replace(",", "")
    return int(s) if s.isdigit() else None


def parse_all(tables, dname):
    rows = []
    state_pct = isd_pct = None
    for t in tables:
        for row in t:
            if len(row) < 7:
                continue
            joined = " ".join(str(c) for c in row)
            if "Mathematics" not in joined:
                continue
            if len(row) >= 12 and "%" in row[5]:
                if row[0] == "Statewide":
                    state_pct = pct(row[5])
                elif row[0] == "ISD":
                    isd_pct = pct(row[5])
                elif row[0] == "District" and row[1] == dname:
                    rows.append({"subgroup": "All Students",
                                 "pct_proficient": pct(row[5]),
                                 "pct_advanced": pct(row[6]),
                                 "n_tested": num(row[-1])})
    for r in rows:
        r["state_pct"] = state_pct
        r["isd_pct"] = isd_pct
    return rows


def parse_eth(tables, dname):
    rows = []
    for t in tables:
        for row in t:
            if (len(row) >= 11 and row[0] == dname
                    and "Mathematics" in row[2] and "%" in row[4]):
                rows.append({"subgroup": row[3],
                             "pct_proficient": pct(row[4]),
                             "pct_advanced": pct(row[5]),
                             "n_tested": num(row[-1]),
                             "state_pct": None, "isd_pct": None})
    return rows


def sel(r, dropdown_id, value, extra_wait=0):
    """Select and wait for cascade to settle."""
    r.select(dropdown_id, value)
    if extra_wait > 0:
        r.page.wait_for_timeout(extra_wait)


def ensure_math(r):
    """Force subjects to Math and verify."""
    r.page.wait_for_timeout(2000)
    r.select("subjects", "Math")
    r.page.wait_for_timeout(3000)
    val = r.page.evaluate("() => document.querySelector('#subjects').value")
    if val != "Math":
        print(f"    WARNING: subjects={val!r}, retrying...")
        r.page.wait_for_timeout(3000)
        r.select("subjects", "Math")
        r.page.wait_for_timeout(3000)
    return r.page.evaluate("() => document.querySelector('#subjects').value")


def save(all_rows):
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for rec in all_rows:
            w.writerow(rec)


def main():
    all_rows = []
    print("Starting M-STEP Math v2 scraper...")

    with MiSchoolDataReport(URL, headless=True,
                            step_pause_ms=WAIT,
                            report_pause_ms=15000) as r:
        current_isd = None
        for isd_code, dist_code, dist_name in DISTRICTS:
            print(f"\n{'='*50}")
            print(f"{dist_name}")
            print(f"{'='*50}")

            if current_isd != isd_code:
                sel(r, "isds", isd_code, extra_wait=3000)
                current_isd = isd_code
            sel(r, "districts", dist_code, extra_wait=3000)
            sel(r, "assessmentPrograms", "Mstep", extra_wait=3000)

            for year_code, year_label in YEARS:
                sel(r, "schoolYears", year_code, extra_wait=3000)

                for grade_code, grade_int in GRADES:
                    sel(r, "grades", grade_code, extra_wait=2000)
                    sel(r, "reportCategories", "AllStudents", extra_wait=2000)

                    # Force Math as the LAST selection before fire
                    subj = ensure_math(r)
                    if subj != "Math":
                        print(f"  {year_label} G{grade_int}: subjects stuck at {subj!r}, SKIP")
                        continue

                    cls, txt = r.view_button_state()
                    if "disabled" in cls:
                        print(f"  {year_label} G{grade_int}: DISABLED ({txt!r})")
                        continue

                    t0 = time.time()
                    r.fire_report()
                    tables = r.results_tables(min_rows=1)
                    parsed = parse_all(tables, dist_name)
                    for p in parsed:
                        all_rows.append({"district": dist_name,
                                         "school_year": year_label,
                                         "grade": grade_int, **p})

                    if parsed:
                        p0 = parsed[0]
                        print(f"  {year_label} G{grade_int}: {p0['pct_proficient']}% "
                              f"(st={p0['state_pct']}% n={p0['n_tested']}) "
                              f"[{time.time()-t0:.0f}s]")
                    else:
                        print(f"  {year_label} G{grade_int}: NO DATA [{time.time()-t0:.0f}s]")

                    # Ethnicity for Troy & Novi
                    if dist_name in ("Troy School District",
                                     "Novi Community School District"):
                        sel(r, "reportCategories", "Ethnicity", extra_wait=2000)
                        subj2 = ensure_math(r)
                        if subj2 == "Math":
                            r.fire_report()
                            tables2 = r.results_tables(min_rows=1)
                            parsed2 = parse_eth(tables2, dist_name)
                            for p in parsed2:
                                all_rows.append({"district": dist_name,
                                                 "school_year": year_label,
                                                 "grade": grade_int, **p})
                            subs = {p["subgroup"][:12]: p["pct_proficient"]
                                    for p in parsed2}
                            print(f"         Eth: {subs}")

                    save(all_rows)

    print(f"\nDone: {len(all_rows)} rows -> {OUT}")


if __name__ == "__main__":
    main()
