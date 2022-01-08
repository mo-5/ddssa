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
            for i, req in enumerate(requirements.parse(f)):
                if len(req.specs) > 1:
                    search_range = PackageIds.RANGE
                elif (
                    "~" in req.specs[0][0]
                    or "*" in req.specs[0][1]
                    and len(req.specs) == 1
                ):
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
                else:
                    search_range = PackageIds.SINGLE
                self._package_data[str(i)] = [req.name, req.specs, search_range]
