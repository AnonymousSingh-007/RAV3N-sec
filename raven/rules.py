import re

RULES = [

    # ========================
    # 🔥 Code Execution Risks
    # ========================
    {
        "name": "eval_usage",
        "pattern": r"\beval\s*\(",
        "severity": "HIGH",
        "message": "Use of eval() can lead to code execution",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Use ast.literal_eval() instead of eval()"
    },
    {
        "name": "exec_usage",
        "pattern": r"\bexec\s*\(",
        "severity": "HIGH",
        "message": "Use of exec() is dangerous",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Avoid exec(); use safer alternatives"
    },
    {
        "name": "compile_usage",
        "pattern": r"\bcompile\s*\(",
        "severity": "MEDIUM",
        "message": "compile() can execute dynamic code",
        "confidence": 0.7,
        "noisy": False,
        "fix": "Avoid dynamic compilation of untrusted input"
    },

    # ========================
    # 💻 Command Injection
    # ========================
    {
        "name": "os_system",
        "pattern": r"os\.system\s*\(",
        "severity": "HIGH",
        "message": "os.system() can lead to command injection",
        "confidence": 0.9,
        "noisy": False,
        "fix": "Use subprocess with argument list instead of shell commands"
    },
    {
        "name": "subprocess_shell",
        "pattern": r"subprocess\..*shell\s*=\s*True",
        "severity": "HIGH",
        "message": "shell=True can lead to command injection",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Set shell=False and pass arguments as list"
    },
    {
        "name": "popen_usage",
        "pattern": r"os\.popen\s*\(",
        "severity": "HIGH",
        "message": "os.popen() is unsafe",
        "confidence": 0.85,
        "noisy": False,
        "fix": "Use subprocess.run() instead"
    },
    {
        "name": "subprocess_call",
        "pattern": r"subprocess\.(call|run|Popen)\s*\(",
        "severity": "MEDIUM",
        "message": "Check subprocess usage for injection risks",
        "confidence": 0.6,
        "noisy": False,
        "fix": "Ensure inputs are sanitized"
    },

    # ========================
    # 🔑 Hardcoded Secrets
    # ========================
    {
        "name": "hardcoded_password",
        "pattern": r"password\s*=\s*['\"].{4,}['\"]",
        "severity": "MEDIUM",
        "message": "Hardcoded password detected",
        "confidence": 0.8,
        "noisy": False,
        "fix": "Use environment variables or secure vaults"
    },
    {
        "name": "hardcoded_api_key",
        "pattern": r"api[_-]?key\s*=\s*['\"].{8,}['\"]",
        "severity": "HIGH",
        "message": "Hardcoded API key detected",
        "confidence": 0.9,
        "noisy": False,
        "fix": "Move API keys to environment variables"
    },
    {
        "name": "hardcoded_token",
        "pattern": r"token\s*=\s*['\"].{8,}['\"]",
        "severity": "HIGH",
        "message": "Hardcoded token detected",
        "confidence": 0.9,
        "noisy": False,
        "fix": "Store tokens securely outside source code"
    },
    {
        "name": "aws_secret",
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "HIGH",
        "message": "Possible AWS access key exposed",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Rotate credentials immediately and use IAM roles"
    },

    # ========================
    # 🌐 Web Vulnerabilities
    # ========================
    {
        "name": "sql_query_concat",
        "pattern": r"(SELECT|INSERT|UPDATE|DELETE).*\+.*",
        "severity": "HIGH",
        "message": "Possible SQL injection via string concatenation",
        "confidence": 0.85,
        "noisy": False,
        "fix": "Use parameterized queries"
    },
    {
        "name": "cursor_execute_format",
        "pattern": r"execute\s*\(.*[%+].*\)",
        "severity": "HIGH",
        "message": "Possible SQL injection via string formatting",
        "confidence": 0.9,
        "noisy": False,
        "fix": "Use parameterized queries instead of string formatting"
    },
    {
        "name": "input_usage",
        "pattern": r"\binput\s*\(",
        "severity": "LOW",
        "message": "User input detected—validate input properly",
        "confidence": 0.4,
        "noisy": True,
        "fix": "Validate and sanitize all user inputs"
    },
    {
        "name": "flask_debug",
        "pattern": r"debug\s*=\s*True",
        "severity": "MEDIUM",
        "message": "Debug mode should not be enabled in production",
        "confidence": 0.7,
        "noisy": False,
        "fix": "Set debug=False in production"
    },

    # ========================
    # 📁 File Handling Risks
    # ========================
    {
        "name": "pickle_load",
        "pattern": r"pickle\.load\s*\(",
        "severity": "HIGH",
        "message": "pickle.load() is unsafe with untrusted data",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Avoid pickle; use JSON or safe formats"
    },
    {
        "name": "yaml_load",
        "pattern": r"yaml\.load\s*\(",
        "severity": "HIGH",
        "message": "yaml.load() is unsafe—use safe_load()",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Use yaml.safe_load()"
    },

    # ========================
    # 🔐 Crypto Issues
    # ========================
    {
        "name": "md5_usage",
        "pattern": r"hashlib\.md5\s*\(",
        "severity": "HIGH",
        "message": "MD5 is insecure for cryptographic purposes",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Use SHA-256 or bcrypt"
    },
    {
        "name": "sha1_usage",
        "pattern": r"hashlib\.sha1\s*\(",
        "severity": "HIGH",
        "message": "SHA1 is deprecated for security use",
        "confidence": 0.9,
        "noisy": False,
        "fix": "Use SHA-256 or stronger algorithms"
    },

    # ========================
    # 🌍 Network Risks
    # ========================
    {
        "name": "requests_no_verify",
        "pattern": r"requests\..*verify\s*=\s*False",
        "severity": "HIGH",
        "message": "SSL verification disabled",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Enable SSL verification"
    },
    {
        "name": "http_url",
        "pattern": r"http://",
        "severity": "LOW",
        "message": "Unencrypted HTTP used",
        "confidence": 0.5,
        "noisy": True,
        "fix": "Use HTTPS instead"
    },

    # ========================
    # 🧩 Misc
    # ========================
    {
        "name": "bare_except",
        "pattern": r"except\s*:",
        "severity": "MEDIUM",
        "message": "Bare except hides errors",
        "confidence": 0.7,
        "noisy": False,
        "fix": "Catch specific exceptions"
    },
    {
        "name": "debug_print",
        "pattern": r"\bprint\s*\(",
        "severity": "LOW",
        "message": "Debug print statement found",
        "confidence": 0.3,
        "noisy": True,
        "fix": "Remove debug prints in production"
    },

    # ========================
    # 🤖 AI / LLM Risks
    # ========================
    {
        "name": "openai_api_key",
        "pattern": r"openai\.api_key\s*=\s*['\"].+['\"]",
        "severity": "HIGH",
        "message": "Hardcoded OpenAI API key detected",
        "confidence": 0.95,
        "noisy": False,
        "fix": "Store API keys in environment variables"
    },
]