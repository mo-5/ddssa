""" tests contains any unit tests for backend files
"""
import unittest
import os
from capstone_project.backend.cst.cst_supplier import CSTSupplier
from capstone_project.tests.test_utils import TestUtils
import io
import unittest.mock
from contextlib import redirect_stdout


class TestASTSupplier(unittest.TestCase):
    """TestASTSupplier is responsible for ensuring the correct
    functionality of created and supplied AST nodes derived from
    Python files.
    """

    def setUp(self):
        # Clear object instance for each test
        self._test_path = TestUtils().get_test_path()
        self._cst_supplier = CSTSupplier()
        self._cst_supplier.create_ast_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_simple.py",
            )
        )

        self._cst_supplier.get_libcst_module_from_file(
            os.path.join(
                self._test_path,
                "static_test_files",
                "sr_simple.py",
            )
        )
        self._ast_list = self._cst_supplier.get_ast_list()

    def test_has_loop_nodes(self):
        """Test to see if the supplier can find loop nodes in a file"""
        self.assertTrue(
            self._cst_supplier.has_loop_nodes() == True,
            "Should have detected loops nodes in this file",
        )
        self.assertTrue(
            len(self._cst_supplier.get_loop_nodes_for_file()) == 1,
            "Should have detected 1 loop in this file",
        )

    def test_unparsed_ast(self):
        with redirect_stdout(io.StringIO()) as f:
            self._cst_supplier._print_parsed_ast()
        s = f.getvalue()
        self.assertTrue("{'body': " in s)

    def test_unparsed_ast(self):
        with redirect_stdout(io.StringIO()) as f:
            self._cst_supplier._print_unparsed_ast()
        s = f.getvalue()
        self.assertTrue("import time" in s)

    def test_sr_request(self):
        sr_data = self._cst_supplier.sr_request(
            [
                os.path.join(
                    self._test_path,
                    "static_test_files",
                    "sr_simple.py",
                )
            ]
        )
        self.assertTrue(len(sr_data[0][1]) == 3)
