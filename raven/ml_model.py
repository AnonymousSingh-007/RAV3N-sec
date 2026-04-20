from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# tiny dataset (you will expand later)
samples = [
    ("eval(user_input)", 1),
    ("os.system(cmd)", 1),
    ("print('hello')", 0),
    ("x = 5 + 2", 0),
]

texts = [s[0] for s in samples]
labels = [s[1] for s in samples]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)


def predict(code_line):
    X_test = vectorizer.transform([code_line])
    pred = model.predict(X_test)[0]
    prob = model.predict_proba(X_test)[0][1]

    return pred, prob