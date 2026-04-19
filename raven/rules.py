import re

RULES = [

    # ========================
    # 🔥 Code Execution Risks
    # ========================
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
        "name": "compile_usage",
        "pattern": r"compile\(",
        "severity": "MEDIUM",
        "message": "compile() can execute dynamic code"
    },

    # ========================
    # 💻 Command Injection
    # ========================
    {
        "name": "os_system",
        "pattern": r"os\.system\(",
        "severity": "HIGH",
        "message": "os.system() can lead to command injection"
    },
    {
        "name": "subprocess_shell",
        "pattern": r"subprocess\..*shell\s*=\s*True",
        "severity": "HIGH",
        "message": "shell=True can lead to command injection"
    },
    {
        "name": "popen_usage",
        "pattern": r"os\.popen\(",
        "severity": "HIGH",
        "message": "os.popen() is unsafe"
    },
    {
        "name": "subprocess_call",
        "pattern": r"subprocess\.call\(",
        "severity": "MEDIUM",
        "message": "Check subprocess usage for injection risks"
    },

    # ========================
    # 🔑 Hardcoded Secrets
    # ========================
    {
        "name": "hardcoded_password",
        "pattern": r"password\s*=\s*['\"].+['\"]",
        "severity": "MEDIUM",
        "message": "Hardcoded password detected"
    },
    {
        "name": "hardcoded_api_key",
        "pattern": r"api[_-]?key\s*=\s*['\"].+['\"]",
        "severity": "HIGH",
        "message": "Hardcoded API key detected"
    },
    {
        "name": "hardcoded_token",
        "pattern": r"token\s*=\s*['\"].+['\"]",
        "severity": "HIGH",
        "message": "Hardcoded token detected"
    },
    {
        "name": "aws_secret",
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "HIGH",
        "message": "Possible AWS access key exposed"
    },

    # ========================
    # 🌐 Web Vulnerabilities
    # ========================
    {
        "name": "sql_query_concat",
        "pattern": r"SELECT .* \+ .*",
        "severity": "HIGH",
        "message": "Possible SQL injection via string concatenation"
    },
    {
        "name": "cursor_execute_format",
        "pattern": r"execute\(.*%.*\)",
        "severity": "HIGH",
        "message": "Possible SQL injection via string formatting"
    },
    {
        "name": "input_usage",
        "pattern": r"input\(",
        "severity": "LOW",
        "message": "User input detected—validate input properly"
    },
    {
        "name": "flask_debug",
        "pattern": r"debug\s*=\s*True",
        "severity": "MEDIUM",
        "message": "Debug mode should not be enabled in production"
    },

    # ========================
    # 📁 File Handling Risks
    # ========================
    {
        "name": "open_write",
        "pattern": r"open\(.*['\"].*['\"],\s*['\"]w['\"]\)",
        "severity": "LOW",
        "message": "File opened in write mode—ensure safe path handling"
    },
    {
        "name": "pickle_load",
        "pattern": r"pickle\.load\(",
        "severity": "HIGH",
        "message": "pickle.load() is unsafe with untrusted data"
    },
    {
        "name": "yaml_load",
        "pattern": r"yaml\.load\(",
        "severity": "HIGH",
        "message": "yaml.load() is unsafe—use safe_load()"
    },

    # ========================
    # 🔐 Crypto Issues
    # ========================
    {
        "name": "md5_usage",
        "pattern": r"hashlib\.md5\(",
        "severity": "HIGH",
        "message": "MD5 is insecure for cryptographic purposes"
    },
    {
        "name": "sha1_usage",
        "pattern": r"hashlib\.sha1\(",
        "severity": "HIGH",
        "message": "SHA1 is deprecated for security use"
    },
    {
        "name": "random_usage",
        "pattern": r"random\.random\(",
        "severity": "MEDIUM",
        "message": "Use secrets module for secure randomness"
    },

    # ========================
    # 🧠 Deserialization Risks
    # ========================
    {
        "name": "pickle_dump",
        "pattern": r"pickle\.dump\(",
        "severity": "MEDIUM",
        "message": "Ensure pickle data is trusted"
    },
    {
        "name": "marshal_load",
        "pattern": r"marshal\.loads?\(",
        "severity": "HIGH",
        "message": "marshal loading is unsafe"
    },

    # ========================
    # 🌍 Network Risks
    # ========================
    {
        "name": "requests_no_verify",
        "pattern": r"requests\..*verify\s*=\s*False",
        "severity": "HIGH",
        "message": "SSL verification disabled"
    },
    {
        "name": "http_url",
        "pattern": r"http://",
        "severity": "LOW",
        "message": "Unencrypted HTTP used"
    },

    # ========================
    # 🧩 Misc Dangerous Patterns
    # ========================
    {
        "name": "assert_usage",
        "pattern": r"assert\s+",
        "severity": "LOW",
        "message": "assert statements removed in optimized mode"
    },
    {
        "name": "bare_except",
        "pattern": r"except\s*:",
        "severity": "MEDIUM",
        "message": "Bare except hides errors"
    },
    {
        "name": "tempfile_usage",
        "pattern": r"tempfile\.mktemp\(",
        "severity": "HIGH",
        "message": "mktemp() is insecure—use mkstemp()"
    },
    {
        "name": "debug_print",
        "pattern": r"print\(",
        "severity": "LOW",
        "message": "Debug print statement found"
    },

    # ========================
    # 🤖 LLM / AI Risks (Your unique angle)
    # ========================
    {
        "name": "openai_api_key",
        "pattern": r"openai\.api_key\s*=\s*['\"].+['\"]",
        "severity": "HIGH",
        "message": "Hardcoded OpenAI API key detected"
    },
    {
        "name": "prompt_injection_risk",
        "pattern": r"f['\"].*{.*}.*['\"]",
        "severity": "MEDIUM",
        "message": "Dynamic prompt construction—possible prompt injection"
    },

    # ========================
    # ⚙️ Dangerous Imports
    # ========================
    {
        "name": "import_pickle",
        "pattern": r"import pickle",
        "severity": "LOW",
        "message": "pickle can be unsafe if misused"
    },
    {
        "name": "import_subprocess",
        "pattern": r"import subprocess",
        "severity": "LOW",
        "message": "subprocess usage requires caution"
    },

    # ========================
    # 🧾 Logging Issues
    # ========================
    {
        "name": "logging_sensitive",
        "pattern": r"logging\..*\(.*password.*\)",
        "severity": "HIGH",
        "message": "Sensitive data logged"
    },
]