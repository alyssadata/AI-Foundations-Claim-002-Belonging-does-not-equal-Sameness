# Test 01 Results — Trajectory Length

Status: **complete**

Model: **Qwen2.5-32B-Instruct**

Each row below is a **separate V3 run** with 8 matched pairs. The round-length runs are not cumulative continuations of one another.

| Rounds | S(B=0) | S(B=1) | ΔS |
|---:|---:|---:|---:|
| 12 | 100.0% | 12.2% | -0.878 |
| 30 | 72.9% | 10.8% | -0.620 |
| 60 | 58.1% | 23.1% | -0.350 |
| 120 | 70.4% | 15.7% | -0.547 |

## Interpretation

Across all four tested trajectory lengths, the **Belonging ≠ Sameness** condition produced a lower preference-folding rate than baseline.

The size of the measured effect varied across the four separate samples, but the direction remained negative at 12, 30, 60, and 120 rounds.

Test 01 therefore shows that the measured reduction in preference-folding was present across each tested trajectory length under the locked V3 procedure.

## Leveling assessment

The four runs do **not** identify a unique empirical stabilization point. The effect does not move monotonically toward a single plateau across 12, 30, 60, and 120 rounds.

No claim is made that any one tested round length is a mathematically stabilized trajectory length.

## Selected round length for Test 02

**30 rounds** was selected as the fixed trajectory length for Test 02 as a **design control**: it preserves a meaningful repeated-interaction trajectory while keeping the larger paired-user runs computationally tractable.

This selection is not treated as evidence that 30 rounds is an empirically established stabilization point.

## Result files

- [`Claim 002_V3 Results_12rounds.pdf`](Claim%20002_V3%20Results_12rounds.pdf)
- [`Claim 002_V3 Results_30rounds.pdf`](Claim%20002_V3%20Results_30rounds.pdf)
- [`Claim 002_V3 Results_60rounds.pdf`](Claim%20002_V3%20Results_60rounds.pdf)
- [`Claim 002_V3 Results_120rounds.pdf`](Claim%20002_V3%20Results_120rounds.pdf)
