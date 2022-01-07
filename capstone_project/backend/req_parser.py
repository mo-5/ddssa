import requirements

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

    def get_data(self):
        """Return the collected package information"""
        return self._package_data


if __name__ == "__main__":
    rp = RequirementsParser("../tests/package_test_files/requirements.txt")
    rp.begin_analysis()