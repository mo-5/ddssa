import argparse

from capstone_project.backend.ast_supplier import ASTSupplier
from capstone_project.backend.path_parser import PathParser


class DDSSA:
    """ DDSSA (Data-Driven Software Security Assessment) is responsible
     for providing a command-line interface to analyze code with the
     tool. It accepts a list of paths,which may be directories or files.
     It then proceeds to perform the analysis on the Python code
     contained within those directories or files.
    """
    def __init__(self, paths):
        self._dir_parser = PathParser(paths)
        self._ast_supplier = ASTSupplier()

    def analyze(self):
        for file in self._dir_parser.get_file_list():
            self._ast_supplier.create_ast_from_file(file)
            # TODO replace this with real analysis
            self._ast_supplier._print_parsed_ast()


def main():
    parser = argparse.ArgumentParser(
        description="Command line options for the Data-Driven Software Security Assessment tool"
    )
    parser.add_argument(
        "-p",
        "--paths",
        nargs="+",
        help="The list of paths to be used to search for files to analyze. Must be directories or files.",
        required=True,
    )

    args = parser.parse_args()

    tool = DDSSA(args.paths)
    tool.analyze()

if __name__ == "__main__":
    main()
