# MR Fluid Quantitative Research
Literature-based quantitative re-analysis of published experimental results on magnetorheological (MR) fluids using structured data, Python analysis, statistical calculations and data visualization.
## Project Overview
Magnetorheological (MR) fluids are smart materials whose rheological behaviour changes in response to an applied magnetic field. Their behaviour is important in applications such as adaptive dampers, valves, clutches and other controllable systems.
This project quantitatively analyses published experimental results from three research papers covering different aspects of MR-fluid behaviour:
- non-uniform magnetic-field flow response;
- steady-state rheological behaviour and constitutive-model comparison;
- transient response to rapid changes in magnetic field.
The project does **not** contain original laboratory measurements. The numerical data were derived from published experimental results and analysed using Python.
The main purpose is to develop a reproducible workflow for extracting, organising, analysing and interpreting experimental literature.
---
## Research Questions
The analysis focuses on the following questions:
1. How does magnetic excitation affect the reported MR-fluid response?
2. How does MR-fluid formulation affect the measured response?
3. How different are increasing and decreasing loading paths in a non-uniform magnetic field?
4. How much does the choice of constitutive model affect the estimated yield stress?
5. What response times are reported for MR fluids under rapid magnetic-field changes?
6. What experimental questions can be formulated from the combined observations?
---
## Source Papers
### P1 — Non-uniform magnetic-field response
Kubík, M. et al. (2023).
*Magnetorheological fluids subjected to non-uniform magnetic fields: experimental characterization.*
Smart Materials and Structures, 32, 035007.
This paper provides the data used for the non-uniform-field flow analysis, including MR-fluid formulation properties, pressure-flow response, slope factors and increasing/decreasing loading paths.
### P2 — Rheological model comparison
Xie, J., Liu, C., & Cai, D. (2020).
*Analysis and Experimental Study on Rheological Performances of Magnetorheological Fluids.*
Mechanika, 26(1), 31-34.
This paper provides the Bingham and Casson yield-stress values used for the constitutive-model comparison.
### P3 — Transient response
Kubík, M. et al. (2022).
*Transient response of magnetorheological fluid on rapid change of magnetic field in shear mode.*
Scientific Reports, 12, 10612.
This paper provides the transient response measurements and reported relationships used for the response-time analysis.
Detailed source information is stored in:
`references/SOURCE_PAPERS.md`
---
## Dataset
The project contains **43 source-derived literature records**:
| Source | Records |
|---|---:|
| P1 | 27 |
| P2 | 8 |
| P3 | 8 |
| **Total** | **43** |
The master dataset is:
`data/00_MASTER_literature_dataset_43_records.csv`
Additional source-specific datasets are stored in the `data/` directory.
The dataset preserves source information such as:
- source paper;
- source table, figure or section;
- material/sample;
- experimental condition;
- measured quantity;
- units;
- data status.
### Missing Data
Values that are not reported in the source papers are not estimated.
For example, the unavailable MRF-122EG decreasing-stage value at 300 A-turns is retained as missing rather than being interpolated.
Published ranges are also retained as ranges when the source does not provide enough information to reconstruct individual observations.
---
# Analysis
## P1 — Non-uniform Magnetic Field
P1 examines MR-fluid behaviour in a non-uniform magnetic field using three formulations:
| Fluid | Iron content | Base viscosity |
|---|---:|---:|
| MRF-122EG | 22 vol.% | 56 cP |
| MRF-132DG | 32 vol.% | 156 cP |
| MRF-140CG | 40 vol.% | 648 cP |
The project analyses the reported pressure-flow slope factor:
`K = k(B) / k(0)`
where:
- `k(B)` is the pressure-flow slope at the applied magnetic condition;
- `k(0)` is the zero-field pressure-flow slope.
### Maximum increasing-stage K
| Fluid | Maximum increasing-stage K |
|---|---:|
| MRF-122EG | 6.71 |
| MRF-132DG | 2.76 |
| MRF-140CG | 1.61 |
For MRF-122EG, the tabulated values include:
- 900 A-turns: K = 6.60
- 600 A-turns: K = 6.71
- 300 A-turns: K = 2.27
- 0 A-turns: K = 1.00
The project uses the structured table values for quantitative analysis and records the small discrepancy between the source table and prose in the project audit.
### Loading-path analysis
A descriptive path-dependence indicator is calculated as:
`Path gap (%) = 100 × (K_increasing - K_decreasing) / K_increasing`
The active-field comparison excludes:
- the 0 A-turns baseline;
- the unavailable MRF-122EG 300 A-turns decreasing-stage observation.
Mean active-field path gaps are:
| Fluid | Mean path gap |
|---|---:|
| MRF-122EG | +74.23% |
| MRF-132DG | +34.80% |
| MRF-140CG | -8.57% |
This quantity is used as a **path-dependence indicator**. It is not described as a thermodynamic hysteresis measurement.
---
# P2 — Yield-Stress and Constitutive-Model Analysis
P2 reports Bingham and Casson yield-stress estimates at four magnetic flux densities.
| Magnetic flux density | Bingham | Casson |
|---:|---:|---:|
| 0.23 T | 1369 Pa | 1043 Pa |
| 0.44 T | 3703 Pa | 3080 Pa |
| 0.65 T | 6491 Pa | 5625 Pa |
| 0.86 T | 8825 Pa | 7627 Pa |
From 0.23 T to 0.86 T:
- Bingham yield stress increases by approximately 6.45×;
- Casson yield stress increases by approximately 7.31×.
The Casson estimate is lower than the Bingham estimate at every field level.
The percentage difference is calculated as:
`Difference (%) = 100 × (Bingham - Casson) / Bingham`
The mean difference is:
**16.89%**
This demonstrates that the selected constitutive model can materially affect the numerical yield-stress estimate.
### Exploratory Field Scaling
An exploratory power-law relationship was also examined:
`τ_y = a B^n`
where:
- `τ_y` = yield stress;
- `B` = magnetic flux density;
- `a` = fitted coefficient;
- `n` = fitted exponent.
The four-point exploratory fits give:
| Model | Exponent n | Log-scale R² |
|---|---:|---:|
| Bingham | 1.431 | 0.990 |
| Casson | 1.532 | 0.983 |
These fits are treated as **exploratory descriptions of the four available field levels**, not as universal constitutive laws.
---
# P3 — Transient Response
P3 investigates the transient response of MR fluid following rapid changes in magnetic field.
Reported hardware response measurements include:
- T63I = 0.21 ms;
- T90I = 0.335 ms at 1 A;
- T90I = 0.365 ms at 2 A;
- approximately 0.4 ms initial dead time.
The source also reports rheological response-time ranges:
| Fluid/sample group | Reported T90 |
|---|---:|
| MRHCCS4-A / MRHCCS4-B | 5.5–1.9 ms |
| MRF-132DG / MRC-C1L | 1.4–0.8 ms |
The project retains these as published ranges rather than creating artificial point-level observations.
The source reports that transient response is influenced by factors including:
- shear rate;
- magnetization;
- carrier-fluid viscosity.
The reported master relationship is also recorded:
`T* = 4.1939 Mn^-0.35`
This equation is treated as a **source-reported relationship** and is not independently refitted by this project.
---
# Main Quantitative Findings
The main results of the analysis are:
| Analysis | Result |
|---|---|
| P1 maximum increasing-stage K | 6.71, MRF-122EG at 600 A-turns |
| P1 mean active-field path gap | 28.39% |
| P1 MRF-122EG mean path gap | +74.23% |
| P1 MRF-132DG mean path gap | +34.80% |
| P1 MRF-140CG mean path gap | -8.57% |
| P2 Bingham yield-stress range | 1369–8825 Pa |
| P2 Casson yield-stress range | 1043–7627 Pa |
| Mean Casson difference from Bingham | 16.89% lower |
| P2 Bingham exploratory exponent | n = 1.431 |
| P2 Casson exploratory exponent | n = 1.532 |
| P3 reported T90 envelope | 0.8–5.5 ms |
These values describe the selected published observations and calculations performed from them. They are not presented as universal MR-fluid properties.
---
# Cross-Paper Interpretation
The three papers provide complementary information:
```text
P1
Non-uniform field
       ↓
Formulation + loading path
       ↓
Flow response

P2
Magnetic flux density
       ↓
Yield stress
       ↓
Constitutive-model dependence

P3
Magnetic-field change
       ↓
Transient rheological response
       ↓
Response time