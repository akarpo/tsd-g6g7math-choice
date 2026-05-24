#!/usr/bin/env python3
"""Probe table formats for each reportCategory — dump raw structure."""
import sys, os
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
from mischooldata import MiSchoolDataReport

URL = "https://www.mischooldata.org/grades-3-8-state-testing-includes-psat-data-proficiency/"

CATS = [
    ("AllStudents", "All Students"),
    ("Ethnicity", "Ethnicity"),
    ("EconomicallyDisadvantaged", "Econ Dis"),
    ("StudentsWithDisabilities", "SPED"),
]

with MiSchoolDataReport(URL, headless=True, step_pause_ms=6000, report_pause_ms=15000) as r:
    r.select("isds", "106")
    r.select("districts", "1608")
    r.select("assessmentPrograms", "Mstep")
    r.select("schoolYears", "26")  # 2024-25
    r.select("grades", "Grade06")
    r.select("subjects", "Math")

    for cat_val, cat_label in CATS:
        print(f"\n{'='*70}")
        print(f"  {cat_label} ({cat_val})")
        print(f"{'='*70}")

        r.select_no_cascade("reportCategories", cat_val)
        r.page.wait_for_timeout(2000)

        subj = r.page.evaluate("() => document.querySelector('#subjects').value")
        cat = r.page.evaluate("() => document.querySelector('#reportCategories').value")
        print(f"  subjects={subj!r}  reportCategories={cat!r}")

        r.fire_report()
        tables = r.results_tables(min_rows=1)
        print(f"  {len(tables)} tables total")

        for i, t in enumerate(tables):
            if len(t) < 2:
                continue
            # Skip the bootstrap-multiselect widget tables
            if all(len(row) <= 2 for row in t):
                continue
            ncols = max(len(row) for row in t)
            print(f"\n  --- Table {i}: {len(t)} rows x {ncols} cols ---")
            for row in t[:5]:
                print(f"    [{len(row)} cols] {row}")
            if len(t) > 5:
                print(f"    ... ({len(t)-5} more rows)")
