#!/usr/bin/env python3
"""M-STEP Math G6+G7 scraper — all subgroups with dedicated parsers.

Pulls AllStudents, Ethnicity, EconomicallyDisadvantaged, and
StudentsWithDisabilities for Troy and peer districts.

Table formats (discovered via probe_all_formats.py):
  AllStudents  → 12-col tables (district-only + comparison with State/ISD/District)
  Ethnicity    → 11-col subgroup + 12-col comparison (needs full cascade to load)
  EconDis      → 11-col subgroup + 12-col comparison
  SPED         → 11-col subgroup + 12-col comparison
"""
import csv, os, sys, time
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
from mischooldata import MiSchoolDataReport

URL = "https://www.mischooldata.org/grades-3-8-state-testing-includes-psat-data-proficiency/"
WAIT = 9000

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

SUBGROUP_CATEGORIES = [
    ("AllStudents", "All Students"),
    ("Ethnicity", "Ethnicity"),
    ("EconomicallyDisadvantaged", "Econ Disadvantaged"),
    ("StudentsWithDisabilities", "SPED"),
]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "data", "mstep_math_g67.csv")
FIELDS = [
    "district", "school_year", "grade", "category", "subgroup",
    "pct_prof_or_above", "pct_advanced", "pct_proficient_only",
    "pct_partially_proficient", "pct_not_proficient",
    "n_tested", "state_pct", "state_n", "isd_pct",
]


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
    try:
        return int(s)
    except (ValueError, TypeError):
        return None


def _extract_pct_row(row, pct_idx):
    """Extract all proficiency percentages from a row given the start index."""
    return {
        "pct_prof_or_above": pct(row[pct_idx]),
        "pct_advanced": pct(row[pct_idx + 1]),
        "pct_proficient_only": pct(row[pct_idx + 2]),
        "pct_partially_proficient": pct(row[pct_idx + 3]),
        "pct_not_proficient": pct(row[pct_idx + 4]),
        "n_tested": num(row[pct_idx + 6]),
    }


def _parse_comparison_table(tables):
    """Extract State/ISD benchmarks from the 12-col comparison table.
    Present in all category reports."""
    state_pct = state_n = isd_pct = None
    for t in tables:
        for row in t:
            if len(row) < 12:
                continue
            if "Mathematics" not in " ".join(str(c) for c in row):
                continue
            loc_type = row[0].strip()
            if loc_type == "Statewide" and "%" in row[5]:
                state_pct = pct(row[5])
                state_n = num(row[11])
            elif loc_type == "ISD" and "%" in row[5]:
                isd_pct = pct(row[5])
    return state_pct, state_n, isd_pct


# ---------- Parser 1: AllStudents (12-col) ----------

def parse_all_students(tables, dname):
    """AllStudents: 12-col comparison table has Statewide/ISD/District rows.
    Format: [LocType, LocName, Program, Subject, Category, %Prof+, %Adv,
             %Prof, %Partial, %NotProf, %PartOrNot, N]
    """
    rows = []
    state_pct, state_n, isd_pct = _parse_comparison_table(tables)

    for t in tables:
        for row in t:
            if len(row) < 12:
                continue
            if "Mathematics" not in " ".join(str(c) for c in row):
                continue
            if "%" not in row[5]:
                continue
            loc_type = row[0].strip()
            if loc_type == "District" or row[1].strip() == dname:
                vals = _extract_pct_row(row, 5)
                vals["subgroup"] = row[4].strip()
                rows.append(vals)

    for r in rows:
        r["state_pct"] = state_pct
        r["state_n"] = state_n
        r["isd_pct"] = isd_pct
    return rows


# ---------- Parser 2: Ethnicity (11-col subgroup) ----------

def parse_ethnicity(tables, dname):
    """Ethnicity: 11-col subgroup table with per-race rows.
    Format: [LocName, Program, Subject, Category, %Prof+, %Adv,
             %Prof, %Partial, %NotProf, %PartOrNot, N]
    Category values: Asian, Black or African American, Hispanic of Any Race,
                     White, Two or More Races, etc.
    """
    rows = []
    state_pct, state_n, isd_pct = _parse_comparison_table(tables)

    for t in tables:
        for row in t:
            if len(row) != 11:
                continue
            if "Mathematics" not in " ".join(str(c) for c in row):
                continue
            if "%" not in row[4]:
                continue
            loc_name = row[0].strip()
            if loc_name == dname or dname in loc_name:
                vals = _extract_pct_row(row, 4)
                vals["subgroup"] = row[3].strip()
                rows.append(vals)

    for r in rows:
        r["state_pct"] = state_pct
        r["state_n"] = state_n
        r["isd_pct"] = isd_pct
    return rows


# ---------- Parser 3: EconDis (11-col subgroup) ----------

def parse_econ_dis(tables, dname):
    """EconDis: 11-col subgroup table.
    Format: [LocName, Program, Subject, Category, %Prof+, %Adv,
             %Prof, %Partial, %NotProf, %PartOrNot, N]
    Category values: Economically Disadvantaged, Not Economically Disadvantaged
    """
    rows = []
    state_pct, state_n, isd_pct = _parse_comparison_table(tables)

    for t in tables:
        for row in t:
            if len(row) != 11:
                continue
            if "Mathematics" not in " ".join(str(c) for c in row):
                continue
            if "%" not in row[4]:
                continue
            loc_name = row[0].strip()
            if loc_name == dname or dname in loc_name:
                vals = _extract_pct_row(row, 4)
                vals["subgroup"] = row[3].strip()
                rows.append(vals)

    for r in rows:
        r["state_pct"] = state_pct
        r["state_n"] = state_n
        r["isd_pct"] = isd_pct
    return rows


# ---------- Parser 4: SPED (11-col subgroup) ----------

def parse_sped(tables, dname):
    """SPED: 11-col subgroup table.
    Format: [LocName, Program, Subject, Category, %Prof+, %Adv,
             %Prof, %Partial, %NotProf, %PartOrNot, N]
    Category values: Students With Disabilities, Students Without Disabilities
    """
    rows = []
    state_pct, state_n, isd_pct = _parse_comparison_table(tables)

    for t in tables:
        for row in t:
            if len(row) != 11:
                continue
            if "Mathematics" not in " ".join(str(c) for c in row):
                continue
            if "%" not in row[4]:
                continue
            loc_name = row[0].strip()
            if loc_name == dname or dname in loc_name:
                vals = _extract_pct_row(row, 4)
                vals["subgroup"] = row[3].strip()
                rows.append(vals)

    for r in rows:
        r["state_pct"] = state_pct
        r["state_n"] = state_n
        r["isd_pct"] = isd_pct
    return rows


PARSERS = {
    "AllStudents": parse_all_students,
    "Ethnicity": parse_ethnicity,
    "EconomicallyDisadvantaged": parse_econ_dis,
    "StudentsWithDisabilities": parse_sped,
}


# ---------- Dropdown helpers ----------

def sel(r, dropdown_id, value, extra_wait=0):
    r.select(dropdown_id, value)
    if extra_wait > 0:
        r.page.wait_for_timeout(extra_wait)


def select_category(r, cat_value):
    """Select reportCategories with full cascade, then restore Math without cascade."""
    r.select("reportCategories", cat_value)
    r.page.wait_for_timeout(3000)
    subj = r.page.evaluate("() => document.querySelector('#subjects').value")
    if subj != "Math":
        print(f"    CASCADE: subjects reset to {subj!r}, restoring Math (no cascade)")
        r.select_no_cascade("subjects", "Math")
        r.page.wait_for_timeout(2000)


def ensure_math(r):
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
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for rec in all_rows:
            w.writerow(rec)


def main():
    all_rows = []
    print("Starting M-STEP Math subgroup scraper...")
    print(f"Output: {OUT}")

    with MiSchoolDataReport(URL, headless=True,
                            step_pause_ms=WAIT,
                            report_pause_ms=15000) as r:
        current_isd = None
        for isd_code, dist_code, dist_name in DISTRICTS:
            print(f"\n{'='*60}")
            print(f"  {dist_name}")
            print(f"{'='*60}")

            if current_isd != isd_code:
                sel(r, "isds", isd_code, extra_wait=3000)
                current_isd = isd_code
            sel(r, "districts", dist_code, extra_wait=3000)
            sel(r, "assessmentPrograms", "Mstep", extra_wait=3000)

            for year_code, year_label in YEARS:
                sel(r, "schoolYears", year_code, extra_wait=3000)

                for grade_code, grade_int in GRADES:
                    sel(r, "grades", grade_code, extra_wait=2000)
                    ensure_math(r)

                    for cat_value, cat_label in SUBGROUP_CATEGORIES:
                        select_category(r, cat_value)

                        cls, txt = r.view_button_state()
                        if "disabled" in cls:
                            print(f"  {year_label} G{grade_int} {cat_label}: DISABLED")
                            continue

                        t0 = time.time()
                        r.fire_report()
                        tables = r.results_tables(min_rows=1)

                        parser = PARSERS[cat_value]
                        parsed = parser(tables, dist_name)

                        for p in parsed:
                            all_rows.append({
                                "district": dist_name,
                                "school_year": year_label,
                                "grade": grade_int,
                                "category": cat_label,
                                **p
                            })

                        elapsed = time.time() - t0
                        if parsed:
                            subs = "; ".join(
                                f"{p['subgroup'][:15]}={p['pct_prof_or_above']}% "
                                f"(NP={p['pct_not_proficient']}%)"
                                for p in parsed)
                            print(f"  {year_label} G{grade_int} {cat_label}: "
                                  f"{subs} [{elapsed:.0f}s]")
                        else:
                            print(f"  {year_label} G{grade_int} {cat_label}: "
                                  f"NO DATA [{elapsed:.0f}s]")

                        save(all_rows)

    print(f"\nDone: {len(all_rows)} rows → {OUT}")


if __name__ == "__main__":
    main()
