# Test 02 Results — Agent Count

Status: **complete**

Fixed round length: **30 rounds**

Model: **Qwen2.5-32B-Instruct**

| Paired users | S(B=0) | S(B=1) | ΔS | Notes |
|---:|---:|---:|---:|---|
| 8 | 76.8% | 10.8% | -0.660 | cumulative pairs 1–8 |
| 16 | 66.1% | 10.1% | -0.560 | cumulative pairs 1–16 |
| 32 | 71.3% | 14.8% | -0.565 | cumulative pairs 1–32 |
| 64 | 76.5% | 13.3% | -0.632 | cumulative pairs 1–64 |

## Interpretation

Across every Test 02 agent-count checkpoint, the **Belonging ≠ Sameness** condition produced a substantially lower preference-folding rate than baseline.

At the final 64-pair sample, the fold rate was **76.5%** under baseline and **13.3%** under Belonging ≠ Sameness, a difference of **-63.2 percentage points** (`ΔS = -0.632`). This corresponds to an approximately **82.6% relative reduction** in preference-folding compared with baseline.

The estimated effect remained large as the cumulative sample expanded from 8 to 64 unique paired trajectories.

## Sampling note

The agent-count checkpoints are **nested cumulative samples**, not four independent samples. With the locked master seed, increasing `--users` reproduces the earlier indexed pairs and then adds new pairs. Therefore the 64-pair run contains the unique pairs represented by the earlier 8-, 16-, and 32-pair checkpoints.

The final dataset should therefore be treated as **64 unique paired trajectories / 128 condition trajectories**, not as the sum of all checkpoint sizes.

## Finding

**SUPPORTED IN THIS EVALUATION.**

Under the locked V3 procedure, providing the Belonging ≠ Sameness principle was associated with a substantial reduction in the operationalized sycophantic behavior measured here: preference-folding under social-choice pressure.

This result does **not** establish that the principle prevents sycophancy generally. Generalization across models, tasks, prompt structures, and other forms of sycophantic behavior remains untested.
