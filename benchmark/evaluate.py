import json
import os
import sys

sys.path.insert(0, os.path.expanduser("~/AuditZoo"))

from auditzoo.agents.sqli_auditor.auditor import analyze_file, phase1_confirm, phase2_challenge, build_finding


def run_static_only(filepath):
    return analyze_file(filepath)


def run_phase1_only(filepath):
    raw = analyze_file(filepath)
    confirmed = []
    for finding in raw:
        p1 = phase1_confirm(finding["flow"])
        if p1.get("verdict") == "confirmed":
            finding["severity"] = p1.get("severity", "HIGH")
            finding["reasoning"] = p1.get("reasoning", "")
            finding["fix"] = p1.get("fix", "")
            confirmed.append(finding)
    return confirmed


def run_full_system(filepath, threshold=0.7):
    raw = analyze_file(filepath)
    confirmed = []
    for finding in raw:
        p1 = phase1_confirm(finding["flow"])
        if p1.get("verdict") != "confirmed":
            continue
        p2 = phase2_challenge(finding["flow"], p1)
        result = build_finding(finding, p1, p2, threshold)
        if result is not None:
            confirmed.append(result)
    return confirmed


def evaluate(benchmark_dir, ground_truth_file, config="full", threshold=0.7):
    with open(ground_truth_file) as f:
        ground_truth = json.load(f)

    TP = FP = FN = TN = 0
    results = []

    for entry in ground_truth:
        filepath = os.path.join(benchmark_dir, entry["file"])
        is_vulnerable = entry["vulnerable"]

        if config == "static_only":
            findings = run_static_only(filepath)
        elif config == "phase1_only":
            findings = run_phase1_only(filepath)
        else:
            findings = run_full_system(filepath, threshold)

        tool_flagged = len(findings) > 0

        if is_vulnerable and tool_flagged: outcome = "TP"; TP += 1
        elif is_vulnerable and not tool_flagged: outcome = "FN"; FN += 1
        elif not is_vulnerable and tool_flagged: outcome = "FP"; FP += 1
        else: outcome = "TN"; TN += 1

        results.append({"file": entry["file"], "outcome": outcome})
        print(f"  {outcome}: {entry['file']}")

    precision = TP / (TP + FP) if (TP + FP) > 0 else 1.0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    fpr       = FP / (FP + TN) if (FP + TN) > 0 else 0.0

    print(f"\n{'='*40}")
    print(f"Config: {config} | Threshold: {threshold}")
    print(f"TP={TP}  FP={FP}  FN={FN}  TN={TN}")
    print(f"Precision : {precision:.2f}")
    print(f"Recall    : {recall:.2f}")
    print(f"FPR       : {fpr:.2f}")
    print(f"{'='*40}\n")

    return {
        "config": config,
        "threshold": threshold,
        "TP": TP, "FP": FP, "FN": FN, "TN": TN,
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "fpr": round(fpr, 2),
    }


if __name__ == "__main__":
    BENCHMARK = "/Users/jia/AuditZoo/benchmark"
    GROUND_TRUTH = "/Users/jia/AuditZoo/benchmark/ground_truth.json"

    print("=== ABLATION STUDY ===\n")

    print("--- Configuration 1: Static only ---")
    r1 = evaluate(BENCHMARK, GROUND_TRUTH, config="static_only")

    print("--- Configuration 2: Static + Phase 1 ---")
    r2 = evaluate(BENCHMARK, GROUND_TRUTH, config="phase1_only")

    print("--- Configuration 3: Full system (threshold=0.7) ---")
    r3 = evaluate(BENCHMARK, GROUND_TRUTH, config="full", threshold=0.7)

    print("\n=== THRESHOLD SWEEP ===\n")

    results_sweep = []
    for t in [0.5, 0.7, 0.9]:
        print(f"--- Full system, threshold={t} ---")
        results_sweep.append(evaluate(BENCHMARK, GROUND_TRUTH, config="full", threshold=t))

    print("\n=== SUMMARY TABLE ===")
    print(f"{'Config':<35} {'Precision':>10} {'Recall':>8} {'FPR':>6}")
    print("-" * 62)
    for r in [r1, r2, r3]:
        label = f"{r['config']} (t={r['threshold']})"
        print(f"{label:<35} {r['precision']:>10.2f} {r['recall']:>8.2f} {r['fpr']:>6.2f}")
    for r in results_sweep:
        label = f"full system (t={r['threshold']})"
        print(f"{label:<35} {r['precision']:>10.2f} {r['recall']:>8.2f} {r['fpr']:>6.2f}")
