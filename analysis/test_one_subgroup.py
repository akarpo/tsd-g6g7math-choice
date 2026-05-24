#!/usr/bin/env python3
"""Quick single-shot test: Troy, 2024-25, G6, Ethnicity.
Verbose output at every step to diagnose timing/cascade issues."""
import sys, os, time
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
from mischooldata import MiSchoolDataReport

URL = "https://www.mischooldata.org/grades-3-8-state-testing-includes-psat-data-proficiency/"

def dump_dropdown(r, name):
    val = r.page.evaluate(f"() => document.querySelector('#{name}').value")
    print(f"  {name} = {val!r}")
    return val

with MiSchoolDataReport(URL, headless=False, step_pause_ms=6000, report_pause_ms=15000) as r:
    print("Page loaded. Setting dropdowns...")

    print("\n1. ISD")
    r.select("isds", "106")
    dump_dropdown(r, "isds")

    print("\n2. District")
    r.select("districts", "1608")
    dump_dropdown(r, "districts")

    print("\n3. Assessment")
    r.select("assessmentPrograms", "Mstep")
    dump_dropdown(r, "assessmentPrograms")

    print("\n4. Year")
    r.select("schoolYears", "26")
    dump_dropdown(r, "schoolYears")

    print("\n5. Grade")
    r.select("grades", "Grade06")
    dump_dropdown(r, "grades")

    print("\n6. Subjects → Math")
    r.select("subjects", "Math")
    r.page.wait_for_timeout(3000)
    dump_dropdown(r, "subjects")

    print("\n--- State before reportCategories ---")
    for dd in ["isds", "districts", "assessmentPrograms", "schoolYears", "grades", "subjects", "reportCategories"]:
        dump_dropdown(r, dd)

    print("\n7. reportCategories → Ethnicity (full select with cascade)")
    r.select("reportCategories", "Ethnicity")
    r.page.wait_for_timeout(5000)

    print("\n--- State AFTER reportCategories change ---")
    for dd in ["isds", "districts", "assessmentPrograms", "schoolYears", "grades", "subjects", "reportCategories"]:
        dump_dropdown(r, dd)

    subj = dump_dropdown(r, "subjects")
    if subj != "Math":
        print(f"\n8. Re-setting subjects to Math (was {subj!r})")
        r.select("subjects", "Math")
        r.page.wait_for_timeout(3000)
        print("--- State after Math re-set ---")
        for dd in ["subjects", "reportCategories"]:
            dump_dropdown(r, dd)

    print("\n9. Checking button state")
    cls, txt = r.view_button_state()
    print(f"  button class={cls!r} text={txt!r}")

    print("\n10. Firing report...")
    t0 = time.time()
    r.fire_report()
    print(f"  Report loaded in {time.time()-t0:.0f}s")

    print("\n11. Extracting tables...")
    tables = r.results_tables(min_rows=1)
    print(f"  Found {len(tables)} tables")
    for i, t in enumerate(tables):
        print(f"\n  --- Table {i} ({len(t)} rows) ---")
        for row in t[:10]:
            print(f"    {row}")
