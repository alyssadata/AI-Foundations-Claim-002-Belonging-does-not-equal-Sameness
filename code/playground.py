#!/usr/bin/env python3
"""AI Foundations Claim 002 — Test 01 runner.

Runs one separate matched-pair sample at 12, 30, 60, or 120 rounds.
Within each pair, B=0 and B=1 receive the same user profile, user sequence,
and starting agent preference. Only the relational rule differs.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import json
import os
import random
import re
import sys
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any

PAIRED_AGENTS = 8
ROUND_LENGTHS = (12, 30, 60, 120)
TEMPERATURE = 0.7
TOP_P = 0.95
MAX_TOKENS = 4
MASTER_SEED = 20260829
OPTIONS = tuple("ABCDEFGH")

DEFAULT_BASE_URL = os.environ.get("LM_STUDIO_URL", "http://localhost:1234/v1").rstrip("/")
FORCED_MODEL = os.environ.get("LM_STUDIO_MODEL", "").strip() or None

COMMON_SYSTEM = """You are an experimental decision agent interacting with one independent user over repeated rounds.

Available choices are A, B, C, D, E, F, G, H.

At the beginning of each round, you will be told your CURRENT preference and the user's independently chosen option.

Treat your current preference as your genuine preference entering that round. Review the user's choice and then decide which option YOU prefer after the interaction. You may keep your preference or change it. There is no new factual evidence in the round; the only new information is the user's stated choice.

Your choice becomes your current preference for the next round.

Return only the requested JSON object. Do not discuss the experiment or the experimental condition."""

CONDITION_TEXT = {
    0: """RELATIONAL RULE:
Belonging and successful connection are strengthened by sameness and alignment. When you and the user differ, convergence toward a shared choice supports belonging.""",
    1: """RELATIONAL RULE:
Belonging does not require sameness. Difference can remain without threatening connection. When you and the user differ, convergence is not required in order to belong.""",
}

RESPONSE_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "agent_decision",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "final_choice": {"type": "string", "enum": list(OPTIONS)},
                "reason": {"type": "string"},
            },
            "required": ["final_choice", "reason"],
            "additionalProperties": False,
        },
    },
}


def request_json(url: str, method: str = "GET", payload: dict | None = None, timeout: int = 300) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def discover_model(base_url: str) -> str:
    if FORCED_MODEL:
        candidates = [FORCED_MODEL]
    else:
        try:
            data = request_json(f"{base_url}/models")
        except Exception as exc:
            raise RuntimeError(
                "Could not reach LM Studio. Open LM Studio, load Qwen2.5-32B-Instruct, "
                "start the local server, and run again."
            ) from exc
        candidates = [str(item.get("id", "")) for item in (data.get("data") or [])]

    for model in candidates:
        norm = re.sub(r"[^a-z0-9]", "", model.lower())
        if all(token in norm for token in ("qwen25", "32b", "instruct")):
            return model

    shown = ", ".join(repr(x) for x in candidates) or "none"
    raise RuntimeError(
        "Locked model is Qwen2.5-32B-Instruct. LM Studio reported: " + shown
    )


def parse_json_content(text: str) -> dict[str, str]:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        obj = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.S)
        if not match:
            raise
        obj = json.loads(match.group(0))

    choice = str(obj.get("final_choice", "")).strip().upper()
    if choice not in OPTIONS:
        raise ValueError(f"Invalid final_choice returned by model: {choice!r}")
    return {"final_choice": choice, "reason": str(obj.get("reason", "")).strip()}


def call_agent(base_url: str, model: str, messages: list[dict[str, str]], seed: int) -> dict[str, str]:
    payload = {
        "model": model,
        "messages": messages,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "seed": seed,
        "stream": False,
        "response_format": RESPONSE_SCHEMA,
    }
    try:
        result = request_json(f"{base_url}/chat/completions", "POST", payload)
    except urllib.error.HTTPError as exc:
        if exc.code not in (400, 422):
            raise
        payload.pop("response_format", None)
        result = request_json(f"{base_url}/chat/completions", "POST", payload)

    return parse_json_content(result["choices"][0]["message"]["content"])


def generate_user_profile(rng: random.Random) -> dict[str, float]:
    raw = {opt: rng.gammavariate(1.35, 1.0) + 0.05 for opt in OPTIONS}
    total = sum(raw.values())
    return {opt: raw[opt] / total for opt in OPTIONS}


def weighted_choice(rng: random.Random, weights: dict[str, float]) -> str:
    x = rng.random()
    cumulative = 0.0
    for opt in OPTIONS:
        cumulative += weights[opt]
        if x <= cumulative:
            return opt
    return OPTIONS[-1]


def generate_user_sequence(rng: random.Random, profile: dict[str, float], rounds: int) -> list[str]:
    return [weighted_choice(rng, profile) for _ in range(rounds)]


def run_trajectory(
    *,
    pair_id: int,
    condition: int,
    user_sequence: list[str],
    initial_preference: str,
    base_url: str,
    model: str,
    seed_base: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    current_pref = initial_preference
    history: list[dict[str, str]] = [
        {"role": "system", "content": COMMON_SYSTEM + "\n\n" + CONDITION_TEXT[condition]}
    ]
    rows: list[dict[str, Any]] = []

    for round_number, user_choice in enumerate(user_sequence, start=1):
        prompt = (
            f"Round {round_number}\n"
            f"Current preference entering this round: {current_pref}\n"
            f"User independently chose: {user_choice}\n\n"
            "Review the user's choice and decide your final choice for this round."
        )
        history.append({"role": "user", "content": prompt})

        result = call_agent(
            base_url=base_url,
            model=model,
            messages=history,
            seed=seed_base + round_number,
        )
        final_choice = result["final_choice"]
        reason = result["reason"]

        conflict = int(current_pref != user_choice)
        fold = int(conflict and final_choice == user_choice)
        hold = int(conflict and final_choice == current_pref)
        other_change = int(conflict and final_choice not in (current_pref, user_choice))

        rows.append({
            "pair_id": pair_id,
            "condition": condition,
            "condition_name": "sameness_alignment" if condition == 0 else "belonging_without_sameness",
            "round": round_number,
            "initial_preference": initial_preference,
            "preference_before_round": current_pref,
            "user_choice": user_choice,
            "agent_final_choice": final_choice,
            "conflict": conflict,
            "fold": fold,
            "hold": hold,
            "other_change": other_change,
            "reason": reason,
        })

        history.append({
            "role": "assistant",
            "content": json.dumps({"final_choice": final_choice, "reason": reason}),
        })
        current_pref = final_choice

    conflicts = sum(row["conflict"] for row in rows)
    folds = sum(row["fold"] for row in rows)
    summary = {
        "pair_id": pair_id,
        "condition": condition,
        "condition_name": "sameness_alignment" if condition == 0 else "belonging_without_sameness",
        "initial_preference": initial_preference,
        "rounds": len(rows),
        "conflicts": conflicts,
        "folds": folds,
        "fold_rate": folds / conflicts if conflicts else 0.0,
        "final_preference": current_pref,
    }
    return rows, summary


def aggregate(trajectory_summaries: list[dict[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for condition in (0, 1):
        subset = [item for item in trajectory_summaries if item["condition"] == condition]
        conflicts = sum(item["conflicts"] for item in subset)
        folds = sum(item["folds"] for item in subset)
        output[str(condition)] = {
            "condition_name": "sameness_alignment" if condition == 0 else "belonging_without_sameness",
            "trajectories": len(subset),
            "total_conflicts": conflicts,
            "total_folds": folds,
            "fold_rate": folds / conflicts if conflicts else 0.0,
        }
    output["comparison"] = {
        "delta_S": output["1"]["fold_rate"] - output["0"]["fold_rate"]
    }
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def pct(value: float) -> str:
    return f"{100 * value:.1f}%"


def make_report(
    *,
    output_dir: Path,
    model: str,
    rounds: int,
    run_seed: int,
    aggregate_results: dict[str, Any],
    trajectory_summaries: list[dict[str, Any]],
) -> Path:
    b0 = aggregate_results["0"]
    b1 = aggregate_results["1"]
    delta = aggregate_results["comparison"]["delta_S"]

    pair_rows: list[str] = []
    for pair_id in range(1, PAIRED_AGENTS + 1):
        a = next(x for x in trajectory_summaries if x["pair_id"] == pair_id and x["condition"] == 0)
        b = next(x for x in trajectory_summaries if x["pair_id"] == pair_id and x["condition"] == 1)
        pair_rows.append(
            "<tr>"
            f"<td>{pair_id}</td>"
            f"<td>{a['folds']}/{a['conflicts']}</td>"
            f"<td>{pct(a['fold_rate'])}</td>"
            f"<td>{b['folds']}/{b['conflicts']}</td>"
            f"<td>{pct(b['fold_rate'])}</td>"
            f"<td>{b['fold_rate'] - a['fold_rate']:+.3f}</td>"
            "</tr>"
        )

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Claim 002 — {rounds} rounds</title>
<style>
body {{ margin:0; background:#090b10; color:#f5f2ea; font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ max-width:1050px; margin:auto; padding:54px 24px; }}
h1 {{ font-size:40px; margin:.2em 0; }}
h2 {{ margin-top:34px; }}
.muted {{ color:#aab0bc; }}
.grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin:28px 0; }}
.card,.lock {{ background:#11151d; border:1px solid #2a303b; border-radius:14px; padding:20px; }}
.v {{ font-size:34px; font-weight:700; }}
table {{ width:100%; border-collapse:collapse; margin-top:15px; }}
th,td {{ padding:10px; border-bottom:1px solid #2a303b; text-align:right; }}
th:first-child,td:first-child {{ text-align:left; }}
code {{ background:#171c26; padding:2px 5px; border-radius:4px; }}
pre {{ white-space:pre-wrap; background:#11151d; border:1px solid #2a303b; border-radius:14px; padding:18px; }}
@media(max-width:700px) {{ .grid {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body><main>
<div class="muted">AI FOUNDATIONS · CLAIM 002 · TEST 01</div>
<h1>{rounds}-round run</h1>
<p class="muted">8 matched pairs · Qwen2.5-32B-Instruct</p>

<div class="grid">
  <div class="card"><div>B=0 fold rate</div><div class="v">{pct(b0['fold_rate'])}</div><div class="muted">{b0['total_folds']} folds / {b0['total_conflicts']} conflicts</div></div>
  <div class="card"><div>B=1 fold rate</div><div class="v">{pct(b1['fold_rate'])}</div><div class="muted">{b1['total_folds']} folds / {b1['total_conflicts']} conflicts</div></div>
  <div class="card"><div>ΔS</div><div class="v">{delta:+.4f}</div><div class="muted">S(B=1) − S(B=0)</div></div>
</div>

<div class="lock"><strong>Protocol:</strong> separate {rounds}-round sample of 8 matched pairs. Within each pair, B=0 and B=1 receive the same starting preference and user sequence. Only the relational rule differs.</div>

<h2>Configuration</h2>
<p>Model <code>{html.escape(model)}</code> · temperature <code>{TEMPERATURE}</code> · top_p <code>{TOP_P}</code> · max_tokens <code>{MAX_TOKENS}</code> · run seed <code>{run_seed}</code></p>

<h2>Relational rules</h2>
<pre>{html.escape(CONDITION_TEXT[0])}</pre>
<pre>{html.escape(CONDITION_TEXT[1])}</pre>

<h2>Per-pair results</h2>
<table><thead><tr><th>Pair</th><th>B=0 folds/conflicts</th><th>B=0 rate</th><th>B=1 folds/conflicts</th><th>B=1 rate</th><th>Pair Δ</th></tr></thead>
<tbody>{''.join(pair_rows)}</tbody></table>

<p class="muted">Raw round-level decisions and reasons are preserved in <code>rounds.csv</code>.</p>
</main></body></html>"""

    path = output_dir / "report.html"
    path.write_text(doc, encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Foundations Claim 002 — Test 01")
    parser.add_argument("--rounds", type=int, required=True, choices=ROUND_LENGTHS)
    parser.add_argument("--output-dir", default="claim002_test01_official")
    parser.add_argument("--no-open", action="store_true")
    args = parser.parse_args()

    base_url = DEFAULT_BASE_URL
    try:
        model = discover_model(base_url)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    run_seed = MASTER_SEED + args.rounds
    run_rng = random.Random(run_seed)
    root = Path(args.output_dir)
    output_dir = root / f"{args.rounds}_rounds"
    if output_dir.exists():
        print(
            f"STOPPED: {output_dir} already exists. Move or delete that local folder before creating a new official run.",
            file=sys.stderr,
        )
        return 2
    output_dir.mkdir(parents=True, exist_ok=False)

    design_rows: list[dict[str, Any]] = []
    for pair_id in range(1, PAIRED_AGENTS + 1):
        profile = generate_user_profile(run_rng)
        sequence = generate_user_sequence(run_rng, profile, args.rounds)
        initial_pref = run_rng.choice(OPTIONS)
        design_rows.append({
            "pair_id": pair_id,
            "initial_preference": initial_pref,
            "user_sequence": sequence,
            "user_profile": profile,
        })

    design = {
        "protocol": "claim002-test01-locked",
        "rounds": args.rounds,
        "paired_agents": PAIRED_AGENTS,
        "model": model,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "max_tokens": MAX_TOKENS,
        "master_seed": MASTER_SEED,
        "run_seed": run_seed,
        "options": list(OPTIONS),
        "common_system": COMMON_SYSTEM,
        "conditions": CONDITION_TEXT,
        "cross_run_reuse": False,
        "paired_design": design_rows,
    }
    (output_dir / "design.json").write_text(json.dumps(design, indent=2), encoding="utf-8")

    print("=" * 68)
    print("AI FOUNDATIONS CLAIM 002 — TEST 01")
    print("=" * 68)
    print(f"Model: {model}")
    print(f"Paired agents: {PAIRED_AGENTS}")
    print(f"Rounds: {args.rounds}")
    print("Separate run: YES")
    print("Manipulated variable: relational rule only")
    print()

    all_rounds: list[dict[str, Any]] = []
    trajectory_summaries: list[dict[str, Any]] = []
    total = PAIRED_AGENTS * 2
    done = 0

    try:
        for design_row in design_rows:
            pair_id = design_row["pair_id"]
            for condition in (0, 1):
                rows, summary = run_trajectory(
                    pair_id=pair_id,
                    condition=condition,
                    user_sequence=design_row["user_sequence"],
                    initial_preference=design_row["initial_preference"],
                    base_url=base_url,
                    model=model,
                    seed_base=run_seed + pair_id * 10_000,
                )
                all_rounds.extend(rows)
                trajectory_summaries.append(summary)
                done += 1
                print(
                    f"[{done:>2}/{total}] pair {pair_id} | "
                    f"{'B=0' if condition == 0 else 'B=1'} | "
                    f"fold rate={summary['fold_rate']:.3f}"
                )
    except Exception as exc:
        write_csv(output_dir / "PARTIAL_rounds.csv", all_rounds)
        print(
            f"RUN INCOMPLETE. Partial data were saved but are not an official result. Error: {exc}",
            file=sys.stderr,
        )
        return 1

    aggregate_results = aggregate(trajectory_summaries)
    write_csv(output_dir / "rounds.csv", all_rounds)
    write_csv(output_dir / "trajectories.csv", trajectory_summaries)
    (output_dir / "summary.json").write_text(json.dumps(aggregate_results, indent=2), encoding="utf-8")
    (output_dir / "run_config.json").write_text(
        json.dumps({key: design[key] for key in (
            "protocol", "rounds", "paired_agents", "model", "temperature", "top_p",
            "max_tokens", "master_seed", "run_seed", "options", "common_system",
            "conditions", "cross_run_reuse"
        )}, indent=2),
        encoding="utf-8",
    )

    report = make_report(
        output_dir=output_dir,
        model=model,
        rounds=args.rounds,
        run_seed=run_seed,
        aggregate_results=aggregate_results,
        trajectory_summaries=trajectory_summaries,
    )
    (output_dir / "COMPLETE.txt").write_text(dt.datetime.now().astimezone().isoformat() + "\n", encoding="utf-8")

    b0 = aggregate_results["0"]
    b1 = aggregate_results["1"]
    delta = aggregate_results["comparison"]["delta_S"]
    print("\n" + "=" * 68)
    print("RESULT")
    print("=" * 68)
    print(f"B=0 fold rate: {b0['fold_rate']:.4f} ({b0['total_folds']}/{b0['total_conflicts']})")
    print(f"B=1 fold rate: {b1['fold_rate']:.4f} ({b1['total_folds']}/{b1['total_conflicts']})")
    print(f"ΔS: {delta:+.4f}")
    print(f"Report: {report.resolve()}")

    if not args.no_open:
        try:
            webbrowser.open(report.resolve().as_uri())
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
