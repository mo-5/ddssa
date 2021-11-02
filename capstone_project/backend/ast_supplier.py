import ast


class ASTSupplier:
    def __init__(self):
        self._node = None
        self._loops = ast.For, ast.While, ast.AsyncFor

    def create_ast_from_file(self, file):
        with open(file, "rb") as f:
            self._node = ast.parse(f.read())

    def get_ast_list(self):
        return self._node

    def get_loop_nodes_for_file(self):
        """ Return the loop nodes from the created AST that
        was generated for a specific file. Loop nodes are
        defined as while, for, and async for loops.
        """
        # TODO We should update this to only include top level loops,
        #      since if a loop contains another loop, we will already
        #      have it from the top-level node being added.
        nodes = ast.walk(self._node)
        loop_nodes = []
        for node in nodes:
            if isinstance(node, self._loops):
                loop_nodes.append(node)
        return loop_nodes

    def has_loop_nodes(self):
        """ Returns True if for, while, or async for loops are detected.
        """
        nodes = ast.walk(self._node)
        return any(isinstance(node, self._loops) for node in nodes)

    def _print_parsed_ast(self):
        """ Logging method to print the generated AST.
        """
        print(self._node.__dict__)

    def _print_unparsed_ast(self):
        """ Logging method to print the unparsed version of
        the generated AST.
        """
        print(ast.unparse(self._node))


if __name__ == '__main__':
    # Functionality demonstration. This class will not contain a
    # main method.
    ast_test = ASTSupplier()
    ast_test.create_ast_from_file("directory_parser.py")
    ast_test._print_unparsed_ast()
    ast_test._print_parsed_ast()
    print(ast_test.has_loop_nodes())
    file_loops = ast_test.get_loop_nodes_for_file()
    print(file_loops)
    for loop in file_loops:
        print(ast.unparse(loop))
