"""This module contains the PoetryLockParser class"""

import tomli

from ddssa.backend.parsing.package_ids import PackageIds
from ddssa.backend.parsing.package_parser import PackageParser


class PoetryLockParser(PackageParser):
    """This class is responsible for parsing requirements from a
    poetry.lock file for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a poetry.lock file"""
        with open(self._filename, "rb") as f:
            try:
                toml_dict = tomli.load(f)
                for i, package in enumerate(toml_dict["package"]):
                    self._package_data[str(i)] = [
                        package["name"],
                        [("==", package["version"])],
                        PackageIds.SINGLE,
                    ]
            except tomli.TOMLDecodeError as e:
                raise RuntimeError("Poetry lockfile is invalid") from e
