import unittest
import pandas as pd

from capstone_project.backend.file_generator.html_generator import HTMLGenerator
from capstone_project.backend.parsing.package_ids import PackageIds


class TestHTMLGenerator(unittest.TestCase):
    """Test the html generator to ensure that the html is being generated correctly."""

    def setUp(self):
        self.html = HTMLGenerator()

    def test_initial_html(self):
        """Test that the initial HTML is generated properly."""
        file = self.html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1>",
            file,
            "The initial html is not correct. Expected: "
            "<h1>Data-Driven Software Security Assessment Report</h1>"
            f"but got {file}",
        )

    def test_add_sr_data_with_list(self):
        """Test that the addition of one file with one sr statement includes a list in
        the html report."""
        self.html.add_sr_data([("ast_coordinator.py", [(26, "    print(loop)")])])
        file = self.html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Stall "
            "Statements</h2><div>File <b>ast_coordinator.py</b> contains 1 stall "
            "statement:</div><div><ol><li> Line number: 26, statement: print(loop)"
            "</li></ol></div>",
            file,
            "The generated html is not correct. Expected: "
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Stall "
            "Statements</h2><div>File <b>ast_coordinator.py</b> contains 1 stall "
            "statement:</div><div><ol><li> Line number: 26, statement: print(loop)"
            "</li></ol></div>"
            f"but got {file}",
        )

    def test_add_sr_data_with_list_multiple_items(self):
        """Test that the addition of multiples file with multiple sr statements
        includes a list in the html report."""
        self.html.add_sr_data(
            [
                ("ast_coordinator.py", [(26, "    print(loop)")]),
                ("ast_supplier.py", [(27, "print(loop)"), (28, "time.sleep(1)")]),
            ]
        )
        file = self.html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Stall "
            "Statements</h2><div>File <b>ast_coordinator.py</b> contains 1 stall "
            "statement:</div><div><ol><li> Line number: 26, statement: print(loop)"
            "</li></ol></div><div>File <b>ast_supplier.py</b> contains 2 stall "
            "statements:</div><div><ol><li> Line number: 27, statement: print(loop)"
            "</li><li> Line number: 28, statement: time.sleep(1)</li></ol></div>",
            file,
            "The generated html is not correct. Expected: "
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Stall "
            "Statements</h2><div>File <b>ast_coordinator.py</b> contains 1 stall "
            "statement:</div><div><ol><li> Line number: 26, statement: print(loop)"
            "</li></ol></div><div>File <b>ast_supplier.py</b> contains 2 stall "
            "statements:</div><div><ol><li> Line number: 27, statement: print(loop)"
            "</li><li> Line number: 28, statement: time.sleep(1)</li></ol></div>"
            f"but got {file}",
        )

    def test_add_dependency_vulnerability_data_without_vulnerabilities(self):
        """Test that not adding any vulnerabilities produces the correct html report."""
        vulnerability_data = pd.DataFrame(index=["Name", "Version", "CVEs", "Mode"])
        self.html.add_dependency_vulnerability_data(vulnerability_data)
        file = self.html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1>",
            file,
            f"The initial html is not correct. Expected <h1>Data-Driven Software"
            f"Security Assessment Report</h1>"
            f"but got {file}",
        )

    def test_add_dependency_vulnerability_data_with_single_dependency(self):
        """Test that a single dependency with vulnerabilities produces the correct html
        report."""
        vulnerability_data = pd.DataFrame(index=["Name", "Version", "CVEs", "Mode"])
        vulnerability_data["0"] = [
            "one",
            [("==", "1.1.1")],
            ["CVE-1", "CVE-2"],
            PackageIds.SINGLE,
        ]
        self.html.add_dependency_vulnerability_data(vulnerability_data)
        file = self.html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Dependency "
            "Vulnerabilities</h2><div><div>The following dependency has "
            "vulnerabilities:</div><ol><li>one == 1.1.1<ul>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-1>CVE-1</a></li>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-2>CVE-2</a></li>"
            "</ul></li></ol>",
            file,
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Dependency "
            "Vulnerabilities</h2><div><div>The following dependencies have "
            "vulnerabilities:</div><ol><li>one == 1.1.1<ul>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-1>CVE-1</a></li>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-2>CVE-2</a></li>"
            "</ul></li>"
            "<li>two >= 1.1, < 2.2<ul>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-3>CVE-3</a></li>"
            "</ul></li></ol>"
            f"but got {file}",
        )

    def test_add_dependency_vulnerability_data_with_multiple_dependencies(self):
        """Test that multiple dependencies with vulnerabilities produces the correct
        html report."""
        vulnerability_data = pd.DataFrame(index=["Name", "Version", "CVEs", "Mode"])
        vulnerability_data["0"] = [
            "one",
            [("==", "1.1.1")],
            ["CVE-1", "CVE-2"],
            PackageIds.SINGLE,
        ]
        vulnerability_data["1"] = [
            "two",
            [(">=", "1.1"), ("<", "2.2")],
            ["CVE-3"],
            PackageIds.SINGLE,
        ]
        self.html.add_dependency_vulnerability_data(vulnerability_data)
        file = self.html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Dependency "
            "Vulnerabilities</h2><div><div>The following dependencies have "
            "vulnerabilities:</div><ol><li>one == 1.1.1<ul>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-1>CVE-1</a></li>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-2>CVE-2</a></li>"
            "</ul></li>"
            "<li>two >= 1.1, < 2.2<ul>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-3>CVE-3</a></li>"
            "</ul></li></ol>",
            file,
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Dependency "
            "Vulnerabilities</h2><div><div>The following dependencies have "
            "vulnerabilities:</div><ol><li>one == 1.1.1<ul>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-1>CVE-1</a></li>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-2>CVE-2</a></li>"
            "</ul></li>"
            "<li>two >= 1.1, < 2.2<ul>"
            "<li><a href=https://nvd.nist.gov/vuln/detail/CVE-3>CVE-3</a></li>"
            "</ul></li></ol>"
            f"but got {file}",
        )
