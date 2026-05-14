# raven/rules.py

RULES = [

    # =========================
    # CODE EXECUTION
    # =========================

    {
        "rule_id": "PY100",
        "pattern": r"\beval\s*\(",
        "severity": "CRITICAL",
        "message": "eval() usage detected",
        "fix": "Avoid eval(); use safer parsing",
        "cwe": "CWE-95",
        "confidence": 0.98,
    },

    {
        "rule_id": "PY101",
        "pattern": r"\bexec\s*\(",
        "severity": "CRITICAL",
        "message": "exec() usage detected",
        "fix": "Avoid exec()",
        "cwe": "CWE-78",
        "confidence": 0.98,
    },

    {
        "rule_id": "PY102",
        "pattern": r"os\.system\s*\(",
        "severity": "HIGH",
        "message": "os.system() detected",
        "fix": "Use subprocess safely",
        "cwe": "CWE-78",
        "confidence": 0.95,
    },

    {
        "rule_id": "PY103",
        "pattern": r"subprocess\.(call|Popen|run).*shell\s*=\s*True",
        "severity": "CRITICAL",
        "message": "Shell injection risk",
        "fix": "Avoid shell=True",
        "cwe": "CWE-78",
        "confidence": 0.98,
    },

    # =========================
    # DESERIALIZATION
    # =========================

    {
        "rule_id": "PY104",
        "pattern": r"pickle\.load",
        "severity": "HIGH",
        "message": "Unsafe pickle deserialization",
        "fix": "Avoid untrusted pickle data",
        "cwe": "CWE-502",
        "confidence": 0.92,
    },

    {
        "rule_id": "PY105",
        "pattern": r"yaml\.load",
        "severity": "HIGH",
        "message": "Unsafe YAML loading",
        "fix": "Use yaml.safe_load()",
        "cwe": "CWE-20",
        "confidence": 0.90,
    },

    # =========================
    # CRYPTO
    # =========================

    {
        "rule_id": "PY106",
        "pattern": r"\bmd5\b",
        "severity": "MEDIUM",
        "message": "Weak hash algorithm detected",
        "fix": "Use SHA-256 or bcrypt",
        "cwe": "CWE-327",
        "confidence": 0.80,
    },

    {
        "rule_id": "PY107",
        "pattern": r"\bsha1\b",
        "severity": "MEDIUM",
        "message": "Weak SHA1 detected",
        "fix": "Use SHA-256+",
        "cwe": "CWE-327",
        "confidence": 0.80,
    },

    {
        "rule_id": "PY108",
        "pattern": r"random\.random",
        "severity": "LOW",
        "message": "Insecure randomness",
        "fix": "Use secrets module",
        "cwe": "CWE-330",
        "confidence": 0.70,
    },

    # =========================
    # WEB SECURITY
    # =========================

    {
        "rule_id": "PY109",
        "pattern": r"debug\s*=\s*True",
        "severity": "HIGH",
        "message": "Debug mode enabled",
        "fix": "Disable debug in production",
        "cwe": "CWE-489",
        "confidence": 0.88,
    },

    {
        "rule_id": "PY110",
        "pattern": r"verify\s*=\s*False",
        "severity": "HIGH",
        "message": "SSL verification disabled",
        "fix": "Enable SSL verification",
        "cwe": "CWE-295",
        "confidence": 0.90,
    },

    {
        "rule_id": "PY111",
        "pattern": r"requests\.(get|post)\(.+http://",
        "severity": "MEDIUM",
        "message": "Insecure HTTP request",
        "fix": "Use HTTPS",
        "cwe": "CWE-319",
        "confidence": 0.75,
    },

    # =========================
    # SQL INJECTION
    # =========================

    {
        "rule_id": "PY112",
        "pattern": r"SELECT.+\+.+input",
        "severity": "CRITICAL",
        "message": "Potential SQL Injection",
        "fix": "Use parameterized queries",
        "cwe": "CWE-89",
        "confidence": 0.95,
    },

    {
        "rule_id": "PY113",
        "pattern": r"cursor\.execute\s*\(.+\+",
        "severity": "HIGH",
        "message": "Dynamic SQL query detected",
        "fix": "Use parameterized queries",
        "cwe": "CWE-89",
        "confidence": 0.92,
    },

    # =========================
    # HARDCODED SECRETS
    # =========================

    {
        "rule_id": "PY114",
        "pattern": r"(password|passwd|secret|token|api_key)\s*=\s*[\"'].*[\"']",
        "severity": "HIGH",
        "message": "Hardcoded secret detected",
        "fix": "Use environment variables",
        "cwe": "CWE-798",
        "confidence": 0.85,
    },

    # =========================
    # TEMP FILES
    # =========================

    {
        "rule_id": "PY115",
        "pattern": r"tempfile\.mktemp",
        "severity": "HIGH",
        "message": "Insecure temporary file",
        "fix": "Use NamedTemporaryFile",
        "cwe": "CWE-377",
        "confidence": 0.88,
    },

    # =========================
    # ASSERT MISUSE
    # =========================

    {
        "rule_id": "PY116",
        "pattern": r"\bassert\b",
        "severity": "LOW",
        "message": "assert statement detected",
        "fix": "Avoid assert for security checks",
        "cwe": "CWE-617",
        "confidence": 0.60,
        "noisy": True,
    },

    # =========================
    # DJANGO / FLASK
    # =========================

    {
        "rule_id": "PY117",
        "pattern": r"csrf_exempt",
        "severity": "HIGH",
        "message": "CSRF protection disabled",
        "fix": "Avoid csrf_exempt",
        "cwe": "CWE-352",
        "confidence": 0.90,
    },

    # =========================
    # JWT
    # =========================

    {
        "rule_id": "PY118",
        "pattern": r"jwt\.decode\(.*verify\s*=\s*False",
        "severity": "CRITICAL",
        "message": "JWT verification disabled",
        "fix": "Enable JWT verification",
        "cwe": "CWE-347",
        "confidence": 0.95,
    },

]