import pandas as pd


class PackageParser:
    """PackageParser is an informal abstract class that will be
    implemented by three different package parsers. These methods
    will include specific logic to parse and return packages from
    a given package management file."""

    def __init__(self, filename):
        self._package_data = pd.DataFrame(index=["Name", "Version", "Range"])
        self._filename = filename

    def parse_packages(self):
        pass

    def get_data(self):
        """Return the collected package information"""
        return self._package_data

    def begin_analysis(self):
        """Call to begin parsing of a given file for package
        and to return the package information after parsing."""
        self.parse_packages()
        self.get_data()
