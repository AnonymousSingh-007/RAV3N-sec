# raven/features.py

import re


def extract_features(line: str):
    line_lower = line.lower()

    return [
        # 🔥 Dangerous functions
        int("eval(" in line),
        int("exec(" in line),
        int("os.system" in line),
        int("subprocess" in line),
        int("pickle.load" in line),
        int("yaml.load" in line),

        # 💉 Injection patterns
        int("select" in line_lower and "+" in line),
        int("%" in line and "execute" in line_lower),
        int("input(" in line),

        # 🔑 Secrets
        int("password" in line_lower),
        int("api_key" in line_lower or "apikey" in line_lower),
        int("token" in line_lower),

        # 🌐 Network risks
        int("http://" in line_lower),
        int("verify=False" in line),

        # 🔐 Crypto issues
        int("md5" in line_lower),
        int("sha1" in line_lower),

        # 🧠 Prompt / AI risk
        int("f\"" in line or "f'" in line),

        # 📏 Structural features
        len(line),
        line.count("("),
        line.count("="),
    ]