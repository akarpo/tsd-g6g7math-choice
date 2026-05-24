#!/usr/bin/env python3
"""Probe the High School State Testing (SAT) page dropdowns."""
import sys, os
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
from mischooldata import MiSchoolDataReport

URL = "https://www.mischooldata.org/high-school-state-testing-proficiency/"

with MiSchoolDataReport(URL, headless=True, step_pause_ms=6000, report_pause_ms=10000) as r:
    r.select("isds", "106")
    r.select("districts", "1608")

    print("=== Assessment Programs ===")
    for val, label in r.options("assessmentPrograms"):
        print(f"  {val!r:20s} → {label!r}")

    # Try SAT first, fall back to whatever is available
    progs = [v for v, l in r.options("assessmentPrograms") if v != '-10']
    for prog in progs:
        print(f"\n=== {prog} ===")
        r.select("assessmentPrograms", prog)
        r.page.wait_for_timeout(3000)

        print(f"  School Years:")
        for val, label in r.options("schoolYears"):
            if val != '-10':
                print(f"    {val!r:20s} → {label!r}")

        r.select("schoolYears", "26")
        r.page.wait_for_timeout(2000)

        print(f"  Grades:")
        for val, label in r.options("grades"):
            print(f"    {val!r:20s} → {label!r}")

        print(f"  Subjects:")
        for val, label in r.options("subjects"):
            print(f"    {val!r:20s} → {label!r}")

        print(f"  Report Categories:")
        for val, label in r.options("reportCategories"):
            print(f"    {val!r:20s} → {label!r}")

        # Fire a sample report to check table format
        grades = [v for v, l in r.options("grades") if v != '-10']
        subjects = [v for v, l in r.options("subjects") if v != '-10']
        if grades and subjects:
            r.select("grades", grades[0])
            r.select("subjects", subjects[0])
            r.select_no_cascade("reportCategories", "AllStudents")
            r.fire_report()
            tables = r.results_tables(min_rows=1)
            print(f"\n  Sample tables: {len(tables)}")
            for i, t in enumerate(tables):
                if len(t) < 2 or all(len(row) <= 2 for row in t):
                    continue
                ncols = max(len(row) for row in t)
                print(f"  --- Table {i}: {len(t)} rows x {ncols} cols ---")
                for row in t[:3]:
                    print(f"    [{len(row)} cols] {row}")
