""" tests contains any unit tests for backend files
"""

import os
import unittest

from ddssa.backend.cst.cst_supplier import CSTSupplier
from ddssa.backend.metrics.sr_calculator import SRCalculator
from ddssa.tests.utils import Utils


class TestSR(unittest.TestCase):
    """TestSR is responsible for ensuring the correct functionality
    of Stall Ratio calculations and returned objects.
    """

    def setUp(self):
        # Clear object instance for each test
        self._test_path = Utils().get_test_path()
        self._calculator = SRCalculator("test_file"), CSTSupplier()

    def test_sr_logic_simple(self):
        """Test a simple SR example file to ensure all pattern
        matching stall occurrences are caught by SRCalculator
        """
        test_calc, cst_supp = self._calculator

        # Case 1: Simple examples only
        cst_supp.create_ast_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_simple.py",
            )
        )
        test_calc.set_filename("sr_simple.py")
        cst_supp.get_libcst_module_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_simple.py",
            )
        )
        nodes = test_calc.calculate_sr(
            cst_supp.get_loop_nodes_for_file(), cst_supp._libcst_module
        )
        self.assertTrue(
            nodes[0] == "sr_simple.py",
            "File name did not match what was expected.",
        )
        self.assertTrue(
            len(nodes[1]) == 3,
            "Returned detections list was empty when it " "should be of size 3",
        )
        self.assertTrue(
            nodes[1][0][0] == 12,
            "Line number of first match did" " not match what was expected.",
        )
        # Specifically check if blank lines are being preserved in
        # the line numbering (currently failing due to known issue).
        self.assertTrue(
            nodes[1][1][0] == 14,
            "Line number of next match did" " not match what was expected.",
        )

    def test_sr_logic_complex(self):
        """Test a complex SR example file to ensure all pattern
        matching stall occurrences and frivolous operations are
        caught by SRCalculator.
        """
        test_calc, cst_supp = self._calculator

        # Case 2: Complex example
        cst_supp.create_ast_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_advanced.py",
            )
        )
        test_calc.set_filename("sr_advanced.py")
        cst_supp.get_libcst_module_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_advanced.py",
            )
        )
        nodes = test_calc.calculate_sr(
            cst_supp.get_loop_nodes_for_file(), cst_supp._libcst_module
        )

        self.assertTrue(
            nodes[0] == "sr_advanced.py",
            "File name did not match what was expected.",
        )
        self.assertTrue(
            nodes[1][0][0] == 16,
            "Line number of first match did" " not match what was expected.",
        )
        # Check to ensure we got all of the stall statements
        self.assertTrue(
            len(nodes[1]) == 8,
            "Number of identified stall " "statements was not correct.",
        )

    def test_sr_logic_none(self):
        """Test a file with no stall statements to ensure
        SRCalcuator does not report stalls when none are
        present.
        """
        test_calc, cst_supp = self._calculator

        # Case 3: No stall statement example
        cst_supp.create_ast_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_none.py",
            )
        )
        test_calc.set_filename("sr_none.py")
        cst_supp.get_libcst_module_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_none.py",
            )
        )
        nodes = test_calc.calculate_sr(
            cst_supp.get_loop_nodes_for_file(), cst_supp._libcst_module
        )

        self.assertTrue(
            nodes[0] == "sr_none.py",
            "File name did not match what was expected.",
        )
        self.assertTrue(
            len(nodes[1]) == 0,
            "Returned detections list was not empty when it" "should have been",
        )

    def test_sr_edge(self):
        """Test edge conditions of SRCalculator to ensure it
        can handle bad inputs without crashing.
        """
        test_calc, _ = self._calculator

        # Case 1: None file path
        try:
            test_calc.set_filename(None)
            self.fail("Successfully managed to set the file path to None")
        except TypeError:
            # We expect a TypeError since we shouldn't be able to set
            # the filename to None
            pass

        # Case 2: File path to non-existent file and None nodes
        test_calc.set_filename("dummy.txt")
        try:
            # We should still return from this, just with the file
            # having no detected lines.
            test_calc.calculate_sr(None, None)
        except TypeError:
            self.fail("No None checking present in calculate_sr()")

    def test_sr_logic_medium(self):
        """Test a mediumn SR example file to ensure all pattern
        matching stall occurrences and frivolous operations are
        caught by SRCalculator.
        """
        test_calc, cst_supp = self._calculator

        # Case 2: Complex example
        cst_supp.create_ast_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_medium.py",
            )
        )
        test_calc.set_filename("sr_medium.py")
        cst_supp.get_libcst_module_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_medium.py",
            )
        )
        nodes = test_calc.calculate_sr(
            cst_supp.get_loop_nodes_for_file(), cst_supp._libcst_module
        )

        self.assertTrue(
            nodes[0] == "sr_medium.py",
            "File name did not match what was expected.",
        )
        self.assertTrue(
            nodes[1][0][0] == 17,
            "Line number of first match did" " not match what was expected.",
        )
        # Check to ensure we got all of the stall statements
        self.assertTrue(
            len(nodes[1]) == 9,
            "Number of identified stall " "statements was not correct.",
        )
