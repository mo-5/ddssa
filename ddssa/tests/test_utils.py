""" tests contains any unit tests for backend files
"""
import os


class TestUtils:
    """This class contains common resources that appear across unit tests"""

    def __init__(self):
        self._test_path = os.path.join(os.getcwd(), "capstone_project", "tests")

    def get_test_path(self):
        """Get the path to the test directory in the running context"""
        return self._test_path
