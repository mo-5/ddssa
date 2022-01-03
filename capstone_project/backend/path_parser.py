import os


class PathParser:
    """PathParser provides utilities to obtain a list of Python files
    given a list of paths.
    """

    def __init__(self, paths):
        self._paths = paths

    def get_file_list(self):
        valid_directories = [p for p in self._paths if os.path.isdir(p)]
        valid_files = [p for p in self._paths if os.path.isfile(p)]
        file_list = []

        for directory in valid_directories:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith(".py"):
                        file_list.append(os.path.join(root, file))
        for file in valid_files:
            if file.endswith(".py"):
                file_list.append(file)

        file_list.sort()
        return file_list
