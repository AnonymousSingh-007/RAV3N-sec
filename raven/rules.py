# raven/rules.py
RULES = [

    {
        "rule_id": "PY100",
        "pattern": r"pickle\.load",
        "severity": "HIGH",
        "message": "Unsafe pickle deserialization",
        "fix": "Avoid untrusted pickle data",
        "cwe": "CWE-502",
    },

    {
        "rule_id": "PY101",
        "pattern": r"yaml\.load",
        "severity": "HIGH",
        "message": "Unsafe YAML loading",
        "fix": "Use yaml.safe_load()",
        "cwe": "CWE-20",
    },

    {
        "rule_id": "PY102",
        "pattern": r"md5",
        "severity": "MEDIUM",
        "message": "Weak hash algorithm detected",
        "fix": "Use SHA-256 or bcrypt",
        "cwe": "CWE-327",
    },

]