# MR Fluid Quantitative Research
A literature-based quantitative study of magnetorheological (MR) fluid behaviour using published experimental data from three research papers.
The project focuses on three connected aspects of MR fluid behaviour:
* flow response under non-uniform magnetic fields,
* sensitivity of yield-stress estimates to constitutive-model selection, and
* transient response to changes in magnetic field.
The analysis was carried out in Python using data extracted from the cited papers. The original published observations are kept separate from values calculated during the analysis.
---
## Research question
MR fluids can change their rheological behaviour when exposed to a magnetic field, but their useful performance depends on more than the steady-state response alone.
This project investigates:
1. How the reported flow response changes with magnetic field and formulation.
2. How much the estimated yield stress changes when Bingham and Casson models are used.
3. Whether simple field-to-yield-stress scaling can describe the available data.
4. How increasing and decreasing field conditions differ in the reported non-uniform-field experiments.
5. What the published transient-response measurements indicate about the dynamic timescale of MR fluid behaviour.
6. How steady-state and transient behaviour can be considered together when thinking about MR fluid system design.
---
## Approach
The analysis uses three published studies as the primary sources.
### P1 - Non-uniform magnetic field
Kubík et al. (2023) investigated MR fluids subjected to non-uniform magnetic fields.
The project uses the reported slope factor
$$
K = \frac{k(B)}{k(0)}
$$
to compare the flow response of three MR fluid formulations during increasing and decreasing magnetic-field conditions.
The three formulations considered are:
* MRF-122EG
* MRF-132DG
* MRF-140CG
The analysis examines the reported field-response curves, formulation differences, and the difference between increasing and decreasing field paths.
A source value that was not reported for MRF-122EG at 300 A-turns during the decreasing stage is retained as missing in the dataset. No value was estimated or fabricated.
### P2 - Rheological model comparison
Xie, Liu and Cai (2020) reported rheological measurements of MR fluid at four magnetic flux densities.
The project compares yield-stress estimates obtained using:
* the Bingham model, and
* the Casson model.
The analysis calculates the percentage difference between the two estimates and also performs an exploratory power-law analysis of yield stress against magnetic flux density.
The power-law analysis is treated only as a descriptive exploration because the source provides four field levels. It is not presented as a universal constitutive law.
### P3 - Transient response
Kubík et al. (2022) investigated the transient response of MR fluid following rapid changes in magnetic field.
The project preserves the response-time ranges reported in the paper rather than reconstructing individual measurements that were not published as complete point-level data.
The analysis therefore focuses on the reported millisecond-scale response envelope and the published master-curve relationship.
---
## Main observations
### 1. Non-uniform-field response
The largest increasing-stage value of the reported slope factor was:
**K = 6.71 for MRF-122EG at 600 A-turns.**
The three formulations showed substantially different responses under the reported conditions.
The increasing and decreasing field paths also did not behave identically, indicating that the measured response depends on the field history and formulation.
This project refers to the calculated quantity as a **path-dependence indicator** rather than thermodynamic hysteresis.
### 2. Constitutive-model sensitivity
For the P2 data:
* Bingham yield stress: **1369-8825 Pa**
* Casson yield stress: **1043-7627 Pa**
* Mean difference between the two estimates: **16.89%**
The choice of constitutive model therefore has a measurable effect on the reported yield-stress estimate.
### 3. Exploratory scaling
A log-log power-law fit was examined using the four reported magnetic-field levels.
The resulting exponents were approximately:
* Bingham: **n = 1.431**
* Casson: **n = 1.532**
These results are treated as exploratory descriptions of the available data and should not be interpreted as universal material laws.
### 4. Transient behaviour
The published P3 response-time ranges considered in this project were:
* MRHCCS4-A/B: **5.5-1.9 ms**
* MRF-132DG/MRC-C1L: **1.4-0.8 ms**
The reported values therefore place the observed transient response on a millisecond timescale.
The published master curve is also retained:
$$
T^* = 4.1939\,Mn^{-0.35}
$$
No point-level response-time pairs were reconstructed from the published ranges.
---
## Research framework
The three papers address different parts of MR fluid behaviour.
The project therefore does not combine their measurements as though they were obtained from one experiment.
Instead, they are treated as three separate evidence streams:
**P1:** magnetic field → flow response
**P2:** magnetic field → yield stress
**P3:** field/shear/material conditions → transient response
These observations are then used to formulate a possible future experimental direction in which steady-state performance and dynamic response are considered together.
The proposed experiment is future work and was **not performed as part of this project**.
---
## Data integrity
A major part of this project was keeping the distinction between published data and derived analysis clear.
The following rules were followed:
* Published numerical values were transcribed into structured CSV files.
* Derived quantities are calculated by Python rather than manually entered.
* Missing source observations remain missing.
* Published ranges are kept as ranges.
* Point-level measurements are not reconstructed when they are not available in the source.
* Exploratory fits are explicitly identified as exploratory.
* The three source papers are analysed separately before the cross-paper synthesis.
* No new experimental measurements were added.
The complete source verification and audit notes are available in the `audit/` directory.
---
## Project structure
```text
MR_Fluid_MITACS_FINAL/
│
├── README.md
├── CITATION.cff
├── PROJECT_MANIFEST.csv
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── 00_MASTER_literature_dataset_43_records.csv
│   ├── 01_P1_nonuniform_field_fluid_properties.csv
│   ├── 02_P1_nonuniform_field_flow_response.csv
│   ├── 03_P2_rheology_yield_stress.csv
│   ├── 04_P3_transient_fluid_properties.csv
│   ├── 05_P3_transient_response_times.csv
│   ├── 06_P3_other_reported_results.csv
│   ├── DATA_DICTIONARY.md
│   └── ...
│
├── src/
│   └── MR_Fluid_quantitative_analysis.py
│
├── results/
│   └── derived quantitative results
│
├── figures/
│   └── research figures generated by the analysis
│
├── report/
│   └── MITACS_LEVEL_RESEARCH_REPORT.md
│
├── references/
│   └── SOURCE_PAPERS.md
│
└── audit/
    ├── SOURCE_VERIFICATION.md
    ├── FINAL_AUDIT_CHECKLIST.md
    └── REPRODUCIBILITY_TESTS.md
```
---
## Reproducibility
The complete analysis can be regenerated from the supplied source-data tables.
### Requirements
Python 3.x with the packages listed in:
```text
requirements.txt
```
### Run the analysis
From the project root:
```bash
python src/MR_Fluid_quantitative_analysis.py
```
The script reads the structured data in `data/`, performs the quantitative analysis, writes the derived tables to `results/`, and regenerates the figures in `figures/`.
No external dataset is required to reproduce the calculations contained in this repository.
---
## Source papers
### P1
Kubík, M. et al. (2023).
**Magnetorheological fluids subjected to non-uniform magnetic fields: experimental characterization.**
*Smart Materials and Structures*, 32, 035007.
DOI: 10.1088/1361-665X/acb473
### P2
Xie, L., Liu, Y. and Cai, J. (2020).
**Analysis and Experimental Study on Rheological Performances of Magnetorheological Fluids.**
*Mechanika*, 26(1), 31-34.
DOI: 10.5755/j01.mech.26.1.25244
### P3
Kubík, M. et al. (2022).
**Transient response of magnetorheological fluid on rapid change of magnetic field in shear mode.**
*Scientific Reports*, 12, 10612.
DOI: 10.1038/s41598-022-14718-5
Full source details and access information are provided in:
```text
references/SOURCE_PAPERS.md
```
---
## Limitations
This is a literature-based quantitative research project rather than a new experimental study.
The main limitations are:
1. The analysis is restricted to the data reported by the three selected papers.
2. The P2 exploratory scaling analysis uses only four magnetic-field levels.
3. The P1 formulation comparison contains only three formulations and is therefore descriptive rather than a universal concentration law.
4. The P3 source reports response-time ranges for the relevant measurements rather than complete point-level datasets.
5. Differences in experimental setup and material conditions between the three papers prevent direct numerical merging of all measurements into one constitutive model.
These limitations are kept explicit because the purpose of the project is to analyse published evidence without overstating what the data can support.
---
## What this project demonstrates
This project demonstrates a complete literature-to-analysis workflow:
**research papers → source extraction → structured dataset → quantitative analysis → derived results → figures → scientific interpretation**
The main emphasis is not simply on producing graphs, but on maintaining traceability between published observations, calculations, and conclusions.
---
## Status
**Project status: Complete.**
This repository represents the final version of the project. The analysis, datasets, figures, report, references, and audit material are included in the repository.
No experimental data were collected for this project.
No unpublished experimental results are claimed.
---
## Author
**Forum Tailor**
B.Tech Robotics & Automation
Zeal College of Engineering and Research, Pune, India
