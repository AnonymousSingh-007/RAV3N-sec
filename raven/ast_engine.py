# raven/ast_engine.py

import ast


class SecurityVisitor(ast.NodeVisitor):

    def __init__(self, filename):
        self.filename = filename
        self.findings = []

    def add_finding(
        self,
        node,
        severity,
        rule_id,
        message,
        fix,
        confidence=0.95,
        cwe=None,
    ):
        self.findings.append({
            "line": node.lineno,
            "severity": severity,
            "rule_id": rule_id,
            "message": message,
            "type": "ast",
            "confidence": confidence,
            "noisy": False,
            "fix": fix,
            "cwe": cwe,
        })

    def visit_Call(self, node):

        # eval()
        if isinstance(node.func, ast.Name):
            if node.func.id == "eval":
                self.add_finding(
                    node,
                    "HIGH",
                    "PY001",
                    "Use of eval() detected",
                    "Replace eval() with ast.literal_eval()",
                    cwe="CWE-95"
                )

            elif node.func.id == "exec":
                self.add_finding(
                    node,
                    "HIGH",
                    "PY002",
                    "Use of exec() detected",
                    "Avoid dynamic execution",
                    cwe="CWE-78"
                )

        # os.system()
        if isinstance(node.func, ast.Attribute):

            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "os"
                and node.func.attr == "system"
            ):
                self.add_finding(
                    node,
                    "HIGH",
                    "PY003",
                    "os.system() detected",
                    "Use subprocess.run([...], shell=False)",
                    cwe="CWE-78"
                )

            # subprocess shell=True
            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "subprocess"
            ):

                for kw in node.keywords:
                    if kw.arg == "shell":
                        if (
                            isinstance(kw.value, ast.Constant)
                            and kw.value.value is True
                        ):
                            self.add_finding(
                                node,
                                "HIGH",
                                "PY004",
                                "subprocess with shell=True detected",
                                "Use shell=False",
                                cwe="CWE-78"
                            )

        self.generic_visit(node)

    def visit_Assign(self, node):

        secret_keywords = [
            "password",
            "passwd",
            "token",
            "secret",
            "api_key",
            "apikey",
        ]

        for target in node.targets:

            if isinstance(target, ast.Name):

                name = target.id.lower()

                if any(k in name for k in secret_keywords):

                    if isinstance(node.value, ast.Constant):

                        if isinstance(node.value.value, str):

                            self.add_finding(
                                node,
                                "MEDIUM",
                                "PY005",
                                "Hardcoded secret detected",
                                "Move secrets to environment variables",
                                cwe="CWE-798"
                            )

        self.generic_visit(node)


def scan_ast(code, filename="<unknown>"):

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []

    visitor = SecurityVisitor(filename)

    visitor.visit(tree)

    return visitor.findings