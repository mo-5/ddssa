import argparse
import os
import sys
import threading

from capstone_project.backend.ast.ast_supplier import ASTSupplier
from capstone_project.backend.file_generator.html_generator import HTMLGenerator
from capstone_project.backend.parsing.package_supplier import PackageSupplier
from capstone_project.backend.parsing.path_parser import PathParser

# Needed to add the capstone_project module to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


class DDSSA:
    """DDSSA (Data-Driven Software Security Assessment) is responsible
    for providing a command-line interface to analyze code with the
    tool. It accepts a list of paths,which may be directories or files.
    It then proceeds to perform the analysis on the Python code
    contained within those directories or files.
    """

    def __init__(self, paths, api_key=None):
        self._dir_parser = PathParser(paths)
        self._ast_supplier = ASTSupplier()
        self._package_supplier = PackageSupplier(api_key)

    def analyze(self):
        """Perform both static and dependency vulnerability analysis on a
        target directory. Once analysis concludes, return the HTML to be
        displayed on the frontend to the user.
        """
        html_file = HTMLGenerator()

        sr_thread = threading.Thread(target=self._static_analysis(html_file))
        vul_thread = threading.Thread(target=self._vulnerability_analysis(html_file))
        sr_thread.start()
        vul_thread.start()
        sr_thread.join()
        vul_thread.join()

        html = html_file.get_html()
        return html

    def _vulnerability_analysis(self, html_file):
        # Add dependency vulnerability data
        html_file.add_dependency_vulnerability_data(
            self._package_supplier.package_request(
                self._dir_parser.get_requirement_file_list()[-1]
            )
        )

    def _static_analysis(self, html_file):
        sr_data = []
        for file in self._dir_parser.get_python_file_list():
            sr_data.append(
                self._ast_supplier.sr_request(file, file.split(os.path.sep)[-1])
            )
        # Add SR analysis data, filtering out files without stall statements
        html_file.add_sr_data(
            [sr_detection for sr_detection in sr_data if len(sr_detection[1]) > 0]
        )


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
    parser.add_argument(
        "-k",
        "--api-key",
        help="The NIST NVD API key. Optional.",
    )

    args = parser.parse_args()

    tool = DDSSA(args.paths, args.api_key)
    tool.analyze()


if __name__ == "__main__":
    main()
