import ast


class ASTSupplier:
    def __init__(self):
        self._content = []

    def create_ast_from_file(self, files):
        for file in files:
            with open(file, "rb") as f:
                self._content.append(ast.parse(f.read()))

    def print_parsed_ast(self):
        for content in self._content:
            print(ast.unparse(content))

    def get_ast_list(self):
        return self._content
