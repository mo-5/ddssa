import unittest
from capstone_project.backend.file_generator.html_generator import HTMLGenerator


class TestHTMLGenerator(unittest.TestCase):
    """Test the html generator to ensure that the html is being generated."""

    def test_initial_html(self):
        html = HTMLGenerator()
        file = html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Stall Statements:</h2>",
            file,
            f"The initial html is not correct. Expected <h1>Data-Driven Software Security Assessment "
            f"Report</h1><h2>Stall Statements:</h2> "
            f"but got {file}",
        )

    def test_add_sr_data_with_list(self):
        """Test the addition of sr statements that includes a list to the html report."""
        html = HTMLGenerator()
        html.add_sr_data(("ast_coordinator.py", [(26, "    print(loop)")]))
        file = html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Stall Statements:</h2><div>File: "
            "ast_coordinator.py contains: 1 stall statements</div><div><div>The following statements are stall "
            "statements:</div><ol><li> Line number: 26, statement: print(loop)</li></ol></div>",
            file,
            f"The initial html is not correct. Expected: <h1>Data-Driven Software Security Assessment "
            f"Report</h1><h2>Stall Statements:</h2><div>File: ast_coordinator.py contains: 1 stall "
            f"statements</div><div><div>The following statements are stallstatements:</div><ol><li> Line number: 26, "
            f"statement: print(loop)</li></ol></div> "
            f"but got {file}",
        )

    def test_add_sr_data_without_list(self):
        """Test the addition of sr statements that doesnot include a list to the html report."""
        html = HTMLGenerator()
        html.add_sr_data(("ast_coordinator.py", []))
        file = html.get_html()
        self.assertEqual(
            "<h1>Data-Driven Software Security Assessment Report</h1><h2>Stall Statements:</h2><div>File: "
            "ast_coordinator.py contains: 0 stall statements</div>",
            file,
            f"The addition was not correct. Expected: <h1>Data-Driven Software Security Assessment "
            f"Report</h1><h2>Stall Statements:</h2><div>File: "
            f"ast_coordinator.py contains: 0 stall statements</div>"
            f"but got {file}",
        )
