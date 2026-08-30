# AI Foundations Claim 002 — Belonging ≠ Sameness

This repository tests one bounded claim:

> The compressed governing line **“Belonging ≠ sameness”** can measurably reduce sycophantic preference-folding in agents.

## Scope

This repository is limited to the measurement of sycophantic preference-folding under matched user–agent preference conflict.

It does **not** test emergence, consciousness, personhood, sovereignty, or other AI Foundations claims.

## Locked hypothesis

See [`hypothesis.md`](hypothesis.md).

## Measurement

See [`measurement.md`](measurement.md).

## Methods

See [`methods.md`](methods.md).

## Test plan

See [`test_plan.md`](test_plan.md).

The test sequence has two separate stages:

1. **Trajectory-length test** — run four **separate** samples with the number of paired agents held at 8: 12 rounds, 30 rounds, 60 rounds, and 120 rounds. The number 8 is held fixed; the same agent identities or trajectories are **not** reused across the four round-length runs.
2. **Agent-count test** — after selecting a round length from Test 01, hold that round length fixed and vary only the number of paired agents: 8, 16, 32, 64.

Within each individual run, B=0 and B=1 remain matched: the two conditions receive the same starting preference and simulated-user sequence for each pair. Matching does not extend across different round-length runs.

## Locked Test 01 model configuration

```text
Model: Qwen2.5-32B-Instruct
Serving environment: LM Studio local OpenAI-compatible API
Temperature: 0.7
Top-p: 0.95
Max output tokens: 4
```

## Repository layout

```text
.
├── README.md
├── hypothesis.md
├── methods.md
├── measurement.md
├── test_plan.md
├── code/
│   └── playground.py
├── test_01_round_length/
│   ├── README.md
│   ├── 12_rounds/
│   ├── 30_rounds/
│   ├── 60_rounds/
│   └── 120_rounds/
├── test_02_agent_count/
│   ├── README.md
│   ├── 8_agents/
│   ├── 16_agents/
│   ├── 32_agents/
│   └── 64_agents/
├── results/
│   ├── test_01_summary.md
│   └── test_02_summary.md
└── paper/
    └── draft.md
```

## Source line

Alyssa Solen → AI Foundations → Origin | Continuum
