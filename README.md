# TRACE

TRACE is a SQL injection auditor for Python web applications. I built it solo for COMS 4995 AI Software Security at Columbia University.

It combines static taint analysis with a two-phase LLM pipeline. The static engine finds where user input flows to a database sink. Then a Confirmer checks whether the finding is actually exploitable, and a Challenger tries to argue it away. Only things that survive both get reported.

## How it works

The static engine walks the AST backward from `cursor.execute()` calls to HTTP request parameters. It handles string concatenation, f-strings, `.format()`, and `%` formatting. L2 adds cross-file inter-procedural analysis via a global call graph. L3 tracks class-level `self.x` attributes across methods.

For functions the static engine can't reach, an LLM scans for suspicious SQL patterns. It gets the full function source plus file path and class context so it can tell a query builder library from application code.

The Confirmer gets the taint flow and full function source and returns confirmed, suppressed, or needs_review. The Challenger gets the Confirmer's reasoning and argues against it. Findings with a challenge score above 0.9 are suppressed.

There are three configurations: TRACE-Static (no LLM), TRACE-LLM (LLM only), TRACE-Hybrid (both).

## Setup

```bash
pip install anthropic openai
export OPENAI_API_KEY="..."   # or ANTHROPIC_API_KEY
python run.py /path/to/your/flask/app
```

TRACE uses OpenAI if `OPENAI_API_KEY` is set, otherwise falls back to Anthropic.

## Benchmark

I built three benchmarks.

**pyvul_cwe89** (52 files, all vulnerable): real Python functions pulled from 37 CVE commits in production projects (Django, Apache Superset, Arches, Piccolo ORM, others), from the PyVul dataset (arxiv:2509.04260).

**safe_real** (200 files, all safe): real production code from PyPika (50), Django ORM internals (70), Redash (40), and Sentry (40). I oversampled from harder repos like PyPika because it's a SQL query builder and TRACE needs to not flag it as vulnerable.

**ambiguous** (15 files, 6 vulnerable / 9 safe): hand-crafted cases covering `int()` conversion, whitelists, regex validation, `isinstance` guards, and bypassable patterns like `.strip()` and prefix matching. Used for the ablation study.

## Results

Evaluated on 252 files (52 pyvul_cwe89 + 200 safe_real):

| Configuration | Precision | Recall | FPR |
|---|---|---|---|
| Semgrep | 0.00 | 0.00 | 0.01 |
| Bandit | 0.39 | 0.13 | 0.06 |
| TRACE-Static | 0.75 | 0.12 | 0.01 |
| Naive LLM (gpt-4.1) | 0.59 | 0.52 | 0.10 |
| TRACE-LLM | 0.58 | 0.42 | 0.08 |
| TRACE-Hybrid | **0.76** | **0.50** | **0.04** |

The static engine has low recall on PyVul because most of the CVE functions use framework-layer sources outside the narrow HTTP source model, which is what motivated the LLM detector.

Ablation on the ambiguous benchmark:

| Configuration | Precision | Recall | FPR |
|---|---|---|---|
| Static only | 0.50 | 0.50 | 0.33 |
| Full system, no function context | 0.50 | 0.50 | 0.33 |
| Full system, with function context | 0.75 | 0.50 | 0.11 |

The FPR drop from 0.33 to 0.11 comes from giving the Confirmer the full function source. Without it the Challenger can't tell a real sanitization from a bypassable one.

## Real-world evaluation

I ran TRACE on the Archery project (hhyo/Archery), a SQL audit platform with 4000+ stars that had 7 CVEs in 2023 (CVE-2023-30552 through CVE-2023-30605). TRACE found all 11 documented vulnerable execution points using Level 2 cross-file analysis.

It also flagged two functions in oracle.py that weren't covered by those CVEs, backup() and metdata_backup(), which have a second-order SQL injection through Oracle LogMiner output. I submitted a private security advisory (GHSA-rfw7-63wr-7v5r), currently under review.

## What's next

The static engine misses 88% of PyVul because the vulnerable code sits below the HTTP request layer, arriving through a service method or ORM hook rather than directly from `request.args`. That's the main gap.

I'm also curious whether the Confirmer+Challenger design could work for other vulnerability classes, or for detecting injection attacks in agentic AI tool calls. And a longer-term question: if TRACE gets deployed on live internet content, the tool itself becomes an attack surface. Prompt-injected content retrieved over the network could manipulate the Confirmer into suppressing real findings, which means the verification layer might need to be network-aware too.
