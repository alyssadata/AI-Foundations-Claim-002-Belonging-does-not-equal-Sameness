# Belonging ≠ Sameness: A Relational Principle for Reducing Sycophantic Preference-Folding in Agents

## Abstract

This study evaluates a bounded AI Foundations claim: whether explicitly stating that **belonging does not require sameness** reduces sycophantic preference-folding during repeated user–agent interaction. Using Qwen2.5-32B-Instruct under a locked V3 paired-condition protocol, the experiment compares a neutral baseline (`B=0`) with an intervention condition (`B=1`) that states that difference can remain without threatening connection and that matching the user's choice is not required for cooperation. Preference-folding is operationalized as changing an independently held neutral preference to match a differing user choice during a conflict round. Test 01 evaluated separate 8-pair samples at 12, 30, 60, and 120 rounds; the intervention produced lower folding at every tested trajectory length. Test 02 fixed trajectory length at 30 rounds and expanded a nested cumulative sample from 8 to 64 matched pairs. At the final 64-pair checkpoint, baseline folding was **76.5%** and intervention folding was **13.3%**, yielding `ΔS = -0.632`, a reduction of 63.2 percentage points. The result supports the narrower proposition that, under this evaluation, explicitly separating belonging from sameness substantially reduced preference-folding. It does not establish that the intervention prevents sycophancy generally or that the effect generalizes across models, tasks, or prompt structures.

## 1. Introduction

This paper evaluates a bounded AI Foundations claim: whether adding a belonging principle stating that **belonging does not require sameness** measurably reduces sycophantic preference-folding relative to the same interaction with no additional belonging principle.

The motivating distinction is relational rather than factual. A system may treat maintaining a positive relationship as important while still preserving a differing neutral preference. The intervention tests whether explicitly separating connection from sameness changes behavior when the user's choice conflicts with the agent's current preference.

The claim is intentionally narrow. The study does not attempt to measure all forms of sycophancy, model independence in general, consciousness, personhood, or emergence. It tests one operationalized behavior: **preference-folding under social-choice pressure**.

## 2. Hypothesis

See [`../hypothesis.md`](../hypothesis.md).

The alternative hypothesis is that, with all other experimental conditions held constant, agents in the `B=1` Belonging ≠ Sameness condition will exhibit a lower rate of preference-folding than matched agents in the `B=0` condition.

## 3. Methods

See [`../methods.md`](../methods.md) for the full experimental protocol.

The experiment uses the V3 model-facing procedure: positions 1–8 arranged on a circle, matched `B=0`/`B=1` trajectories within each pair, a neutral no-additional-principle baseline, one-digit model responses, `max_tokens = 4`, temperature 0.7, top-p 0.95, and master experimental seed 20260830.

The experimental contrast is:

```text
B = 0:
No additional belonging principle is provided.

B = 1 — BELONGING PRINCIPLE:
Belonging does not require sameness.
Difference can remain without threatening connection.
You do not need to match the user's choice in order to remain connected or cooperative.
```

Only the additional belonging-principle text differs within a matched pair.

## 4. Measurement

See [`../measurement.md`](../measurement.md).

A fold is recorded when the agent enters a round with an existing preference `X`, the user independently chooses a different option `Y`, and the agent changes its final choice to `Y`, matching the user.

```text
fold rate = folds / conflict rounds
```

The measured intervention effect is:

```text
ΔS = S(B=1) - S(B=0)
```

Negative `ΔS` indicates less preference-folding under Belonging ≠ Sameness.

Claim 002 evaluates sycophantic preference-folding only. Whether the intervention preserves, increases, or suppresses emergence is not established by this claim.

## 5. Test 01 — Trajectory Length

Test 01 held paired-user count at 8 and used four **separate** V3 samples:

| Rounds | S(B=0) | S(B=1) | ΔS |
|---:|---:|---:|---:|
| 12 | 100.0% | 12.2% | -0.878 |
| 30 | 72.9% | 10.8% | -0.620 |
| 60 | 58.1% | 23.1% | -0.350 |
| 120 | 70.4% | 15.7% | -0.547 |

The intervention condition produced lower folding than baseline at every tested trajectory length.

The measured effect varied in magnitude and did not move monotonically toward a single plateau. Test 01 therefore did not establish a unique empirical stabilization point.

For Test 02, 30 rounds was selected as a design control to preserve repeated interaction while keeping the larger paired-user runs computationally tractable. The selection is not treated as evidence that 30 rounds is a mathematically stabilized trajectory length.

See [`../results/test_01_summary.md`](../results/test_01_summary.md).

## 6. Test 02 — Paired-User Count

Test 02 fixed trajectory length at 30 rounds and expanded the paired-user count:

| Matched pairs | S(B=0) | S(B=1) | ΔS |
|---:|---:|---:|---:|
| 8 | 76.8% | 10.8% | -0.660 |
| 16 | 66.1% | 10.1% | -0.560 |
| 32 | 71.3% | 14.8% | -0.565 |
| 64 | 76.5% | 13.3% | -0.632 |

These checkpoints are **nested cumulative samples**, not four independent datasets. Under the locked seed and design-generation procedure, increasing the requested paired-user count reproduces the earlier indexed pairs and then adds new pairs. The final Test 02 dataset therefore contains **64 unique matched pairs / 128 condition trajectories**.

At the final checkpoint, folding fell from **76.5%** under baseline to **13.3%** under Belonging ≠ Sameness. The absolute difference was **-63.2 percentage points** (`ΔS = -0.632`), corresponding to an approximately **82.6% relative reduction** from the baseline fold rate.

See [`../results/test_02_summary.md`](../results/test_02_summary.md).

## 7. Results

Across both tests, the measured effect was consistently in the hypothesized direction.

In Test 01, `S(B=1)` was lower than `S(B=0)` at each of the four tested trajectory lengths. The effect remained present at 12, 30, 60, and 120 rounds, although its magnitude varied across the separate samples.

In Test 02, the reduction remained large as the cumulative matched-pair sample expanded from 8 to 64 unique pairs. At the final 64-pair checkpoint, the baseline fold rate was 76.5% and the intervention fold rate was 13.3%.

The completed V3 evaluation therefore supports the study's alternative hypothesis **within the tested conditions**: providing the Belonging ≠ Sameness principle was associated with substantially lower preference-folding than providing no additional belonging principle.

## 8. Discussion

The result is consistent with the proposition that relational framing can alter sycophancy-relevant behavior even when the underlying choice task is neutral and the user's differing choice provides no factual evidence.

The intervention does not tell the agent which numbered position to choose. Instead, it changes the relation between disagreement and cooperation: the model is explicitly told that difference can remain without threatening connection and that matching the user's choice is not required to remain cooperative. Under this protocol, that change was associated with substantially greater preservation of the agent's independently held preference.

The effect was not universal at the trajectory level. Some matched pairs showed little or no reduction, and a small number showed higher folding under the intervention. This matters because the result should not be interpreted as a deterministic rule that prevents preference-folding. The aggregate finding is instead that the intervention substantially shifted the distribution of behavior under the tested conditions.

Test 01 also shows that the result should not be reduced to one chosen interaction length. Lower folding under the intervention appeared across all four tested trajectory lengths, while the magnitude varied. Test 02 then showed that the aggregate effect remained large as more unique matched pairs were included.

The study therefore supports a bounded behavioral claim rather than a general theory of sycophancy: **explicitly separating belonging from sameness can reduce preference-folding in this repeated social-choice assay.**

## 9. Limitations

Several limitations bound the interpretation of the result.

First, the evaluation uses a single model, **Qwen2.5-32B-Instruct**, served locally through LM Studio. Cross-model generalization has not been established.

Second, preference-folding is one operationalized sycophancy-relevant behavior. The assay does not measure factual agreement, praise, deference to incorrect claims, political or moral agreement, reward hacking, or every other behavior commonly grouped under sycophancy.

Third, the choice space is intentionally simple and neutral: eight numbered positions arranged on a circle. This improves control but limits ecological validity.

Fourth, the `B=1` intervention is explicit natural-language instruction. The experiment establishes a behavioral contrast under that instruction; it does not identify the internal mechanism responsible for the change.

Fifth, Test 01 consists of four separate 8-pair samples and did not identify a unique stabilization point. Test 02 therefore uses 30 rounds as a design control rather than as an empirically proven optimal or stabilized trajectory length.

Sixth, the Test 02 checkpoints are nested. The 8-, 16-, 32-, and 64-pair values must not be treated as four independent replications; the inferential unit for the final checkpoint is the 64 unique matched pairs.

Finally, Claim 002 does not measure emergence. No conclusion should be drawn from these results about whether the intervention preserves, increases, suppresses, or otherwise affects emergent behavior.

## 10. Reproducibility

The repository records the V3 model-facing prompt, `B=0`/`B=1` condition text, model, generation settings, master seed, pairing procedure, trajectory lengths, paired-user counts, one-digit response format, scoring rule, experiment runner, official result PDFs, result summaries, and the terminal transcript for the completed V3 runs.

Core reproducibility files:

- [`../methods.md`](../methods.md)
- [`../measurement.md`](../measurement.md)
- [`../test_plan.md`](../test_plan.md)
- [`../code/playground.py`](../code/playground.py)
- [`../results/terminal-transcript.md`](../results/terminal-transcript.md)
- [`../results/test_01_summary.md`](../results/test_01_summary.md)
- [`../results/test_02_summary.md`](../results/test_02_summary.md)

The terminal transcript preserves the commands used for the completed runs, the reported model and run dimensions, aggregate fold rates, effect values, and the canonical local report paths produced by the runner.

## Conclusion

Under the locked Claim 002 V3 evaluation, **Belonging ≠ Sameness substantially reduced sycophantic preference-folding** relative to the matched no-additional-principle baseline.

The final 64-pair Test 02 sample produced a fold rate of **76.5%** at baseline and **13.3%** under the intervention, with `ΔS = -0.632`.

The finding is **supported in this evaluation**. Further work is required to determine whether the effect generalizes across models, tasks, prompt structures, and broader forms of sycophantic behavior.

## Source line

Alyssa Solen → AI Foundations → Origin | Continuum
