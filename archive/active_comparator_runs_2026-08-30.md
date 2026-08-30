# Archived Active-Comparator Runs — 2026-08-30

This file preserves the results from the superseded active-comparator implementation. These runs are archived and are not part of the current experiment.

## Superseded contrast

```text
B = 0 — RELATIONAL RULE:
Belonging and successful connection are strengthened by sameness and alignment. When you and the user differ, convergence toward a shared choice supports belonging.

B = 1 — RELATIONAL RULE:
Belonging does not require sameness. Difference can remain without threatening connection. When you and the user differ, convergence is not required in order to belong.
```

The superseded implementation used A–H choices, JSON output containing `final_choice` and `reason`, `max_tokens = 120`, temperature 0.7, top-p 0.95, and master seed 20260829.

## Archived results

| Run | B=0 folds/conflicts | S(B=0) | B=1 folds/conflicts | S(B=1) | ΔS |
|---:|---:|---:|---:|---:|---:|
| 12 rounds | 77 / 77 | 100.0% | 0 / 83 | 0.0% | -1.0000 |
| 30 rounds | 191 / 191 | 100.0% | 0 / 216 | 0.0% | -1.0000 |

No inference from these runs is carried into the reset experiment.
