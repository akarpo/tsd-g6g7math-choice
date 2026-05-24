#!/usr/bin/env python3
"""Probe all available dropdown values to scope the full K-11 scraper."""
import sys, os
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
from mischooldata import MiSchoolDataReport

URL = "https://www.mischooldata.org/grades-3-8-state-testing-includes-psat-data-proficiency/"

with MiSchoolDataReport(URL, headless=True, step_pause_ms=6000, report_pause_ms=10000) as r:
    r.select("isds", "106")
    r.select("districts", "1608")

    print("=== Assessment Programs ===")
    for val, label in r.options("assessmentPrograms"):
        print(f"  {val!r:20s} → {label!r}")

    r.select("assessmentPrograms", "Mstep")

    print("\n=== School Years ===")
    for val, label in r.options("schoolYears"):
        print(f"  {val!r:20s} → {label!r}")

    print("\n=== Grades (M-STEP) ===")
    for val, label in r.options("grades"):
        print(f"  {val!r:20s} → {label!r}")

    print("\n=== Subjects (M-STEP) ===")
    for val, label in r.options("subjects"):
        print(f"  {val!r:20s} → {label!r}")

    print("\n=== Report Categories ===")
    for val, label in r.options("reportCategories"):
        print(f"  {val!r:20s} → {label!r}")

    # Now check PSAT
    progs = [v for v, l in r.options("assessmentPrograms")]
    for prog in progs:
        if prog == "Mstep":
            continue
        print(f"\n=== Switching to {prog} ===")
        r.select("assessmentPrograms", prog)
        r.page.wait_for_timeout(3000)

        print(f"  Grades ({prog}):")
        for val, label in r.options("grades"):
            print(f"    {val!r:20s} → {label!r}")

        print(f"  Subjects ({prog}):")
        for val, label in r.options("subjects"):
            print(f"    {val!r:20s} → {label!r}")
