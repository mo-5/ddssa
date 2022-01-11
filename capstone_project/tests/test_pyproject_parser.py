import os
import unittest

from capstone_project.tests.test_utils import TestUtils
from capstone_project.backend.parsing.package_ids import PackageIds
from capstone_project.backend.parsing.pyproject_parser import PyprojectParser


class TestPyprojectParser(unittest.TestCase):
    """TestPyprojectParser is responsible for testing the pyproject.toml package
    parser."""

    def setUp(self):
        self._test_path = TestUtils().get_test_path()

    def test_pyproject_parser(self):
        """Test that the parser can extract all requirements from a properly-formatted
        pyproject.toml file."""
        parser = PyprojectParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "pyproject",
                "valid.pyproject.toml",
            )
        )

        data = parser.begin_analysis()

        # Test that the correct number of requirements were extracted
        size = data.shape[1]
        self.assertEqual(
            5,
            size,
            f"Number of requirements identified was not correct. Expected 5 "
            f"but got {size}",
        )

        # Test that the first requirement is the expected one
        requirement = data["0"].to_numpy()
        name = requirement[0]
        version = requirement[1]
        search_range = requirement[2]
        self.assertEqual(
            "setuptools",
            name,
            f"The name for the requirement was not correct. Expected setuptools "
            f"but got {name}",
        )
        self.assertEqual(
            (">=", "40.6.0"),
            version[0],
            f"The version for the requirement was not correct. "
            f'Expected (">=", "40.6.0") but got {version}.',
        )
        self.assertEqual(
            PackageIds.MAX,
            search_range,
            f"The search range for the requirement was not correct. Expected "
            f"MAX but got {search_range}",
        )

        # Test that the last requirement is the expected one
        requirement = data["4"].to_numpy()
        name = requirement[0]
        version = requirement[1]
        search_range = requirement[2]
        self.assertEqual(
            "other",
            name,
            f"The name for the requirement was not correct. Expected other "
            f"but got {name}",
        )
        self.assertEqual(
            (">=", "1.0.0"),
            version[0],
            f"The version for the requirement was not correct. "
            f'Expected (">=", "1.0.0") but got {version}.',
        )
        self.assertEqual(
            ("<", "1.1.0"),
            version[1],
            f"The version for the requirement was not correct. "
            f'Expected ("<", "1.1.0") but got {version}.',
        )
        self.assertEqual(
            PackageIds.RANGE,
            search_range,
            f"The search range for the requirement was not correct. Expected "
            f"RANGE but got {search_range}",
        )

    def test_pyproject_parser_bad_req_1(self):
        """Test that a malformed pyproject.toml file causes an error to be raised
        during parsing."""
        parser = PyprojectParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "pyproject",
                "invalid_1.pyproject.toml",
            )
        )

        try:
            parser.begin_analysis()
            self.fail(
                "Analysis should not complete successfully for a malformed "
                "pyproject.toml file."
            )
        except RuntimeError as e:
            self.assertEqual("pyproject file is invalid", str(e))

    def test_pyproject_parser_bad_req_2(self):
        """Test that a malformed pyproject.toml file causes an error to be raised
        during parsing."""
        parser = PyprojectParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "pyproject",
                "invalid_2.pyproject.toml",
            )
        )

        try:
            parser.begin_analysis()
            self.fail(
                "Analysis should not complete successfully for a malformed "
                "pyproject.toml file."
            )
        except RuntimeError as e:
            self.assertEqual("pyproject file is invalid", str(e))
