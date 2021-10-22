import os

class DirectoryParser:
    def __init__(self):
        self.file_list = []        

    def get_file_list(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    self.file_list.append(os.path.join(root, file))
        self.file_list.sort()
        return self.file_list

    def get_list(self):
        return self.file_list

