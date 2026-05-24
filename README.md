# Troy School District G6-G7 Math: Has IM + Detracking Outperformed Its Characteristics?

A data-driven analysis of Troy School District's Fall 2023 adoption of
**Illustrative Mathematics** and **detracking** of 6th and 7th grade math,
benchmarked against 295 level-matched peer districts nationally.

**Live presentation:** [tsd-g6g7math-choice.pages.dev](https://tsd-g6g7math-choice.pages.dev)

## One-line answer

**No.** Troy ranks **197 of 295** level-matched peers (bottom third) in math
recovery during the exact IM adoption window (2022-23 to 2024-25). Birmingham,
in the same county with tracking intact, recovered **9x more**.

## Data sources

| Source | Metric | Coverage |
|--------|--------|----------|
| **SEDA 2025.1** (Stanford CEPA) | NAEP-anchored grade-level units (cs_mn) | 14,580 districts, G3-G8, 2009-2025 |
| **MI School Data / M-STEP** | % proficient or advanced | Michigan districts, G6-G7, 2015-2025 |
| **Education Scorecard 2026** | Demographic-adjusted gains | 108 math "Districts on the Rise" |

## Key findings

1. **Bottom third of peers** -- Troy's IM-window recovery (+0.024 GL) ranks
   197/295 among districts with similar pre-COVID math levels
2. **Asian subgroup crisis** -- G7 Asian math is *still declining* (-0.094)
   under IM; high-Asian peers with tracking (Bellevue, Issaquah) show robust
   recovery
3. **Detracking reversals** -- SFUSD (12 years) and Cambridge both reversed
   course after widening achievement gaps
4. **Course access != achievement** -- The "50% Algebra 1" claim mirrors
   SFUSD's decade of misleading enrollment metrics
5. **Opportunity cost** -- Three MI peers (Birmingham, Bloomfield Hills,
   Northville) recovered 3-9x more with tracking intact

## Peer selection

| Peer set | Criteria | N |
|----------|----------|---|
| Level-matched | Pre-COVID G6+G7 math within +/-0.25 GL of Troy (+0.937) | 296 |
| High-Asian | >=20% Asian enrollment, pre-COVID math >=+0.50 | 107 |
| MI affluent | Oakland County + Northville (same state test) | 8 |

## Slides

| # | Title |
|---|-------|
| 1 | Title |
| 2 | The question -- and the one-line answer |
| 3 | What Troy did and when |
| 4 | Troy's pre-COVID math position |
| 5 | Troy fell 59 places in the national rankings |
| 6 | MI peer leaderboard: Troy fell from 2nd to 4th |
| 7 | The post-COVID decline |
| 8 | The critical test: IM-window recovery |
| 9 | MI peers: Troy ranks 6th of 8 |
| 10 | G7 tracked-vs-IM comparison year |
| 11 | Asian subgroup crisis |
| 12 | G7 Asian still declining under IM |
| 13 | Subgroup waterfall |
| 14 | M-STEP proficiency numbers |
| 15 | SFUSD: 12 years of detracking, then reversal |
| 16 | Cambridge: detracked, now reversing |
| 17 | The "50% Algebra 1" claim |
| 18 | What high-performing districts do differently |
| 19 | IM evidence gaps |
| 20 | Conclusions |
| 21 | Methodology |
| 22 | References |

## Project structure

```
index.html                    HTML slide viewer (arrow keys, touch, fullscreen)
slides/                       PNG slide images (01.png - 20.png)
charts/                       10 matplotlib charts embedded in slides
data/
  seda_math_g67_subset.csv    596 rows -- 24 districts, G6+G7, all years/subgroups
  seda_math_peers_full.csv    296 level-matched peers with deltas
  mstep_math_g67.csv          M-STEP proficiency data
docs/
  analysis.md                 Full written analysis
deck/
  Troy_G6G7_Math_Executive_Summary.pptx
analysis/
  extract_seda_math.py        Extract from 426MB SEDA file
  find_math_peers.py           Scan 14,580 districts for level-matched peers
  analyze_seda_math.py        Six-part SEDA analysis
  build_charts.py             Generate 10 matplotlib charts
  build_deck.py               Generate PowerPoint deck
  render_slides.py            Render slides as PNG images
  pull_mstep_v2.py            M-STEP scraper (uses bundled mischooldata.py)
```

## Reproduction

```sh
# Requires: python 3.9+, matplotlib, pandas, numpy, python-pptx
pip install matplotlib pandas numpy python-pptx

# Download SEDA 2025.1 (426MB) from educationdata.urban.org
# Place as seda_admindist_long_cs_2025.1.csv in project root

# Extract subset, find peers, run analysis
python analysis/extract_seda_math.py
python analysis/find_math_peers.py
python analysis/analyze_seda_math.py

# Generate charts, deck, and slide images
python analysis/build_charts.py
python analysis/build_deck.py
python analysis/render_slides.py
```

## Related

- [tsd-k5ela-choice](https://github.com/akarpo/tsd-k5ela-choice) -- K-5 ELA
  curriculum analysis for Troy SD
