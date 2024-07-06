"""This module contains the PipParser class"""

from dparse import parse, filetypes
from ddssa.backend.parsing.package_parser import PackageParser


class PipParser(PackageParser):
    """This class is responsible for parsing requirements from a
    Pipfile or Pipfile.lock file for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a Pipfile file or
        Pipfile.lock file."""

        # Determine which file type we are working with.
        if self._filename.rsplit(".", 1)[-1] == "lock":
            file_type = filetypes.pipfile_lock
        else:
            file_type = filetypes.pipfile

        # Parse out requirement strings and pass them along
        with open(self._filename, "r", encoding="UTF-8") as f:
            try:
                data = parse(f.read(), file_type)
            except Exception as e:
                raise RuntimeError(f"{file_type} is invalid.") from e
            for i, package in enumerate(data.dependencies):
                self.basic_req_parse(i, package.line.split(" ")[0])
