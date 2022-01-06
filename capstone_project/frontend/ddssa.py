import argparse
import os
import sys
from capstone_project.backend.path_parser import PathParser
from capstone_project.backend.ast_supplier import ASTSupplier
from capstone_project.backend.pdf_generator import PDFGenerator


# Needed to add the capstone_project module to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class DDSSA:
    """DDSSA (Data-Driven Software Security Assessment) is responsible
    for providing a command-line interface to analyze code with the
    tool. It accepts a list of paths,which may be directories or files.
    It then proceeds to perform the analysis on the Python code
    contained within those directories or files.
    """

    def __init__(self, paths):
        self._dir_parser = PathParser(paths)
        self._ast_supplier = ASTSupplier()

    def analyze(self):
        pdf_file = PDFGenerator()
        pdf_file.add_header("Stall Statements:")
        for file in self._dir_parser.get_file_list():
            self._ast_supplier.sr_request(file, file.split(os.path.sep)[-1], pdf_file)
        pdf_file.save_pdf("report.pdf")


def main():
    parser = argparse.ArgumentParser(
        description="Command line options for the Data-Driven Software "
        "Security Assessment tool"
    )
    parser.add_argument(
        "-p",
        "--paths",
        nargs="+",
        help="The list of paths to be used to search for files to "
        "analyze. Must be directories or files.",
        required=True,
    )

    args = parser.parse_args()

    tool = DDSSA(args.paths)
    tool.analyze()


if __name__ == "__main__":
    main()
