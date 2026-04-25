import os

# default ignore folders
DEFAULT_IGNORES = {
    ".git",
    "venv",
    ".venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode"
}


def get_python_files(path, ignore_dirs=None):
    if ignore_dirs is None:
        ignore_dirs = DEFAULT_IGNORES

    python_files = []

    for root, dirs, files in os.walk(path):
        # remove ignored dirs in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    return python_files