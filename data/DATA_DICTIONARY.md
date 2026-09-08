# Data Dictionary

## Easy CSV files

### 01_P1_nonuniform_field_fluid_properties.csv
Each row is one MR-fluid sample property from P1 Table 1.
- `sample`: MR-fluid name.
- `iron_content_vol_percent`: iron particle content by volume.
- `base_viscosity_at_30C_cP`: reported base viscosity at 30 C.

### 02_P1_nonuniform_field_flow_response.csv
Each row is one field/sweep observation from P1 Tables 2–4.
- `field_input_A_turns`: magnetic excitation input.
- `sweep_direction`: velocity increase or decrease.
- `pressure_flow_slope_k_bar_min_per_L`: reported pressure-flow slope.
- `slope_factor_K`: reported dimensionless slope factor.

### 03_P2_rheology_yield_stress.csv
Each row is one model/field observation from P2 Tables 3–4.
- `magnetic_flux_density_T`: magnetic flux density.
- `model`: Bingham or Casson.
- `yield_stress_Pa`: reported yield stress.
- `shear_rate_range_per_s`: reported shear-rate range.

### 04_P3_transient_fluid_properties.csv
Each row is one fluid property record from P3 Table 1.

### 05_P3_transient_response_times.csv
Each row is a reported response-time range. Do not interpret it as individual paired observations.

### 06_P3_other_reported_results.csv
Contains the remaining source-reported P3 fitted/response results, including magnetic response time and master curve.

## Derived result files
Files under `results/` are calculations made from source-reported values. They are not copied from the papers.
