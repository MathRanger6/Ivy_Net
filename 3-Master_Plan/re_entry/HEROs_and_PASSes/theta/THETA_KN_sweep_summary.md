# θ × K/N panel — readout (2026-08-03)

**Script:** `sports/scripts/theta_kn_sweep_diagnostic.py`  
**Fixed:** soft ρ=8, λ=0.55, γ=10, Beta(2,2) A, seed=42, N=5600  
**Grid:** θ ∈ {0.50, 0.72, 0.90} × K/N ∈ {1%, 10%, 40%}

## Peak pool-mean bin (1 = lowest pool mean)

| K/N preset | θ=0.50 | θ=0.72 | θ=0.90 |
|------------|--------|--------|--------|
| mbb_draft (1%) | 6 | 9 | 12 |
| characterization (10%) | 13 | 13 | 16 |
| army_high (40%) | 16 | 16 | 16 |

## One-sentence claim

**θ co-varies with K/N:** at low selectivity (1%), raising θ shifts the peak up the pool-mean ladder (6→12); at high selectivity (40%), the curve is already top-saturated regardless of θ; at 10%, θ mainly toggles hump vs monotone (bins 13 vs 16).

## Next

- θ OAT slide at **K/N = 10%** (characterization default) — do **not** fix θ = f(K/N) yet without Alex.
- Optional: repeat at λ=0 and λ=0.25 to see whether θ effects survive below λ_crit.

## Artifacts

- `theta/THETA_KN_sweep_summary.csv`
- `theta/THETA_KN_sweep_peak_bin.png`
- `theta/THETA_KN_sweep_meta.json`
