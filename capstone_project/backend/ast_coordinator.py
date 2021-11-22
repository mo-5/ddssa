import ast

from capstone_project.backend.ast_supplier import ASTSupplier


class ASTCoordinator:
    """ ASTCoordinator is responsible for passing individual files
    retrieved by the directory parser and then passing them on to
    ASTSupplier. The goal is to spawn multiple threads each controlling
    an ASTSupplier to improve static analysis for larger systems.
    """
    def __init__(self):
        # TODO Redo this class and introduce multi-threading
        self._ast_suppliers = None

    def perform_static_analysis(self, files):
        # Determine how many threads to create
        self._create_ast_suppliers()

        # Pass files to the spawned ASTSuppliers.
        for file in files:
            self._ast_suppliers.create_ast_from_file(file)
            loops = ast.unparse(self._ast_suppliers.get_loop_nodes_for_file())
            for loop in loops:
                print(loop)

    def _create_ast_suppliers(self):
        self._ast_suppliers = ASTSupplier()
