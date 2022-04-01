"""This module contains the TestPoetryLockParser test class"""


import os
import unittest

from ddssa.tests.test_utils import TestUtils
from ddssa.backend.parsing.package_ids import PackageIds
from ddssa.backend.parsing.poetry_lock_parser import PoetryLockParser


class TestPoetryLockParser(unittest.TestCase):
    """TestPoetryLockParser is responsible for testing the poetry.lock package
    parser."""

    def setUp(self):
        self._test_path = TestUtils().get_test_path()

    def test_poetry_lock_parser(self):
        """Test that the parser can extract all requirements from a properly-formatted
        lockfile."""
        parser = PoetryLockParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "poetry",
                "valid.poetry.lock",
            )
        )

        data = parser.begin_analysis()

        # Test that the correct number of requirements were extracted
        size = data.shape[1]
        self.assertEqual(
            31,
            size,
            f"Number of requirements identified was not correct. Expected 31 "
            f"but got {size}",
        )

        # Test that the first requirement is the expected one
        requirement = data["0"].to_numpy()
        name = requirement[0]
        version = requirement[1]
        search_range = requirement[2]
        self.assertEqual(
            "astroid",
            name,
            f"The name for the requirement was not correct. Expected astroid "
            f"but got {name}",
        )
        self.assertEqual(
            ("==", "2.9.2"),
            version[0],
            f"The version for the requirement was not correct. "
            f'Expected ("==", "2.9.2") but got {version}.',
        )
        self.assertEqual(
            PackageIds.SINGLE,
            search_range,
            f"The search range for the requirement was not correct. Expected "
            f"SINGLE but got {search_range}",
        )

        # Test that the last requirement is the expected one
        requirement = data["30"].to_numpy()
        name = requirement[0]
        version = requirement[1]
        search_range = requirement[2]
        self.assertEqual(
            "wrapt",
            name,
            f"The name for the requirement was not correct. Expected wrapt "
            f"but got {name}",
        )
        self.assertEqual(
            ("==", "1.13.3"),
            version[0],
            f"The version for the requirement was not correct. "
            f'Expected ("==", "1.13.3") but got {version}.',
        )
        self.assertEqual(
            PackageIds.SINGLE,
            search_range,
            f"The search range for the requirement was not correct. Expected "
            f"SINGLE but got {search_range}",
        )

    def test_poetry_lock_parser_bad_req(self):
        """Test that a malformed lockfile causes an error to be raised during
        parsing."""
        parser = PoetryLockParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "poetry",
                "invalid.poetry.lock",
            )
        )

        try:
            parser.begin_analysis()
            self.fail(
                "Analysis should not complete successfully for a malformed lockfile."
            )
        except RuntimeError as e:
            self.assertEqual("Poetry lockfile is invalid", str(e))
