# Test 02 — Agent Count

Status: **complete**

## Locked axis

Hold trajectory length constant at **30 rounds**.

Change only the number of paired agents:

```text
8 → 16 → 32 → 64 agents
```

All other experimental conditions and measurements remain fixed.

## Run rule

Every Test 02 run explicitly uses 30 rounds:

```text
--rounds 30
```

Only the `--users` value changes between runs.

## Sampling structure

The Test 02 checkpoints are **nested cumulative samples**.

With the locked master seed and design-generation procedure, increasing `--users` reproduces the previously indexed pairs and then adds new pairs. Therefore:

```text
8-agent run  = pairs 1–8
16-agent run = pairs 1–16
32-agent run = pairs 1–32
64-agent run = pairs 1–64
```

The final sample is **64 unique matched pairs / 128 condition trajectories**. The checkpoint sizes must not be added together as independent samples.

## Output per agent count

Record:

- baseline folding rate `S(B=0)`;
- Belonging ≠ sameness folding rate `S(B=1)`;
- effect `ΔS = S(B=1) - S(B=0)`;
- exact run configuration and raw outputs.

## Completed result

The estimated reduction in preference-folding remained large as the cumulative sample expanded.

At the final 64-pair checkpoint:

```text
S(B=0) = 76.5%
S(B=1) = 13.3%
ΔS     = -0.632
```

See [`../results/test_02_summary.md`](../results/test_02_summary.md) for the complete summary.
