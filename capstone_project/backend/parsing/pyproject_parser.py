import tomli

from capstone_project.backend.parsing.package_parser import PackageParser


class PyprojectParser(PackageParser):
    """This class is responsible for parsing requirements from a
    pyproject.toml file for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a pyproject.toml file"""
        with open(self._filename, "rb") as f:
            try:
                toml_dict = tomli.load(f)
                packages = toml_dict["build-system"]["requires"]

                # Ensure the structure containing the requirements is as expected
                if not isinstance(packages, list):
                    raise RuntimeError("pyproject file is invalid")

                for i, req in enumerate(packages):
                    self.basic_req_parse(i, req)
            except (tomli.TOMLDecodeError, KeyError) as e:
                raise RuntimeError("pyproject file is invalid") from e
