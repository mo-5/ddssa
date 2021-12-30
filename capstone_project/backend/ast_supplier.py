import ast
from capstone_project.backend.pdf_generator import PDFGenerator
from capstone_project.backend.sr_calculator import SRCalculator


class ASTSupplier:
    def __init__(self):
        self._node = None
        self._loops = ast.For, ast.While, ast.AsyncFor
        self._sr_calculator = None

    def create_ast_from_file(self, file):
        with open(file, "rb") as f:
            # TODO  We need to preserve blank lines to keep accurate
            #       track of line numbers (AST parses them out).
            #       Comments are also ignored, so we need to somehow
            #       find a statement that is valid python that does
            #       nothing and is indented correctly to fix this.
            temp = f.read().splitlines()
            final = []
            for line in temp:
                if not line.decode().split():
                    line = b'#' # Wrong as AST parses this out as well.
                final.append(line)

            ast_bytes = b''
            for curr_byte in final:
                ast_bytes += curr_byte + b'\n'

            self._node = ast.parse(ast_bytes)

    def get_ast_list(self):
        return self._node

    def get_loop_nodes_for_file(self):
        """ Return the loop nodes from the created AST that
        was generated for a specific file. Loop nodes are
        defined as while, for, and async for loops.
        """
        nodes = ast.walk(self._node)
        loop_nodes = []
        for node in nodes:
            if isinstance(node, self._loops):
                loop_nodes.append(node)

        # Prune list to remove sub loops
        deletion_nodes = []
        for i in range(len(loop_nodes)):
            for j in range(len(loop_nodes)):
                if i >= len(loop_nodes):
                    break
                if i != j and ast.unparse(loop_nodes[j]).replace(" ", "") \
                        in ast.unparse(loop_nodes[i]).replace(" ", ""):
                    deletion_nodes.append(loop_nodes[j])
            for deleted in deletion_nodes:
                try:
                    loop_nodes.remove(deleted)
                except ValueError:
                    continue

        return loop_nodes

    def has_loop_nodes(self):
        """ Returns True if for, while, or async for loops are detected.
        """
        nodes = ast.walk(self._node)
        return any(isinstance(node, self._loops) for node in nodes)

    def sr_request(self, file, filename, pdf_file):
        """ Request for SR to be calculated. We employ this creation
        method to avoid needing to instantiate an SRCalculator unless
        we explicitly need it for analysis.
        """
        self.create_ast_from_file(file)
        nodes = self.get_loop_nodes_for_file()
        if self._sr_calculator is None:
            self._sr_calculator = SRCalculator(filename)
        else:
            self._sr_calculator.set_filename(filename)
        sr_data = self._sr_calculator.calculate_sr(nodes)
        pdf_file.add_sr_data(sr_data)

    def _print_parsed_ast(self):
        """ Logging method to print the generated AST.
        """
        print(self._node.__dict__)

    def _print_unparsed_ast(self):
        """ Logging method to print the unparsed version of
        the generated AST.
        """
        print(ast.unparse(self._node))
