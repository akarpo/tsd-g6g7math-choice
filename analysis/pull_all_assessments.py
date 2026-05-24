#!/usr/bin/env python3
"""Comprehensive M-STEP / PSAT / SAT scraper — all grades, subjects, subgroups.

Pulls Math + ELA for:
  M-STEP  Grades 3-7
  PSAT    Grade 8
  SAT     Grade 11
All subgroup categories, all peer districts, from 2016-17 onward.

Resume-capable: reads existing CSV and skips already-pulled combos.
"""
import csv, os, sys, time
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
from mischooldata import MiSchoolDataReport

URL_38 = "https://www.mischooldata.org/grades-3-8-state-testing-includes-psat-data-proficiency/"
URL_HS = "https://www.mischooldata.org/high-school-state-testing-proficiency/"

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
    ("18", "2016-17"),
    ("19", "2017-18"),
    ("20", "2018-19"),
    ("22", "2020-21"),
    ("23", "2021-22"),
    ("24", "2022-23"),
    ("25", "2023-24"),
    ("26", "2024-25"),
]

# (page_url, assessment_code, assessment_label, grades, subjects)
ASSESSMENTS = [
    (URL_38, "Mstep", "M-STEP", [
        ("Grade03", 3), ("Grade04", 4), ("Grade05", 5),
        ("Grade06", 6), ("Grade07", 7),
    ], [("Math", "Math"), ("Ela", "ELA")]),
    (URL_38, "Psat", "PSAT", [
        ("Grade08", 8),
    ], [("Math", "Math"), ("Ela", "ELA")]),
    (URL_HS, "Sat", "SAT", [
        ("Grade11", 11),
    ], [("Math", "Math"), ("Ela", "ELA")]),
]

CATEGORIES = [
    ("AllStudents", "All Students"),
    ("Ethnicity", "Ethnicity"),
    ("EconomicallyDisadvantaged", "Econ Disadvantaged"),
    ("StudentsWithDisabilities", "SPED"),
    ("Gender", "Gender"),
    ("EnglishLanguageLearners", "ELL"),
]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "data", "proficiency_all.csv")
FIELDS = [
    "district", "school_year", "assessment", "grade", "subject",
    "category", "subgroup",
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


def _extract_pct(row, idx):
    return {
        "pct_prof_or_above": pct(row[idx]),
        "pct_advanced": pct(row[idx + 1]),
        "pct_proficient_only": pct(row[idx + 2]),
        "pct_partially_proficient": pct(row[idx + 3]),
        "pct_not_proficient": pct(row[idx + 4]),
        "n_tested": num(row[idx + 6]),
    }


def _has_subject(row_text, subject_code):
    """Check if a table row matches the current subject."""
    if subject_code == "Math":
        return "Math" in row_text
    else:
        return "ELA" in row_text or "EBRW" in row_text or "English" in row_text


# ---------- Parsers ----------

def _parse_comparison(tables, subject_code):
    """Extract State/ISD benchmarks from comparison tables."""
    state_pct = state_n = isd_pct = None
    for t in tables:
        for row in t:
            ncols = len(row)
            if ncols < 11:
                continue
            row_text = " ".join(str(c) for c in row)
            if not _has_subject(row_text, subject_code):
                continue
            loc_type = row[0].strip()
            # Comparison tables: col[0] = LocType
            # M-STEP: 12 cols, pct at col[5]
            # SAT: 11 cols, pct at col[4]
            if loc_type == "Statewide":
                pct_idx = 5 if ncols >= 12 else 4
                if "%" in row[pct_idx]:
                    state_pct = pct(row[pct_idx])
                    state_n = num(row[ncols - 1])
            elif loc_type == "ISD":
                pct_idx = 5 if ncols >= 12 else 4
                if "%" in row[pct_idx]:
                    isd_pct = pct(row[pct_idx])
    return state_pct, state_n, isd_pct


def parse_all_students(tables, dname, subject_code):
    """AllStudents parser — handles both M-STEP (12-col) and SAT (11-col)."""
    rows = []
    state_pct, state_n, isd_pct = _parse_comparison(tables, subject_code)

    for t in tables:
        for row in t:
            ncols = len(row)
            if ncols < 11:
                continue
            row_text = " ".join(str(c) for c in row)
            if not _has_subject(row_text, subject_code):
                continue

            # M-STEP comparison: 12 cols, col[0]=LocType
            if ncols >= 12 and row[0].strip() == "District":
                if "%" in row[5]:
                    vals = _extract_pct(row, 5)
                    vals["subgroup"] = row[4].strip()
                    rows.append(vals)
            # M-STEP district-only: 12 cols, col[0]=LocName
            elif ncols >= 12 and (row[0].strip() == dname or dname in row[0].strip()):
                if row[0].strip() not in ("Statewide", "ISD", "District", "") and "%" in row[5]:
                    vals = _extract_pct(row, 5)
                    vals["subgroup"] = row[4].strip()
                    rows.append(vals)
            # SAT district-only: 11 cols, col[0]=LocName
            elif ncols == 11 and (row[0].strip() == dname or dname in row[0].strip()):
                if row[0].strip() not in ("Statewide", "ISD", "District", "") and "%" in row[4]:
                    vals = _extract_pct(row, 4)
                    vals["subgroup"] = row[3].strip()
                    rows.append(vals)

    for r in rows:
        r["state_pct"] = state_pct
        r["state_n"] = state_n
        r["isd_pct"] = isd_pct
    return rows


def parse_subgroup(tables, dname, subject_code):
    """Subgroup parser (Ethnicity, EconDis, SPED, Gender, ELL).
    M-STEP subgroups: 11 cols [LocName, Program, Subject, Category, pcts..., N]
    SAT subgroups: 10 cols [LocName, Subject, Category, pcts..., N] (probable)
    """
    rows = []
    state_pct, state_n, isd_pct = _parse_comparison(tables, subject_code)

    for t in tables:
        for row in t:
            ncols = len(row)
            if ncols < 10:
                continue
            row_text = " ".join(str(c) for c in row)
            if not _has_subject(row_text, subject_code):
                continue
            loc = row[0].strip()
            if loc in ("Statewide", "ISD", "District", ""):
                continue
            if loc != dname and dname not in loc:
                continue

            # M-STEP subgroup: 11 cols, pct at col[4]
            if ncols == 11 and "%" in row[4]:
                vals = _extract_pct(row, 4)
                vals["subgroup"] = row[3].strip()
                rows.append(vals)
            # SAT subgroup: 10 cols, pct at col[3]
            elif ncols == 10 and "%" in row[3]:
                vals = _extract_pct(row, 3)
                vals["subgroup"] = row[2].strip()
                rows.append(vals)

    for r in rows:
        r["state_pct"] = state_pct
        r["state_n"] = state_n
        r["isd_pct"] = isd_pct
    return rows


# ---------- Dropdown helpers ----------

def sel(r, dropdown_id, value, extra_wait=0):
    r.select(dropdown_id, value)
    if extra_wait > 0:
        r.page.wait_for_timeout(extra_wait)


def select_category(r, cat_value, subject_code):
    """Select reportCategories with full cascade, then restore subject without cascade."""
    r.select("reportCategories", cat_value)
    r.page.wait_for_timeout(3000)
    subj = r.page.evaluate("() => document.querySelector('#subjects').value")
    if subj != subject_code:
        print(f"    CASCADE: subjects reset to {subj!r}, restoring {subject_code}")
        r.select_no_cascade("subjects", subject_code)
        r.page.wait_for_timeout(2000)


def ensure_subject(r, subject_code):
    r.page.wait_for_timeout(2000)
    r.select("subjects", subject_code)
    r.page.wait_for_timeout(3000)
    val = r.page.evaluate("() => document.querySelector('#subjects').value")
    if val != subject_code:
        print(f"    WARNING: subjects={val!r}, retrying {subject_code}...")
        r.page.wait_for_timeout(3000)
        r.select("subjects", subject_code)
        r.page.wait_for_timeout(3000)
    return r.page.evaluate("() => document.querySelector('#subjects').value")


# ---------- Resume ----------

def load_existing():
    """Load existing rows and build a set of already-pulled combos."""
    existing = []
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.append(row)
                key = (row["district"], row["school_year"], row["assessment"],
                       str(row["grade"]), row["subject"], row["category"])
                done.add(key)
    return existing, done


def save(all_rows):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for rec in all_rows:
            w.writerow(rec)


def main():
    existing, done = load_existing()
    all_rows = list(existing)
    print(f"Starting comprehensive assessment scraper...")
    print(f"Output: {OUT}")
    print(f"Resuming with {len(existing)} existing rows, {len(done)} combos done")

    current_url = None
    r = None

    try:
        for page_url, assess_code, assess_label, grades, subjects in ASSESSMENTS:
            # Open new browser if page URL changed
            if current_url != page_url:
                if r:
                    r.close()
                print(f"\n{'#'*60}")
                print(f"  Opening {assess_label} page...")
                print(f"{'#'*60}")
                r = MiSchoolDataReport(page_url, headless=True,
                                       step_pause_ms=WAIT,
                                       report_pause_ms=15000)
                r.open()
                current_url = page_url

            current_isd = None
            for isd_code, dist_code, dist_name in DISTRICTS:
                print(f"\n{'='*60}")
                print(f"  {dist_name} — {assess_label}")
                print(f"{'='*60}")

                if current_isd != isd_code:
                    sel(r, "isds", isd_code, extra_wait=3000)
                    current_isd = isd_code
                sel(r, "districts", dist_code, extra_wait=3000)
                sel(r, "assessmentPrograms", assess_code, extra_wait=3000)

                for year_code, year_label in YEARS:
                    sel(r, "schoolYears", year_code, extra_wait=3000)

                    for grade_code, grade_int in grades:
                        sel(r, "grades", grade_code, extra_wait=2000)

                        for subj_code, subj_label in subjects:
                            ensure_subject(r, subj_code)

                            for cat_value, cat_label in CATEGORIES:
                                key = (dist_name, year_label, assess_label,
                                       str(grade_int), subj_label, cat_label)
                                if key in done:
                                    continue

                                select_category(r, cat_value, subj_code)

                                cls, txt = r.view_button_state()
                                if "disabled" in cls:
                                    print(f"  {year_label} G{grade_int} {subj_label} {cat_label}: DISABLED")
                                    done.add(key)
                                    continue

                                t0 = time.time()
                                r.fire_report()
                                tables = r.results_tables(min_rows=1)

                                if cat_value == "AllStudents":
                                    parsed = parse_all_students(tables, dist_name, subj_code)
                                else:
                                    parsed = parse_subgroup(tables, dist_name, subj_code)

                                for p in parsed:
                                    all_rows.append({
                                        "district": dist_name,
                                        "school_year": year_label,
                                        "assessment": assess_label,
                                        "grade": grade_int,
                                        "subject": subj_label,
                                        "category": cat_label,
                                        **p
                                    })

                                elapsed = time.time() - t0
                                if parsed:
                                    subs = "; ".join(
                                        f"{p['subgroup'][:12]}={p['pct_prof_or_above']}%"
                                        for p in parsed[:3])
                                    extra = f" +{len(parsed)-3} more" if len(parsed) > 3 else ""
                                    print(f"  {year_label} G{grade_int} {subj_label} {cat_label}: "
                                          f"{subs}{extra} [{elapsed:.0f}s]")
                                else:
                                    print(f"  {year_label} G{grade_int} {subj_label} {cat_label}: "
                                          f"NO DATA [{elapsed:.0f}s]")

                                done.add(key)
                                save(all_rows)

    finally:
        if r:
            r.close()

    print(f"\nDone: {len(all_rows)} rows → {OUT}")


if __name__ == "__main__":
    main()
