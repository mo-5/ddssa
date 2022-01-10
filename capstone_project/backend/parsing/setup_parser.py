import configparser
import os
import sys

import pkg_resources
import requirements
import setup_cfg_fmt
import setup_py_upgrade

from capstone_project.backend.parsing.package_ids import PackageIds
from capstone_project.backend.parsing.package_parser import PackageParser


class SetupParser(PackageParser):
    """This class is responsible for parsing requirements from
    setup.py and setup.cfg files for a provided Python project."""

    def parse_packages(self):
        """Parse out package information from a setup.cfg file. If
        a setup.py file is provided, convert it to a setup.cfg file
        and format it before parsing."""
        if self._filename.split(".")[-1] == "py":
            self._convert_to_cfg()

        # Format to a consistent format
        args = sys.argv
        args[0] = self._filename
        try:
            setup_cfg_fmt.main(args)
        except SystemExit:
            # Script exits on success, pass on it
            pass
        except configparser.ParsingError as e:
            # This is an actual error we need to handle
            raise RuntimeError("setup.cfg is not properly formatted") from e

        # Parse out the packages
        config = configparser.ConfigParser()
        config.read(self._filename)
        packages = config["options"]["install_requires"].strip().split("\n")

        try:
            for i, req in enumerate(packages):
                if "=" not in req:
                    # setup.cfg doesn't need to specify a version, we need to
                    # take that into account.
                    self._package_data[str(i)] = [req, "", PackageIds.NO_VER]
                else:
                    temp = list(requirements.parse(req))[0]
                    self.basic_req_parse(i, temp)
        except pkg_resources.packaging.requirements.InvalidRequirement as e:
            raise RuntimeError("setup.cfg file contains an unknown requirement") from e
        except IndexError:
            raise RuntimeError("setup.cfg file is invalid")

    def _convert_to_cfg(self):
        """Converts a setup.py file to a setup.cfg file"""
        # The script needs the directory, not the file itself
        args = sys.argv
        args[0] = self._filename.rsplit(os.sep, 1)[0]
        try:
            setup_py_upgrade.main(args)
        except SystemExit as e:
            raise RuntimeError("Unsupported header in setup.cfg") from e
        self._filename = self._filename.rsplit(".", 1)[0] + ".cfg"
