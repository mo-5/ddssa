import os


class PathParser:
    """PathParser provides utilities to obtain a list of Python
    and requirement files given a list of paths."""

    REQUIREMENT_FILE_NAMES = [
        "requirements.txt",
        "Pipfile",
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
    ]

    def __init__(self, paths):
        self._paths = paths
        self._python_files = []
        self._requirement_files = []
        self._process()

    def _process(self):
        valid_directories = [p for p in self._paths if os.path.isdir(p)]
        valid_files = [p for p in self._paths if os.path.isfile(p)]

        for directory in valid_directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".py"):
                        self._python_files.append(os.path.join(root, file))
                    elif file in PathParser.REQUIREMENT_FILE_NAMES:
                        self._requirement_files.append(os.path.join(root, file))

        for file in valid_files:
            if file.endswith(".py"):
                self._python_files.append(file)
            elif any(map(file.endswith, PathParser.REQUIREMENT_FILE_NAMES)):
                self._python_files.append(file)

        self._python_files.sort()
        self._requirement_files.sort()

    def get_python_file_list(self):
        return self._python_files

    def get_requirement_file_list(self):
        return self._requirement_files
