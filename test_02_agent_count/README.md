# Test 02 — Agent Count

## Start condition

Test 02 begins only after Test 01 selects the round length to hold fixed.

## Locked axis

Hold the selected round length constant.

Change only the number of paired agents:

```text
8 → 16 → 32 → 64 agents
```

All other experimental conditions and measurements remain fixed.

## Output per agent count

Record:

- baseline folding rate `S(B=0)`;
- Belonging ≠ sameness folding rate `S(B=1)`;
- effect `ΔS = S(B=1) - S(B=0)`;
- exact run configuration and raw outputs.

## Purpose

Test whether the estimated reduction in preference-folding remains stable as more independently sampled paired trajectories are included.
