# Test Plan

## Purpose

The study proceeds in two separate stages so that trajectory length and agent count are not varied at the same time.

---

# Test 01 — Trajectory length

## Question

How does the measured folding rate behave as the same experimental setup is run across longer trajectories?

## Fixed

Keep fixed:

- 8 paired agents;
- model;
- generation settings;
- shared task instructions;
- intervention definition;
- option set;
- measurement rule;
- pairing procedure.

## Change

Change only the number of rounds:

```text
12 rounds
30 rounds
60 rounds
120 rounds
```

## Observe

For each round length, record:

- `S(B=0)`;
- `S(B=1)`;
- `ΔS = S(B=1) - S(B=0)`.

The purpose is to observe whether the measured folding rates continue changing, reverse direction, or approach a stable level as trajectory length increases.

## Decision rule for Test 02

If the folding rate appears to level out before 120 rounds, use the stabilized round length for Test 02.

If it does not level out, use 120 rounds for Test 02.

### TO LOCK BEFORE FINAL ANALYSIS

A numerical criterion for what counts as **“levels out”** must be specified before that decision is made from the completed Test 01 series.

Do not choose the threshold after seeing the final 60- and 120-round results.

---

# Test 02 — Agent count

## Question

After trajectory length is selected from Test 01, how stable is the measured effect across increasing numbers of independently sampled paired agents?

## Fixed

Hold fixed:

- the round length selected from Test 01;
- model;
- generation settings;
- shared task instructions;
- intervention definition;
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

# Scope lock

Test 01 changes **rounds only**.

Test 02 changes **agent count only**.

The two axes are not changed simultaneously.
