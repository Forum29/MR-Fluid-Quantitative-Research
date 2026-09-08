# Reproducibility Test Record

Date of final regeneration: 2026-09-08

## Automated checks

- Python syntax compilation: PASS
- Master dataset count: 43 records
- P1/P2/P3 partition: 27 / 8 / 8 records
- P1 flow table: 24 rows
- P2 rheology table: 8 rows
- P3 response-range table: 2 rows
- P1 MRF-122EG / 300 A-turns / velocity decrease: missing value preserved
- P1 MRF-122EG / 600 A-turns / velocity increase: K = 6.71
- P1 MRF-132DG / 900 A-turns / velocity increase: K = 2.76
- P1 MRF-140CG base viscosity: 648 cP
- P2 Bingham values: 1369, 3703, 6491, 8825 Pa
- P2 Casson values: 1043, 3080, 5625, 7627 Pa
- P3 published T90 ranges: 5.5–1.9 ms and 1.4–0.8 ms
- Derived result tables regenerated: 11
- Research figures regenerated: 8
- Cross-paper pooling regression: not performed
- Artificial P3 point reconstruction: not performed

## Regeneration command

From the repository root:

```bash
python src/MR_Fluid_quantitative_analysis.py
```

A successful run ends with:

```text
ANALYSIS COMPLETED SUCCESSFULLY.
All source-count, missing-data, and regeneration checks: PASS.
```

## Freeze decision

**PASS.** The repository is internally consistent and suitable for portfolio/GitHub use as a literature-based quantitative research project. It must not be described as an original experimental study.
