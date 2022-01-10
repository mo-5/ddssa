import pkg_resources
import requirements

from capstone_project.backend.parsing.package_ids import PackageIds
from capstone_project.backend.parsing.package_parser import PackageParser


class RequirementsParser(PackageParser):
    """This class is responsible for parsing requirements from a
    requirements.txt file for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a
        requirements.txt file"""
        with open(self._filename, "r") as f:
            try:
                for i, req in enumerate(requirements.parse(f)):
                    if len(req.specs) == 0:
                        self._package_data[str(i)] = [
                            req, "", PackageIds.NO_VER]
                    else:
                        self.basic_req_parse(i, req)
            except pkg_resources.packaging.requirements.InvalidRequirement as e:
                raise RuntimeError(
                    "requirements.txt file contains an unknown requirement"
                ) from e
            except IndexError:
                raise RuntimeError("requirements.txt file is invalid")
