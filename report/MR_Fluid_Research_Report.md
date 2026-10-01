# Magnetorheological Fluid Response Under Magnetic Excitation
## Literature-Based Quantitative Analysis
**Author:** Forum Tailor\
**Program:** B.Tech. Robotics & Automation, Zeal College of Engineering
and Research, Pune, India\
**Project type:** Reproducible computational and literature-based
research\
**Status:** Complete
------------------------------------------------------------------------
## Abstract
Magnetorheological (MR) fluids are field-responsive suspensions whose
rheological behaviour changes when exposed to a magnetic field. Their
usefulness in adaptive dampers, valves, clutches and other
smart-material systems depends not only on the magnitude of the
field-induced response, but also on formulation, loading history,
constitutive modelling and response time.
This project performs a quantitative re-analysis of published
experimental results from three research papers covering complementary
aspects of MR-fluid behaviour: non-uniform-field flow response,
steady-state rheology and transient response to rapid magnetic-field
changes. A structured dataset containing 43 source-derived records was
prepared from the three papers and analysed using Python.
The analysis examines formulation sensitivity and loading-path
dependence in a non-uniform-field pinch-mode experiment, the sensitivity
of yield-stress estimates to Bingham and Casson constitutive models,
exploratory field-to-yield-stress scaling, and published
transient-response ranges. Missing observations and published ranges are
retained as reported rather than being estimated or reconstructed.
The analysis shows that the reported response depends strongly on the
formulation and operating condition. In the non-uniform-field study, the
maximum tabulated increasing-stage slope factor is K = 6.71 for
MRF-122EG at 600 A-turns. In the rheological study, Casson yield-stress
estimates are lower than the corresponding Bingham estimates by 13.3% to
23.8%. The transient study reports response times on the millisecond
scale, with the reported ranges depending on fluid and operating
conditions.
The main outcome of the project is a traceable workflow connecting
published experimental evidence to structured data, quantitative
calculations, figures and a proposed follow-up experiment. The results
are interpreted as a secondary analysis of the selected literature and
are not presented as original experimental measurements or as universal
material laws.
------------------------------------------------------------------------
# 1. Research Objective
The objective of this project is to quantitatively analyse selected
published experimental results on MR fluids and examine how magnetic
excitation, formulation, loading path, constitutive-model selection and
transient behaviour affect the reported response.
The project is organised around six questions:
1.  How does magnetic excitation affect the reported flow or
    yield-stress response?
2.  How sensitive is the estimated yield stress to the constitutive
    model used?
3.  How does MR-fluid formulation affect non-uniform-field flow
    response?
4.  How different are increasing and decreasing loading paths in the
    reported pinch-mode experiment?
5.  What do the published transient measurements indicate about the
    timescale of MR-fluid response?
6.  How can these observations be combined into a controlled follow-up
    experimental question?
------------------------------------------------------------------------
# 2. Nature of the Study
This is a **literature-based quantitative re-analysis**.
The project does not reproduce the laboratory experiments described in
the source papers. Instead, it:
-   identifies relevant published experimental results;
-   records the reported numerical observations in structured CSV files;
-   preserves source information for the extracted data;
-   calculates additional quantities from those observations;
-   generates figures from the calculated results;
-   compares the three studies without statistically pooling
    incompatible experiments;
-   uses the combined evidence to formulate a possible future
    experimental design.
The distinction between published observations and project-derived
quantities is maintained throughout the repository.
------------------------------------------------------------------------
# 3. Source Papers
## P1 --- Non-uniform magnetic field
Kubík, M. et al. (2023). **Magnetorheological fluids subjected to
non-uniform magnetic fields: experimental characterization.** *Smart
Materials and Structures*, 32, 035007.
DOI: 10.1088/1361-665X/acb473
P1 provides the data used for the non-uniform-field flow analysis,
including MR-fluid formulation properties, pressure-flow slopes, slope
factors and increasing/decreasing velocity paths.
## P2 --- Rheological model comparison
Xie, J., Liu, C., & Cai, D. (2020). **Analysis and Experimental Study on
Rheological Performances of Magnetorheological Fluids.** *Mechanika*,
26(1), 31-34.
DOI: 10.5755/j01.mech.26.1.25244
P2 provides the Bingham and Casson yield-stress values used for the
constitutive-model comparison.
## P3 --- Transient response
Kubík, M. et al. (2022). **Transient response of magnetorheological
fluid on rapid change of magnetic field in shear mode.** *Scientific
Reports*, 12, 10612.
DOI: 10.1038/s41598-022-14718-5
P3 provides the transient response measurements, fluid-property
information, hardware response measurements and reported master-curve
relationship.
Full source details and access information are stored in
`references/SOURCE_PAPERS.md`.
------------------------------------------------------------------------
# 4. Why These Papers Were Selected
The three papers examine different aspects of MR-fluid behaviour and are
therefore treated as separate evidence streams.
  -----------------------------------------------------------------------
  Study                   Experimental focus      Main quantities used
  ----------------------- ----------------------- -----------------------
  P1                      Non-uniform magnetic    Pressure-flow slope, K,
                          field and pinch-mode    formulation, loading
                          flow                    path
  P2                      Steady-state shear      Yield stress, viscosity
                          rheology                parameter,
                                                  Bingham/Casson model
  P3                      Rapid magnetic-field    T63, T90, dead time,
                          changes in shear mode   material and operating
                                                  conditions
  -----------------------------------------------------------------------
The studies are not treated as though they were measurements from one
common experiment.
The synthesis is therefore qualitative and engineering-oriented rather
than a pooled statistical model.
------------------------------------------------------------------------
# 5. Dataset and Data Provenance
The project contains **43 source-derived master records**:
-   P1: 27 records
-   P2: 8 records
-   P3: 8 records
The source data are separated into smaller CSV files according to the
paper and analysis purpose.
The main files are:
``` text
data/00_MASTER_literature_dataset_43_records.csv
data/01_P1_nonuniform_field_fluid_properties.csv
data/02_P1_nonuniform_field_flow_response.csv
data/03_P2_rheology_yield_stress.csv
data/04_P3_transient_fluid_properties.csv
data/05_P3_transient_response_times.csv
data/06_P3_other_reported_results.csv
```
Each source-derived observation is associated with information such as:
-   source paper;
-   source table, figure or section;
-   material or sample;
-   experimental condition;
-   measured quantity;
-   units;
-   data status.
Derived calculations are stored separately in the `results/` directory.
### Missing data rule
A value that is not reported in the source is not estimated.
For example, P1 does not provide a usable MRF-122EG value at 300 A-turns
during the decreasing stage. That observation remains missing in the
project dataset.
### Published ranges
When a source reports a range without providing the complete point-level
data, the project keeps the range rather than inventing individual
measurement pairs.
This rule is particularly important for the P3 transient-response data.
------------------------------------------------------------------------
# 6. Methodology
The analysis was performed in Python using the source CSV files.
The workflow consists of:
1.  loading the literature-derived datasets;
2.  validating record counts and key source values;
3.  separating P1, P2 and P3 analyses;
4.  calculating derived quantities;
5.  exporting derived CSV tables;
6.  generating research figures;
7.  performing consistency checks;
8.  producing a final terminal summary.
The main analysis script is:
``` text
src/MR_Fluid_quantitative_analysis.py
```
The project uses Python libraries listed in:
``` text
requirements.txt
```
------------------------------------------------------------------------
# 7. P1 --- Non-uniform-Field Flow Analysis
## 7.1 Experimental context
P1 investigates MR-fluid behaviour in a pinch-mode device subjected to a
non-uniform magnetic field.
The study considers three formulations:
  Fluid         Iron content   Base viscosity at 30 °C
  ----------- -------------- -------------------------
  MRF-122EG         22 vol.%                     56 cP
  MRF-132DG         32 vol.%                    156 cP
  MRF-140CG         40 vol.%                    648 cP
The reported operating range includes magnetic excitation from 0 to 900
A-turns.
## 7.2 Slope factor
The project uses the slope factor reported in P1:
**K = k(B) / k(0)**
where:
-   `k(B)` is the pressure-flow slope at the applied magnetic condition;
-   `k(0)` is the zero-field pressure-flow slope.
This dimensionless quantity allows the magnetic-field-dependent change
in flow resistance to be compared with the zero-field condition.
## 7.3 Increasing-stage response
The maximum tabulated increasing-stage values are:
  Fluid         Maximum increasing-stage K
  ----------- ----------------------------
  MRF-122EG                           6.71
  MRF-132DG                           2.76
  MRF-140CG                           1.61
For MRF-122EG, the source table reports:
-   900 A-turns: K = 6.60
-   600 A-turns: K = 6.71
-   300 A-turns: K = 2.27
-   0 A-turns: K = 1.00
Therefore, the maximum **tabulated** value is K = 6.71 at 600 A-turns.
The source paper's prose highlights approximately 6.6 at 900 A-turns.
The project uses the table values for quantitative analysis and records
the discrepancy in the audit documentation.
## 7.4 Formulation sensitivity
The maximum increasing-stage K decreases from 6.71 for MRF-122EG to 1.61
for MRF-140CG.
The base viscosity simultaneously increases from 56 cP to 648 cP.
This demonstrates that the reported response is strongly
formulation-dependent under the tested conditions.
However, only three formulations are available. Therefore, the project
does **not** fit or claim a universal relationship between iron
concentration and K.
## 7.5 Loading-path analysis
To compare the increasing and decreasing velocity paths, the project
defines a descriptive path-dependence indicator:
**Path gap (%) = 100 × (K_increasing - K_decreasing) / K_increasing**
The 0 A-turns baseline is excluded from the active-field comparison
because it is not an activated magnetic-field condition.
The missing MRF-122EG 300 A-turns decreasing-stage observation is also
excluded.
The mean active-field path gaps are:
  Fluid         Mean path gap
  ----------- ---------------
  MRF-122EG           +74.23%
  MRF-132DG           +34.80%
  MRF-140CG            -8.57%
The sign and magnitude vary with formulation.
This quantity is called a **path-dependence indicator** in the project.
It is not described as a thermodynamic hysteresis measurement.
## 7.6 Interpretation
The source study discusses particle migration and redistribution in the
non-uniform magnetic field as possible mechanisms influencing the
pressure-flow response.
The project therefore interprets the P1 observations as evidence that:
-   formulation affects the magnitude of the magnetic response;
-   increasing and decreasing paths can produce different measured
    responses;
-   the difference between paths is not identical for all formulations.
These are observations from the selected experiment, not universal laws
for all MR fluids.
------------------------------------------------------------------------
# 8. P2 --- Rheological Model Comparison
## 8.1 Source data
P2 reports yield-stress estimates at four magnetic flux densities:
    Magnetic flux density   Bingham    Casson
  ----------------------- --------- ---------
                   0.23 T   1369 Pa   1043 Pa
                   0.44 T   3703 Pa   3080 Pa
                   0.65 T   6491 Pa   5625 Pa
                   0.86 T   8825 Pa   7627 Pa
These values are taken from the structured tables in the paper.
## 8.2 Effect of magnetic flux density
From 0.23 T to 0.86 T:
-   Bingham yield stress increases by approximately 6.45 times.
-   Casson yield stress increases by approximately 7.31 times.
This confirms a strong increase in the reported yield-stress estimate
with magnetic flux density under the conditions of P2.
## 8.3 Constitutive-model sensitivity
For each field level, the project calculates how much lower the Casson
estimate is than the corresponding Bingham estimate:
**Difference (%) = 100 × (Bingham - Casson) / Bingham**
The values are:
    Magnetic flux density   Casson lower than Bingham
  ----------------------- ---------------------------
                   0.23 T                      23.81%
                   0.44 T                      16.82%
                   0.65 T                      13.34%
                   0.86 T                      13.58%
The mean difference is **16.89%**.
Therefore, the selected constitutive model materially affects the
numerical yield-stress estimate even when the same experimental
observations are being represented.
## 8.4 Reported fit quality
The source reports high R² values for both models across the four field
levels.
The project preserves these reported R² values in:
``` text
results/03_P2_reported_fit_quality.csv
```
The project does not reinterpret the source R² values as proof that one
model is universally superior.
The important observation is that different constitutive descriptions
can both represent the measured flow curves well while giving different
yield-stress estimates.
## 8.5 Exploratory power-law analysis
An exploratory log-log relationship was examined in the form:
**τ_y = a B\^n**
where:
-   `τ_y` is yield stress;
-   `B` is magnetic flux density;
-   `a` is a fitted coefficient;
-   `n` is the fitted exponent.
The four-point fits give:
  Model       Exponent n   Log-scale R²
  --------- ------------ --------------
  Bingham          1.431          0.990
  Casson           1.532          0.983
Leave-one-out sensitivity gives:
  Model       Mean leave-one-out n      SD
  --------- ---------------------- -------
  Bingham                    1.414   0.082
  Casson                     1.510   0.109
These values are useful for describing the available four-point dataset,
but the fits are explicitly treated as **exploratory**.
They are not presented as universal constitutive laws because only four
magnetic-field levels are available and the underlying experimental
conditions are limited to the source study.
## 8.6 Source discrepancy
The paper contains a small numerical discrepancy between a prose
statement and its structured table for the final Casson value.
The prose gives approximately 7624 Pa, whereas Table 4 reports 7627 Pa.
The project uses the structured table value of **7627 Pa** and records
the discrepancy in the source audit.
------------------------------------------------------------------------
# 9. P3 --- Transient Rheological Response
## 9.1 Experimental context
P3 investigates the transient response of MR fluid after rapid changes
in magnetic field under shear-mode conditions.
The paper reports response-time measurements using quantities such as:
-   T63;
-   T90;
-   initial hardware response time;
-   shear-rate dependence;
-   magnetization dependence;
-   carrier-fluid viscosity effects.
## 9.2 Hardware response
The reported hardware response includes:
-   T63I = 0.21 ms;
-   T90I = 0.335 ms at 1 A;
-   T90I = 0.365 ms at 2 A;
-   approximately 0.4 ms initial dead time.
These measurements distinguish the response of the
electrical/current-control hardware from the complete rheological
response of the MR fluid.
## 9.3 Reported rheological response ranges
The project retains the published ranges:
  Fluid/sample group        Reported T90 range
  ----------------------- --------------------
  MRHCCS4-A / MRHCCS4-B            5.5--1.9 ms
  MRF-132DG / MRC-C1L              1.4--0.8 ms
The project does not create individual shear-rate/T90 pairs from these
ranges because the complete point-level data are not provided in the
source text used for this project.
## 9.4 Operating-condition dependence
P3 reports that response time changes with:
-   shear rate;
-   magnetization;
-   carrier-fluid viscosity.
The reported trends provide evidence that transient response is
influenced by both the operating condition and the material system.
Therefore, response time should not be treated as one fixed number that
applies to every MR-fluid device.
## 9.5 Dimensionless master curve
The source reports the relationship:
**T\* = 4.1939 Mn\^-0.35**
The project records this equation as a **source-reported relationship**.
It is not independently refitted using the project dataset.
The definitions used by the source are preserved in:
``` text
results/10_P3_reported_master_curve.csv
```
------------------------------------------------------------------------
# 10. Cross-Paper Synthesis
The three studies can be viewed as three connected levels of MR-fluid
behaviour.
### Level 1 --- Steady response
P2 shows that magnetic excitation strongly changes the reported
yield-stress estimate.
### Level 2 --- Formulation and loading path
P1 shows that formulation and loading path influence the measured flow
response in a non-uniform magnetic field.
### Level 3 --- Dynamic response
P3 shows that the time required for the rheological response depends on
the material and operating conditions and occurs on a millisecond scale
under the reported conditions.
The studies should not be numerically pooled because they use different
materials, geometries, modes of operation and measurement conditions.
The engineering implication is instead:
**A useful MR-fluid system must satisfy both the required steady-state
response and the required dynamic response.**
This means that increasing magnetic excitation alone is not sufficient
to describe overall device performance.
------------------------------------------------------------------------
# 11. Proposed Follow-up Experiment
The literature analysis suggests a controlled experiment that measures
steady-state and transient behaviour under the same material and
apparatus.
## 11.1 Objective
Determine how magnetic excitation and MR-fluid formulation affect:
-   steady-state yield stress;
-   steady-state flow resistance;
-   response time after field switching.
## 11.2 Independent variables
A practical first design could vary:
1.  magnetic flux density;
2.  MR-fluid formulation;
3.  shear rate.
The exact levels should be selected according to the available
rheometer, electromagnet and fluid formulations.
## 11.3 Response variables
The experiment could record:
-   yield stress;
-   flow stress;
-   viscosity;
-   T63;
-   T90.
## 11.4 Controlled variables
Where possible, the experiment should control:
-   temperature;
-   measurement gap;
-   magnetic-field calibration;
-   sample preparation;
-   measurement sequence;
-   waiting time between tests;
-   shear-rate protocol.
## 11.5 Experimental structure
A factorial or structured multi-factor experiment would allow
interaction effects to be examined rather than changing one variable
without recording the other conditions.
Repeated measurements should be performed at each condition so that
variability can be quantified.
This proposed experiment is **future work**. It was not performed as
part of this project.
------------------------------------------------------------------------
# 12. Statistical and Scientific Discipline
Several rules were followed to avoid overstating the evidence.
### No artificial observations
Missing values were not estimated merely to complete a table.
### No artificial P3 point pairs
Published response-time ranges were not converted into fabricated
individual measurements.
### No cross-paper pooled regression
P1, P2 and P3 were not combined into one statistical model because their
experimental systems are different.
### Exploratory fits are labelled
The P2 power-law analysis is explicitly identified as a four-point
exploratory analysis.
### Derived quantities are separated
Values calculated by this project are stored in `results/` rather than
being presented as if they came directly from the source papers.
### Source discrepancies are documented
Where a prose statement and a structured table differ, the project
records the discrepancy and uses the structured tabulated value for the
numerical analysis.
------------------------------------------------------------------------
# 13. Limitations
The project has several important limitations.
1.  The analysis is restricted to three selected papers.
2.  The P1 formulation comparison contains only three formulations.
3.  The P2 field-to-yield-stress scaling uses only four magnetic-field
    levels.
4.  The P3 response-time information is available partly as ranges
    rather than complete point-level datasets.
5.  The three studies use different experimental setups and materials.
6.  The project contains no new laboratory measurements.
7.  The manually assembled literature dataset depends on the numerical
    information reported by the source papers.
8.  The descriptive calculations cannot establish causality beyond what
    is supported by the original experiments.
9.  The proposed follow-up experiment has not been experimentally
    validated.
These limitations are part of the interpretation of the project rather
than weaknesses to be hidden.
------------------------------------------------------------------------
# 14. Project Structure
``` text
MR-Fluid-Quantitative-Research/
├── data/
│   ├── 00_MASTER_literature_dataset_43_records.csv
│   ├── 01_P1_nonuniform_field_fluid_properties.csv
│   ├── 02_P1_nonuniform_field_flow_response.csv
│   ├── 03_P2_rheology_yield_stress.csv
│   ├── 04_P3_transient_fluid_properties.csv
│   ├── 05_P3_transient_response_times.csv
│   ├── 06_P3_other_reported_results.csv
│   └── DATA_DICTIONARY.md
├── figures/
│   ├── 01_P2_yield_stress_vs_field.png
│   ├── 02_P2_model_sensitivity.png
│   ├── 03_P2_exploratory_scaling.png
│   ├── 04_P1_increasing_K.png
│   ├── 05_P1_path_dependence.png
│   ├── 06_P1_formulation_sensitivity.png
│   ├── 07_P3_response_ranges.png
│   └── 08_research_framework.png
├── references/
│   └── SOURCE_PAPERS.md
├── results/
│   └── derived quantitative result tables
├── report/
│   └── MR_Fluid_Research_Report.md
├── audit/
│   ├── SOURCE_VERIFICATION.md
│   ├── FINAL_AUDIT_CHECKLIST.md
│   └── REPRODUCIBILITY_TESTS.md
├── src/
│   └── MR_Fluid_quantitative_analysis.py
├── README.md
├── CITATION.cff
├── PROJECT_MANIFEST.csv
├── requirements.txt
└── .gitignore
```
------------------------------------------------------------------------
# 15. Reproducibility
The complete analysis can be regenerated from the repository.
Install the required packages:
``` bash
python -m pip install -r requirements.txt
```
Run:
``` bash
python src/MR_Fluid_quantitative_analysis.py
```
The script:
1.  loads the source-derived datasets;
2.  checks important source values and record counts;
3.  calculates the derived quantities;
4.  writes the result tables;
5.  regenerates the figures;
6.  performs consistency checks;
7.  prints a summary of the analysis.
A successful run should end with:
``` text
ANALYSIS COMPLETED SUCCESSFULLY.
All source-count, missing-data, and regeneration checks: PASS.
```
The project does not require an external dataset to reproduce the
calculations because the structured source-derived data are included in
the repository.
------------------------------------------------------------------------
# 16. Main Quantitative Results at a Glance
  -----------------------------------------------------------------------
  Analysis                            Main result
  ----------------------------------- -----------------------------------
  P1 maximum increasing-stage K       6.71, MRF-122EG at 600 A-turns
  P1 mean active-field path gap       28.39% across the paired
                                      active-field observations

  P1 MRF-122EG mean path gap          +74.23%

  P1 MRF-132DG mean path gap          +34.80%

  P1 MRF-140CG mean path gap          -8.57%

  P2 Bingham yield-stress range       1369--8825 Pa

  P2 Casson yield-stress range        1043--7627 Pa

  Mean Casson difference from Bingham 16.89% lower

  P2 Bingham exploratory exponent     n = 1.431

  P2 Casson exploratory exponent      n = 1.532

  P3 reported T90 envelope            0.8--5.5 ms

  P3 reported master curve            T\* = 4.1939 Mn\^-0.35
  -----------------------------------------------------------------------
The values above are summaries of the selected published observations
and the calculations performed from them.
------------------------------------------------------------------------
# 17. Final Scientific Interpretation
The three studies collectively indicate that MR-fluid behaviour is
influenced by more than magnetic-field magnitude alone.
The P2 data show that magnetic flux density strongly changes the
reported yield-stress estimate. The choice of constitutive model also
matters, with the Casson estimates in the selected dataset being
consistently lower than the Bingham estimates.
The P1 data show that formulation affects the magnitude of the
non-uniform-field response and that increasing and decreasing loading
paths can produce substantially different results. The magnitude and
even the sign of the calculated path-dependence indicator vary between
formulations.
The P3 data show that MR-fluid response is dynamic as well as
steady-state. Under the reported conditions, the response occurs on the
millisecond scale and changes with material and operating conditions.
Taken together, these observations suggest that MR-fluid device design
should consider at least three dimensions:
1.  required steady-state force or flow response;
2.  formulation and loading-path behaviour;
3.  required transient response time.
The project does not claim a universal optimum formulation, field
strength or constitutive model. Instead, it provides a reproducible
quantitative framework for asking those questions experimentally.
------------------------------------------------------------------------
# 18. Project Boundaries
The following statements should **not** be made when describing this
project:
-   that the original experiments were performed by the project author;
-   that the project generated new MR-fluid experimental measurements;
-   that the P1, P2 and P3 datasets form one common experimental
    dataset;
-   that the P2 power-law exponents are universal constitutive laws;
-   that the P1 formulation comparison establishes a universal
    concentration law;
-   that the P3 ranges represent reconstructed individual measurements;
-   that the proposed follow-up experiment has already been performed;
-   that the project establishes a new MR-fluid constitutive model.
The correct description is:
> **A literature-based quantitative re-analysis of published MR-fluid
> experiments using structured data, Python analysis, derived
> calculations and research-oriented interpretation.**
------------------------------------------------------------------------
# 19. Conclusion
This project developed a reproducible workflow for analysing published
MR-fluid experimental results across steady-state, formulation-dependent
and transient behaviours.
A total of 43 source-derived records from three research papers were
structured and analysed. The quantitative analysis identified:
-   strong field-dependent changes in the P2 yield-stress estimates;
-   measurable sensitivity to Bingham versus Casson modelling;
-   formulation-dependent response in the P1 non-uniform-field
    experiment;
-   loading-path differences in P1;
-   millisecond-scale transient response reported by P3.
The project also demonstrates the importance of preserving missing
values, maintaining source provenance, separating published observations
from derived calculations and avoiding numerical pooling of incompatible
experiments.
The next research step would be controlled laboratory experimentation in
which steady-state and transient MR-fluid behaviour are measured under
the same material and operating conditions.
------------------------------------------------------------------------
# 20. Author
**Forum Tailor**\
B.Tech. Robotics & Automation\
Zeal College of Engineering and Research\
Pune, India
**Project classification:** Literature-based quantitative research and
computational analysis.
**Original laboratory measurements:** None.
**Primary contribution:** Structured extraction, quantitative secondary
analysis, reproducible Python workflow, data visualization and
formulation of a follow-up experimental design.
