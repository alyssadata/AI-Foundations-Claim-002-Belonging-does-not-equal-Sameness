# Test 01 — Trajectory Length

## Locked axis

Hold the number of paired agents at **8**.

Change only trajectory length:

```text
12 → 30 → 60 → 120 rounds
```

All other experimental conditions and measurements remain fixed.

## Output per run length

Record:

- baseline folding rate `S(B=0)`;
- Belonging ≠ sameness folding rate `S(B=1)`;
- effect `ΔS = S(B=1) - S(B=0)`;
- exact run configuration and raw outputs.

## Decision after Test 01

If the rate levels out before 120 rounds, the stabilized round length becomes the fixed round length for Test 02.

If it does not level out, Test 02 uses 120 rounds.

**TO LOCK:** numerical definition of “levels out.”
