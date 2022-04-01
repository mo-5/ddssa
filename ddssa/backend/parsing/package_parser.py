""" This module contains the PackageParser class"""

import pandas as pd
import requirements

from ddssa.backend.parsing.package_ids import PackageIds


class PackageParser:
    """PackageParser is an informal abstract class that will be
    implemented by the various package parsers. These methods
    will include specific logic to parse and return packages from
    a given package management file."""

    def __init__(self, filename):
        self._package_data = pd.DataFrame(index=["Name", "Version", "Mode"])
        self._filename = filename

    def parse_packages(self):
        """Parse packages from the file associated with this parser."""

    def basic_req_parse(self, i, req_string):
        """Parse requirement information from the syntax req==ver"""
        req = list(requirements.parse(req_string))[0]

        if len(req.specs) == 0:
            search_range = PackageIds.NO_VER
        elif len(req.specs) > 1:
            search_range = PackageIds.RANGE
        elif "~" in req.specs[0][0] or "*" in req.specs[0][1] and len(req.specs) == 1:
            search_range = PackageIds.RANGE
            req.specs = [
                (">=", req.specs[0][1]),
                (
                    "<",
                    req.specs[0][1].rsplit(".", 1)[0][:-1]
                    + (str(float(req.specs[0][1].rsplit(".", 1)[0][-1]) + 1)),
                ),
            ]
        elif ">" in req.specs[0][0] and len(req.specs) == 1:
            search_range = PackageIds.MAX
        elif "!" in req.specs[0][0] and len(req.specs) == 1:
            search_range = PackageIds.EXCLUDE
        else:
            search_range = PackageIds.SINGLE
        self._package_data[str(i)] = [req.name, req.specs, search_range]

    def get_data(self):
        """Return the collected package information"""
        return self._package_data

    def begin_analysis(self):
        """Call to begin parsing of a given file for package
        and to return the package information after parsing."""
        self.parse_packages()
        return self.get_data()
