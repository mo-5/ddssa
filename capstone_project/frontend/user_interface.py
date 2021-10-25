from capstone_project.backend.ast_supplier import ASTSupplier
from capstone_project.backend.directory_parser import DirectoryParser


class _UserInterface:
    def __init__(self):
        self._dir_parse = DirectoryParser()
        self._ast_supplier = ASTSupplier()
        self._welcome = "Data-Driven Software Security Assessment"

        print(self._welcome)
        self._path = input("Please supply a path for analysis: ")

    def analyze(self):
        self._ast_supplier.create_ast_from_file(
            self._dir_parse.get_file_list(self._path))
        self._ast_supplier.print_parsed_ast()


if __name__ == '__main__':
    ui = _UserInterface()
    ui.analyze()
