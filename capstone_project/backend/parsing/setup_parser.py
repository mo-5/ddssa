from capstone_project.backend.parsing.package_parser import PackageParser


class SetupParser(PackageParser):
    """This class is responsible for parsing requirements from
    setup.py and setup.cfg files for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a setup.cfg file. If
        a setup.py file is provided, convert it to a setup.cfg file
        and format it before parsing."""
        pass
