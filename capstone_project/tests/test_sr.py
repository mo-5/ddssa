import unittest

import capstone_project.backend.sr_calculator as sr_calc

class TestSR(unittest.TestCase):
    """ TestSR is responsible for ensuring the correct functionality
    of Stall Ratio calculations and returned objects.
    """

    def setUp(self):
        # Clear object instance for each test
        return SRCalculator("test_file")

    def test_sr_logic(self):
        test_calc = setup()
        sr_calc.set_filename("path goes here")

    def test_sr_edge(self):
        test_calc = setup()

        # Case 1: Bad file path input
        try:
            test_calc.set_filename(None)
            self.fail("Successfully managed to set the file path to None")
        except Exception:
            pass

        # Case 2: File path to non-existent file
        test_calc.set_filename("dummy.txt")
        test_calc.calculate_sr()

