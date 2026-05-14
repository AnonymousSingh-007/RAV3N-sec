# train.py

from raven.models import RavenModel

samples = [

    # Vulnerable
    ("eval(user_input)", 1),
    ("exec(code)", 1),
    ("os.system(cmd)", 1),
    ("subprocess.call(cmd, shell=True)", 1),
    ("pickle.load(file)", 1),
    ("yaml.load(data)", 1),
    ("SELECT * FROM users + input()", 1),
    ("password='admin123'", 1),
    ("requests.get(url, verify=False)", 1),
    ("hashlib.md5(password)", 1),
    ("tempfile.mktemp()", 1),
    ("input()", 1),

    # Safe
    ("print('hello world')", 0),
    ("x = 5 + 2", 0),
    ("safe_function()", 0),
    ("json.loads(data)", 0),
    ("for i in range(10): pass", 0),
    ("hashlib.sha256(data)", 0),
    ("requests.get(url)", 0),
]

model = RavenModel()

model.train(samples)