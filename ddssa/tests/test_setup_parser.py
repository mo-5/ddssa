""" tests contains any unit tests for backend files
"""

import configparser
import os
import unittest

from ddssa.backend.parsing.package_ids import PackageIds
from ddssa.backend.parsing.setup_parser import SetupParser
from ddssa.tests.utils import Utils


class TestSetupParser(unittest.TestCase):
    """TestSetupParser is responsible for testing the setup.py
    and setup.cfg package parser."""

    def setUp(self):
        self._test_path = Utils().get_test_path()

    def test_setup_parser_cfg(self):
        """Test that the parser can extract all requirements from a
        properly-formatted setup.cfg file."""

        parser = SetupParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "setup_good",
                "setup.cfg",
            )
        )

        data = parser.begin_analysis()

        # Check to see all requirements were identified.
        size = data.shape[1]

        self.assertTrue(
            size == 3,
            f"Number of requirements identified was not correct. Expected 3 "
            f"but got {size}",
        )

        col_0 = data["0"].to_numpy()
        col_1 = data["1"].to_numpy()

        # Check to see if the first search range was correctly identified.
        search_range = col_0[2]
        self.assertTrue(
            search_range == PackageIds.NO_VER,
            f"The search range for the requirement was not correct. Expected "
            f"NO_VER but got {search_range}",
        )

        # Check to see if the first name was correctly identified.
        name = col_0[0]
        self.assertTrue(
            name == "docutils",
            f"The name for the requirement was not correct. Expected docutils "
            f"but got {name}",
        )

        # Check to see if the first version is empty.
        version = col_0[1]
        self.assertTrue(
            len(version) == 0,
            f"The number of version for the requirement was not correct. "
            f"Expected 0 but got {len(version)}.",
        )

        # Check to see if the second version is not empty.
        version = col_1[1]
        self.assertTrue(
            len(version) == 2,
            f"The number of version for the requirement was not correct. "
            f"Expected 2 but got {len(version)}.",
        )

    @unittest.skip(
        "Will overwrite setup.py file. Run when needed and revert changes "
        "once done. "
    )
    def test_setup_parser_py(self):
        """Test that the parser can extract all requirements from a
        properly-formatted setup.py file."""

        parser = SetupParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "setup_good",
                "setup.py",
            )
        )

        data = parser.begin_analysis()

        col_0 = data["0"].to_numpy()
        col_1 = data["1"].to_numpy()

        # Check to see if the first version is empty.
        version = col_0[1]
        self.assertTrue(
            len(version) == 0,
            f"The number of version for the requirement was not correct. "
            f"Expected 0 but got {len(version)}.",
        )

        # Check to see if the second version is not empty.
        version = col_1[1]
        self.assertTrue(
            len(version) == 2,
            f"The number of version for the requirement was not correct. "
            f"Expected 2 but got {len(version)}.",
        )

    def test_setup_parser_cfg_bad(self):
        """Test that the parser fails when trying to extract package
        information from an incorrectly formatted setup.py file."""

        parser = SetupParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "setup_bad",
                "setup.cfg",
            )
        )

        self.assertRaises(RuntimeError, parser.begin_analysis)

    def test_setup_parser_py_bad(self):
        """Test that the parser fails when trying to extract package
        information from an incorrectly formatted setup.py file."""

        parser = SetupParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "setup_bad",
                "setup.py",
            )
        )

        try:
            parser.begin_analysis()
            self.fail(
                "Analysis should not complete successfully for a file that "
                "contains malformed requirements."
            )
        except RuntimeError:
            pass
