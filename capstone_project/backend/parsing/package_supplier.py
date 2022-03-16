""" This module contains the PackageSupplier class"""
from capstone_project.backend.api.vulnerability_aggregator import VulnerabilityAggregator
from capstone_project.backend.parsing.pip_parser import PipParser
from capstone_project.backend.parsing.poetry_lock_parser import PoetryLockParser
from capstone_project.backend.parsing.pyproject_parser import PyProjectParser
from capstone_project.backend.parsing.req_parser import RequirementsParser
from capstone_project.backend.parsing.setup_parser import SetupParser


class PackageSupplier:
    """PackageSupplier is responsible for supplying package files
    to the correct package dependency parser based on the package
    file that has been requested to be analyzed.
    """

    def __init__(self, api_key):
        self._package_parser = None
        self._package_data = None
        self._vul_api = VulnerabilityAggregator(api_key)

    def package_request(self, path):
        """Handle a package request"""

        # Pass it to the appropriate parser
        if path[-7:] == "Pipfile" or path[-12:] == "Pipfile.lock":
            self._package_parser = PipParser(path)
        elif path[-16:] == "requirements.txt":
            self._package_parser = RequirementsParser(path)
        elif path[-14:] == "pyproject.toml":
            self._package_parser = PyProjectParser(path)
        elif path[-8:] == "setup.py" or path[-9:] == "setup.cfg":
            self._package_parser = SetupParser(path)
        elif path[-11:] == "poetry.lock":
            self._package_parser = PoetryLockParser(path)

        # Analyze for dependencies and built out the data frame
        self._package_data = self._package_parser.begin_analysis()

        # Build out a new dataframe from the returned query results
        return self._vul_api.coordinate_queries(self._package_parser.begin_analysis())
