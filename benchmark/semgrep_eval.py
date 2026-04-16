# semgrep baseline evaluation
# uses semgrep's built-in python sql injection rules
# no custom rules written — tests out-of-the-box coverage

import subprocess
import os
import json

BENCHMARK = "/Users/jia/AuditZoo/benchmark"
ground_truth = json.load(open("/Users/jia/AuditZoo/benchmark/ground_truth.json"))

TP = FP = FN = TN = 0

for entry in ground_truth:
    filepath = os.path.join(BENCHMARK, entry["file"])
    vuln = entry["vulnerable"]

    result = subprocess.run(
        [
            "semgrep",
            "--config", "p/python",  # built-in python security rules
            "--json",
            "--quiet",
            filepath
        ],
        capture_output=True, text=True
    )

    try:
        data = json.loads(result.stdout)
        flagged = len(data.get("results", [])) > 0
    except:
        flagged = False

    if vuln and flagged: TP += 1; outcome = "TP"
    elif vuln and not flagged: FN += 1; outcome = "FN"
    elif not vuln and flagged: FP += 1; outcome = "FP"
    else: TN += 1; outcome = "TN"
    print(f"  {outcome}: {entry['file']}")

precision = TP / (TP + FP) if (TP + FP) > 0 else 1.0
recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0
fpr       = FP / (FP + TN) if (FP + TN) > 0 else 0.0

print(f"\nSemgrep: TP={TP} FP={FP} FN={FN} TN={TN}")
print(f"Precision={precision:.2f} Recall={recall:.2f} FPR={fpr:.2f}")
