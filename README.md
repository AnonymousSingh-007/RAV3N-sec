# 🦅 RAV3N-sec — AI-Ready Vulnerability Scanner

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/AnonymousSingh-007/RAV3N-sec)
[![Stars](https://img.shields.io/github/stars/AnonymousSingh-007/RAV3N-sec?style=social)](https://github.com/AnonymousSingh-007/RAV3N-sec/stargazers)


**A fast, local static analyzer that combines Regex + AST to detect 30+ security vulnerabilities in Python code.**

Built with 🔥 by a B.Tech CS student grinding CTFs and AI-security fusion. Perfect for quick code reviews, bug bounty prep, and learning secure coding.


---

## ✨ Features

- **🔍 Smart Scanning** — Analyzes Python files using Abstract Syntax Trees (AST) to find vulnerabilities that simple regex misses.
- **🛡️ 30+ Vulnerability Detections**:
  - **Code Execution:** `eval()`, `exec()`, `compile()`
  - **Command Injection:** `os.system`, `subprocess` with `shell=True`
  - **Secrets:** Hardcoded API keys (Stripe, AWS, Slack), passwords, and tokens.
  - **Web Risks:** SQL injection patterns, Flask debug mode.
  - **Unsafe Deserialization:** `pickle.load`, `yaml.load`.
  - **Weak Crypto:** MD5, SHA1, insecure `random` usage.
- **📊 Severity Grading** — Categorizes findings into **HIGH**, **MEDIUM**, and **LOW** risk.
- **🖥️ Rich CLI** — Beautiful terminal output with syntax highlighting and clear actionable reports.

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repo
git clone [https://github.com/AnonymousSingh-007/RAV3N-sec.git](https://github.com/AnonymousSingh-007/RAV3N-sec.git)
cd RAV3N-sec

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Usage

Scan a file for vulnerabilities:

```bash
python -m raven.cli scan test.py
```
```bash
python -m raven.cli test.py --html --output myreport.html  

python -m raven.cli  tests --html    
```
---

## 📋 Detection Summary

| Category | Examples | Severity |
| :--- | :--- | :--- |
| **Code Execution** | `eval()`, `exec()` | 🔴 HIGH |
| **Command Injection** | `subprocess.run(..., shell=True)` | 🔴 HIGH |
| **Hardcoded Secrets** | AWS Keys, Stripe Keys, DB Passwords | 🔴 HIGH |
| **Weak Crypto** | `hashlib.md5()`, `random.random()` | 🟡 MED |
| **Insecure Web** | `app.run(debug=True)`, SQL patterns | 🟡 MED |

---

## 🛠️ Project Structure

```text
RAV3N-sec/
├── raven/
│   ├── cli.py        # Typer CLI entry point
│   ├── rules.py      # Core detection logic & AST visitors
│   ├── reports.py    # UI/Output formatting using Rich
│   └── __init__.py
├── test.py           # Sample file for testing vulns
├── pyproject.toml    # Build system & dependencies
└── README.md
```


## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

**#LearnInPublic** — Built live while prepping for security internships and grinding picoCTF.

---

**Star** ⭐ this repo if it helps you secure your code!
```
