from capstone_project.backend.parsing.package_parser import PackageParser
from dparse import parse, filetypes


class PipParser(PackageParser):
    """This class is responsible for parsing requirements from a
    Pipfile or Pipfile.lock file for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a Pipfile file or
        Pipfile.lock file."""
        pass
