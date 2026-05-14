# raven/features.py

import re


KEYWORDS = [
    "eval",
    "exec",
    "pickle",
    "subprocess",
    "os.system",
    "shell=True",
    "input",
    "password",
    "token",
    "md5",
    "yaml.load",
]


def extract_features(code):

    features = []

    code_lower = code.lower()

    # keyword presence
    for keyword in KEYWORDS:

        features.append(
            1 if keyword.lower() in code_lower else 0
        )

    # length
    features.append(len(code))

    # special chars
    features.append(len(re.findall(r"[(){};]", code)))

    return features