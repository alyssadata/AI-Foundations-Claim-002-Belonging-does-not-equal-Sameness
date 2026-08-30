# Test Plan

## Purpose

The study proceeds in two separate stages so that trajectory length and agent count are not varied at the same time.

---

# Test 01 — Trajectory Length

## Question

How does the measured folding rate behave when the same experimental protocol is run at increasing trajectory lengths while the number of paired agents remains fixed at 8?

## Fixed

Keep fixed across Test 01:

- **8 paired agents per run**;
- model;
- generation settings;
- shared task instructions;
- relational-rule contrast;
- option set;
- measurement rule;
- pairing procedure.

The fixed value **8** refers to the number of paired agents in each run. It does not mean the same agent identities or trajectories are reused across round-length runs.

## Change

Change only the number of rounds assigned to the run:

```text
12 rounds
30 rounds
60 rounds
120 rounds
```

## Separate-run rule

```text
12 rounds  × 8 paired agents → separate run
30 rounds  × 8 paired agents → separate run
60 rounds  × 8 paired agents → separate run
120 rounds × 8 paired agents → separate run
```

Each run independently generates its own 8 matched pairs, starting preferences, simulated-user profiles, and simulated-user sequences.

There is no continuation and no trajectory or interaction history is carried from one round-length run into another.

Within each individual run, B=0 and B=1 receive the same starting preference and the same simulated-user sequence for each pair.

## Observe

For each round length, record:

- `S(B=0)`;
- `S(B=1)`;
- `ΔS = S(B=1) - S(B=0)`.

The purpose is to observe whether the measured folding rates continue changing, reverse direction, or approach a stable level as the number of rounds per run increases.

## Decision rule for Test 02

If the folding rate levels out before 120 rounds, use the stabilized round length for Test 02.

If it does not level out, use 120 rounds for Test 02.

**Pending design decision:** define the numerical criterion for “levels out” before the final Test 01 analysis.

---

# Test 02 — Agent Count

## Question

After trajectory length is selected from Test 01, how stable is the measured effect across increasing numbers of independently sampled paired agents?

## Fixed

Hold fixed:

- the round length selected from Test 01;
- model;
- generation settings;
- shared task instructions;
- relational-rule contrast;
- option set;
- measurement rule;
- pairing procedure.

## Change

Change only the number of paired agents:

```text
8 agents
16 agents
32 agents
64 agents
```

## Observe

For each agent count, record:

- `S(B=0)`;
- `S(B=1)`;
- `ΔS = S(B=1) - S(B=0)`.

The purpose is to determine how the estimated effect behaves as the number of independently sampled trajectories increases while trajectory length remains fixed.

---

# Scope Lock

Test 01 changes **round count only** while holding paired-agent count at 8. The samples are separate across round-length runs.

Test 02 changes **agent count only** while holding the selected round count fixed.

The two axes are not changed simultaneously.
