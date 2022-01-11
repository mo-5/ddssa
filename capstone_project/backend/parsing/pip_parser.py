import requirements

from capstone_project.backend.parsing.package_ids import PackageIds
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
                print(len(data.dependencies))
            except Exception:
                raise RuntimeError(f"{file_type} is invalid.")
            for i, package in enumerate(data.dependencies):
                if "=" not in str(package.specs):
                    # Account for the possible lack of a version identifier
                    self._package_data[str(i)] = [package.name, "", PackageIds.NO_VER]
                else:
                    # Ignore hashes with split
                    self.basic_req_parse(
                        i, list(requirements.parse(package.line.split(" ")[0]))[0]
                    )
