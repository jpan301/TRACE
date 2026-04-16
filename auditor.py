# TRACE: SQL Injection Auditor
# auditzoo/agents/sqli_auditor/auditor.py
# Jenny Pan - jp3956 - COMS 4995 AI Software Security

import ast
import os
import json
import anthropic
try:
    from openai import OpenAI as OpenAIClient
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# set TRACE_LLM_BACKEND to "openai" or "anthropic"
# defaults to anthropic if OPENAI_API_KEY is not set
TRACE_LLM_BACKEND = "openai" if (os.environ.get("OPENAI_API_KEY") and OPENAI_AVAILABLE) else "anthropic"
TRACE_LLM_MODEL = os.environ.get("TRACE_LLM_MODEL", "gpt-4.1" if TRACE_LLM_BACKEND == "openai" else "claude-opus-4-5")

try:
    from autogen_core import MessageContext
    from auditzoo import BaseAnalysisAgent, Request, Response
    AUDITZOO_AVAILABLE = True
except ImportError:
    AUDITZOO_AVAILABLE = False


# --- these are the places where user input enters the program ---
# Flask and Django both have different ways to access request data
# so I have to cover both

SOURCES = {
    "request.args.get",    # Flask URL params like ?id=1
    "request.form.get",    # Flask form submissions
    "request.values.get",  # Flask, covers both args and form
    "request.json",        # Flask JSON body
    "request.data",        # Flask raw request body
    "request.GET.get",     # Django URL params
    "request.POST.get",    # Django form submissions
}

# --- these are the database calls that actually execute SQL ---
# if user input reaches any of these without being parameterized, it's a vulnerability

SINKS = {
    "cursor.execute",
    "cur.execute",       # common short alias
    "c.execute",         # common short alias
    "db.execute",        # common short alias
    "conn.execute",
    "connection.execute",
    "session.execute",   # SQLAlchemy
    "execute",           # bare execute() calls
}


# --- helper to get the full dotted name from a function call node ---
# e.g. cursor.execute(query) gives us the string "cursor.execute"
# this is recursive because calls can be chained like a.b.c

def get_call_name(node):
    if isinstance(node, ast.Attribute):
        return get_call_name(node.value) + "." + node.attr
    elif isinstance(node, ast.Name):
        return node.id
    return ""


# --- check if an AST node is a recognized user input source ---

def is_source(node):
    if isinstance(node, ast.Call):
        name = get_call_name(node.func)
        # check if the call name matches any of our known sources
        return any(
            name.endswith(s.split(".")[-1]) and s.split(".")[-2] in name
            for s in SOURCES if "." in s
        )
    if isinstance(node, ast.Attribute):
        name = get_call_name(node)
        return name in SOURCES
    return False


# --- check if a cursor.execute() call is already safe (parameterized) ---
# a safe call looks like: cursor.execute("SELECT...", (user_id,))
# unsafe looks like: cursor.execute("SELECT..." + user_id)
# the key difference is whether the user value is a separate second argument

def is_parameterized(node):
    if isinstance(node, ast.Call) and len(node.args) >= 2:
        first_arg = node.args[0]
        # first argument has to be a plain string literal, not a variable
        if isinstance(first_arg, ast.Constant) and isinstance(first_arg.value, str):
            return True
    return False


# --- the main taint walk ---
# starts at the sink argument and works backwards through assignments
# trying to find if user input is the origin
# returns (True/False, list of code lines showing the path)

def taint_walk(arg_node, assignments, depth=0):
    # stop if we've gone too deep, something is probably wrong
    if depth > 10:
        return False, []

    # base case: we landed directly on a source like request.args.get("id")
    if is_source(arg_node):
        return True, [ast.unparse(arg_node)]

    # handle wrapped calls like text(f"...") in SQLAlchemy
    # need to look inside the wrapper to find the actual string
    if isinstance(arg_node, ast.Call):
        for inner_arg in arg_node.args:
            tainted, flow = taint_walk(inner_arg, assignments, depth + 1)
            if tainted:
                return True, flow

    # if we have a variable name, look up what it was assigned to
    if isinstance(arg_node, ast.Name):
        var_name = arg_node.id
        if var_name not in assignments:
            return False, []

        assigned_value = assignments[var_name]

        # the variable was assigned directly from user input
        if is_source(assigned_value):
            return True, [f"{var_name} = {ast.unparse(assigned_value)}"]

        # the variable was built by concatenation, f-string, or .format()
        if isinstance(assigned_value, (ast.BinOp, ast.JoinedStr, ast.Call)):
            tainted, sub_flow = check_expression(assigned_value, assignments, depth)
            if tainted:
                return True, sub_flow + [f"{var_name} = {ast.unparse(assigned_value)}"]

        # the variable was assigned from another variable, keep walking back
        if isinstance(assigned_value, ast.Name):
            tainted, sub_flow = taint_walk(assigned_value, assignments, depth + 1)
            if tainted:
                return True, sub_flow + [f"{var_name} = {ast.unparse(assigned_value)}"]

    # if the argument itself is a concatenation or f-string (not a variable)
    if isinstance(arg_node, (ast.BinOp, ast.JoinedStr)):
        return check_expression(arg_node, assignments, depth)

    return False, []


# --- check if a concatenation or f-string contains tainted data ---
# BinOp covers "SELECT " + user_id  (the + operator)
# BinOp also covers "WHERE id = '%s'" % user_id  (the % operator)
# JoinedStr covers f"SELECT * WHERE id = {user_id}"

def check_expression(node, assignments, depth=0):
    if isinstance(node, ast.BinOp):
        # check left side first, then right
        tainted, flow = taint_walk(node.left, assignments, depth + 1)
        if tainted:
            return True, flow
        tainted, flow = taint_walk(node.right, assignments, depth + 1)
        if tainted:
            return True, flow

    if isinstance(node, ast.JoinedStr):
        # f-strings have FormattedValue nodes for each {variable}
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                tainted, flow = taint_walk(value.value, assignments, depth + 1)
                if tainted:
                    return True, flow

    # "SELECT %s" % var  or  "SELECT {}".format(var)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "format":
            # "...{}...".format(var) -- check all format arguments
            for arg in node.args:
                tainted, flow = taint_walk(arg, assignments, depth + 1)
                if tainted:
                    return True, flow
            for kw in node.keywords:
                tainted, flow = taint_walk(kw.value, assignments, depth + 1)
                if tainted:
                    return True, flow

    return False, []


# --- collect all variable assignments in a function body ---
# returns a dict of variable_name -> the AST node it was assigned to
# if a variable is assigned twice, we keep the latest one

def collect_assignments(func_node):
    assignments = {}
    for node in ast.walk(func_node):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments[target.id] = node.value
        elif isinstance(node, ast.AnnAssign):  # type-annotated assignment like x: int = 5
            if isinstance(node.target, ast.Name) and node.value:
                assignments[node.target.id] = node.value
    return assignments


# --- build a call graph for the whole file ---
# maps function name -> its AST node and parameter names
# needed for inter-procedural analysis (following calls into other functions)

def build_call_graph(tree):
    call_graph = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            param_names = [arg.arg for arg in node.args.args]
            call_graph[node.name] = {
                "node": node,
                "params": param_names,
            }
    return call_graph


# --- extended taint walk that can follow calls into other functions ---
# the basic taint_walk only stays inside one function
# this version also jumps into helper functions defined in the same file
# visited_funcs tracks which functions we already entered to avoid infinite loops

def taint_walk_interprocedural(arg_node, assignments, call_graph,
                                visited_funcs=None, depth=0):
    if visited_funcs is None:
        visited_funcs = set()

    if depth > 15:
        return False, []

    # try the regular taint walk first
    tainted, flow = taint_walk(arg_node, assignments, depth)
    if tainted:
        return True, flow

    # if the argument is a call to a known local function, jump into it
    if isinstance(arg_node, ast.Call):
        func_name = ""
        if isinstance(arg_node.func, ast.Name):
            func_name = arg_node.func.id
        elif isinstance(arg_node.func, ast.Attribute):
            func_name = arg_node.func.attr

        if func_name and func_name in call_graph and func_name not in visited_funcs:
            visited_funcs.add(func_name)
            callee = call_graph[func_name]
            callee_node = callee["node"]
            callee_params = callee["params"]

            # get the assignments inside the called function
            callee_assignments = collect_assignments(callee_node)

            # map the arguments from the call site to the parameter names
            # e.g. build_query(user_id) means user_id maps to whatever
            # the first parameter of build_query is named
            for i, call_arg in enumerate(arg_node.args):
                if i < len(callee_params):
                    callee_assignments[callee_params[i]] = call_arg

            # look for sinks inside the called function
            for node in ast.walk(callee_node):
                if not isinstance(node, ast.Call):
                    continue
                call_name = get_call_name(node.func)
                if not any(call_name.endswith(s.split(".")[-1]) for s in SINKS):
                    continue
                if is_parameterized(node):
                    continue
                if not node.args:
                    continue

                tainted, sub_flow = taint_walk_interprocedural(
                    node.args[0], callee_assignments, call_graph,
                    visited_funcs.copy(), depth + 1
                )
                if tainted:
                    return True, sub_flow + [ast.unparse(arg_node)]

    # if the argument is a variable assigned from a function call, follow it
    if isinstance(arg_node, ast.Name):
        var_name = arg_node.id
        if var_name in assignments:
            assigned = assignments[var_name]
            if isinstance(assigned, ast.Call):
                tainted, sub_flow = taint_walk_interprocedural(
                    assigned, assignments, call_graph,
                    visited_funcs, depth + 1
                )
                if tainted:
                    return True, sub_flow + [f"{var_name} = {ast.unparse(assigned)}"]

    return False, []


# --- analyze a single function for SQL injection ---
# walks the function looking for sink calls (cursor.execute etc)
# for each sink, runs the taint walk to see if user input reaches it

def analyze_function(func_node, filename, call_graph=None):
    findings = []
    assignments = collect_assignments(func_node)

    for node in ast.walk(func_node):
        if not isinstance(node, ast.Call):
            continue

        call_name = get_call_name(node.func)

        # skip if this isn't a recognized sink
        if not any(call_name.endswith(s.split(".")[-1]) for s in SINKS):
            continue

        # skip if it's already using parameterized queries
        if is_parameterized(node):
            continue

        # skip if there are no arguments (shouldn't happen but just in case)
        if not node.args:
            continue

        query_arg = node.args[0]  # the first argument is the SQL query string

        # use inter-procedural walk if we have a call graph
        if call_graph:
            tainted, flow = taint_walk_interprocedural(
                query_arg, assignments, call_graph
            )
        else:
            tainted, flow = taint_walk(query_arg, assignments)

        if tainted:
            flow.append(ast.unparse(node))  # add the sink itself as the last step
            findings.append({
                "file": filename,
                "line": node.lineno,
                "sink": ast.unparse(node),
                "flow": flow,
                "function": func_node.name,
            })

    return findings


# --- parse a file and run analysis on every function in it ---

def analyze_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        source = f.read()

    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError as e:
        print(f"Skipping {filepath} - syntax error: {e}")
        return []

    call_graph = build_call_graph(tree)

    findings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            findings.extend(analyze_function(node, filepath, call_graph))

    return findings


# --- unified LLM call helper ---
# routes to OpenAI or Anthropic depending on which key is available
# so we can switch backends without changing the rest of the code

def llm_call(prompt, max_tokens=1024):
    if TRACE_LLM_BACKEND == "openai":
        client = OpenAIClient(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model=TRACE_LLM_MODEL,
            temperature=0,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    else:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model=TRACE_LLM_MODEL,
            max_tokens=max_tokens,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text.strip()


# --- Phase 1: Confirmer ---
# sends the taint path to the LLM and asks if it's actually exploitable
# the LLM only sees the taint path, not the full file
# temperature=0 so results are consistent every run

def phase1_confirm(flow, function_source=None):
    # format the flow chain as numbered lines for the prompt
    flow_text = "\n".join(f"  Line {i+1}: {line}" for i, line in enumerate(flow))

    # build optional function source section for the prompt
    source_section = ""
    if function_source:
        source_section = f"""\n\nFULL FUNCTION SOURCE (check for whitelist, validation, or sanitization):\n```python\n{function_source}\n```"""

    prompt = f"""You are a security analysis tool performing SQL injection detection.

You will be given a taint path extracted from Python source code by static analysis.
This path represents the assignment chain connecting a user-controlled input to a SQL execution call.

Your task: determine whether an attacker-controlled value can reach the SQL execution point
without passing through a parameterized placeholder.

RULES:
- A parameterized placeholder means cursor.execute(sql, (value,)) where the value is a separate argument.

TAINT PATH:
{flow_text}{source_section}

Respond ONLY in this exact JSON format. No text outside the JSON.

{{
  "verdict": "confirmed" or "suppressed" or "needs_review",
  "reasoning": "one or two sentences explaining why",
  "severity": "HIGH" or "MEDIUM" or "LOW",
  "fix": "the corrected version of the sink call"
}}

Use "needs_review" when the finding is ambiguous - for example when some inputs are
parameterized but others are not, or when the sanitization present may be incomplete."""

    raw = llm_call(prompt, max_tokens=1024)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # sometimes the model adds extra text around the JSON, strip it out
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])


# --- Phase 2: Challenger ---
# adversarial pass - the LLM is asked to argue AGAINST the finding
# if it can't find a strong argument, the finding is real
# this reduces false positives and prevents confirmation bias

def phase2_challenge(flow, confirmer_result):
    client = anthropic.Anthropic()

    flow_text = "\n".join(f"  Line {i+1}: {line}" for i, line in enumerate(flow))

    prompt = f"""You are an adversarial security reviewer.
A prior analysis has flagged the following code path as a SQL injection vulnerability.
Your task is NOT to confirm this finding.
Your task is to construct the strongest possible argument that this finding is a FALSE POSITIVE.

Look for any reason the finding might be wrong:
- Is there a type conversion (e.g. int(), float()) between source and sink that makes injection impossible?
- Is the variable reassigned to a safe value between source and sink?
- Is there any sanitization or validation that makes the value safe?
- Is this function only ever called with hardcoded arguments, never from an HTTP route?
- Does the path show incomplete evidence?

TAINT PATH:
{flow_text}

PRIOR ANALYSIS VERDICT:
  verdict: {confirmer_result.get('verdict')}
  reasoning: {confirmer_result.get('reasoning')}

Respond ONLY in this exact JSON format. No text outside the JSON.

{{
  "challenge_score": a number between 0.0 and 1.0,
  "rationale": "your strongest argument that this is a false positive"
}}

Scoring guide:
  0.0 - 0.3: No credible argument against the finding. It is real.
  0.3 - 0.7: Some uncertainty but finding is likely real.
  0.7 - 0.9: Meaningful reason to doubt. Report as MEDIUM confidence.
  0.9 - 1.0: Strong evidence this is a false positive. Suppress it."""

    raw = llm_call(prompt, max_tokens=1024)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])


# --- build the final output record for a confirmed finding ---
# returns None if the Challenger suppressed it (score too high)

def build_finding(raw, p1, p2, threshold=0.7):
    score = p2.get("challenge_score", 0.0)

    # challenger was too confident this is a false positive, skip it
    if score >= 0.9:
        return None

    # if challenger had meaningful doubt, downgrade to MEDIUM
    severity = p1.get("severity", "HIGH")
    if score >= threshold:
        severity = "MEDIUM"

    return {
        "file":                raw["file"],
        "line":                raw["line"],
        "function":            raw["function"],
        "source":              raw["flow"][0] if raw["flow"] else "",
        "sink":                raw["sink"],
        "flow":                raw["flow"],
        "severity":            severity,
        "reasoning":           p1.get("reasoning", ""),
        "fix":                 p1.get("fix", ""),
        "challenge_score":     score,
        "challenge_rationale": p2.get("rationale", ""),
    }


# --- helper to extract full function source for LLM context ---
# gives the LLM the complete function body so it can see
# any whitelist checks, validation, or sanitization around the sink

def get_function_source(filepath, func_name):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        tree = ast.parse(source)
        lines = source.splitlines()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == func_name:
                    start = node.lineno - 1
                    end = node.end_lineno
                    return "\n".join(lines[start:end])
    except Exception:
        pass
    return None


# --- main audit runner ---
# takes a file or directory path, runs the full pipeline on every .py file
# prints progress as it goes so you can see what's happening

def run_audit(repo_path, threshold=0.7):
    if os.path.isfile(repo_path):
        py_files = [repo_path]
    else:
        py_files = []
        for root, dirs, files in os.walk(repo_path):
            for fname in files:
                if fname.endswith(".py"):
                    py_files.append(os.path.join(root, fname))

    print(f"Scanning {len(py_files)} file(s)...")

    all_findings = []
    suppressed = 0

    for filepath in py_files:
        raw_findings = analyze_file(filepath)
        if not raw_findings:
            continue

        print(f"  {filepath}: {len(raw_findings)} candidate(s)")

        for raw in raw_findings:
            # Phase 1: confirm the finding is actually exploitable
            # pass the full function source so the LLM can see
            # any sanitization or validation around the sink
            func_source = get_function_source(filepath, raw["function"])
            p1 = phase1_confirm(raw["flow"], function_source=func_source)
            verdict = p1.get("verdict")
            if verdict == "suppressed":
                suppressed += 1
                print(f"    Suppressed by Confirmer: {raw['sink']}")
                continue
            if verdict == "needs_review":
                # report as MEDIUM confidence - needs human triage
                finding = {
                    "file":               raw["file"],
                    "line":               raw["line"],
                    "function":           raw["function"],
                    "source":             raw["flow"][0] if raw["flow"] else "",
                    "sink":               raw["sink"],
                    "flow":               raw["flow"],
                    "severity":           "MEDIUM",
                    "reasoning":          p1.get("reasoning", ""),
                    "fix":                p1.get("fix", ""),
                    "challenge_score":    None,
                    "challenge_rationale": "needs_review - not sent to Challenger",
                    "verdict":            "needs_review",
                }
                print(f"    Needs review [MEDIUM]: {raw['sink']}")
                all_findings.append(finding)
                continue

            # Phase 2: try to argue it's a false positive
            p2 = phase2_challenge(raw["flow"], p1)
            finding = build_finding(raw, p1, p2, threshold)

            if finding is None:
                suppressed += 1
                print(f"    Suppressed by Challenger (score {p2.get('challenge_score')}): {raw['sink']}")
            else:
                print(f"    Confirmed [{finding['severity']}]: {raw['sink']}")
                all_findings.append(finding)

    print(f"\nDone. {len(all_findings)} finding(s) reported, {suppressed} suppressed.")
    return all_findings


# --- AuditZoo agent wrapper ---
# this is what AuditZoo calls when you run the agent through the framework

class SQLiAuditorAgent(BaseAnalysisAgent):

    def __init__(self):
        super().__init__("TRACE SQL injection auditor")

    async def _handle_request(self, message: Request, ctx: MessageContext) -> Response:
        if message.type != "task.sqli_audit":
            return Response.fail("Unknown task type")

        repo_path = message.payload.get("repo_path")
        if not repo_path:
            return Response.fail("No repo_path provided")

        findings = run_audit(repo_path)
        return Response.ok(data={"findings": findings})

# --- Path 1: broad source model ---
# treats all function parameters as potentially tainted
# this is needed to detect framework-layer SQL injection
# where the source is not an HTTP request but an internal function argument
# tradeoff: will produce more false positives than the narrow HTTP source model
# the LLM layer then has a real job to do suppressing those false positives

BROAD_MODE = False  # set to True to enable broad source model


def is_broad_source(node, param_names):
    # in broad mode, any function parameter is a taint source
    if BROAD_MODE and isinstance(node, ast.Name) and node.id in param_names:
        return True
    return is_source(node)


def taint_walk_broad(arg_node, assignments, param_names, depth=0):
    if depth > 10:
        return False, []

    # check both narrow HTTP sources and broad parameter sources
    if is_source(arg_node):
        return True, [ast.unparse(arg_node)]

    if BROAD_MODE and isinstance(arg_node, ast.Name) and arg_node.id in param_names:
        return True, [f"{arg_node.id} (function parameter - untrusted in broad mode)"]

    if isinstance(arg_node, ast.Call):
        for inner_arg in arg_node.args:
            tainted, flow = taint_walk_broad(inner_arg, assignments, param_names, depth + 1)
            if tainted:
                return True, flow

    if isinstance(arg_node, ast.Name):
        var_name = arg_node.id
        if var_name not in assignments:
            return False, []
        assigned_value = assignments[var_name]

        if is_source(assigned_value):
            return True, [f"{var_name} = {ast.unparse(assigned_value)}"]

        if BROAD_MODE and isinstance(assigned_value, ast.Name) and assigned_value.id in param_names:
            return True, [f"{var_name} = {assigned_value.id} (function parameter)"]

        if isinstance(assigned_value, (ast.BinOp, ast.JoinedStr, ast.Call)):
            tainted, sub_flow = check_expression_broad(assigned_value, assignments, param_names, depth)
            if tainted:
                return True, sub_flow + [f"{var_name} = {ast.unparse(assigned_value)}"]

        if isinstance(assigned_value, ast.Name):
            tainted, sub_flow = taint_walk_broad(assigned_value, assignments, param_names, depth + 1)
            if tainted:
                return True, sub_flow + [f"{var_name} = {ast.unparse(assigned_value)}"]

    if isinstance(arg_node, (ast.BinOp, ast.JoinedStr)):
        return check_expression_broad(arg_node, assignments, param_names, depth)

    return False, []


def check_expression_broad(node, assignments, param_names, depth=0):
    if isinstance(node, ast.BinOp):
        tainted, flow = taint_walk_broad(node.left, assignments, param_names, depth + 1)
        if tainted:
            return True, flow
        tainted, flow = taint_walk_broad(node.right, assignments, param_names, depth + 1)
        if tainted:
            return True, flow
    if isinstance(node, ast.JoinedStr):
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                tainted, flow = taint_walk_broad(value.value, assignments, param_names, depth + 1)
                if tainted:
                    return True, flow
    # "...{x}...".format(x=val) or "...".format(**dict)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "format":
            for arg in node.args:
                tainted, flow = taint_walk_broad(arg, assignments, param_names, depth + 1)
                if tainted:
                    return True, flow
            for kw in node.keywords:
                # handles both named kwargs and **dict unpacking (arg=None)
                tainted, flow = taint_walk_broad(kw.value, assignments, param_names, depth + 1)
                if tainted:
                    return True, flow
    return False, []


def analyze_function_broad(func_node, filename, call_graph=None):
    # same as analyze_function but uses broad taint walk
    findings = []
    assignments = collect_assignments(func_node)
    param_names = [arg.arg for arg in func_node.args.args]

    for node in ast.walk(func_node):
        if not isinstance(node, ast.Call):
            continue
        call_name = get_call_name(node.func)
        if not any(call_name.endswith(s.split(".")[-1]) for s in SINKS):
            continue
        if is_parameterized(node):
            continue
        if not node.args:
            continue

        query_arg = node.args[0]
        tainted, flow = taint_walk_broad(query_arg, assignments, param_names)

        if tainted:
            findings.append({
                "file": filename,
                "line": node.lineno,
                "function": func_node.name,
                "sink": call_name,
                "flow": flow,
                "source": "broad_param" if not any("request" in f for f in flow) else "http_request",
            })
    return findings


def analyze_file_broad(filepath):
    # same as analyze_file but uses broad source model
    import sys
    _self = sys.modules[__name__]
    old_mode = _self.BROAD_MODE
    _self.BROAD_MODE = True

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            source = f.read()
        try:
            tree = ast.parse(source)
        except SyntaxError as e:
            print(f"Skipping {filepath} - syntax error: {e}")
            _self.BROAD_MODE = old_mode
            return []

        call_graph = build_call_graph(tree)
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                findings.extend(analyze_function_broad(node, filepath, call_graph))
        return findings
    finally:
        _self.BROAD_MODE = old_mode


# --- Level 2: cross-file inter-procedural analysis ---
# the existing call graph only covers functions defined in the same file
# this builds a global call graph across every .py file in a repo
# so we can follow taint into helper functions in other files

def build_global_call_graph(repo_path):
    # walk all python files in the repo and collect every function definition
    # maps function name -> list of entries (because different files can define
    # functions with the same name)
    global_cg = {}
    for root, dirs, files in os.walk(repo_path):
        # skip folders that aren't application code
        dirs[:] = [d for d in dirs if d not in {
            'venv', '.venv', 'env', 'migrations', '__pycache__',
            '.git', 'node_modules', 'dist', 'build', 'tests', 'test'
        }]
        for fname in files:
            if not fname.endswith('.py'):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    source = f.read()
                tree = ast.parse(source)
            except Exception:
                continue
            for node in ast.walk(tree):
                if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                param_names = [arg.arg for arg in node.args.args]
                entry = {
                    'node': node,
                    'params': param_names,
                    'filepath': fpath,
                }
                if node.name not in global_cg:
                    global_cg[node.name] = []
                global_cg[node.name].append(entry)
    return global_cg


# --- Level 3: object attribute and return value tracking ---
# handles cases like self.key_name being built from user input
# and cases where a helper function returns a tainted SQL string

def collect_attribute_assignments(func_node):
    # finds self.x = <value> assignments inside a method
    attr_assignments = {}
    for node in ast.walk(func_node):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if (isinstance(target, ast.Attribute) and
                    isinstance(target.value, ast.Name) and
                    target.value.id == 'self'):
                attr_assignments[target.attr] = node.value
    return attr_assignments


def collect_class_attribute_assignments(class_node):
    # collects self.x = value assignments across ALL methods in a class
    # so taint can flow from __init__ storing self.sql = param
    # to another method that later calls cursor.execute(self.sql)
    class_attrs = {}
    for node in ast.walk(class_node):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        param_names = [arg.arg for arg in node.args.args]
        for child in ast.walk(node):
            if not isinstance(child, ast.Assign):
                continue
            for target in child.targets:
                if (isinstance(target, ast.Attribute) and
                        isinstance(target.value, ast.Name) and
                        target.value.id == 'self'):
                    # if the value is a parameter, mark it as broad source
                    if isinstance(child.value, ast.Name) and child.value.id in param_names:
                        class_attrs[target.attr] = None  # None = tainted param
                    else:
                        class_attrs[target.attr] = child.value
    return class_attrs


def get_enclosing_class_node(tree, func_node):
    # finds the class that contains a given function node
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in ast.walk(node):
                if item is func_node:
                    return node
    return None


def collect_return_values(func_node):
    # finds all return statements and returns the values being returned
    returns = []
    for node in ast.walk(func_node):
        if isinstance(node, ast.Return) and node.value is not None:
            returns.append(node.value)
    return returns


# --- the full taint walk combining Level 2 and Level 3 ---
# tries local functions first, then global (cross-file),
# then follows self.x attribute reads,
# then follows return values of called functions

def taint_walk_full(arg_node, assignments, attr_assignments,
                    local_cg, global_cg, visited_funcs=None, depth=0):
    if visited_funcs is None:
        visited_funcs = set()
    if depth > 25:
        return False, []

    # narrow HTTP source check first
    if is_source(arg_node):
        return True, [ast.unparse(arg_node)]

    # broad: a None sentinel means this variable came from a function parameter
    if isinstance(arg_node, ast.Name) and arg_node.id in assignments:
        if assignments[arg_node.id] is None:
            return True, [f"{arg_node.id} (function parameter - untrusted)"]

    # follow variable assignments backward
    if isinstance(arg_node, ast.Name):
        var_name = arg_node.id
        if var_name in assignments:
            av = assignments[var_name]
            if av is None:
                return True, [f"{var_name} (function parameter - untrusted)"]
            if is_source(av):
                return True, [f"{var_name} = {ast.unparse(av)}"]
            if isinstance(av, (ast.BinOp, ast.JoinedStr, ast.Call)):
                tainted, flow = check_expression_full(
                    av, assignments, attr_assignments,
                    local_cg, global_cg, visited_funcs, depth)
                if tainted:
                    return True, flow + [f"{var_name} = {ast.unparse(av)}"]
            if isinstance(av, ast.Name):
                tainted, flow = taint_walk_full(
                    av, assignments, attr_assignments,
                    local_cg, global_cg, visited_funcs, depth + 1)
                if tainted:
                    return True, flow + [f"{var_name} = {ast.unparse(av)}"]
            # Level 3: variable assigned from a self.x attribute read
            if isinstance(av, ast.Attribute):
                tainted, flow = taint_walk_full(
                    av, assignments, attr_assignments,
                    local_cg, global_cg, visited_funcs, depth + 1)
                if tainted:
                    return True, flow + [f"{var_name} = {ast.unparse(av)}"]

    # Level 3: self.x attribute read - check if that attribute was tainted
    if isinstance(arg_node, ast.Attribute):
        attr_name = arg_node.attr
        if attr_name in attr_assignments:
            tainted, flow = taint_walk_full(
                attr_assignments[attr_name], assignments, attr_assignments,
                local_cg, global_cg, visited_funcs, depth + 1)
            if tainted:
                return True, flow + [f"self.{attr_name} (attribute taint)"]

    # concatenation, f-string, or .format() expression
    if isinstance(arg_node, (ast.BinOp, ast.JoinedStr, ast.Call)):
        return check_expression_full(
            arg_node, assignments, attr_assignments,
            local_cg, global_cg, visited_funcs, depth)

    # follow calls into local or global functions
    if isinstance(arg_node, ast.Call):
        func_name = ""
        if isinstance(arg_node.func, ast.Name):
            func_name = arg_node.func.id
        elif isinstance(arg_node.func, ast.Attribute):
            func_name = arg_node.func.attr

        if func_name and func_name not in visited_funcs:
            # try local call graph first then global
            candidates = []
            if func_name in local_cg:
                candidates.append(local_cg[func_name])
            if func_name in global_cg:
                candidates.extend(global_cg[func_name])

            for callee in candidates:
                visited_funcs.add(func_name)
                callee_node = callee['node']
                callee_params = callee['params']
                callee_assignments = collect_assignments(callee_node)
                callee_attrs = collect_attribute_assignments(callee_node)

                # map call arguments to parameter names at the call site
                for i, call_arg in enumerate(arg_node.args):
                    if i < len(callee_params):
                        callee_assignments[callee_params[i]] = call_arg

                # mark unmapped params as broad sources (None sentinel)
                for p in callee_params:
                    if p not in callee_assignments:
                        callee_assignments[p] = None

                # Level 2: look for sinks inside the callee
                for node in ast.walk(callee_node):
                    if not isinstance(node, ast.Call):
                        continue
                    call_name = get_call_name(node.func)
                    if not any(call_name.endswith(s.split(".")[-1]) for s in SINKS):
                        continue
                    if is_parameterized(node):
                        continue
                    if not node.args:
                        continue
                    tainted, flow = taint_walk_full(
                        node.args[0], callee_assignments, callee_attrs,
                        local_cg, global_cg, visited_funcs.copy(), depth + 1)
                    if tainted:
                        fp = callee.get('filepath', 'unknown')
                        return True, flow + [f"called {func_name}() in {fp}"]

                # Level 3: check if the callee returns tainted data
                for ret_val in collect_return_values(callee_node):
                    tainted, flow = taint_walk_full(
                        ret_val, callee_assignments, callee_attrs,
                        local_cg, global_cg, visited_funcs.copy(), depth + 1)
                    if tainted:
                        return True, flow + [
                            f"return value of {func_name}() is tainted"]

    return False, []


def check_expression_full(node, assignments, attr_assignments,
                          local_cg, global_cg, visited_funcs, depth=0):
    # handles BinOp (+, %), JoinedStr (f-string), and .format() calls
    if isinstance(node, ast.BinOp):
        for side in (node.left, node.right):
            tainted, flow = taint_walk_full(
                side, assignments, attr_assignments,
                local_cg, global_cg, visited_funcs, depth + 1)
            if tainted:
                return True, flow
    if isinstance(node, ast.JoinedStr):
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                tainted, flow = taint_walk_full(
                    value.value, assignments, attr_assignments,
                    local_cg, global_cg, visited_funcs, depth + 1)
                if tainted:
                    return True, flow
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'format':
            for arg in node.args:
                tainted, flow = taint_walk_full(
                    arg, assignments, attr_assignments,
                    local_cg, global_cg, visited_funcs, depth + 1)
                if tainted:
                    return True, flow
            for kw in node.keywords:
                tainted, flow = taint_walk_full(
                    kw.value, assignments, attr_assignments,
                    local_cg, global_cg, visited_funcs, depth + 1)
                if tainted:
                    return True, flow
    return False, []


def analyze_file_full(filepath, global_cg=None):
    # runs the complete Level 1+2+3 analysis on a single file
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        tree = ast.parse(source)
    except SyntaxError as e:
        print(f"Skipping {filepath} - syntax error: {e}")
        return []

    local_cg = build_call_graph(tree)
    if global_cg is None:
        global_cg = {}

    # build class-level attribute maps for all classes in the file
    # so taint can flow from self.x assigned in __init__ to other methods
    class_attr_maps = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_attr_maps[node.name] = collect_class_attribute_assignments(node)

    findings = []
    for func_node in ast.walk(tree):
        if not isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        assignments = collect_assignments(func_node)

        # get class-level attribute assignments if this is a method
        # start with class-level attrs so self.x from __init__ is visible
        enclosing_class = get_enclosing_class_node(tree, func_node)
        if enclosing_class and enclosing_class.name in class_attr_maps:
            # merge class-level attrs with method-level attrs
            # method-level takes precedence (more specific)
            attr_assignments = dict(class_attr_maps[enclosing_class.name])
            attr_assignments.update(collect_attribute_assignments(func_node))
        else:
            attr_assignments = collect_attribute_assignments(func_node)

        param_names = [arg.arg for arg in func_node.args.args]

        # always mark params as broad sources with None sentinel
        # even if they were reassigned later - the reassigned value may
        # still be derived from the param (e.g. name = name or "default")
        for p in param_names:
            assignments[p] = None

        for node in ast.walk(func_node):
            if not isinstance(node, ast.Call):
                continue
            call_name = get_call_name(node.func)
            if not any(call_name.endswith(s.split(".")[-1]) for s in SINKS):
                continue
            if is_parameterized(node):
                continue
            if not node.args:
                continue

            tainted, flow = taint_walk_full(
                node.args[0], assignments, attr_assignments,
                local_cg, global_cg, set(), 0)

            if tainted:
                findings.append({
                    'file': filepath,
                    'line': node.lineno,
                    'function': func_node.name,
                    'sink': call_name,
                    'flow': flow,
                    'source': 'http_request' if any(
                        'request' in f for f in flow) else 'broad_param',
                })
    return findings


# --- LLM detector ---
# runs on functions the static engine missed
# looks for SQL injection patterns that don't have a sink in the current function
# e.g. SQL string construction that gets returned and executed elsewhere
# sends the full function source to the LLM and asks if it looks vulnerable
# the Challenger then filters the LLM's findings to reduce false positives

# keywords that suggest a function is SQL-related even without a direct sink
SQL_SMELL_KEYWORDS = {
    'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE',
    'JOIN', 'execute', 'cursor', 'sql', 'query', 'SQL',
}

def function_smells_like_sql(func_source):
    # quick check before calling the LLM - only run on functions
    # that actually contain SQL-related code
    return any(kw in func_source for kw in SQL_SMELL_KEYWORDS)


def llm_detect(func_source, func_name):
    # asks the LLM directly: is this function a SQL injection vulnerability?
    # used for cases the static engine cannot reach (no sink in scope)
    client = anthropic.Anthropic()

    prompt = f"""You are a security analysis tool detecting SQL injection vulnerabilities.

Look at this Python function and determine if it contains or contributes to a SQL injection vulnerability.

Pay attention to:
- SQL strings built by concatenating or interpolating user-controlled values
- Functions that return tainted SQL strings for execution elsewhere
- Patterns where user input reaches a SQL construction point without sanitization
- String formatting with % or .format() or f-strings that include parameters

Do NOT flag:
- Correct parameterized queries where user values are separate arguments
- ORM calls like filter(), get(), filter_by() which are always parameterized
- Functions that only use hardcoded SQL strings with no variable interpolation
- Functions where all inputs are validated by whitelist, isinstance(x, int), or regex

FUNCTION NAME: {func_name}

FUNCTION SOURCE:
```python
{func_source}
```

Respond ONLY in this exact JSON format. No text outside the JSON.

{{
  "vulnerable": true or false,
  "confidence": "high" or "medium" or "low",
  "reasoning": "one or two sentences explaining why",
  "sink_present": true or false
}}"""

    raw = llm_call(prompt, max_tokens=512)
    try:
        clean = raw.replace('```json', '').replace('```', '').strip()
        return json.loads(clean)
    except Exception:
        return {"vulnerable": False, "confidence": "low", "reasoning": "parse error"}


def analyze_file_llm(filepath, static_findings=None, global_cg=None):
    # runs the LLM detector on functions the static engine missed
    # static_findings: list of findings already found by analyze_file_full
    # so we don't double-report the same function

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        tree = ast.parse(source)
        lines = source.splitlines()
    except SyntaxError as e:
        print(f"Skipping {filepath} - syntax error: {e}")
        return []

    # collect function names already found by static engine
    already_found = set()
    if static_findings:
        for f in static_findings:
            already_found.add(f['function'])

    findings = []

    for func_node in ast.walk(tree):
        if not isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        # skip functions the static engine already flagged
        if func_node.name in already_found:
            continue

        func_source = '\n'.join(lines[func_node.lineno-1:func_node.end_lineno])

        # only run LLM on functions that smell like SQL
        if not function_smells_like_sql(func_source):
            continue

        # get enclosing class for context if available
        # include class name and file path so LLM can recognize
        # query builder libraries vs application code
        class_context = ""
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if item is func_node:
                        class_context = (
                            f"# file: {filepath}\n"
                            f"# class: {node.name}\n"
                            f"# note: consider whether this class is a SQL query builder\n"
                            f"# library (where SQL construction is intentional) or\n"
                            f"# application code (where user input may flow in)\n"
                        )
                        break

        full_source = class_context + func_source if class_context else f"# file: {filepath}\n" + func_source

        result = llm_detect(full_source, func_node.name)

        if not result.get('vulnerable', False):
            continue

        # only report medium or high confidence findings
        if result.get('confidence') == 'low':
            continue

        findings.append({
            'file': filepath,
            'line': func_node.lineno,
            'function': func_node.name,
            'sink': 'llm_detected',   # no static sink found
            'flow': [result.get('reasoning', '')],
            'source': 'llm_detector',
            'confidence': result.get('confidence'),
            'sink_present': result.get('sink_present', False),
        })

    return findings


def analyze_file_llm_only(filepath):
    # TRACE-LLM configuration: LLM detector + Confirmer + Challenger
    # no static analysis - works on any language
    # detects via LLM, then filters with two-phase adversarial pipeline
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        tree = ast.parse(source)
        lines = source.splitlines()
    except SyntaxError as e:
        print(f"Skipping {filepath} - syntax error: {e}")
        return []

    confirmed = []
    for func_node in ast.walk(tree):
        if not isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        func_source = "\n".join(lines[func_node.lineno-1:func_node.end_lineno])
        if not function_smells_like_sql(func_source):
            continue

        # step 1: LLM detector
        result = llm_detect(func_source, func_node.name)
        if not result.get('vulnerable', False):
            continue
        if result.get('confidence') == 'low':
            continue

        # step 2: Confirmer
        flow = [result.get('reasoning', '')]
        func_full = get_function_source(filepath, func_node.name)
        p1 = phase1_confirm(flow, function_source=func_full)
        if p1.get('verdict') == 'suppressed':
            continue

        # step 3: Challenger
        if p1.get('verdict') == 'confirmed':
            p2 = phase2_challenge(flow, p1)
            finding = build_finding(
                {'file': filepath, 'line': func_node.lineno,
                 'function': func_node.name, 'sink': 'llm_detected',
                 'flow': flow, 'source': 'llm_only'},
                p1, p2, threshold=0.7)
            if finding is not None:
                confirmed.append(finding)
        else:
            # needs_review - include as medium confidence
            confirmed.append({
                'file': filepath, 'line': func_node.lineno,
                'function': func_node.name, 'sink': 'llm_detected',
                'flow': flow, 'source': 'llm_only',
                'severity': 'MEDIUM', 'verdict': 'needs_review',
            })
    return confirmed


def analyze_file_hybrid(filepath, global_cg=None):
    # full hybrid analysis: static engine first, then LLM detector for misses
    static_findings = analyze_file_full(filepath, global_cg)

    # run LLM detector on functions the static engine did not flag
    llm_findings = analyze_file_llm(filepath, static_findings, global_cg)

    return static_findings, llm_findings
