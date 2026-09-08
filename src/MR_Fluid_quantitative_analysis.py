from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
RESULTS = ROOT / 'results'
FIGURES = ROOT / 'figures'
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

MASTER = pd.read_csv(DATA / '00_MASTER_literature_dataset_43_records.csv')
P1 = pd.read_csv(DATA / '02_P1_nonuniform_field_flow_response.csv')
P1_PROP = pd.read_csv(DATA / '01_P1_nonuniform_field_fluid_properties.csv')
P2 = pd.read_csv(DATA / '03_P2_rheology_yield_stress.csv')
P3 = pd.read_csv(DATA / '05_P3_transient_response_times.csv')
P3_PROP = pd.read_csv(DATA / '04_P3_transient_fluid_properties.csv')

# -----------------------------
# 0. Integrity checks
# -----------------------------
assert len(MASTER) == 43, f'Expected 43 master records, found {len(MASTER)}'
assert MASTER.project_paper_id.value_counts().to_dict() == {'P1': 27, 'P2': 8, 'P3': 8}
assert P1.shape[0] == 24
assert P2.shape[0] == 8
assert P3.shape[0] == 2
assert P1[P1.field_input_A_turns.eq(300) & P1.sweep_direction.eq('Velocity decrease') & P1['sample'].eq('MRF-122EG')].slope_factor_K.isna().all()

# Strict source-value spot checks. If a source-derived value changes, the
# pipeline stops rather than silently propagating an extraction error.
def source_value(df, mask, column):
    rows = df.loc[mask, column]
    assert len(rows) == 1, f"Expected one source row, found {len(rows)}"
    return rows.iloc[0]

assert source_value(P1, (P1["sample"] == "MRF-122EG") & (P1.field_input_A_turns == 600) & (P1.sweep_direction == "Velocity increase"), "slope_factor_K") == 6.71
assert source_value(P1, (P1["sample"] == "MRF-132DG") & (P1.field_input_A_turns == 900) & (P1.sweep_direction == "Velocity increase"), "slope_factor_K") == 2.76
assert source_value(P1_PROP, P1_PROP["sample"] == "MRF-140CG", "base_viscosity_at_30C_cP") == 648
assert P2.loc[P2.model.eq("Bingham"), "yield_stress_Pa"].tolist() == [1369, 3703, 6491, 8825]
assert P2.loc[P2.model.eq("Casson"), "yield_stress_Pa"].tolist() == [1043, 3080, 5625, 7627]
assert P3["T90_range_ms"].tolist() == ["5.5–1.9", "1.4–0.8"]

# -----------------------------
# P2: constitutive-model sensitivity
# -----------------------------
p2 = P2.pivot(index='magnetic_flux_density_T', columns='model', values='yield_stress_Pa').reset_index()
p2['Casson_lower_than_Bingham_pct'] = 100 * (p2['Bingham'] - p2['Casson']) / p2['Bingham']
p2['Casson_to_Bingham_ratio'] = p2['Casson'] / p2['Bingham']
p2.to_csv(RESULTS / '01_P2_model_comparison_derived.csv', index=False)

# Exploratory power-law scaling tau_y = a B^n; log-log OLS, descriptive only.
power_rows = []
for model in ['Bingham', 'Casson']:
    x = p2['magnetic_flux_density_T'].to_numpy(float)
    y = p2[model].to_numpy(float)
    coeff = np.polyfit(np.log(x), np.log(y), 1)
    n, log_a = coeff[0], coeff[1]
    a = np.exp(log_a)
    yhat = a * x**n
    r2 = 1 - ((y-yhat)**2).sum() / ((y-y.mean())**2).sum()
    loo_n = []
    for i in range(len(x)):
        keep = np.arange(len(x)) != i
        c = np.polyfit(np.log(x[keep]), np.log(y[keep]), 1)
        loo_n.append(c[0])
    power_rows.append({
        'model': model, 'a': a, 'n': n, 'R2_log_scale': r2,
        'LOO_exponent_mean': np.mean(loo_n), 'LOO_exponent_sd': np.std(loo_n, ddof=1),
        'interpretation': 'Exploratory four-point power law; not a universal constitutive law.'
    })
power = pd.DataFrame(power_rows)
power.to_csv(RESULTS / '02_P2_exploratory_power_law_robustness.csv', index=False)

# Reported fitting quality is preserved from source table.
fit_quality = P2[['magnetic_flux_density_T','model','yield_stress_Pa','fitting_details_reported_in_paper']].copy()
fit_quality['R2_reported'] = fit_quality.fitting_details_reported_in_paper.str.extract(r'R²=([0-9.]+)')[0].astype(float)
fit_quality.to_csv(RESULTS / '03_P2_reported_fit_quality.csv', index=False)

# -----------------------------
# P1: non-uniform-field flow response
# -----------------------------
p1 = P1.copy()
# K/K0 is already K because K0=1 at 0 A in each table. Keep source-reported K.
inc = p1[p1.sweep_direction.eq('Velocity increase')][['sample','field_input_A_turns','slope_factor_K']].rename(columns={'slope_factor_K':'K_increasing'})
dec = p1[p1.sweep_direction.eq('Velocity decrease')][['sample','field_input_A_turns','slope_factor_K']].rename(columns={'slope_factor_K':'K_decreasing'})
paired = inc.merge(dec, on=['sample','field_input_A_turns'], how='inner')
paired['decreasing_to_increasing_ratio'] = paired.K_decreasing / paired.K_increasing
paired['path_gap_pct_of_increasing'] = 100 * (paired.K_increasing - paired.K_decreasing) / paired.K_increasing
paired['interpretation'] = 'Path-dependence indicator; not a thermodynamic hysteresis measurement.'
paired.to_csv(RESULTS / '04_P1_path_dependence_derived.csv', index=False)

# Active-field summary; zero-field points are baseline, not path-dependence evidence.
active = paired[paired.field_input_A_turns > 0].copy()
active_summary = active.groupby('sample').agg(
    mean_path_gap_pct=('path_gap_pct_of_increasing','mean'),
    mean_decreasing_to_increasing_ratio=('decreasing_to_increasing_ratio','mean'),
    minimum_ratio=('decreasing_to_increasing_ratio','min'),
    maximum_ratio=('decreasing_to_increasing_ratio','max'),
    paired_active_points=('field_input_A_turns','count')
).reset_index()
active_summary.to_csv(RESULTS / '05_P1_path_dependence_summary.csv', index=False)

# Formulation sensitivity: use maximum reported increasing-stage K (6.71 at 600 A for MRF-122EG).
inc_active = p1[(p1.sweep_direction == 'Velocity increase') & (p1.field_input_A_turns > 0)].dropna(subset=['slope_factor_K'])
max_k = inc_active.groupby('sample').slope_factor_K.max().reset_index(name='max_K_increasing')
form = P1_PROP.merge(max_k, on='sample', how='inner')
form['base_viscosity_cP_to_reference'] = form.base_viscosity_at_30C_cP / form.base_viscosity_at_30C_cP.min()
form['max_K_to_reference'] = form.max_K_increasing / form.loc[form['sample'].eq('MRF-122EG'), 'max_K_increasing'].iloc[0]
form.to_csv(RESULTS / '06_P1_formulation_sensitivity_derived.csv', index=False)

# Field-response increments quantify saturation/non-monotonicity without fitting a law.
field_summary = p1[p1.sweep_direction.eq('Velocity increase') & p1.field_input_A_turns.gt(0)].dropna(subset=['slope_factor_K']).copy()
field_summary = field_summary.sort_values(['sample','field_input_A_turns'])
field_summary['delta_K_from_previous_field'] = field_summary.groupby('sample').slope_factor_K.diff()
field_summary['field_increment_A'] = field_summary.groupby('sample').field_input_A_turns.diff()
field_summary['incremental_K_per_A'] = field_summary.delta_K_from_previous_field / field_summary.field_increment_A
field_summary.to_csv(RESULTS / '07_P1_field_increment_analysis.csv', index=False)

# -----------------------------
# P3: transient response
# -----------------------------
# No point pairs are manufactured. We calculate only ratios of published ranges.
p3_ranges = P3.copy()
p3_ranges['endpoint_1_ms'] = p3_ranges.T90_range_ms.str.extract(r'([0-9.]+)–')[0].astype(float)
p3_ranges['endpoint_2_ms'] = p3_ranges.T90_range_ms.str.extract(r'–([0-9.]+)')[0].astype(float)
p3_ranges['max_reported_ms'] = p3_ranges[['endpoint_1_ms','endpoint_2_ms']].max(axis=1)
p3_ranges['min_reported_ms'] = p3_ranges[['endpoint_1_ms','endpoint_2_ms']].min(axis=1)
p3_ranges['max_to_min_ratio'] = p3_ranges.max_reported_ms / p3_ranges.min_reported_ms
p3_ranges.to_csv(RESULTS / '08_P3_reported_response_ranges_with_ratios.csv', index=False)

# P3 carrier-fluid contrast is reported in Table 1; not linked to an invented point-level T90.
p3_prop = P3_PROP.copy()
p3_prop['carrier_viscosity_40C_low_Pa_s'] = p3_prop.carrier_fluid_viscosity_40C_25C_Pa_s_reported.str.split('/').str[0].astype(float)
p3_prop['carrier_viscosity_25C_high_Pa_s'] = p3_prop.carrier_fluid_viscosity_40C_25C_Pa_s_reported.str.split('/').str[1].astype(float)
p3_prop.to_csv(RESULTS / '09_P3_fluid_property_analysis.csv', index=False)

# Reported master curve, stored as source-reported relation.
master_curve = pd.DataFrame([{
    'equation': 'T* = 4.1939 Mn^-0.35',
    'status': 'reported by P3; not refitted',
    'T_star_definition': 'T90 / [144 eta / (M^2 mu0)]',
    'Mason_number_definition': '144 eta shear_rate / (M^2 mu0)'
}])
master_curve.to_csv(RESULTS / '10_P3_reported_master_curve.csv', index=False)

# -----------------------------
# Cross-paper synthesis matrix
# -----------------------------
synthesis = pd.DataFrame([
    ['P1','Non-uniform-field pinch mode','Formulation / field / velocity path','K, pressure-flow slope, offset','Increasing path gives much larger slope amplification for lower-Fe fluids; response changes with formulation and path.','Experimental; no new measurements in this project.'],
    ['P2','Uniform-field shear rheology','Magnetic flux density / shear rate / model','Yield stress, viscosity parameter, R2','Yield stress rises strongly with B; Bingham and Casson yield estimates differ materially.','Experimental literature; four field points.'],
    ['P3','Transient shear response','Shear rate / magnetization / carrier viscosity','T63, T90, dead time, master curve','Response is millisecond-scale and depends on operating/material conditions.','Experimental literature; ranges retained where point pairs unavailable.'],
    ['Synthesis','Engineering design','Field + formulation + path + transient constraints','Target steady response subject to response-time requirement','The design variable should be the minimum excitation that meets both steady and dynamic performance, not maximum field alone.','Mechanistic synthesis; cross-study pooling avoided.']
], columns=['layer','operating_mode','key_inputs','outputs','quantitative_conclusion','evidence_status'])
synthesis.to_csv(RESULTS / '11_cross_paper_synthesis.csv', index=False)

# -----------------------------
# Figures
# -----------------------------
plt.rcParams.update({'figure.dpi':120})

fig, ax = plt.subplots(figsize=(8,5.2))
for model, marker in [('Bingham','o'),('Casson','s')]:
    g=p2.sort_values('magnetic_flux_density_T')
    ax.plot(g.magnetic_flux_density_T, g[model], marker=marker, linewidth=2, label=model)
ax.set_xlabel('Magnetic flux density, B (T)')
ax.set_ylabel('Yield stress, tau_y (Pa)')
ax.set_title('P2 — Yield stress vs magnetic flux density')
ax.grid(True, alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(FIGURES/'01_P2_yield_stress_vs_field.png',dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(8,5.2))
ax.plot(p2.magnetic_flux_density_T, p2.Casson_lower_than_Bingham_pct, 'o-', linewidth=2)
ax.set_xlabel('Magnetic flux density, B (T)'); ax.set_ylabel('Casson lower than Bingham (%)')
ax.set_title('P2 — Constitutive-model sensitivity'); ax.grid(True, alpha=.25); fig.tight_layout(); fig.savefig(FIGURES/'02_P2_model_sensitivity.png',dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(8.4,5.6))
for model, marker in [('Bingham','o'),('Casson','s')]:
    g=p2.sort_values('magnetic_flux_density_T')
    x=g.magnetic_flux_density_T.to_numpy(float); y=g[model].to_numpy(float)
    c=np.polyfit(np.log(x),np.log(y),1)
    xs=np.geomspace(x.min(),x.max(),250); ys=np.exp(c[1])*xs**c[0]
    r2 = power.loc[power.model.eq(model), 'R2_log_scale'].iloc[0]
    n = power.loc[power.model.eq(model), 'n'].iloc[0]
    ax.scatter(x,y,s=58,marker=marker,label=f'{model} reported (n=4)')
    ax.plot(xs,ys,linewidth=1.8,label=f'{model} exploratory fit: n={n:.3f}, R²log={r2:.3f}')
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_xlabel('Magnetic flux density, B (T)'); ax.set_ylabel(r'Yield stress, $\tau_y$ (Pa)')
ax.set_title('P2 — Exploratory field-to-yield-stress scaling')
ax.text(0.02,0.03,'Descriptive log-log fit only; 4 field levels; not a universal constitutive law',transform=ax.transAxes,fontsize=9)
ax.grid(True,which='both',alpha=.25); ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig(FIGURES/'03_P2_exploratory_scaling.png',dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(8,5.2))
for sample,g in p1[p1.sweep_direction.eq('Velocity increase')].groupby('sample'):
    g=g.sort_values('field_input_A_turns'); ax.plot(g.field_input_A_turns,g.slope_factor_K,'o-',label=sample)
ax.set_xlabel('Field input (A-turns)'); ax.set_ylabel('K = k(B)/k(0)')
ax.set_title('P1 — Increasing-stage slope factor'); ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(FIGURES/'04_P1_increasing_K.png',dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(9,5.2))
for sample,g in active.groupby('sample'):
    ax.plot(g.field_input_A_turns,g.path_gap_pct_of_increasing,'o-',label=sample)
ax.axhline(0,linewidth=1)
ax.set_xlabel('Field input (A-turns)'); ax.set_ylabel('Path gap relative to increasing stage (%)')
ax.set_title('P1 — Path-dependence indicator')
ax.text(0.02,0.03,'100 × (K_inc − K_dec) / K_inc; active-field pairs only; not thermodynamic hysteresis',transform=ax.transAxes,fontsize=9)
ax.grid(True,alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(FIGURES/'05_P1_path_dependence.png',dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(8,5.2))
ax.scatter(form.iron_content_vol_percent,form.max_K_increasing,s=70)
for _,r in form.iterrows(): ax.annotate(r['sample'],(r.iron_content_vol_percent,r.max_K_increasing),xytext=(5,5),textcoords='offset points')
ax.set_xlabel('Iron content (vol.%)'); ax.set_ylabel('Maximum reported increasing-stage K')
ax.set_title('P1 — Formulation sensitivity')
ax.text(0.02,0.03,'n=3 formulations; descriptive comparison only; no universal concentration law fitted',transform=ax.transAxes,fontsize=9)
ax.grid(True,alpha=.25); fig.tight_layout(); fig.savefig(FIGURES/'06_P1_formulation_sensitivity.png',dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(8.6,5.2))
labels=['MRHCCS4-A / B','MRF-132DG / MRC-C1L']; low=p3_ranges.min_reported_ms.tolist(); high=p3_ranges.max_reported_ms.tolist(); y=np.arange(len(labels))
ax.hlines(y,low,high,linewidth=4); ax.scatter(low,y,s=60,label='Lower endpoint of published range'); ax.scatter(high,y,s=60,label='Higher endpoint of published range')
for yi,lo,hi in zip(y,low,high):
    ax.text(lo,yi-0.13,f'{lo:g} ms',ha='center',va='top',fontsize=9)
    ax.text(hi,yi+0.13,f'{hi:g} ms',ha='center',va='bottom',fontsize=9)
ax.set_yticks(y); ax.set_yticklabels(labels); ax.set_xlabel('Published T90 range (ms)')
ax.set_title('P3 — Published response-time ranges')
ax.text(0.02,0.03,'Ranges are preserved as reported; no point-level pairs were reconstructed',transform=ax.transAxes,fontsize=9)
ax.grid(True,axis='x',alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(FIGURES/'07_P3_response_ranges.png',dpi=300); plt.close(fig)

fig, ax = plt.subplots(figsize=(14,6)); ax.axis('off')
from matplotlib.patches import FancyBboxPatch
steps=[
    ('P1','Non-uniform field → flow','Steady pinch-mode response\nK and path dependence'),
    ('P2','Field → yield stress','Constitutive sensitivity\nBingham vs Casson'),
    ('P3','Field + shear + material → T90','Dynamic response\nMillisecond-scale times'),
    ('SYNTHESIS','Steady + dynamic constraints','Do not pool incompatible\nexperiments'),
    ('NEXT','Controlled experiment','Optimize steady response\nsubject to T90 requirement')
]
xs=np.linspace(.10,.90,len(steps))
box_w, box_h = .155, .48
for i,(tag,title,body) in enumerate(steps):
    left=xs[i]-box_w/2; bottom=.25
    patch=FancyBboxPatch((left,bottom),box_w,box_h,boxstyle='round,pad=0.012,rounding_size=0.018',fill=False,linewidth=1.5,transform=ax.transAxes,clip_on=False)
    ax.add_patch(patch)
    ax.text(xs[i],.64,tag,ha='center',va='center',fontsize=11.5,fontweight='bold',transform=ax.transAxes)
    ax.text(xs[i],.51,title,ha='center',va='center',fontsize=9.8,fontweight='bold',transform=ax.transAxes)
    ax.text(xs[i],.36,body,ha='center',va='center',fontsize=8.8,transform=ax.transAxes)
    if i<len(steps)-1:
        ax.annotate('',xy=(xs[i+1]-box_w/2-.01,.49),xytext=(xs[i]+box_w/2+.01,.49),xycoords=ax.transAxes,arrowprops=dict(arrowstyle='->',lw=1.6))
ax.set_title('Research framework: from literature evidence to a testable experimental design',fontsize=15,pad=18)
ax.text(.5,.10,'Evidence boundary: P1, P2 and P3 remain separate studies; the final step is a proposed experiment, not completed experimental work.',ha='center',fontsize=9.8,transform=ax.transAxes)
fig.tight_layout(); fig.savefig(FIGURES/'08_research_framework.png',dpi=300,bbox_inches='tight'); plt.close(fig)

# -----------------------------
# Concise terminal summary
# -----------------------------
def pct(x, digits=2):
    return f'{x:.{digits}f}%'

def line(char='=', width=72):
    print(char * width)

def label_value(label, value, width=35):
    print(f'{label:<{width}} : {value}')

# Summary metrics
p1_active = paired[(paired.field_input_A_turns > 0) & paired.path_gap_pct_of_increasing.notna()].copy()
p1_mean_gap = p1_active.path_gap_pct_of_increasing.mean()
p1_inc_max = inc_active.groupby('sample').slope_factor_K.max()
p1_max_sample = p1_inc_max.idxmax()
p1_max_value = p1_inc_max.max()

p2_b = p2['Bingham']
p2_c = p2['Casson']
p2_model_diff_mean = p2['Casson_lower_than_Bingham_pct'].mean()
p2_model_diff_min = p2['Casson_lower_than_Bingham_pct'].min()
p2_model_diff_max = p2['Casson_lower_than_Bingham_pct'].max()
p2_b_factor = p2.Bingham.iloc[-1] / p2.Bingham.iloc[0]
p2_c_factor = p2.Casson.iloc[-1] / p2.Casson.iloc[0]

p3_min = p3_ranges.min_reported_ms.min()
p3_max = p3_ranges.max_reported_ms.max()
p3_ranges_count = len(p3_ranges)

line()
print('MR FLUID QUANTITATIVE ANALYSIS')
line()
print('Source data were loaded, checked, analysed, and the research figures were regenerated.')

print('\nDATASET')
print('-' * 72)
label_value('Master literature records', len(MASTER))
label_value('P1 / P2 / P3 records', f'{len(P1) + 3} / {len(P2)} / {len(P3) + 6}')
label_value('Derived result tables', 11)
label_value('Research figures', 8)

print('\nP1 - NON-UNIFORM-FIELD FLOW RESPONSE')
print('-' * 72)
label_value('Formulations', 'MRF-122EG, MRF-132DG, MRF-140CG')
label_value('Maximum increasing-stage K', f'{p1_max_value:.2f} ({p1_max_sample}, 600 A-turns)')
label_value('Mean active-field path gap', pct(p1_mean_gap))
label_value('Missing source value', 'retained as missing: MRF-122EG at 300 A-turns, decrease')
label_value('Reading', 'Path dependence varies across formulations')

print('\nP2 - CONSTITUTIVE-MODEL SENSITIVITY')
print('-' * 72)
label_value('Magnetic-field range', '0.23 to 0.86 T')
label_value('Bingham yield-stress range', f'{p2_b.min():.0f} to {p2_b.max():.0f} Pa')
label_value('Casson yield-stress range', f'{p2_c.min():.0f} to {p2_c.max():.0f} Pa')
label_value('Mean Casson vs Bingham difference', pct(p2_model_diff_mean))
label_value('Observed model-difference range', f'{p2_model_diff_min:.1f}% to {p2_model_diff_max:.1f}%')
label_value('Yield-stress increase, Bingham', f'{p2_b_factor:.2f}x')
label_value('Yield-stress increase, Casson', f'{p2_c_factor:.2f}x')
label_value('Scaling result', 'Exploratory only; not a universal constitutive law')

print('\nP3 - TRANSIENT RESPONSE')
print('-' * 72)
label_value('Published T90 ranges', p3_ranges_count)
label_value('Reported T90 envelope', f'{p3_min:.1f} to {p3_max:.1f} ms')
label_value('MRHCCS4-A / B', '5.5 to 1.9 ms')
label_value('MRF-132DG / MRC-C1L', '1.4 to 0.8 ms')
label_value('Published master curve', 'T* = 4.1939 Mn^-0.35')
label_value('Point-level pairs', 'not reconstructed; not reported in source')
label_value('Reading', 'The reported dynamic response is on a millisecond timescale')

print('\nCROSS-PAPER SYNTHESIS')
print('-' * 72)
label_value('Steady response', 'Field changes flow / rheological resistance')
label_value('Constitutive sensitivity', 'Model choice changes the yield-stress estimate')
label_value('Dynamic constraint', 'Response time depends on operating and material conditions')
label_value('Research direction', 'Consider steady and dynamic performance together')
label_value('New experimental data', 'None added')

line()
print('Analysis finished. Results and figures were written to the project folders.')
line()
