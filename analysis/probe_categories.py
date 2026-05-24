#!/usr/bin/env python3
"""Quick probe to list available reportCategories on the M-STEP proficiency page."""
import sys, os
from mischooldata import MiSchoolDataReport

URL = "https://www.mischooldata.org/grades-3-8-state-testing-includes-psat-data-proficiency/"

with MiSchoolDataReport(URL, headless=True, step_pause_ms=6000, report_pause_ms=10000) as r:
    r.select("isds", "106", timeout=30000)
    r.select("districts", "1608")
    r.select("assessmentPrograms", "Mstep")
    r.select("schoolYears", "26")
    r.select("grades", "Grade06")
    r.select("subjects", "Math")

    cats = r.options("reportCategories")
    print("reportCategories options:")
    for val, label in cats:
        print(f"  value={val!r:30s} label={label!r}")

    # Also dump a sample ethnicity report to debug parsing
    r.select("reportCategories", "Ethnicity")
    r.page.wait_for_timeout(2000)
    subj = r.page.evaluate("() => document.querySelector('#subjects').value")
    if subj != "Math":
        r.select("subjects", "Math")
        r.page.wait_for_timeout(3000)
    r.fire_report()
    tables = r.results_tables(min_rows=1)
    print(f"\nEthnicity tables: {len(tables)}")
    for i, t in enumerate(tables):
        print(f"\n--- Table {i} ({len(t)} rows) ---")
        for row in t[:8]:
            print(f"  {row}")
