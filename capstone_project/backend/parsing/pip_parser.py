from capstone_project.backend.parsing.package_parser import PackageParser
from dparse import parse, filetypes


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
        with open(self._filename, "r") as f:
            try:
                data = parse(f.read(), file_type)
            except Exception:
                raise RuntimeError(f"{file_type} is invalid.")
            for i, package in enumerate(data.dependencies):
                self.basic_req_parse(i, package.line.split(" ")[0])
