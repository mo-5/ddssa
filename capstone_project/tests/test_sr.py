import unittest
import os

from capstone_project.backend.sr_calculator import SRCalculator
from capstone_project.backend.ast_supplier import ASTSupplier

class TestSR(unittest.TestCase):
    """ TestSR is responsible for ensuring the correct functionality
    of Stall Ratio calculations and returned objects.
    """

    def setUp(self):
        # Clear object instance for each test
        return SRCalculator("test_file"), ASTSupplier()

    def test_sr_logic_simple(self):
        test_calc, ast_supp = self.setUp()

        # Case 1: Simple examples only
        ast_supp.create_ast_from_file(
            os.path.join(os.getcwd(), "capstone_project", "tests",
                         "test_files", "sr_simple.py"))
        test_calc.set_filename("sr_simple.py")
        nodes = test_calc.calculate_sr(ast_supp.get_loop_nodes_for_file())
        
        self.assertTrue(nodes[0] == "sr_simple.py", 
                        "File name did not match what was expected.")
        self.assertTrue(len(nodes[1]) == 3, 
                        "Returned detections list was empty when it "
                        "should be of size 3")
        self.assertTrue(nodes[1][0][0] == 5, "Line number of first match did"
                                             " not match what was expected.")
        # Specifically check if blank lines are being preserved in
        # the line numbering (currently failing due to known issue).
        self.assertTrue(nodes[1][0][1] == 7, "Line number of next match did"
                                             " not match what was expected.")
        
    def test_sr_logic_complex(self):
        test_calc, ast_supp = self.setUp()
        
        # Case 2: Complex example
        ast_supp.create_ast_from_file(
            os.path.join(os.getcwd(), "capstone_project", "tests",
                         "test_files", "sr_advanced.py"))
        test_calc.set_filename("sr_advanced.py")
        nodes = test_calc.calculate_sr(ast_supp.get_loop_nodes_for_file())

        self.assertTrue(nodes[0] == "sr_advanced.py",
                        "File name did not match what was expected.")
        self.assertTrue(nodes[1][0][0] == 10, "Line number of first match did"
                                             " not match what was expected.")
        # Check to ensure we got all of the stall statements
        self.assertTrue(len(nodes[1]) == 8, "Number of identified stall "
                                            "statements was not correct.")
        
    def test_sr_logic_none(self):
        test_calc, ast_supp = self.setUp()

        # Case 3: No stall statement example
        ast_supp.create_ast_from_file(
            os.path.join(os.getcwd(), "capstone_project", "tests",
                         "test_files", "sr_none.py"))
        test_calc.set_filename("sr_none.py")
        nodes = test_calc.calculate_sr(ast_supp.get_loop_nodes_for_file())

        self.assertTrue(nodes[0] == "sr_none.py",
                        "File name did not match what was expected.")
        self.assertTrue(len(nodes[1]) == 0,
                        "Returned detections list was not empty when it"
                        "should have been")
        

    def test_sr_edge(self):
        test_calc, ast_supp = self.setUp()

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
            test_calc.calculate_sr(None)
        except TypeError:
            self.fail("No None checking present in calculate_sr()")