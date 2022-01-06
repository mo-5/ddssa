import os

from capstone_project.backend.package_ids import PackageIds
from capstone_project.backend.package_parser import PackageParser


class RequirementsParser(PackageParser):
    """This class is responsible for parsing requirements from a
    requirements.txt file for a provided Python project."""

    def __init__(self, filename):
        super().__init__(filename)

    def parse_packages(self):
        """Parse out package information from a
        requirements.txt file"""
        with open(os.path.join(os.path.dirname(__file__), self._filename), "r") as file:
            for i, line in enumerate(file.readlines()):
                name = line.split(">")[0].split("~")[0].split("=")[0]
                version = [line.split("=")[-1].strip("=").strip()]
                if ">" in line:
                    search_range = PackageIds.MAX
                else:
                    search_range = PackageIds.SINGLE
                self._package_data[str(i)] = [name, version, search_range]

    def get_data(self):
        """Return the collected package information"""
        return self._package_data
