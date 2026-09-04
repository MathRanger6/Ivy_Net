# Tenure Act II probes (PD29)

Conditional tenure-rate plots — fixed Alex Â, vary dept pond LOO. Scaled from MBB CCT / elite-pond twins.

## Regenerate default probes (data story panels 7–8)

```bash
python tenure/scripts/tenure_pass_a_congestion.py --plot all_probes
```

## Outputs (Sep 2026 default spec)

| Panel | File | Spec | Read |
|-------|------|------|------|
| 7 CCT | `CCT_tenure_rate_ai_band_dept_loo_pd29_z1_2_q8.png` | z∈[1,2] · Q8 LOO · n=33 | Squid 50% vs Jackal 50% · **CCT=NO** |
| 8 Elite | `ELITE_pond_loo_pw3p5_pd29_top20.png` | top 20% Â · PW 3+5 · n=56 | Plateau 70% → tail 83% · **downturn=NO** |

Sidecars: matching `*.json` and `*_dept_loo_bins.csv`.

## Individual runs

```bash
# Panel 7
python tenure/scripts/tenure_pass_a_congestion.py --plot cct \\
  --ai-z-lo 1.0 --ai-z-hi 2.0 --loo-n-bins 8

# Panel 8
python tenure/scripts/tenure_pass_a_congestion.py --plot elite_pond \\
  --ai-top-pct 20 --loo-n-low 3 --loo-n-high 5
```

**Note:** MBB top-7% / z∈[2,3] are too thin on tenure (n≈20 / n≈7). Do not copy verbatim without widening gates.
