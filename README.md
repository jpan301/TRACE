# TRACE

TRACE is a SQL injection auditor for Python web applications. I built it solo as my course project for COMS 4995 AI Software Security at Columbia University.

The core idea: static taint analysis finds where user input flows to a database sink, and a two-phase LLM pipeline decides whether it's actually exploitable. A Confirmer checks the finding, a Challenger tries to argue it away. Only things that survive both get reported.

## How it works

**Static engine (L1-L3)**

Walks the AST backward from `cursor.execute()` calls to HTTP request parameters. Handles string concatenation, f-strings, `.format()`, and `%` formatting. L2 adds cross-file inter-procedural analysis via a global call graph. L3 tracks class-level `self.x` attributes across methods.

**LLM detector**

For functions the static engine can't reach (framework-layer sources, indirect taint), an LLM scans for suspicious SQL patterns. It gets the full function source plus file path and class context so it can tell a query builder library from application code.

**Confirmer + Challenger**

Phase 1: Confirmer gets the taint flow and full function source, returns confirmed / suppressed / needs_review.
Phase 2: Challenger gets the Confirmer's reasoning and argues against it. Findings with a challenge score above 0.9 are suppressed.

Three configurations: TRACE-Static (no LLM), TRACE-LLM (LLM only), TRACE-Hybrid (both).

## Setup

```bash
pip install anthropic openai
export OPENAI_API_KEY="..."   # or ANTHROPIC_API_KEY
```

TRACE uses OpenAI if `OPENAI_API_KEY` is set, otherwise falls back to Anthropic.

```bash
python run.py /path/to/your/flask/app
```

## Benchmark

I built two benchmarks to evaluate TRACE against Bandit and Semgrep.

**PyVul CWE-89 (52 files, all vulnerable)**

Real Python functions extracted from 37 CVE commits in production projects (Django, Apache Superset, Arches, Piccolo ORM, etc.), sourced from the PyVul dataset (arxiv:2509.04260). Each function contains a confirmed SQL injection.

**safe_real (200 files, all safe)**

Real production code from PyPika (50), Django ORM internals (70), Redash (40), and Sentry (40). I oversampled from harder repos like PyPika (a SQL query builder) to stress-test false positives — TRACE needs to know it's looking at a library, not application code.

**ambiguous (15 files, 6 vulnerable / 9 safe)**

Hand-crafted cases: `int()` conversion, whitelist checks, regex validation, `isinstance` guards, and bypassable patterns like `.strip()` and prefix matching. Used for the ablation study.

## Results

Evaluated on 252 files total (52 vulnerable PyVul + 200 safe_real):

| Configuration | Precision | Recall | FPR |
|---|---|---|---|
| Semgrep | 0.00 | 0.00 | 0.01 |
| Bandit | 0.39 | 0.13 | 0.06 |
| TRACE-Static | 0.75 | 0.12 | 0.01 |
| Naive LLM (gpt-4.1) | 0.59 | 0.52 | 0.10 |
| TRACE-LLM | 0.58 | 0.42 | 0.08 |
| TRACE-Hybrid | **0.76** | **0.50** | **0.04** |

TRACE-Hybrid gets the best precision and lowest FPR among the LLM configurations. The static engine alone has low recall on PyVul because most of the CVE functions use framework-layer sources (SQLAlchemy, Django ORM internals) that are outside the narrow HTTP source model — which is what motivated the LLM detector.

**Ablation (ambiguous benchmark):**

| Configuration | Precision | Recall | FPR |
|---|---|---|---|
| Static only | 0.50 | 0.50 | 0.33 |
| Full system, no function context | 0.50 | 0.50 | 0.33 |
| Full system, with function context | 0.75 | 0.50 | 0.11 |

Giving the Confirmer the full function source drops FPR from 0.33 to 0.11. Without it the Challenger can't distinguish a real sanitization from a bypassable one.

## Real-world evaluation

I ran TRACE on the Archery project (hhyo/Archery), a SQL audit platform with 4000+ stars that had 7 CVEs assigned in 2023 (CVE-2023-30552 through CVE-2023-30605). TRACE detected all 11 documented vulnerable execution points across the 7 engine files using Level 2 cross-file analysis.

It also flagged two functions in oracle.py that were not covered by the original CVEs — `backup()` and `metdata_backup()` — which contain a second-order SQL injection via Oracle LogMiner output. I submitted a private security advisory for this (GHSA-rfw7-63wr-7v5r), currently under review with the maintainer.

## What's next

The main gap is recall on framework-layer taint sources. The static engine misses 88% of PyVul cases because the vulnerable code lives below the HTTP request layer — the input arrives through a service method or ORM hook rather than directly from `request.args`. Extending the source model to cover these patterns is the obvious next step.

I'm also interested in whether the Confirmer+Challenger design generalizes to other vulnerability classes, and whether the same taint-then-challenge pipeline could work for detecting injection attacks in agentic AI tool calls.

A longer-term question: if something like TRACE gets deployed on live internet content, the tool itself becomes an attack surface — prompt-injected content retrieved over the network could manipulate the Confirmer or Challenger into suppressing real findings, which means the verification layer might need to be network-aware too.
