""" tests contains any unit tests for backend files
"""
import os
import unittest

from capstone_project.backend.parsing.package_ids import PackageIds
from capstone_project.backend.parsing.req_parser import RequirementsParser
from capstone_project.tests.test_utils import TestUtils


class TestReqParser(unittest.TestCase):
    """TestReqParser is responsible for testing the requirements.txt
    package parser."""

    def setUp(self):
        self._test_path = TestUtils().get_test_path()

    def test_req_parser(self):
        """Test a typical requirements.txt file to ensure all packages,
        versions, and search ranges are correctly identified.
        """
        req_parser = RequirementsParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "requirements",
                "requirements.txt",
            )
        )

        data = req_parser.begin_analysis()

        # Check to see all requirements were identified.
        size = data.shape[1]
        self.assertTrue(
            size == 12,
            f"Number of requirements identified was not correct. Expected 12 "
            f"but got {size}",
        )

        col_0 = data["0"].to_numpy()

        # Check to see if the first search range was correctly identified.
        search_range = col_0[2]
        self.assertTrue(
            search_range == PackageIds.MAX,
            f"The search range for the requirement was not correct. Expected "
            f"MAX but got {search_range}",
        )

        # Check to see if the first name was correctly identified.
        name = col_0[0]
        self.assertTrue(
            name == "psutil",
            f"The name for the requirement was not correct. Expected psutil "
            f"but got {name}",
        )

        # Check to see if the first version was correctly identified.
        version = col_0[1]
        self.assertTrue(
            version[0] == (">=", "5.7.0"),
            f"The version for the requirement was not correct. "
            f'Expected (">=", "5.7.0") but got {version}.',
        )

        # Check to see that the size of the versions array in a requirement
        # with a RANGE is 2.
        self.assertTrue(
            len(version[0]) == 2,
            f"The number of versions for the requirement was not correct. "
            f"Expected 2 but got {len(version[0])}.",
        )

        # Check to see if each range is identified correctly.
        search_range = data["1"].to_numpy()[2]
        self.assertTrue(
            search_range == PackageIds.SINGLE,
            f"The search range for the requirement was not correct. Expected "
            f"SINGLE but got {search_range}",
        )

        search_range = data["10"].to_numpy()[2]
        self.assertTrue(
            search_range == PackageIds.RANGE,
            f"The search range for the requirement was not correct. Expected "
            f"RANGE but got {search_range}",
        )

        # Check to see that compatible versions are correctly changed to be
        # a range between PEP defined compatible package versions
        version = data["9"].to_numpy()[1]
        self.assertTrue(
            len(version[0]) == 2,
            f"The number of versions for the compatible requirement was not correct. "
            f"Expected 2 but got {len(version[0])}.",
        )

        # Check to see that wildcard versions are correctly changed to be
        # a range between PEP defined compatible package versions
        version = data["8"].to_numpy()[1]
        self.assertTrue(
            len(version[0]) == 2,
            f"The number of versions for the wildcard requirement was not correct. "
            f"Expected 2 but got {len(version[0])}.",
        )

    def test_req_parser_no_req(self):
        """Test a malformed requirements.txt file to ensure an error is
        thrown such that is can be caught during actual analysis.
        """
        req_parser = RequirementsParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "requirements",
                "bad_requirements.txt",
            )
        )

        try:
            req_parser.begin_analysis()
            self.fail(
                "Analysis should not complete successfully for a file that "
                "does not contain any requirements."
            )
        except RuntimeError:
            pass

    def test_req_parser_bad_req(self):
        """Test a malformed requirements.txt file to ensure an error is
        thrown such that is can be caught during actual analysis.
        """
        req_parser = RequirementsParser(
            os.path.join(
                self._test_path,
                "package_test_files",
                "requirements",
                "bad_requirements_2.txt",
            )
        )

        try:
            req_parser.begin_analysis()
            self.fail(
                "Analysis should not complete successfully for a file that "
                "contains malformed requirements."
            )
        except RuntimeError:
            pass
