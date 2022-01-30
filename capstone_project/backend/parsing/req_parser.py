import pkg_resources

from capstone_project.backend.parsing.package_parser import PackageParser


class RequirementsParser(PackageParser):
    """This class is responsible for parsing requirements from a
    requirements.txt file for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a
        requirements.txt file"""
        with open(self._filename, "r", encoding="UTF-8") as f:
            try:
                for i, req in enumerate(f.readlines()):
                    self.basic_req_parse(i, req)
            except pkg_resources.packaging.requirements.InvalidRequirement as e:
                raise RuntimeError(
                    "requirements.txt file contains an unknown requirement"
                ) from e
            except IndexError:
                raise RuntimeError("requirements.txt file is invalid") from e
