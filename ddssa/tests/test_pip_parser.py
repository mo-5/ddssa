""" tests contains any unit tests for backend files
"""

import os
import unittest

from ddssa.backend.parsing.package_ids import PackageIds
from ddssa.backend.parsing.pip_parser import PipParser
from ddssa.tests.utils import Utils


class TestPipParser(unittest.TestCase):
    """TestSetupParser is responsible for testing the Pipfile
    and Pipfile.lock package parser."""

    def setUp(self):
        self._test_path = Utils().get_test_path()

    def test_pipfile_parser(self):
        """Test that the parser can extract all requirements from a
        properly-formatted Pipfile file."""

        parser = PipParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "pipfile",
                "Pipfile",
            )
        )

        data = parser.begin_analysis()

        # Check to see all requirements were identified.
        size = data.shape[1]

        self.assertTrue(
            size == 4,
            f"Number of requirements identified was not correct. Expected 4 "
            f"but got {size}",
        )

        # Check that the first requirement is identified as SINGLE
        search_range = data["0"].to_numpy()[2]
        self.assertTrue(
            search_range == PackageIds.SINGLE,
            f"The search range for the requirement was not correct. Expected "
            f"SINGLE but got {search_range}",
        )

        # Check that the second requirement is identified as NO_VER
        search_range = data["1"].to_numpy()[2]
        self.assertTrue(
            search_range == PackageIds.NO_VER,
            f"The search range for the requirement was not correct. Expected "
            f"NO_VER but got {search_range}",
        )

    def test_pipfile_parser_bad(self):
        """Test that the parser identifies no requirements out of
        an improperly formatted Pipfile file."""

        parser = PipParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "pipfile",
                "Pipfile_bad",
            )
        )

        data = parser.begin_analysis()

        # Check to see no requirements were identified.
        size = data.shape[1]

        self.assertTrue(
            size == 0,
            f"Number of requirements identified was not correct. Expected 0 "
            f"but got {size}",
        )

    def test_pipfile_lock_parser_bad(self):
        """Test that the parser identifies no requirements out of
        an improperly formatted Pipfile.lock file."""

        parser = PipParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "pipfile",
                "Pipfile_bad.lock",
            )
        )

        data = parser.begin_analysis()

        # Check to see no requirements were identified.
        size = data.shape[1]

        self.assertTrue(
            size == 0,
            f"Number of requirements identified was not correct. Expected 0 "
            f"but got {size}",
        )
