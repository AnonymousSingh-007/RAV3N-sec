# raven/models.py

import os
import joblib
import numpy as np

from sklearn.linear_model import LogisticRegression

from raven.features import extract_features

MODEL_PATH = "raven_model.pkl"


class RavenModel:
    def __init__(self):
        self.model = LogisticRegression(max_iter=500)

    def train(self, samples):
        X = np.array([extract_features(code) for code, _ in samples])
        y = np.array([label for _, label in samples])

        self.model.fit(X, y)

        joblib.dump(self.model, MODEL_PATH)

        print("[+] Model trained and saved.")

    def load(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Model not found. Run train.py first."
            )

        self.model = joblib.load(MODEL_PATH)

    def predict(self, code_line):
        features = np.array(
            extract_features(code_line)
        ).reshape(1, -1)

        probability = self.model.predict_proba(features)[0][1]

        prediction = 1 if probability > 0.65 else 0

        return prediction, round(float(probability), 2)