import re

RULES = [
    {
        "name": "eval_usage",
        "pattern": r"eval\(",
        "severity": "HIGH",
        "message": "Use of eval() can lead to code execution"
    },
    {
        "name": "exec_usage",
        "pattern": r"exec\(",
        "severity": "HIGH",
        "message": "Use of exec() is dangerous"
    },
    {
        "name": "hardcoded_password",
        "pattern": r"password\s*=\s*['\"].+['\"]",
        "severity": "MEDIUM",
        "message": "Hardcoded password detected"
    },
    {
        "name": "subprocess_shell",
        "pattern": r"subprocess\..*shell\s*=\s*True",
        "severity": "HIGH",
        "message": "shell=True can lead to command injection"
    }
]