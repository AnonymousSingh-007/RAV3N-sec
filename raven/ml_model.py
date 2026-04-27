# raven/ml_model.py

from sklearn.linear_model import LogisticRegression
import numpy as np

from raven.features import extract_features

# 🔥 Synthetic dataset (expand later)
samples = [
    ("eval(user_input)", 1),
    ("exec(code)", 1),
    ("os.system(cmd)", 1),
    ("subprocess.call(cmd, shell=True)", 1),
    ("pickle.load(file)", 1),
    ("SELECT * FROM users + input()", 1),
    ("password = 'secret'", 1),
    ("requests.get(url, verify=False)", 1),

    ("print('hello')", 0),
    ("x = 5 + 2", 0),
    ("for i in range(10): pass", 0),
    ("safe_function()", 0),
]

X = np.array([extract_features(s[0]) for s in samples])
y = np.array([s[1] for s in samples])

model = LogisticRegression(max_iter=200)
model.fit(X, y)


def calibrate(prob: float) -> float:
    """Smooth confidence so it feels meaningful"""
    if prob > 0.9:
        return 0.95
    elif prob > 0.75:
        return 0.85
    elif prob > 0.6:
        return 0.75
    else:
        return 0.6


def predict(code_line: str):
    features = np.array(extract_features(code_line)).reshape(1, -1)

    prob = model.predict_proba(features)[0][1]
    pred = int(prob > 0.5)

    confidence = calibrate(prob)

    return pred, confidence