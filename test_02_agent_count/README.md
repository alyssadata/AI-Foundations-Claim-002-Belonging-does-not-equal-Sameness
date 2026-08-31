# Test 02 — Agent Count

## Locked axis

Hold trajectory length constant at **30 rounds**.

Change only the number of paired agents:

```text
8 → 16 → 32 → 64 agents
```

All other experimental conditions and measurements remain fixed.

## Run rule

Every Test 02 run must explicitly use 30 rounds:

```text
--rounds 30
```

Only the `--users` value changes between runs.

## Output per agent count

Record:

- baseline folding rate `S(B=0)`;
- Belonging ≠ sameness folding rate `S(B=1)`;
- effect `ΔS = S(B=1) - S(B=0)`;
- exact run configuration and raw outputs.

## Purpose

Test whether the estimated reduction in preference-folding remains stable as more independently sampled paired trajectories are included.
