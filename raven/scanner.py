import ast
import re
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
                    "type": "regex"
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
                        "message": "AST: eval() usage detected",
                        "type": "ast"
                    })

                if node.func.id == "exec":
                    findings.append({
                        "line": node.lineno,
                        "severity": "HIGH",
                        "message": "AST: exec() usage detected",
                        "type": "ast"
                    })

    return findings


def ai_stub(code):
    # placeholder for future ML model
    return []


def scan_file(path):
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    lines = code.split("\n")

    results = []
    results.extend(scan_regex(lines))
    results.extend(scan_ast(code))
    results.extend(ai_stub(code))

    return results