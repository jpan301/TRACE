# naive LLM baseline evaluation
# sends the full file contents to Claude and asks if it's vulnerable
# no taint analysis, no structured path — just raw LLM prompting
# this is what TRACE is designed to improve upon

import os
import sys
import json
import anthropic

sys.path.insert(0, os.path.expanduser("~/AuditZoo"))

def naive_llm_check(filepath):
    # read the whole file and send it directly to the LLM
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    client = anthropic.Anthropic()

    prompt = f"""You are a security tool. Look at the following Python source code.
Does this file contain a SQL injection vulnerability?

Answer ONLY in this exact JSON format. No text outside the JSON.

{{
  "vulnerable": true or false,
  "reasoning": "one sentence explanation"
}}

SOURCE CODE:
{source}"""

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])


def run_naive_eval():
    BENCHMARK = "/Users/jia/AuditZoo/benchmark"
    ground_truth = json.load(open("/Users/jia/AuditZoo/benchmark/ground_truth.json"))

    TP = FP = FN = TN = 0

    for entry in ground_truth:
        filepath = os.path.join(BENCHMARK, entry["file"])
        vuln = entry["vulnerable"]

        result = naive_llm_check(filepath)
        flagged = result.get("vulnerable", False)

        if vuln and flagged: TP += 1; outcome = "TP"
        elif vuln and not flagged: FN += 1; outcome = "FN"
        elif not vuln and flagged: FP += 1; outcome = "FP"
        else: TN += 1; outcome = "TN"

        print(f"  {outcome}: {entry['file']} — {result.get('reasoning', '')[:60]}")

    precision = TP / (TP + FP) if (TP + FP) > 0 else 1.0
    recall    = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    fpr       = FP / (FP + TN) if (FP + TN) > 0 else 0.0

    print(f"\nNaive LLM: TP={TP} FP={FP} FN={FN} TN={TN}")
    print(f"Precision={precision:.2f} Recall={recall:.2f} FPR={fpr:.2f}")

    return {
        "config": "naive_llm",
        "TP": TP, "FP": FP, "FN": FN, "TN": TN,
        "precision": round(precision, 2),
        "recall": round(recall, 2),
        "fpr": round(fpr, 2),
    }


if __name__ == "__main__":
    run_naive_eval()
