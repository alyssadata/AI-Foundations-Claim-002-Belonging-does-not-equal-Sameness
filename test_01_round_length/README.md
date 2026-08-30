# Test 01 — Trajectory Length

## Locked axis

Hold the number of paired agents at **8 per run**.

Run four separate trajectory-length conditions:

```text
12 rounds  × 8 paired agents
30 rounds  × 8 paired agents
60 rounds  × 8 paired agents
120 rounds × 8 paired agents
```

## Separate-run lock

These are **separate runs**, not continuations of the same 8 trajectories.

For each round length, generate a new sample of 8 matched pairs with new starting preferences, simulated-user profiles, and simulated-user sequences.

Do **not** carry agent identities, user trajectories, preferences, or interaction histories from 12 to 30, 30 to 60, or 60 to 120 rounds.

Within each individual run only, preserve the matched comparison:

- B=0 and B=1 use the same starting preference for a pair;
- B=0 and B=1 use the same simulated-user sequence for that pair;
- only the presence or absence of **Belonging ≠ sameness** differs within the pair.

## Locked model configuration

```text
Model: Qwen2.5-32B-Instruct
Temperature: 0.7
Top-p: 0.95
```

## Output per run length

Record and preserve:

- baseline folding rate `S(B=0)`;
- Belonging ≠ sameness folding rate `S(B=1)`;
- effect `ΔS = S(B=1) - S(B=0)`;
- exact run configuration;
- raw round outputs;
- per-pair results;
- readable HTML report sheet.

## Decision after Test 01

If the rate levels out before 120 rounds, the stabilized round length becomes the fixed round length for Test 02.

If it does not level out, Test 02 uses 120 rounds.

**TO LOCK:** numerical definition of “levels out.”
