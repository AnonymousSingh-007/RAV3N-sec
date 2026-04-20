import ast
import re
from collections import defaultdict
from raven.rules import RULES


def scan_regex(lines):
    findings = []

    for i, line in enumerate(lines, start=1):
        for rule in RULES:
            if re.search(rule["pattern"], line):
                findings.append({
                    "line": i,
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "type": "regex",
                    "confidence": rule.get("confidence", 0.7),
                    "noisy": rule.get("noisy", False),
                    "fix": rule.get("fix", "")
                })

    return findings


def scan_ast(code):
    findings = []

    try:
        tree = ast.parse(code)
    except Exception:
        return findings

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if hasattr(node.func, "id"):
                if node.func.id == "eval":
                    findings.append({
                        "line": node.lineno,
                        "severity": "HIGH",
                        "message": "eval() usage detected",
                        "type": "ast",
                        "confidence": 0.95,
                        "noisy": False,
                        "fix": "Use ast.literal_eval() instead"
                    })

                if node.func.id == "exec":
                    findings.append({
                        "line": node.lineno,
                        "severity": "HIGH",
                        "message": "exec() usage detected",
                        "type": "ast",
                        "confidence": 0.95,
                        "noisy": False,
                        "fix": "Avoid exec()"
                    })

    return findings


# 🔥 DEDUP ENGINE
def deduplicate(findings):
    grouped = {}

    for f in findings:
        key = (f["line"], f["message"])

        if key not in grouped:
            grouped[key] = f.copy()
            grouped[key]["type"] = {f["type"]}
        else:
            grouped[key]["type"].add(f["type"])
            grouped[key]["confidence"] = max(
                grouped[key]["confidence"], f["confidence"]
            )

    # convert type set → string
    final = []
    for f in grouped.values():
        f["type"] = "+".join(sorted(f["type"]))
        final.append(f)

    return final


def scan_file(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    lines = code.split("\n")

    results = []
    results.extend(scan_regex(lines))
    results.extend(scan_ast(code))

    # 🔥 dedup here
    results = deduplicate(results)

    return results