"""This module contains the DDSSA class and a main method"""


import argparse
import concurrent.futures
import os
import sys
from pathlib import Path

import numpy as np

from ddssa.backend.cst.cst_supplier import CSTSupplier
from ddssa.backend.file_generator.html_generator import HTMLGenerator
from ddssa.backend.parsing.package_supplier import PackageSupplier
from ddssa.backend.parsing.path_parser import PathParser

# Needed to add the capstone_project module to the system path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")))


class DDSSA:
    """DDSSA (Data-Driven Software Security Assessment) is responsible
    for providing a command-line interface to analyze code with the
    tool. It accepts a list of paths,which may be directories or files.
    It then proceeds to perform the analysis on the Python code
    contained within those directories or files.
    """

    def __init__(self, paths, api_key=None) -> None:
        self._dir_parser = PathParser(paths)
        self._ast_supplier = CSTSupplier()
        self._package_supplier = PackageSupplier(api_key)

    def analyze(self) -> str:
        """Perform both static and dependency vulnerability analysis on a
        target directory. Once analysis concludes, return the HTML to be
        displayed on the frontend to the user.
        """

        html_file = HTMLGenerator()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_sr = executor.submit(self._static_analysis)
            future_vul = executor.submit(self._vulnerability_analysis)
            concurrent.futures.wait([future_sr, future_vul])

        sr_data = future_sr.result()
        vul_data = future_vul.result()

        if len(sr_data) > 0:
            html_file.add_sr_data([sr_detection for sr_detection in sr_data])
        if vul_data is not None:
            html_file.add_dependency_vulnerability_data(vul_data)

        return html_file.get_html()

    def _vulnerability_analysis(self):
        # Add dependency vulnerability data
        req_list = self._dir_parser.get_requirement_file_list()
        if req_list:
            return self._package_supplier.package_request(req_list)
        else:
            return None

    def _static_analysis(self):
        sr_data = []
        arr = np.array(self._dir_parser.get_python_file_list())
        files = np.array_split(arr, 5)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(
                self._ast_supplier.sr_request, f) for f in files]

        results = [f.result() for f in futures]
        for r in results:
            for sr in r:
                if len(sr[1]) > 0:
                    sr_data.append((sr[0][-1], sr[1]))

        # Add SR analysis data, filtering out files without stall statements
        return sr_data


def main():
    """Provide a command line interface to the Data-Driven Software Security
    Assessment Tool."""

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
    parser.add_argument(
        "-o",
        "--output-path",
        help="Output path for the generated report. Can be a relative or absolute path to a file.",
        required=True,
    )

    args = parser.parse_args()

    output_path = Path(args.output_path)

    # Validate arguments
    if output_path.exists():
        parser.error(
            "Output file for the report already exists, please choose a different file."
        )

    # Run the analysis
    html = DDSSA(args.paths, args.api_key).analyze()

    # Output the report
    try:
        output_path.write_text(html)
    except FileNotFoundError as e:
        raise RuntimeError(
            f"The specified output path {output_path.resolve()} is invalid."
        ) from e


if __name__ == "__main__":
    main()
